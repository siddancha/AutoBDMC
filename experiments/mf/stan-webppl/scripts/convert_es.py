import json
import numpy as np
import struct
import sys

def main():

	# Arguments
	N = int(sys.argv[1])
	L = int(sys.argv[2])
	D = int(sys.argv[3])
	webppl_uncollapsed_file = sys.argv[4]
	webppl_collapsed_file = sys.argv[5]
	stan_uncollapsed_file = sys.argv[6]
	stan_collapsed_file = sys.argv[7]

	# Extract (sorted) items from webppl uncollapsed exact sample JSON file.
	# "items" are the values in webppl's BDMC cacheTable dictionary.
	webppl_uncollapsed_string = open(webppl_uncollapsed_file, 'r').readlines()[0]
	cache_table = json.loads(webppl_uncollapsed_string)
	key_val_pairs = [(key, cache_table[key]) for key in cache_table.keys()]
	mod_key_val_pairs = [([int(x) for x in key.split('_') if x], val) for (key, val) in key_val_pairs]
	mod_key_val_pairs.sort()
	sorted_items = [item[1] for item in mod_key_val_pairs]

	# Extract U, V, UV from items.
	assert len(sorted_items) == N*L + L*D + N*D
	U, sorted_items = np.array(sorted_items[:N*L]).reshape((N, L)), sorted_items[N*L:]
	V, sorted_items = np.array(sorted_items[:L*D]).reshape((L, D)), sorted_items[L*D:]
	UV, sorted_items = np.array(sorted_items[:N*D]).reshape((N, D)), sorted_items[N*D:]
	assert len(sorted_items) == 0

	# Extract items from the dummy webppl collapsed exact sample.
	# Keys will be used, values will be ignored and replaced.
	webppl_collapsed_string = open(webppl_collapsed_file, 'r').readlines()[0]
	cache_table = json.loads(webppl_collapsed_string)
	key_val_pairs = [(key, cache_table[key]) for key in cache_table.keys()]
	mod_key_val_pairs = [([int(x) for x in key.split('_') if x], key, val) for (key, val) in key_val_pairs]
	mod_key_val_pairs.sort()
	assert len(mod_key_val_pairs) == L*D + N
	sorted_items = []
	sorted_items.extend(V.ravel())
	for i in range(N): sorted_items.append(list(UV[i]))
	cache_table = {mod_key_val_pairs[i][1] : sorted_items[i] for i in range(len(mod_key_val_pairs))}
	json.dump(cache_table, open(webppl_collapsed_file, 'w'))

	# Create stan uncollapsed exact sample.
	stream = ""
	# Size of parameters (U and V) for prior and posterior samples (which are the same).
	stream += struct.pack('<i', N*L + L*D)
	stream += struct.pack('<i', N*L + L*D)
	# Size of data - real (UV) and int (3 - N, L, D)
	stream += struct.pack('<i', N*D)
	stream += struct.pack('<i', 3)
	# Write prior sample (matrices in column-major fashion)
	for val in U.T.ravel(): stream += struct.pack('<d', val)
	for val in V.T.ravel(): stream += struct.pack('<d', val)
	# Write posterior sample (matrices in column-major fashion)
	for val in U.T.ravel(): stream += struct.pack('<d', val)
	for val in V.T.ravel(): stream += struct.pack('<d', val)
	# Write data (matrices in column-major fashion)
	for val in UV.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<i', N)
	stream += struct.pack('<i', L)
	stream += struct.pack('<i', D)
	open(stan_uncollapsed_file, 'wb').write(stream)

	# Create stan collapsed exact sample.
	stream = ""
	# Size of parameters (V) for prior and posterior samples (which are the same).
	stream += struct.pack('<i', L*D)
	stream += struct.pack('<i', L*D)
	# Size of data - real (UV) and int (3 - N, L, D)
	stream += struct.pack('<i', N*D)
	stream += struct.pack('<i', 3)
	# Write prior sample (matrices in column-major fashion)
	for val in V.T.ravel(): stream += struct.pack('<d', val)
	# Write posterior sample (matrices in column-major fashion)
	for val in V.T.ravel(): stream += struct.pack('<d', val)
	# Write data (matrices in column-major fashion)
	for val in UV.T.ravel(): stream += struct.pack('<d', val)
	stream += struct.pack('<i', N)
	stream += struct.pack('<i', L)
	stream += struct.pack('<i', D)
	open(stan_collapsed_file, 'wb').write(stream)

if __name__ == '__main__':
	main()