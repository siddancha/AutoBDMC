import numpy as np
import sys

def print_arr (arr):
	ret = "("
	for i in range(len(arr)-1):
		ret += str(arr[i]) + ', '
	ret += str(arr[-1]) + ')'
	return ret

def main():
	N = int(sys.argv[1])
	K = int(sys.argv[2])
	seed = int(sys.argv[3])

	np.random.seed(seed)
	x = np.random.randn(N*K)
	y = np.zeros(N)

	print "N <- " + str(N)
	print "K <- " + str(K)
	print "x <- structure(c" + print_arr(x) + ", .Dim=c(" + str(N) + ", " + str(K) + "))"
	print "y <- c" + print_arr(y)

if __name__ == '__main__':
	main()