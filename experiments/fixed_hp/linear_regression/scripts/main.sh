# User options.
N=100
K=10
BURN_LIST=( 10 100 1000 10000 )
STEPS_LIST=( 10 20 50 100 200 400 800 1200 1600 2000 2500 3000 3500 4000 4500 )
SAMPLES=50
WARMUP=1000
SEED=18

# Subexperiment options.
SUBEXPERIMENT=linear_regression
MODEL=lin_regression_hp
FIXED_HP_MODEL=lr_fixed_hp

# Plotting options.
MODELNAME=Linear_Regression

source experiments/fixed_hp/__common/main.sh