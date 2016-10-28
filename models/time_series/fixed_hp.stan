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
  alpha ~ normal(1.68186, 0.00001);
  beta ~ normal(0.994648, 0.00001);
  sigma ~ normal(-4.09258, 0.00001);
  
  // Sampling parameters.

  // Sampling data.
  for (n in 2:N)
    y[n] ~ normal(alpha + beta * y[n-1], sqrt(sigma*sigma));
}