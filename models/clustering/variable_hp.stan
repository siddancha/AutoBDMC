data {
  int<lower=0> N;
  int<lower=0> D;
  int<lower=0> K;
  vector[D] y[N];
}

transformed data {
  real HALF_D_LOG_TWO_PI;
  vector[K] ONES_VECTOR;

  HALF_D_LOG_TWO_PI <- 0.5 * D * log(2 * 3.14159);
  for (k in 1:K)
    ONES_VECTOR[k] <- 1;
}

parameters {
  // Hyperparameters.
  real scale;
  real sigma;
  
  // Parameters.
  vector[D] mu[K];
  simplex[K] pi;
}

transformed parameters {
  real z[N,K];
  for (n in 1:N)
    for (k in 1:K)
      z[n, k] <- log(pi[k]) - HALF_D_LOG_TWO_PI - D * log(sigma) - 0.5 * (dot_self(mu[k] - y[n]) / (sigma * sigma)); 
}

model {
  // Sampling hyperparameters.
  scale ~ cauchy(0, 5);
  sigma ~ cauchy(0, 5);

  // Sampling parameters.
  for (k in 1:K)
    for (d in 1:D)
      mu[k,d] ~ normal(0, sqrt(scale*scale));
  pi ~ dirichlet(ONES_VECTOR);

  // Sampling data.
  for (n in 1:N)
    increment_log_prob(log_sum_exp(z[n]));
}