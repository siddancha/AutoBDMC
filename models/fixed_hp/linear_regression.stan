data {
	int N;
	int K;
	matrix[N,K] x;
	vector[N] y;
}

parameters {
	// Hyperparameters.
	real sigma;
	real scale;

	// Parameters.
	real alpha;
	vector[K] beta;
}

model {
	// Sampling hyperparameters.
	sigma ~ normal(-0.946046, 0.00001);
	scale ~ normal(0.103093, 0.00001);

	// Sampling parameters.
	alpha ~ normal(0, sqrt(scale*scale));
	for (k in 1:K)
		beta[k] ~ normal(0, sqrt(scale*scale));
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ normal(mu[i], sqrt(sigma*sigma));
	}
}