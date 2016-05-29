import matplotlib.pyplot as plt
import numpy as np
import os
from plotting.util import read_files, pretty_xlim

def main():
	folders = [elem for elem in os.listdir("experiments/fixed_hp/results") if elem[0] == 'b']
	burns = [int(elem.split('_')[1].split('.')[0]) for elem in folders]
	xmin, xmax = np.inf, -np.inf
	for burn, burn_folder in zip(burns, folders):
		aisSteps, aisMeans, aisVars, aisTimes, raisSteps, raisMeans, raisVars, raisTimes =\
			read_files("experiments/fixed_hp/results/" + burn_folder, "steps")
		plt.errorbar(raisSteps, raisMeans, raisVars, label=str(burn))
		xmin, xmax = min(xmin, min(raisSteps)), max(xmax, max(raisSteps))
	plt.xlabel("Number of HMC/No-U-Turn iterations")
	plt.ylabel("Log ML estimate")
	plt.title("Reverse AIS estimates for Fixed Hyperparameter Scheme")
	plt.legend(loc="upper right")
	plt.xlim(*pretty_xlim(xmin, xmax))
	plt.savefig('experiments/fixed_hp/plots/only_rais.pdf', format='pdf', dpi=1000)
	plt.clf()

	legend_handles, legend_labels = [], []
	for burn, burn_folder in zip(burns, folders):
		aisSteps, aisMeans, aisVars, aisTimes, raisSteps, raisMeans, raisVars, raisTimes =\
			read_files("experiments/fixed_hp/results/" + burn_folder, "steps")
		rhandle, _, _ = plt.errorbar(raisSteps, raisMeans, raisVars)
		legend_handles.append(rhandle)
		legend_labels.append('RAIS ' + str(burn))
		ahandle, _, _ = plt.errorbar(aisSteps, aisMeans, aisVars, color='red', linestyle='--')
	legend_handles.append(ahandle)
	legend_labels.append('AIS')

	plt.xlabel("Number of HMC/No-U-Turn iterations")
	plt.ylabel("Log ML estimate")
	plt.legend(legend_handles, legend_labels, loc="lower right")
	plt.xlim(*pretty_xlim(xmin, xmax))
	plt.savefig('experiments/fixed_hp/plots/ais_rais.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()