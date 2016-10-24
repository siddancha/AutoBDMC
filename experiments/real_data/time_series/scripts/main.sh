# User options.
GEN_DATA_ARGS="1"
STEPS_LIST=( 20 50 100 200 400 800 1600 3000 6000 9000 12000 )
SAMPLES=50
WARMUP=1000
SEED=1

# Subexperiment options.
SUBEXPERIMENT=time_series
MODEL=autoregressive

# Plotting options.
MODELNAME=Time_Series

source experiments/real_data/__common/main.sh