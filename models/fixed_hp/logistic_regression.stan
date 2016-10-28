data {
	int N;
	int K;
	matrix[N,K] x;
	int y[N];
}

parameters {
	// Hyperparameters.
	real scale;

	// Parameters.
	real alpha;
	vector[K] beta;
}

model {
	// Sampling hyperparameters.
	scale ~ normal(-0.556333, 0.00001);

	// Sampling parameters.
	alpha ~ normal(0, sqrt(scale*scale));
	for (k in 1:K)
		beta[k] ~ normal(0, sqrt(scale*scale));
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ bernoulli(inv_logit(mu[i]));
	}
}