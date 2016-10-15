data {
	int N;
	int K;
	matrix[N,K] x;
	int y[N];
}

parameters {
	real alpha;
	vector[K] beta;

	real sigma;
}

model {
	vector[N] mu;

	// Setting hyperparameters close to 1.
	sigma ~ normal(1, 0.00001);
	
	// Sampling parameters.
	alpha ~ normal(0, sigma);
	for (k in 1:K)
		beta[k] ~ normal(0, sigma);

	
	// Sampling data.
	mu <- x * beta + alpha;
	for (i in 1:N)
		y[i] ~ bernoulli(inv_logit(mu[i]));
}