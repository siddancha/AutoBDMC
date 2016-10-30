# User options.
GEN_DATA_ARGS=
STEPS_LIST=( 100 200 400 800 1200 1600 3000 4500 6000 8000 10000 12000 15000 )
SAMPLES=100
BURN_LIST=( 10 100 1000 10000 )
WARMUP=1000
SEED=1

# Subexperiment options.
MODEL=time_series

source experiments/fixed_hp/__common/main.sh