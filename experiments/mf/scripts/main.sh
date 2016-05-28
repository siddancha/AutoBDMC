# User options
N=10
L=5
D=10
STEPS_UC=( 250 500 750 1000 1250 1500 1750 2000 2250 2500 2750 3000 3250 3500 3750 4000 4250 4500 4750 5000 5250 5500 5750 6000 6250 6500 6750 7000 7250 7500 7750 8000 8250 8500 8750 9000 9250 9500 9750 10000 )
SAMPLES_UC=50
STEPS_C=( 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 )
SAMPLES_C = 50
WARMUP = 1000
SEED=1

MYHOME=experiments/mf

if [[ $@ =~ --clean ]]; then
	printf "Cleaning experiment files ... "
	rm -rf $MYHOME/gen
	rm -rf $MYHOME/results
	rm -rf $MYHOME/plots
	rm -rf $MYHOME/jobs.list
	printf "Done.\n"
fi

if [[ ! $@ =~ --run ]]; then
	exit 1
fi

if [ ! -d $MYHOME/gen ]; then
	echo  "Creating folders ..."
	mkdir $MYHOME/gen
	mkdir $MYHOME/plots
fi

if [ ! -f models/collapsed ]; then
	echo "Compiling collapsed.stan ..."
	make -C cmdstan ../models/collapsed
fi
if [ ! -f models/uncollapsed ]; then
	echo "Compiling uncollapsed.stan ..."
	make -C cmdstan ../models/uncollapsed
fi

if [ ! -f $MYHOME/gen/uncollapsed.data.R ]; then
	echo "Creating data files ..."
	python $MYHOME/scripts/gen_data_file.py $N $L $D > $MYHOME/gen/uncollapsed.data.R
	cp $MYHOME/gen/uncollapsed.data.R $MYHOME/gen/collapsed.data.R
fi

if [ ! -f $MYHOME/gen/uncollapsed_es.txt ]; then
	echo "Creating exact sample for uncollapsed ..."
	models/uncollapsed bdmc schedule=sigmoidal num_warmup=10 iterations start_steps=10 exact_sample save_file=$MYHOME/gen/uncollapsed_es.txt save_samples=0 data file=$MYHOME/gen/uncollapsed.data.R output file= random seed=$SEED > /dev/null
	echo "Converting to exact sample for collapsed ..."
	python $MYHOME/scripts/convert_es.py $MYHOME/gen/uncollapsed_es.txt $N $L $D > $MYHOME/gen/collapsed_es.txt
fi

if [ ! -d $MYHOME/results ]; then
	echo "Creating local folders ..."
	mkdir $MYHOME/results
	mkdir $MYHOME/results/output_uc
	mkdir $MYHOME/results/output_c
fi

echo "Creating job file ..."
rm $MYHOME/jobs.list
for STEPS in ${STEPS_UC[*]}; do
	OUTPUT_FILE="$MYHOME/results/output_uc/output_${STEPS}_${SAMPLES_UC}.csv"
	if [ ! -f $OUTPUT_FILE ]; then
		echo "models/uncollapsed bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES_UC rais num_weights=$SAMPLES_UC iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/uncollapsed_es.txt data file=$MYHOME/gen/uncollapsed.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_C[*]}; do
	OUTPUT_FILE="$MYHOME/results/output_c/output_${STEPS}_${SAMPLES_C}.csv"
	if [ ! -f $OUTPUT_FILE ]; then
		echo "models/collapsed bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES_C rais num_weights=$SAMPLES_C iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/collapsed_es.txt data file=$MYHOME/gen/collapsed.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
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
python -m experiments.mf.scripts.plot
echo "Note: Figures are now available in experiments/mf/plots"

echo "Done."