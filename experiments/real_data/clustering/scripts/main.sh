# User options.
N=272
D=2
K=2
MU_STD=5
SIGMA_MEAN=0.5
SIGMA_STD=0.3
STEPS_LIST=( 10 20 50 100 200 500 1000 2000 )
SAMPLES=50
WARMUP=1000
SEED=3

# Subexperiment options.
SUBEXPERIMENT=clustering
MODEL=clustering

MYHOME=experiments/real_data/$SUBEXPERIMENT

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

if [[ ! -f $MYHOME/gen/real.data.R ]]; then
	echo "Creating data file ..."
	python -m experiments.real_data.$SUBEXPERIMENT.scripts.gen_data_file $K $MU_STD $SIGMA_MEAN $SIGMA_STD > $MYHOME/gen/real.data.R
fi

if [[ ! -f $MYHOME/gen/exact_sample.txt ]]; then
	echo "Creating exact sample ..."
	python -m experiments.real_data.$SUBEXPERIMENT.scripts.create_es $N $D $K $MU_STD $SIGMA_MEAN $SIGMA_STD $SEED > $MYHOME/gen/exact_sample.txt
fi

if [[ ! -d $MYHOME/results ]]; then
	echo "Creating results folder ..."
	mkdir $MYHOME/results
	mkdir $MYHOME/results/real
	mkdir $MYHOME/results/synthetic
fi

echo "Creating job list ..."
if [[ -f $MYHOME/jobs.list ]]; then rm $MYHOME/jobs.list; fi
touch $MYHOME/jobs.list
for STEPS in ${STEPS_LIST[*]}; do
	OUTPUT_FILE="$MYHOME/results/synthetic/output_${STEPS}_${SAMPLES}.csv"
	if [[ ! -f $OUTPUT_FILE ]]; then
		echo "models/$MODEL bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES rais num_weights=$SAMPLES iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_LIST[*]}; do
	OUTPUT_FILE="$MYHOME/results/real/output_${STEPS}_${SAMPLES}.csv"
	if [[ ! -f $OUTPUT_FILE ]]; then
		echo "models/$MODEL bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES sample_data=0 rais num_weights=1 iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
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
python -m experiments.real_data.__common.plot $SUBEXPERIMENT
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."