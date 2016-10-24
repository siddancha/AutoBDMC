# User options.
GEN_DATA_ARGS="100 3"
BURN_LIST=( 10 100 1000 10000 )
STEPS_LIST=( 10 30 100 300 1000 2000 4000 6000 )
SAMPLES=50
WARMUP=1000
SEED=20

# Subexperiment options.
SUBEXPERIMENT=time_series
MODEL=autoregressive_hp
FIXED_HP_MODEL=ar_fixed_hp

# Plotting options.
MODELNAME=Time_Series

source experiments/fixed_hp/__common/main.sh