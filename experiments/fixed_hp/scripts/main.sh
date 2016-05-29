# User options.
N=100
K=10
BURN_LIST=( 10 100 1000 10000 )
STEPS_LIST=( 200 400 800 1200 1600 2000 2500 3000 3500 )
SAMPLES=10
WARMUP=1000
SEED=6

MYHOME=experiments/fixed_hp

if [[ $@ =~ --clean ]]; then
	printf "Cleaning experiment files ... "
	rm -rf $MYHOME/gen
	rm -rf $MYHOME/results
	rm -rf $MYHOME/plots
	rm -rf $MYHOME/jobs.list
	printf "Done.\n"
fi

if [[ ! $@ =~ --run ]]; then exit 1; fi

if [[ ! -f $MYHOME/gen ]]; then
	echo "Creating folders ..."
	mkdir $MYHOME/gen
	mkdir $MYHOME/plots
fi

if [[ ! -f models/lin_regression ]]; then
	echo "Compiling lin_regression.stan"
	make -C cmdstan ../models/lin_regression
fi
if [[ ! -f $MYHOME/lr_fixed_hp ]]; then
	echo "Compiling lr_fixed_hp.stan"
	make -C cmdstan ../$MYHOME/lr_fixed_hp
fi

if [[ ! -f $MYHOME/gen/regression.data.R ]]; then
	echo "Creating data file ..."
	python $MYHOME/scripts/gen_data_file.py $N $K $SEED > $MYHOME/gen/lr.data.R
fi

if [[ ! -f $MYHOME/gen/exact_sample.txt ]]; then
	echo "Creating exact sample ..."
	$MYHOME/lr_fixed_hp bdmc schedule=sigmoidal num_warmup=10 iterations start_steps=10 exact_sample save_file=$MYHOME/gen/exact_sample.txt save_samples=0 data file=$MYHOME/gen/lr.data.R output file= random seed=$SEED > /dev/null
fi

if [[ ! -f $MYHOME/results ]]; then
	echo "Creating results folder ..."
	mkdir $MYHOME/results
	for BURN in ${BURN_LIST[*]}; do
		BURN_DIR=$MYHOME/results/burn_$BURN
		if [[ ! -f $BURN_DIR ]]; then mkdir $BURN_DIR; fi
	done
fi

echo "Creating job file ..."
rm $MYHOME/jobs.list
for BURN in ${BURN_LIST[*]}; do
	for STEPS in ${STEPS_LIST[*]}; do
		OUTPUT_FILE=$MYHOME/results/burn_${BURN}/output_${STEPS}_${SAMPLES}.csv
		if [[ ! -f $OUTPUT_FILE ]]; then
			echo "models/lin_regression bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES rais num_weights=$SAMPLES num_burn_in=$BURN iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt save_samples=0 data file=$MYHOME/gen/lr.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
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
python -m experiments.fixed_hp.scripts.plot
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."