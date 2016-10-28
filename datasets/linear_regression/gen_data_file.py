from datasets.util import print_arr, standardize
import numpy as np

def read_nhefs_data():
	f = open("datasets/linear_regression/nhefs_book.csv", "r")
	cols = ['qsmk', 'sex', 'age', 'race', 'smokeyrs', 'wt82_71']
	lines = [line.rstrip().split(',') for line in f.readlines()]
	indices = [lines[0].index(head) for head in cols]
	lines = [[line[index] for index in indices] for line in lines[1:]]
	lines = [[float(elem) for elem in line] for line in lines if '' not in line]
	XY = standardize(np.array(lines))
	X = XY[:,:-1]
	Y = XY[:,-1]
	return X, Y

def main():
	X, Y = read_nhefs_data()
	N, K = X.shape
	print "N <- " + str(N)
	print "K <- " + str(K)
	print "x <- structure(c" + print_arr(X.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(K) + "))"
	print "y <- c" + print_arr(Y)

if __name__ == '__main__':
	main()