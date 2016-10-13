# User options
N=10
L=5
D=10
STEPS_WEBPPL_UC=( 10 30 100 300 1000 3000 )
SAMPLES_WEBPPL_UC=50
STEPS_WEBPPL_C=( 10 30 100 300 1000 3000 )
SAMPLES_WEBPPL_C=50
STEPS_STAN_UC=( 10 30 100 300 1000 3000 )
SAMPLES_STAN_UC=50
STEPS_STAN_C=( 10 30 100 300 1000 3000 )
SAMPLES_STAN_C=50
WARMUP=1000
SEED=1

MYHOME=experiments/mf/stan-webppl

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
	echo  "Creating folders ..."
	mkdir $MYHOME/gen
	mkdir $MYHOME/gen/model-files
	mkdir $MYHOME/plots
fi

if [[ ! -f models/collapsed ]]; then
	echo "Compiling collapsed.stan ..."
	make -C cmdstan ../models/collapsed
fi
if [[ ! -f models/uncollapsed ]]; then
	echo "Compiling uncollapsed.stan ..."
	make -C cmdstan ../models/uncollapsed
fi

if [[ ! -f $MYHOME/gen/uncollapsed.data.R ]]; then
	echo "Creating data files ..."
	python $MYHOME/scripts/gen_data_file.py $N $L $D > $MYHOME/gen/uncollapsed.data.R
	cp $MYHOME/gen/uncollapsed.data.R $MYHOME/gen/collapsed.data.R
fi

if [[ ! -f $MYHOME/gen/collapsed.webppl ]]; then
	echo "Creating webppl model files ..."
	cp models/collapsed.webppl $MYHOME/gen/collapsed.webppl
	cp models/uncollapsed.webppl $MYHOME/gen/uncollapsed.webppl
	sed -i.bak "s#N = .*;#N = $N;#;s#L = .*;#L = $L;#;s#D = .*;#D = $D;#;s#STEPS = .*;#STEPS = 1;#;s#SAMPLES = .*;#SAMPLES = $SAMPLES_STAN_UC;#;s#LOADPATH = .*;#LOADPATH = '$MYHOME/gen/webppl_uc_es.json';#" $MYHOME/gen/collapsed.webppl
	sed -i.bak "s#N = .*;#N = $N;#;s#L = .*;#L = $L;#;s#D = .*;#D = $D;#;s#STEPS = .*;#STEPS = 1;#;s#SAMPLES = .*;#SAMPLES = $SAMPLES_STAN_C;#;s#LOADPATH = .*;#LOADPATH = '$MYHOME/gen/webppl_c_es.json';#" $MYHOME/gen/uncollapsed.webppl
fi

if [[ ! -f $MYHOME/gen/webppl_uc_es.json ]]; then
	echo "Creating exact samples ..."
	sed -i.bak "s#LOADPATH = .*;#LOADPATH = undefined;#;s#SAVEPATH = .*;#SAVEPATH = '$MYHOME/gen/webppl_uc_es.json';#" $MYHOME/gen/uncollapsed.webppl
	sed -i.bak "s#LOADPATH = .*;#LOADPATH = undefined;#;s#SAVEPATH = .*;#SAVEPATH = '$MYHOME/gen/webppl_c_es.json';#" $MYHOME/gen/collapsed.webppl
	webppl/webppl $MYHOME/gen/uncollapsed.webppl --random-seed $SEED > /dev/null
	webppl/webppl $MYHOME/gen/collapsed.webppl --random-seed $SEED > /dev/null
	sed -i.bak "s#LOADPATH = .*;#LOADPATH = '$MYHOME/gen/webppl_uc_es.json';#;s#SAVEPATH = .*;#SAVEPATH = undefined;#" $MYHOME/gen/uncollapsed.webppl
	sed -i.bak "s#LOADPATH = .*;#LOADPATH = '$MYHOME/gen/webppl_c_es.json';#;s#SAVEPATH = .*;#SAVEPATH = undefined;#" $MYHOME/gen/collapsed.webppl
	python $MYHOME/scripts/convert_es.py $N $L $D $MYHOME/gen/webppl_uc_es.json $MYHOME/gen/webppl_c_es.json $MYHOME/gen/stan_uc_es.txt $MYHOME/gen/stan_c_es.txt
fi

if [[ ! -d $MYHOME/results ]]; then
	echo "Creating results folder ..."
	mkdir -p $MYHOME/results/webppl/output_uc
	mkdir -p $MYHOME/results/webppl/output_c
	mkdir -p $MYHOME/results/stan/output_uc
	mkdir -p $MYHOME/results/stan/output_c
fi

echo "Creating job file ..."
if [[ -f $MYHOME/jobs.list ]]; then rm $MYHOME/jobs.list; fi
touch $MYHOME/jobs.list
for STEPS in ${STEPS_WEBPPL_UC[*]}; do
	OUTPUT_FILE="$MYHOME/results/webppl/output_uc/output_${STEPS}_${SAMPLES_WEBPPL_UC}.csv"
	MODEL_FILE="$MYHOME/gen/model-files/uc_${STEPS}_${SAMPLES_WEBPPL_UC}.webppl"
	if [ ! -f $OUTPUT_FILE ]; then
		cp $MYHOME/gen/uncollapsed.webppl $MODEL_FILE
		sed -i.bak "s#STEPS = .*;#STEPS = $STEPS;#" $MODEL_FILE
		echo "eval webppl/webppl $MODEL_FILE --random-seed $SEED > $OUTPUT_FILE" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_WEBPPL_C[*]}; do
	OUTPUT_FILE="$MYHOME/results/webppl/output_c/output_${STEPS}_${SAMPLES_WEBPPL_C}.csv"
	MODEL_FILE="$MYHOME/gen/model-files/c_${STEPS}_${SAMPLES_WEBPPL_C}.webppl"
	if [ ! -f $OUTPUT_FILE ]; then
		cp $MYHOME/gen/collapsed.webppl $MODEL_FILE
		sed -i.bak "s#STEPS = .*;#STEPS = $STEPS;#" $MODEL_FILE
		echo "eval webppl/webppl $MODEL_FILE --random-seed $SEED > $OUTPUT_FILE" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_STAN_UC[*]}; do
	OUTPUT_FILE="$MYHOME/results/stan/output_uc/output_${STEPS}_${SAMPLES_STAN_UC}.csv"
	if [ ! -f $OUTPUT_FILE ]; then
		echo "models/uncollapsed bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES_STAN_UC rais num_weights=$SAMPLES_STAN_UC iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/stan_uc_es.txt data file=$MYHOME/gen/uncollapsed.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
	fi
done
for STEPS in ${STEPS_STAN_C[*]}; do
	OUTPUT_FILE="$MYHOME/results/stan/output_c/output_${STEPS}_${SAMPLES_STAN_C}.csv"
	if [ ! -f $OUTPUT_FILE ]; then
		echo "models/collapsed bdmc schedule=sigmoidal num_warmup=$WARMUP ais num_weights=$SAMPLES_STAN_C rais num_weights=$SAMPLES_STAN_C iterations start_steps=$STEPS exact_sample load_file=$MYHOME/gen/stan_c_es.txt data file=$MYHOME/gen/collapsed.data.R output file=$OUTPUT_FILE random seed=$SEED" >> $MYHOME/jobs.list
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
python -m experiments.mf.stan-webppl.scripts.plot 
echo "Note: Figures are now available in $MYHOME/plots"

echo "Done."