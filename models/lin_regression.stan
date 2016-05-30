data {
	int N;
	int K;
	matrix[N,K] x;
	vector[N] y;
}

parameters {
	real alpha;
	vector[K] beta;
	real<lower=0> sigma_sq;
}

model {
	alpha ~ normal(0, 1);
	for (k in 1:K)
		beta[k] ~ normal(0, 1);
	sigma_sq ~ inv_gamma(1, 1);
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ normal(mu[i], sqrt(sigma_sq));
	}
}