data {
  int<lower=0> N;
  int<lower=0> D;
  int<lower=0> K;
  real<lower=0> mu_std;
  real<lower=0> sigma_mean;
  real<lower=0> sigma_std;
  vector[D] y[N];
}

transformed data {
  vector[K] ones;
  for (k in 1:K)
    ones[k] <- 1;
}

parameters {
  vector[D] mu[K];
  real<lower=0> sigma;
  simplex[K] pi;
}

transformed parameters {
  real z[N,K];
  for (n in 1:N)
    for (k in 1:K)
      z[n, k] <- log(pi[k]) - D * log(sigma) - 0.5 * (dot_self(mu[k] - y[n]) / (sigma * sigma)); 
}

model {
  // Prior.
  for (k in 1:K)
    for (d in 1:D)
      mu[k,d] ~ normal(0, mu_std);
  sigma ~ normal(sigma_mean, sigma_std);
  pi ~ dirichlet(ones);

  // Likelihood.
  for (n in 1:N)
    increment_log_prob(log_sum_exp(z[n]));
}