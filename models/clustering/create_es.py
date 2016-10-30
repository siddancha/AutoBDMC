import numpy as np
import struct
import sys

SCALE_SQ_REAL = 1.18756
SIGMA_SQ_REAL = 0.15431

def main():
	N = int(sys.argv[1])
	D = int(sys.argv[2])
	K = int(sys.argv[3])
	seed = int(sys.argv[4])

	np.random.seed(seed)

	# Sample prior hyperparameters.
	scale_sq_0 = 1.0 / np.random.gamma(1.0, 1.0);
	sigma_sq_0 = 1.0 / np.random.gamma(1.0, 1.0);

	# Sample prior parameters.
	mu_0 = np.sqrt(scale_sq_0) * np.random.randn(K, D)
	pi_0 = np.random.dirichlet(np.ones(K))

	# Fix posterior hyperparameters.
	scale_sq_1 = SCALE_SQ_REAL
	sigma_sq_1 = SIGMA_SQ_REAL

	# Sample posterior parameters.
	mu_1 = np.sqrt(scale_sq_1) * np.random.randn(K, D)
	pi_1 = np.random.dirichlet(np.ones(K))

	# Sample data.
	y_1 = np.zeros([N, D])
	for n in range(N):
		z = np.random.multinomial(1, pi_1).argmax()
		y_1[n] = mu_1[z] + np.sqrt(sigma_sq_1) * np.random.randn(D)


	# Create exact sample.
	stream = ""
	# Size of Stan parameters for prior and posterior samples.
	stream += struct.pack('<i', 2 + K*D + K)
	stream += struct.pack('<i', 2 + K*D + K)
	# Size of data - real (y) and int (3 - N, D, K)
	stream += struct.pack('<i', N*D)
	stream += struct.pack('<i', 3)
	# Write prior sample (matrices in column-major fashion)
	stream += struct.pack('<d', scale_sq_0)
	stream += struct.pack('<d', sigma_sq_0)
	for val in mu_0.T.ravel(): stream += struct.pack('<d', val)
	for val in pi_0: stream += struct.pack('<d', val)
	# Write posterior sample (matrices in column-major fashion)
	stream += struct.pack('<d', scale_sq_1)
	stream += struct.pack('<d', sigma_sq_1)
	for val in mu_1.T.ravel(): stream += struct.pack('<d', val)
	for val in pi_1: stream += struct.pack('<d', val)
	# Write data (matrices in column-major fashion)
	for val in y_1.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<i', N)
	stream += struct.pack('<i', D)
	stream += struct.pack('<i', K)

	sys.stdout.write(stream)

if __name__ == '__main__':
	main()