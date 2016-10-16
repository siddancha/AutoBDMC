from experiments.real_data.__common.util import print_arr, standardize
import numpy as np

def read_pima_data():
	f = open("experiments/real_data/logistic_regression/pima-indians-diabetes.data", "r")
	data = [[float(elem) for elem in line.rstrip().split(',')] for line in f.readlines()]
	XY = standardize(np.array(data))
	X = XY[:,:-1]
	Y = XY[:,-1].astype('int')
	return X, Y

def main():
	X, Y = read_pima_data()
	N, K = X.shape
	print "N <- " + str(N)
	print "K <- " + str(K)
	print "x <- structure(c" + print_arr(X.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(K) + "))"
	print "y <- c" + print_arr(Y)

if __name__ == '__main__':
	main()