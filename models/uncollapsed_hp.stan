data {
	int N;
	int L;
	int D;
	matrix[N,D] Y;
}

parameters {
	matrix[N,L] U;
	matrix[L,D] V;

	real<lower=0> sigma_1;
	real<lower=0> sigma_2;
}

model {
	matrix[N,D] mu;

	// Sampling hyperparameters.
	sigma_1 ~ cauchy(0, 5);
	sigma_2 ~ cauchy(0, 5);

	// Sampling parameters.
	for (i in 1:N)
		for (j in 1:L)
			U[i,j] ~ normal(0, sigma_1);

	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(0, sigma_1);

	// Sampling data.
	mu <- U * V;
	for (i in 1:N)
		for (j in 1:D)
			Y[i,j] ~ normal(mu[i,j], sigma_2);
}