# User options.
N=272
D=2
K=2
SIGMA_1=5.0
SIGMA_2=1.0
BURN_LIST=( 10 100 1000 10000 )
STEPS_LIST=( 10 20 50 100 200 500 1000 2000 )
SAMPLES=50
WARMUP=1000
SEED=2

# Subexperiment options.
SUBEXPERIMENT=clustering
MODEL=clustering_hp

# Plotting options.
MODELNAME=Linear_Regression

MYHOME=experiments/fixed_hp/$SUBEXPERIMENT

if [[ $@ =~ --clean ]]; then
	printf "Cleaning experiment files ... "
	rm -rf $MYHOME/gen
	rm -rf $MYHOME/results
	rm -rf $MYHOME/plots
	rm -rf $MYHOME/jobs.list
	printf "Done.\n"
fi

if [[ ! $@ =~ --run ]]; then exit 1; fi

if [[ ! -d $MYHOME/gen ]]; then
	echo "Creating folders ..."
	mkdir $MYHOME/gen
	mkdir $MYHOME/plots
fi

if [[ ! -f models/$MODEL ]]; then
	echo "Compiling $MODEL.stan ..."
	make -C cmdstan ../models/$MODEL
fi
if [[ ! -f $MYHOME/$FIXED_HP_MODEL ]]; then
	echo "Compiling $FIXED_HP_MODEL.stan ..."
	make -C cmdstan ../$MYHOME/$FIXED_HP_MODEL
fi

if [[ ! -f $MYHOME/gen/$MODEL.data.R ]]; then
	echo "Creating data file ..."
	python -m experiments.fixed_hp.$SUBEXPERIMENT.scripts.gen_data_file $N $D $K $SEED > $MYHOME/gen/$MODEL.data.R
fi

if [[ ! -f $MYHOME/gen/exact_sample.txt ]]; then
	echo "Creating exact sample ..."
	python -m experiments.fixed_hp.$SUBEXPERIMENT.scripts.create_es $N $D $K $SIGMA_1 $SIGMA_2 $SEED > $MYHOME/gen/exact_sample.txt
fi

if [[ ! -d $MYHOME/results ]]; then
	echo "Creating results folder ..."
	mkdir $MYHOME/results
	for BURN in ${BURN_LIST[*]}; do
		BURN_DIR=$MYHOME/results/burn_$BURN
		if [[ ! -f $BURN_DIR ]]; then mkdir $BURN_DIR; fi
	done
fi

echo "Creating job file ..."
if [[ -f $MYHOME/jobs.list ]]; then rm $MYHOME/jobs.list; fi
touch $MYHOME/jobs.list
for BURN in ${BURN_LIST[*]}; do
	for STEPS in ${STEPS_LIST[*]}; do
		OUTPUT_FILE=$MYHOME/results/burn_${BURN}/output_${STEPS}_${SAMPLES}.csv
		if [[ ! -f $OUTPUT_FILE ]]; then
			echo "models/$MODEL bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES rais num_weights=$SAMPLES num_burn_in=$BURN iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt save_samples=0 data file=$MYHOME/gen/$MODEL.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
		fi
	done
done

if [[ $@ =~ --parallel ]]; then
	echo "Executing jobs in parallel. This might take a while ..."
	parallel < $MYHOME/jobs.list > /dev/null
else
	echo "Executing jobs in series. This might take a while ..."
	while read CMD; do
		$CMD
	done < $MYHOME/jobs.list
fi

echo "Creating plots ... "
python -m experiments.fixed_hp.__common.plot $SUBEXPERIMENT $MODELNAME
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."