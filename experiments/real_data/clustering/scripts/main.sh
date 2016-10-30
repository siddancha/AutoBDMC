# User options.
N=272
D=2
K=2
STEPS_LIST=( 10 20 50 100 200 400 600 900 1200 1500 )
SAMPLES=100
BURN=100
WARMUP=1000
SEED=1

# Subexperiment options.
MODEL=clustering

MYHOME=experiments/real_data/$MODEL

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

if [[ ! -f models/$MODEL/variable_hp ]]; then
	echo "Compiling $MODEL/variable_hp.stan ..."
	make -C cmdstan ../models/$MODEL/variable_hp
fi

if [[ ! -f $MYHOME/gen/real.data.R ]]; then
	echo "Creating data file ..."
	python -m datasets.$MODEL.gen_data_file $K > $MYHOME/gen/real.data.R
fi

if [[ ! -f $MYHOME/gen/exact_sample.txt ]]; then
	echo "Creating exact sample ..."
	python models/$MODEL/create_es.py $N $D $K $SEED > $MYHOME/gen/exact_sample.txt
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
		echo "models/$MODEL/variable_hp bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES rais num_weights=$SAMPLES num_burn_in=$BURN iterations start_steps=$STEPS exact_sample load_posterior_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_LIST[*]}; do
	OUTPUT_FILE="$MYHOME/results/real/output_${STEPS}_${SAMPLES}.csv"
	if [[ ! -f $OUTPUT_FILE ]]; then
		echo "models/$MODEL/variable_hp bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES sample_data=0 rais num_weights=1 iterations start_steps=$STEPS exact_sample load_posterior_file=$MYHOME/gen/exact_sample.txt data file=$MYHOME/gen/real.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
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
python -m experiments.real_data.__common.plot $MODEL
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."