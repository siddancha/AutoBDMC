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

	// Fixed hyperparameters.
	scale_u ~ normal(VAL_SCALE_U, 0.00001);
	scale_v ~ normal(VAL_SCALE_V, 0.00001);
	sigma ~ normal(VAL_SIGMA, 0.00001);

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