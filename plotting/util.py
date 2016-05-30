import matplotlib.pyplot as plt
import numpy as np
import os

def extract_list (string):
	ll = string.find('[')
	rr = string.find(']')
	return [float(elem) for elem in string[ll+1:rr].split(',')]

def read_files(folder, sort='steps'):
	files = [elem for elem in os.listdir(folder) if elem[0] == 'o']
	steps = np.array([int(elem.split('_')[1]) for elem in files])
	samples = np.array([int(elem.split('_')[2].split('.')[0]) for elem in files])
	aisMeans, aisVars, aisTimes = [], [], []
	raisMeans, raisVars, raisTimes = [], [], []
	for filename in files:
		f = open(folder + "/" + filename, 'rb')
		lines = f.readlines()[-9:]
		aisMeans.extend(extract_list(lines[2]))
		aisVars.extend(extract_list(lines[3]))
		aisTimes.extend(extract_list(lines[4]))
		raisMeans.extend(extract_list(lines[6]))
		raisVars.extend(extract_list(lines[7]))
		raisTimes.extend(extract_list(lines[8]))
	aisMeans, aisVars, aisTimes, raisMeans, raisVars, raisTimes =\
		(np.array(elem) for elem in (aisMeans, aisVars, aisTimes, raisMeans, raisVars, raisTimes))
	aisVars = 1.96 * aisVars / np.sqrt(samples)
	raisVars = 1.96 * raisVars / np.sqrt(samples)
	if sort == 'steps':
		steps, aisMeans, aisVars, aisTimes, raisMeans, raisVars, raisTimes = \
			zip(*sorted(zip(steps, aisMeans, aisVars, aisTimes, raisMeans, raisVars, raisTimes)))
		aisSteps, raisSteps = np.array(steps), np.array(steps)
	else:
		aisSteps, raisSteps = np.array(steps), np.array(steps)
		aisTimes, aisMeans, aisVars, aisSteps = zip(*sorted(zip(aisTimes, aisMeans, aisVars, aisSteps)))
		raisTimes, raisMeans, raisVars, raisSteps = zip(*sorted(zip(raisTimes, raisMeans, raisVars, raisSteps)))
	return aisSteps, aisMeans, aisVars, aisTimes, raisSteps, raisMeans, raisVars, raisTimes

def read_files_dict(folder, sort="steps"):
	aisSteps, aisMeans, aisVars, aisTimes, raisSteps, raisMeans, raisVars, raisTimes = read_files(folder, sort)
	return dict(aisSteps=aisSteps, aisMeans=aisMeans, aisVars=aisVars, aisTimes=aisTimes,\
							raisSteps=raisSteps, raisMeans=raisMeans, raisVars=raisVars, raisTimes=raisTimes);


def pretty_xlim(xmin, xmax, delta=0.01, scale="linear"):
	if scale == "linear":
		left, right = xmin - delta*(xmax-xmin), xmax + delta*(xmax-xmin)
	elif scale == "log":
		left, right = xmin/pow(xmax/xmin, delta), xmax*pow(xmax/xmin, delta)
	else:
		left, right = xmin, xmax
	return left, right