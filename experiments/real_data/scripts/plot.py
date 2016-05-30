import matplotlib.pyplot as plt
import numpy as np
from plotting.util import read_files_dict, pretty_xlim

def main():
	s_dict = read_files_dict("experiments/real_data/results/synthetic")
	r_dict = read_files_dict("experiments/real_data/results/real")
	
	plt.errorbar(s_dict["raisSteps"], s_dict["raisMeans"], s_dict["raisVars"], c='darkred', label='synthetic-RAIS')
	plt.errorbar(s_dict["aisSteps"], s_dict["aisMeans"], s_dict["aisVars"], c='red', label='synthetic-AIS')
	plt.errorbar(r_dict["aisSteps"], r_dict["aisMeans"], s_dict["aisVars"], c='blue', label='real-AIS')
	plt.xlabel("Numer of HMC/No-U-Turn Iterations")
	plt.ylabel("Log ML estimate")
	plt.title("Real dataset validation - Bayesian Linear Regression")
	plt.legend(loc="lower right")
	all_steps = np.concatenate([s_dict["aisSteps"], s_dict["raisSteps"], r_dict["aisSteps"]])
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	plt.xscale('log')
	plt.savefig("experiments/real_data/plots/plot.pdf", format='pdf', dpi=1000)

if __name__ == '__main__':
	main()