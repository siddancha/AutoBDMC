data {
	int<lower=0> N;
	real y[N];
}

parameters {
  // Hyperparameters.
	real alpha;
  real beta;
  real sigma;

  // Parameters.
}

model {
  // Fixed hyperparameters.
  alpha ~ normal(VAL_ALPHA, 0.00001);
  beta ~ normal(VAL_BETA, 0.00001);
  sigma ~ normal(VAL_SIGMA, 0.00001);
  
  // Sampling parameters.

  // Sampling data.
  for (n in 2:N)
    y[n] ~ normal(alpha + beta * y[n-1], sqrt(sigma*sigma));
}