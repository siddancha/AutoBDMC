data {
	int N;
	int K;
	matrix[N,K] x;
	vector[N] y;
}

parameters {
	real alpha;
	vector[K] beta;
	real<lower=0> sigma;

	real<lower=0> sigma_1;
	real<lower=0> sigma_2;
}

model {
	vector[N] mu;

	// Sampling hyperparameters.
	sigma_1 ~ cauchy(0, 5);
	sigma_2 ~ cauchy(0, 5);
	
	// Sampling parameters.
	alpha ~ normal(0, sigma_1);
	for (k in 1:K)
		beta[k] ~ normal(0, sigma_1);
	sigma ~ cauchy(0, sigma_2);

	
	// Sampling data.
	mu <- x * beta + alpha;
	for (i in 1:N)
		y[i] ~ normal(mu[i], sigma);
}