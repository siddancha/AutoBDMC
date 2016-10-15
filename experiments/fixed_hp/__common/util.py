import numpy as np

def print_arr (arr):
	ret = "("
	for i in range(len(arr)-1):
		ret += str(arr[i]) + ', '
	ret += str(arr[-1]) + ')'
	return ret