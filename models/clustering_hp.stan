data {
  int<lower=0> N;
  int<lower=0> D;
  int<lower=0> K;
  vector[D] y[N];
}

transformed data {
  vector[K] ones;
  for (k in 1:K)
    ones[k] <- 1;
}

parameters {
  // Parameters.
  vector[D] mu[K];
  real<lower=0> sigma;
  simplex[K] pi;

  // Hyperparameters.
  real<lower=0> sigma_1;
  real<lower=0> sigma_2;
}

transformed parameters {
  real z[N,K];
  for (n in 1:N)
    for (k in 1:K)
      z[n, k] <- log(pi[k]) - D * log(sigma) - 0.5 * (dot_self(mu[k] - y[n]) / (sigma * sigma)); 
}

model {
  // Sampling hyperparameters.
  sigma_1 ~ cauchy(0, 5);
  sigma_2 ~ cauchy(0, 5);

  // Prior.
  for (k in 1:K)
    for (d in 1:D)
      mu[k,d] ~ normal(0, sigma_1);
  sigma ~ normal(0, sigma_2);
  pi ~ dirichlet(ones);

  // Likelihood.
  for (n in 1:N)
    increment_log_prob(log_sum_exp(z[n]));
}