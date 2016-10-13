data {
	int N;
	int K;
	matrix[N,K] x;
	int y[N];
}

parameters {
	real alpha;
	vector[K] beta;
}

model {
	alpha ~ normal(0, 1);
	for (k in 1:K)
		beta[k] ~ normal(0, 1);
	{
		vector[N] mu;
		mu <- x * beta + alpha;
		for (i in 1:N)
			y[i] ~ bernoulli(inv_logit(mu[i]));
	}
}