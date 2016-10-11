import struct
import sys

def remove_u (stream, start, stop, N, L, D):
	u_size = N * L
	v_size = L * D
	assert stop - start == (u_size + v_size) * 8
	return stream[start + u_size * 8 : stop]

def convert_uncollapsed_to_collapsed(filename, N, L, D):
	u_size = N * L
	v_size = L * D
	y_size = N * D
	stream = open(filename, 'rb').read()
	uc_len = 4 * 4 + 2 * (u_size + v_size) * 8 + y_size * 8 + 3 * 4
	c_len = 4*4 + 2 * v_size * 8 + y_size * 8 + 3 * 4
	assert len(stream) == uc_len
	new_stream = ""
	# Sizes of parameters
	assert struct.unpack('<i', stream[0*4:1*4])[0] == u_size + v_size
	assert struct.unpack('<i', stream[1*4:2*4])[0] == u_size + v_size
	new_stream += struct.pack('<i', v_size)
	new_stream += struct.pack('<i', v_size)
	# Size of data
	assert struct.unpack('<i', stream[2*4:3*4])[0] == y_size
	assert struct.unpack('<i', stream[3*4:4*4])[0] == 3
	new_stream += stream[2*4:4*4]
	prior_start = 4*4
	prior_stop = prior_start + (u_size + v_size) * 8
	posterior_start = prior_stop
	posterior_stop = posterior_start + (u_size + v_size) * 8
	new_stream += remove_u(stream, prior_start, prior_stop, N, L, D)
	new_stream += remove_u(stream, posterior_start, posterior_stop, N, L, D)
	new_stream += stream[posterior_stop:uc_len]
	assert len(new_stream) == c_len
	return new_stream

def main():
	new_stream = convert_uncollapsed_to_collapsed(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
	sys.stdout.write(new_stream)

if __name__ == '__main__':
	main()
