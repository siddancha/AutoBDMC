# User options.
K=8
N=768
STEPS_LIST=( 10 20 30 40 50 60 70 80 90 100 200 300 400 600 800 1000 )
SAMPLES=100
WARMUP=1000
SEED=2

MYHOME=experiments/real_data/logistic_regression

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

if [[ ! -f models/log_regression ]]; then
	echo "Compiling log_regression.stan ..."
	make -C cmdstan ../models/log_regression
fi

if [[ ! -f $MYHOME/gen/real.data.R ]]; then
	echo "Creating data file ..."
	python $MYHOME/scripts/gen_data_file.py > $MYHOME/gen/real.data.R
fi

if [[ ! -f $MYHOME/gen/exact_sample.txt ]]; then
	echo "Creating exact sample ..."
	models/log_regression bdmc schedule=sigmoidal num_warmup=10 iterations start_steps=10 exact_sample save_file=$MYHOME/gen/exact_sample.txt save_samples=0 data file=$MYHOME/gen/real.data.R output file= random seed=$SEED > /dev/null
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
		echo "models/log_regression bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES rais num_weights=$SAMPLES iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_LIST[*]}; do
	OUTPUT_FILE="$MYHOME/results/real/output_${STEPS}_${SAMPLES}.csv"
	if [[ ! -f $OUTPUT_FILE ]]; then
		echo "models/log_regression bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES sample_data=0 rais num_weights=1 iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
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
python -m experiments.real_data.logistic_regression.scripts.plot 
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."