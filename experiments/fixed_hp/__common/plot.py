import matplotlib.pyplot as plt
import numpy as np
import os
from plotting.util import read_files, pretty_xlim
import sys

def main():
	SUBEXP, MODELNAME = sys.argv[1], sys.argv[2].replace('_', ' ')
	subexp_folder = str.format("experiments/fixed_hp/{0}", SUBEXP)
	folders = [elem for elem in os.listdir(subexp_folder + '/results') if elem[0] == 'b']
	burns = [int(elem.split('_')[1].split('.')[0]) for elem in folders]
	xmin, xmax = np.inf, -np.inf
	for burn, burn_folder in zip(burns, folders):
		aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes =\
			read_files(subexp_folder + '/results/' + burn_folder, "steps")
		plt.errorbar(raisSteps, raisMeans, np.array([raisLowers, raisUppers]), label=str(burn))
		xmin, xmax = min(xmin, min(raisSteps)), max(xmax, max(raisSteps))
	plt.xlabel("Number of HMC/No-U-Turn iterations")
	plt.ylabel("Log ML estimate")
	plt.title(str.format("Reverse AIS estimates for Fixed Hyperparameter Scheme ({0})", MODELNAME), fontsize=11)
	plt.legend(loc="upper right")
	plt.xscale("log")
	plt.xlim(*pretty_xlim(xmin, xmax, scale="log"))
	plt.savefig(subexp_folder + '/plots/only_rais.pdf', format='pdf', dpi=1000)
	plt.clf()

	legend_handles, legend_labels = [], []
	for burn, burn_folder in zip(burns, folders):
		aisSteps, aisMeans, aisLowers, aisUppers, aisTimes, raisSteps, raisMeans, raisLowers, raisUppers, raisTimes =\
			read_files(subexp_folder + "/results/" + burn_folder, "steps")
		rhandle, _, _ = plt.errorbar(raisSteps, raisMeans, np.array([raisLowers, raisUppers]))
		legend_handles.append(rhandle)
		legend_labels.append('RAIS ' + str(burn))
		ahandle, _, _ = plt.errorbar(aisSteps, aisMeans, np.array([aisLowers, aisUppers]), color='red', linestyle='--')
	legend_handles.append(ahandle)
	legend_labels.append('AIS')

	plt.xlabel("Number of HMC/No-U-Turn iterations")
	plt.ylabel("Log ML estimate")
	plt.title(str.format("BDMC estimates for Fixed Hyperparameter Scheme ({0})", MODELNAME), fontsize=11)
	plt.legend(legend_handles, legend_labels, loc="lower right")
	plt.xscale("log")
	plt.xlim(*pretty_xlim(xmin, xmax, scale="log"))
	plt.savefig(subexp_folder + '/plots/ais_rais.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()