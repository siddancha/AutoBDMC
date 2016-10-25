from experiments.fixed_hp.__common.util import print_arr
import numpy as np
import sys

def main():
	N, D, K, seed = [int(elem) for elem in sys.argv[1:]]

	np.random.seed(seed)
	y = np.random.randn(N, D)

	print "N <- " + str(N)
	print "D <- " + str(D)
	print "K <- " + str(K)
	print "y <- structure(c" + print_arr(y.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(D) + "))"

if __name__ == '__main__':
	main()