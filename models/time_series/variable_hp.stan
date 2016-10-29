data {
	int<lower=0> N;
	real y[N];
}

parameters {
  // Hyperparameters.
	real alpha;
  real beta;
  real<lower=0> sigma_sq;

  // Parameters.
}

model {
  // Sampling hyperparameters.
  alpha ~ normal(0, 1);
  beta ~ normal(1, 0.1);
  sigma_sq ~ inv_gamma(1, 1);
  
  // Sampling parameters.

  // Sampling data.
  for (n in 2:N)
    y[n] ~ normal(alpha + beta * y[n-1], sqrt(sigma_sq));
}