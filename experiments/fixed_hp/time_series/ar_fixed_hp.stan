data {
	int<lower=0> K;
	int<lower=0> N;
	real y[N];
}

parameters {
	real alpha;
	real beta[K];
	real sigma;
	real sigma_1;
	real sigma_2;
}

model {

	// Setting hyperparameters close to 1.
	sigma_1 ~ normal(1.0/K, 0.00001);
	sigma_2 ~ normal(0.1/K, 0.00001);

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
		y[n] ~ normal(mu, sqrt(sigma*sigma));
	}
}