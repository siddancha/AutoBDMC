# User options.
GEN_DATA_ARGS="50 10 50"
STEPS_LIST=( 10 20 50 100 200 500 1000 2000 )
SAMPLES=50
WARMUP=1000
SEED=1

# Subexperiment options.
SUBEXPERIMENT=matrix_factorization
MODEL=mf_partial_obs

source experiments/real_data/__common/main.sh