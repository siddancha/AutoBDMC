data {
	int N;
	int L;
	int D;
	matrix[N,D] Y;
}

parameters {
	matrix[N,L] U;
	matrix[L,D] V;
}

model {
	matrix[N,D] mu;

	for (i in 1:N)
		for (j in 1:L)
			U[i,j] ~ normal(0, 1);

	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(0, 1);

	mu <- U * V;
	for (i in 1:N)
		for (j in 1:D)
			Y[i,j] ~ normal(mu[i,j], 1);
}