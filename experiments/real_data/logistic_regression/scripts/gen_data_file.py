import numpy as np

def print_arr (arr):
	ret = "("
	for i in range(len(arr)-1):
		ret += str(arr[i]) + ', '
	ret += str(arr[-1]) + ')'
	return ret

def standardize(X):
	X = X - X.mean(axis=0)
	X = X / X.std(axis=0)
	return X

def read_pima_data():
	f = open("experiments/real_data/logistic_regression/pima-indians-diabetes.data", "r")
	data = [[float(elem) for elem in line.rstrip().split(',')] for line in f.readlines()]
	# cols = ['qsmk', 'sex', 'age', 'race', 'smokeyrs', 'wt82_71']
	# lines = [line.rstrip().split(',') for line in f.readlines()]
	# indices = [lines[0].index(head) for head in cols]
	# lines = [[line[index] for index in indices] for line in lines[1:]]
	# lines = [[float(elem) for elem in line] for line in lines if '' not in line]
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