from experiments.fixed_hp.__common.util import print_arr
import numpy as np
import sys

def main():
	N = int(sys.argv[1])
	K = int(sys.argv[2])
	seed = int(sys.argv[3])

	np.random.seed(seed)
	x = np.random.randn(N*K)
	y = np.zeros(N, dtype=int)

	print "N <- " + str(N)
	print "K <- " + str(K)
	print "x <- structure(c" + print_arr(x) + ", .Dim=c(" + str(N) + ", " + str(K) + "))"
	print "y <- c" + print_arr(y)

if __name__ == '__main__':
	main()