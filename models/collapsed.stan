data {
	int N;
	int L;
	int D;
	vector[D] Y[N];
}

transformed data {
	vector[D] mu;
	for (i in 1:D) mu[i] <- 0;
}

parameters {
	matrix[L,D] V;
}

model {
	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(0, 1);

	{
		matrix[D,D] cov;
		cov <- V' * V;
		for (i in 1:D) cov[i,i] <- cov[i,i] + 1;

		for (i in 1:N)
			Y[i] ~ multi_normal(mu, cov);
	}
}