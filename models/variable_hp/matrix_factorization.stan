data {
	int N;
	int L;
	int D;
	matrix[N,D] Y;
}

parameters {
	// Hyperparameters.
	real scale_u;
	real scale_v;
	real sigma;

	// Parameters.
	matrix[N,L] U;
	matrix[L,D] V;
}

model {
	matrix[N,D] UV;

	// Sampling hyperparameters.
	scale_u ~ cauchy(0, 5)
	scale_v ~ cauchy(0, 5)
	sigma ~ cauchy(0, 5)

	// Sampling parameters.
	for (i in 1:N)
		for (j in 1:L)
			U[i,j] ~ normal(0, sqrt(scale_u*scale_u));

	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(0, sqrt(scale_v*scale_v));

	// Sampling data.
	UV <- U * V;
	for (i in 1:N)
		for (j in 1:D)
			if (Y[i,j] > 0)
				Y[i,j] ~ normal(UV[i,j], sqrt(sigma*sigma));
}