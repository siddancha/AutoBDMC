data {
	int N;
	int K;
	matrix[N,K] x;
	vector[N] y;
}

parameters {
	// Hyperparameters.
	real<lower=0> sigma_sq;
	real<lower=0> scale_sq;

	// Parameters.
	real alpha;
	vector[K] beta;
}

model {
	// Fixed hyperparameters.
	sigma_sq ~ normal(0.924901, 0.00001);
	scale_sq ~ normal(0.240021, 0.00001);

	// Sampling parameters.
	alpha ~ normal(0, sqrt(scale_sq));
	for (k in 1:K)
		beta[k] ~ normal(0, sqrt(scale_sq));

	// Sampling data.
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ normal(mu[i], sqrt(sigma_sq));
	}
}