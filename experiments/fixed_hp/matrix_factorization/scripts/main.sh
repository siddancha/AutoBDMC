# User options.
GEN_DATA_ARGS="50 5 50"
STEPS_LIST=( 10 20 50 100 200 400 700 1000 1400 1800 2000 )
SAMPLES=100
BURN_LIST=( 10 100 1000 10000 )
WARMUP=1000
SEED=1

# Subexperiment options.
MODEL=matrix_factorization

source experiments/fixed_hp/__common/main.sh