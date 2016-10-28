from datasets.util import print_arr, standardize
import numpy as np
import sys

def read_old_faithful_data():
	f = open("datasets/clustering/old_faithful.csv", "r")
	data = np.array([line.rstrip().split(',')[1:] for line in f.readlines()[1:]], dtype=float)
	return standardize(data)

def main():
	K = int(sys.argv[1])
	y = read_old_faithful_data()
	N, D = y.shape
	print "N <- " + str(N)
	print "D <- " + str(D)
	print "K <- " + str(K)
	print "y <- structure(c" + print_arr(y.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(D) + "))"

if __name__ == '__main__':
	main()