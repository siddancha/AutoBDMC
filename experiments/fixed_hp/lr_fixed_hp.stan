data {
	int N;
	int K;
	matrix[N,K] x;
	vector[N] y;
}

parameters {
	real alpha;
	vector[K] beta;
	real sigma;
	real sigma_1;
	real sigma_2;
}

model {
	vector[N] mu;

	// Setting hyperparameters close to 1.
	sigma_1 ~ normal(1, 0.00001);
	sigma_2 ~ normal(1, 0.00001);
	
	// Sampling parameters.
	alpha ~ normal(0, sigma_1);
	for (k in 1:K)
		beta[k] ~ normal(0, sigma_1);
	sigma ~ cauchy(0, sigma_2);

	
	// Sampling data.
	mu <- x * beta + alpha;
	for (i in 1:N)
		y[i] ~ normal(mu[i], sqrt(sigma*sigma));
}