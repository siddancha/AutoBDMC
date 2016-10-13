import matplotlib.pyplot as plt
import numpy as np
import os
import re

# Returns the lower and upper errors.
def bootstrap (data, alpha=0.05, num_resamples=10000):
	data = np.array(data)
	mean = data.mean()
	resampleMeans = [np.random.choice(data, size=len(data), replace=True).mean() for i in range(num_resamples)]
	resampleMeans.sort()
	lower = resampleMeans[int(num_resamples * (0.5 * alpha))]
	upper = resampleMeans[int(num_resamples * (1 - 0.5 * alpha))]
	return upper - mean, mean - lower

def extract_data_stan(f):
	lines = [line.rstrip() for line in f.readlines()]
	aisIndex = lines.index('#---- AIS ----')
	raisIndex = lines.index('#-- Rev-AIS --')
	def extract_list (string):
		pairs = [elem.split(',') for elem in string[:-2].translate(None, ' [](').split('),')]
		return [(float(pair[0]), float(pair[1])) for pair in pairs]
	aisData = [extract_list(line) for line in lines[aisIndex+1:raisIndex]]
	raisData = [extract_list(line) for line in lines[raisIndex+1:]]
	return aisData, raisData

def extract_data_webppl(f):
	rows = [[pair.split(',') for pair in row.split('],[') ] for row in re.findall('\'\[\[(.*)\]\]\'', f.read())]
	rows = [[(float(pair[0]), float(pair[1])) for pair in row] for row in rows]
	aisData = [rows[i] for i in range(0, len(rows), 2)]
	raisData = [rows[i] for i in range(1, len(rows), 2)] 
	return aisData, raisData

def read_files(folder, sort='steps', lang='stan'):
	files = [elem for elem in os.listdir(folder) if elem[0] == 'o']
	steps = np.array([int(elem.split('_')[1]) for elem in files])
	samples = np.array([int(elem.split('_')[2].split('.')[0]) for elem in files])
	aisMeans, aisLowers, aisUppers, aisTimes = [], [], [], []
	raisMeans, raisLowers, raisUppers, raisTimes = [], [], [], []
	for filename in files:
		f = open(folder + "/" + filename, 'rb')
		aisData, raisData = extract_data_stan(f) if lang == 'stan' else extract_data_webppl(f)
		aisWeightsData = [np.array([elem[0] for elem in row]) for row in aisData]
		aisTimesData = [np.array([elem[1] for elem in row]) for row in aisData]
		aisCurrLowers, aisCurrUppers = zip(*[bootstrap(row) for row in aisWeightsData])
		aisMeans.extend([row.mean() for row in aisWeightsData])
		aisLowers.extend(aisCurrLowers)
		aisUppers.extend(aisCurrUppers)
		aisTimes.extend([row.mean() for row in aisTimesData])
		raisWeightsData = [np.array([elem[0] for elem in row]) for row in raisData]
		raisTimesData = [np.array([elem[1] for elem in row]) for row in raisData]
		raisCurrLowers, raisCurrUppers = zip(*[bootstrap(row) for row in raisWeightsData])
		raisMeans.extend([row.mean() for row in raisWeightsData])
		raisLowers.extend(raisCurrLowers)
		raisUppers.extend(raisCurrUppers)
		raisTimes.extend([row.mean() for row in raisTimesData])
	if sort == 'steps':
		steps, aisMeans, aisLowers, aisUppers, aisTimes, raisMeans, raisLowers, raisUppers, raisTimes = \
			zip(*sorted(zip(steps, aisMeans, aisLowers, aisUppers, aisTimes, raisMeans, raisLowers, raisUppers, raisTimes)))
		aisSteps, raisSteps = np.array(steps), np.array(steps)
	else:
		aisSteps, raisSteps = np.array(steps), np.array(steps)
		aisTimes, aisMeans, aisLowers, aisUppers, aisSteps = zip(*sorted(zip(aisTimes, aisMeans, aisLowers, aisUppers, aisSteps)))
		raisTimes, raisMeans, raisLowers, raisUppers, raisSteps = zip(*sorted(zip(raisTimes, raisMeans, raisLowers, raisUppers, raisSteps)))
	aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes =\
		(np.array(elem) for elem in (aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes))
	return aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes

def read_files_dict(folder, sort='steps', lang='stan'):
	aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes = read_files(folder, sort, lang)
	return dict(aisSteps=aisSteps, aisMeans=aisMeans, aisLowers=aisLowers, aisUppers=aisUppers, aisTimes=aisTimes,\
							raisSteps=raisSteps, raisMeans=raisMeans, raisLowers=raisLowers, raisUppers=raisUppers, raisTimes=raisTimes);


def pretty_xlim(xmin, xmax, delta=0.01, scale="linear"):
	if scale == "linear":
		left, right = xmin - delta*(xmax-xmin), xmax + delta*(xmax-xmin)
	elif scale == "log":
		left, right = xmin/pow(xmax/xmin, delta), xmax*pow(xmax/xmin, delta)
	else:
		left, right = xmin, xmax
	return left, right