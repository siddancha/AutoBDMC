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
  // Sampling hyperparameters.
  alpha ~ cauchy(0, 5);
  beta ~ cauchy(0, 5);
  sigma ~ cauchy(0, 5);
  
  // Sampling parameters.

  // Sampling data.
  for (n in 2:N)
    y[n] ~ normal(alpha + beta * y[n-1], sqrt(sigma*sigma));
}