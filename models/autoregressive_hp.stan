data {
	int<lower=0> K;
	int<lower=0> N;
	real y[N];
}

parameters {
	real alpha;
	real beta[K];
	real<lower=0> sigma;

	real<lower=0> sigma_1;
	real<lower=0> sigma_2;
}

model {

	// Sampling hyperparameters.
	sigma_1 ~ normal(0, 1.0/K);
	sigma_2 ~ normal(0, 1.0/K);

	// Sampling parameters.
	alpha ~ normal(0, sigma_1);
	for (k in 1:K)
		beta[k] ~ normal(0, sigma_1);
	sigma ~ normal(0, sigma_2);

	// Sampling data.
	for (n in (K+1):N) {
		real mu;
		mu <- alpha;
		for (k in 1:K)
			mu <- mu + beta[k] * y[n-k];
		y[n] ~ normal(mu, sigma);
	}
}