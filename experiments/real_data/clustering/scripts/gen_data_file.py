from experiments.real_data.__common.util import print_arr, standardize
import numpy as np
import sys

def read_old_faithful_data():
	f = open("experiments/real_data/clustering/old_faithful.csv", "r")
	data = np.array([line.rstrip().split(',')[1:] for line in f.readlines()[1:]], dtype=float)
	data[:, 0] = standardize(data[:, 0])
	data[:, 1] = standardize(data[:, 1])
	return data

def main():
	K = int(sys.argv[1])
	mu_std = float(sys.argv[2])
	sigma_mean = float(sys.argv[3])
	sigma_std = float(sys.argv[4])
	data = read_old_faithful_data()
	N, D = data.shape
	print "N <- " + str(N)
	print "D <- " + str(D)
	print "K <- " + str(K)
	print "mu_std <- " + str(mu_std)
	print "sigma_mean <- " + str(sigma_mean)
	print "sigma_std <- " + str(sigma_std)
	print "y <- structure(c" + print_arr(data.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(D) + "))"

if __name__ == '__main__':
	main()