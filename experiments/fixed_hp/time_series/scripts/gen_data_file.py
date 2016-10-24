from experiments.fixed_hp.__common.util import print_arr
import numpy as np
import sys

def main():
	N = int(sys.argv[1])
	K = int(sys.argv[2])
	seed = int(sys.argv[3])

	np.random.seed(seed)
	y = np.random.randn(N)

	print "K <- " + str(K)
	print "N <- " + str(N)
	print "y <- c" + print_arr(y)

if __name__ == '__main__':
	main()