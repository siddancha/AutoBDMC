from experiments.real_data.__common.util import print_arr, standardize
import numpy as np
import sys

def read_google_stock_data():
	f = open("experiments/real_data/time_series/google_stock.txt", "r")
	data = np.array([line.split('\t')[1] for line in f.read().split('\n')][1:], dtype=float)
	return data

def main():
	K, = [int(elem) for elem in sys.argv[1:]]
	y = read_google_stock_data()
	print "K <- " + str(K)
	print "N <- " + str(len(y)) 
	print "y <- c" + print_arr(y)

if __name__ == '__main__':
	main()