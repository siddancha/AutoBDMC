data {
	int N;
	int L;
	int D;
	matrix[N,D] Y;
}

parameters {
	// Hyperparameters.
	real<lower=0> scale_u_sq;
	real<lower=0> scale_v_sq;
	real<lower=0> sigma_sq;

	// Parameters.
	matrix[N,L] U;
	matrix[L,D] V;
}

model {
	matrix[N,D] UV;

	// Fixed hyperparameters.
	scale_u_sq ~ normal(0.363352, 0.00001);
	scale_v_sq ~ normal(0.327693, 0.00001);
	sigma_sq ~ normal(0.582587, 0.00001);

	// Sampling parameters.
	for (i in 1:N)
		for (j in 1:L)
			U[i,j] ~ normal(0, sqrt(scale_u_sq));

	for (i in 1:L)
		for (j in 1:D)
			V[i,j] ~ normal(0, sqrt(scale_v_sq));

	// Sampling data.
	UV <- U * V;
	for (i in 1:N)
		for (j in 1:D)
			if (Y[i,j] > -999999)
				Y[i,j] ~ normal(UV[i,j], sqrt(sigma_sq));
}