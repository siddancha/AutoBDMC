from experiments.real_data.__common.util import print_arr, standardize
import numpy as np
import struct
import sys

def main():
	N = int(sys.argv[1])
	D = int(sys.argv[2])
	K = int(sys.argv[3])
	sigma_hp_1 = float(sys.argv[4])
	sigma_hp_2 = float(sys.argv[5])
	seed = int(sys.argv[6])

	np.random.seed(seed)

	# Sample from prior.
	mu_0 = sigma_hp_1 * np.random.randn(K, D)
	sigma_0 = sigma_hp_2 * np.absolute(np.random.randn())
	p_0 = np.random.dirichlet(np.ones(K))
	
	# Sample from posterior.
	mu_1 = sigma_hp_1 * np.random.randn(K, D)
	sigma_1 = sigma_hp_2 * np.absolute(np.random.randn())
	p_1 = np.random.dirichlet(np.ones(K))

	# Sample data.
	y_1 = np.zeros([N, D])
	for n in range(N):
		z = np.random.multinomial(1, p_1).argmax()
		y_1[n] = mu_1[z] + sigma_1 * np.random.randn(D)

	# Create exact sample.
	stream = ""
	# Size of parameters (mu) for prior and posterior samples.
	stream += struct.pack('<i', K*D + 1 + K + 2)
	stream += struct.pack('<i', K*D + 1 + K + 2)
	# Size of data - real (y) and int (3 - N, D, K)
	stream += struct.pack('<i', N*D)
	stream += struct.pack('<i', 3)
	# Write prior sample (matrices in column-major fashion)
	for val in mu_0.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<d', sigma_0)
	for val in p_0: stream += struct.pack('<d', val)
	stream += struct.pack('<d', sigma_hp_1)
	stream += struct.pack('<d', sigma_hp_2)
	# Write posterior sample (matrices in column-major fashion)
	for val in mu_1.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<d', sigma_1)
	for val in p_1: stream += struct.pack('<d', val)
	stream += struct.pack('<d', sigma_hp_1)
	stream += struct.pack('<d', sigma_hp_2)
	# Write data (matrices in column-major fashion)
	for val in y_1.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<i', N)
	stream += struct.pack('<i', D)
	stream += struct.pack('<i', K)

	sys.stdout.write(stream)

if __name__ == '__main__':
	main()