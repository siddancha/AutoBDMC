from experiments.fixed_hp.__common.util import print_arr
import numpy as np
import sys

def main():
	N, L, D, seed = [int(elem) for elem in sys.argv[1:]]
	np.random.seed(seed)
	Y = np.random.randn(N, D)

	print "N <- " + str(N)
	print "L <- " + str(L)
	print "D <- " + str(D)
	print "Y <- structure(c" + print_arr(Y.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(D) + "))"

if __name__ == '__main__':
	main()