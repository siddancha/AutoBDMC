data {
	int N;
	int L;
	int D;
	real obs_mu;
	real obs_sigma;
	real noise_sigma;
	matrix[N,D] Y;
}

transformed data {
	real mu;
	real sigma;
	mu <- sqrt(obs_mu / L);
	sigma <- sqrt(sqrt((obs_sigma * obs_sigma) / L + (obs_mu * obs_mu) / (L * L)) - (obs_mu / L));
}

parameters {
	matrix[N,L] U;
	matrix[L,D] V;
}

model {
	matrix[N,D] UV;

	for (i in 1:N)
		for (j in 1:L)
			U[i,j] ~ normal(mu, sigma);

	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(mu, sigma);

	UV <- U * V;
	for (i in 1:N)
		for (j in 1:D)
			if (Y[i,j] > 0)
				Y[i,j] ~ normal(UV[i,j], noise_sigma);
}