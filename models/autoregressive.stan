data {
	int<lower=0> K;
	int<lower=0> N;
	real y[N];
}

parameters {
	real alpha;
  real beta[K];
  real sigma;
}

model {

	// Prior.
  alpha ~ normal(0, 2.0/K);
  for (k in 1:K)
    beta[k] ~ normal(1.0/K, 0.1/K);
  sigma ~ normal(0, 20.0/K);
  
  // Likelihood.
  for (n in (K+1):N) {
    real mu;
    mu <- alpha;
    for (k in 1:K)
      mu <- mu + beta[k] * y[n-k];
    y[n] ~ normal(mu, sqrt(sigma*sigma));
  }
}