# User options.
GEN_DATA_ARGS=
STEPS_LIST=( 10 20 30 40 50 60 70 80 90 100 200 300 400 600 800 1000 1200 1500 1800 2000 )
SAMPLES=100
BURN_LIST=( 10 100 1000 10000 )
WARMUP=1000
SEED=1

# Subexperiment options.
MODEL=logistic_regression

source experiments/fixed_hp/__common/main.sh