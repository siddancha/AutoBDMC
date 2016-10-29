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
  // Fixed hyperparameters.
  alpha ~ normal(-0.861565, 0.00001);
  beta ~ normal(1.00691, 0.00001);
  sigma_sq ~ normal(20.1597, 0.00001);
  
  // Sampling parameters.

  // Sampling data.
  for (n in 2:N)
    y[n] ~ normal(alpha + beta * y[n-1], sqrt(sigma_sq));
}