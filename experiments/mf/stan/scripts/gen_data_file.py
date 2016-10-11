import sys

def gen_data_file(N, L, D):
	stream = ""
	stream += "N <- " + str(N) + "\n"
	stream += "L <- " + str(L) + "\n"
	stream += "D <- " + str(D) + "\n"
	stream += "Y <- structure(c("
	for i in range(N*D):
		if i > 0:
			stream += ", "
		stream += "0.0"
	stream += "),.Dim=c(" + str(N) + ", " + str(D) +  ")))"
	return stream

if __name__ == "__main__":
	print gen_data_file(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))