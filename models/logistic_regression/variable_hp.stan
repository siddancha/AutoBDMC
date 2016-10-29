data {
	int N;
	int K;
	matrix[N,K] x;
	int y[N];
}

parameters {
	// Hyperparameters.
	real<lower=0> scale_sq;

	// Parameters.
	real alpha;
	vector[K] beta;
}

model {
	// Sampling hyperparameters.
	scale_sq ~ inv_gamma(1, 1);

	// Sampling parameters.
	alpha ~ normal(0, sqrt(scale_sq));
	for (k in 1:K)
		beta[k] ~ normal(0, sqrt(scale_sq));

	// Sampling data.
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ bernoulli(inv_logit(mu[i]));
	}
}