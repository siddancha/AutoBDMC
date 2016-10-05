import matplotlib.pyplot as plt
import numpy as np
import os

def extract_list (string):
	pairs = [elem.split(',') for elem in string[:-2].translate(None, ' [](').split('),')]
	return [(float(pair[0]), float(pair[1])) for pair in pairs]

def read_files(folder, sort='steps'):
	files = [elem for elem in os.listdir(folder) if elem[0] == 'o']
	steps = np.array([int(elem.split('_')[1]) for elem in files])
	samples = np.array([int(elem.split('_')[2].split('.')[0]) for elem in files])
	aisMeans, aisVars, aisTimes = [], [], []
	raisMeans, raisVars, raisTimes = [], [], []
	for filename in files:
		f = open(folder + "/" + filename, 'rb')
		lines = [line.rstrip() for line in f.readlines()]
		aisIndex = lines.index('#---- AIS ----')
		raisIndex = lines.index('#-- Rev-AIS --')
		aisData = [extract_list(line) for line in lines[aisIndex+1:raisIndex]]
		raisData = [extract_list(line) for line in lines[raisIndex+1:]]
		aisMeans.extend([np.array([elem[0] for elem in row]).mean() for row in aisData])
		aisVars.extend([np.array([elem[0] for elem in row]).std() for row in aisData])
		aisTimes.extend([np.array([elem[1] for elem in row]).mean() for row in aisData])
		raisMeans.extend([np.array([elem[0] for elem in row]).mean() for row in raisData])
		raisVars.extend([np.array([elem[0] for elem in row]).std() for row in raisData])
		raisTimes.extend([np.array([elem[1] for elem in row]).mean() for row in raisData])
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