from datasets.util import print_arr, standardize
import numpy as np
import sys

def read_reduced_movielens_data(N, L, D):
	f = open("datasets/matrix_factorization/u.data", "r")
	data = np.array([line.rstrip().split() for line in f.readlines()], dtype=int)
	data[:, 0] -= 1
	data[:, 1] -= 1
	mean_rating = data[:, 2].astype(float).mean()

	num_users = data[:, 0].max() + 1
	num_items = data[:, 1].max() + 1
	user_freqs = [0] * num_users
	item_freqs = [0] * num_items
	for row in data:
		user_freqs[row[0]] += 1
		item_freqs[row[1]] += 1

	user_indices = dict(zip(zip(*sorted(zip(user_freqs, range(num_users))))[1][-1 * N :], range(N)))
	item_indices = dict(zip(zip(*sorted(zip(item_freqs, range(num_users))))[1][-1 * D :], range(D)))

	Y = -1e6 * np.ones([N, D], dtype=float)
	for row in data:
		if (user_indices.has_key(row[0]) and item_indices.has_key(row[1])):
			Y[user_indices[row[0]]][item_indices[row[1]]] = row[2] - mean_rating

	return Y

def main():
	N, L, D = [int(elem) for elem in sys.argv[1:]]
	Y = read_reduced_movielens_data(N, L, D)
	print "N <- " + str(N)
	print "L <- " + str(L)
	print "D <- " + str(D)
	print "Y <- structure(c" + print_arr(Y.T.ravel()) + ", .Dim=c(" + str(N) + ", " + str(D) + "))"

if __name__ == '__main__':
	main()