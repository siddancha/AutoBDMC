# User options.
N=100
K=10
BURN_LIST=( 10 100 1000 10000 )
STEPS_LIST=( 10 30 100 300 1000 2000 4000 6000 )
SAMPLES=50
WARMUP=1000
SEED=3

# Subexperiment options.
SUBEXPERIMENT=logistic_regression
MODEL=log_regression_hp
FIXED_HP_MODEL=lr_fixed_hp

# Plotting options.
MODELNAME=Logistic_Regression

source experiments/fixed_hp/__common/main.sh