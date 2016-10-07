import matplotlib.pyplot as plt
import numpy as np
import sys
from plotting.util import read_files_dict, pretty_xlim

def main():
	uc_trunc = int(sys.argv[1]) if len(sys.argv) > 1 else 0 #8
	c_trunc = int(sys.argv[2]) if len(sys.argv) > 2 else 0  #-6
	
	uc_dict = read_files_dict("experiments/mf/results/output_uc", sort="steps")
	c_dict = read_files_dict("experiments/mf/results/output_c", sort="steps")
	uc_dict = {key:uc_dict[key][:(uc_trunc if uc_trunc != 0 else len(uc_dict[key]))] for key in uc_dict}
	
	plt.errorbar(uc_dict["aisSteps"], uc_dict["aisMeans"], np.array([uc_dict["aisLowers"], uc_dict["aisUppers"]]), c='red', label='ucAIS')
	plt.errorbar(uc_dict["raisSteps"], uc_dict["raisMeans"], np.array([uc_dict["raisLowers"], uc_dict["raisUppers"]]), c='darkred', label='ucRAIS')
	plt.errorbar(c_dict["aisSteps"], c_dict["aisMeans"], np.array([c_dict["aisLowers"], c_dict["aisUppers"]]), c='blue', label='cAIS')
	plt.errorbar(c_dict["raisSteps"], c_dict["raisMeans"], np.array([c_dict["raisLowers"], c_dict["raisUppers"]]), c='darkblue', label='cRAIS')
	plt.xlabel("HMC/No-U-Turn Steps")
	plt.ylabel("Marginal Likelihood (nats)")
	plt.title("Collapsed vs Uncollapsed Matrix Factorization - Steps")
	plt.legend(loc="lower right")
	all_steps = np.concatenate([uc_dict["aisSteps"], uc_dict["raisSteps"], c_dict["aisSteps"], c_dict["raisSteps"]])
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps)))
	plt.savefig('experiments/mf/plots/steps.pdf', format='pdf', dpi=1000)
	plt.clf()
	
	uc_dict = read_files_dict("experiments/mf/results/output_uc", sort="times")
	c_dict = read_files_dict("experiments/mf/results/output_c", sort="times")
	c_dict = {key:c_dict[key][:(c_trunc if c_trunc != 0 else len(c_dict[key]))] for key in c_dict}

	plt.errorbar(uc_dict["aisTimes"], uc_dict["aisMeans"], np.array([uc_dict["aisLowers"], uc_dict["aisUppers"]]), c='red', label='ucAIS')
	plt.errorbar(uc_dict["raisTimes"], uc_dict["raisMeans"], np.array([uc_dict["raisLowers"], uc_dict["raisUppers"]]), c='darkred', label='ucRAIS')
	plt.errorbar(c_dict["aisTimes"], c_dict["aisMeans"], np.array([c_dict["aisLowers"], c_dict["aisUppers"]]), c='blue', label='cAIS')
	plt.errorbar(c_dict["raisTimes"], c_dict["raisMeans"], np.array([c_dict["raisLowers"], c_dict["raisUppers"]]), c='darkblue', label='cRAIS')
	plt.xlabel("Time (in sec)")
	plt.ylabel("Marginal Likelihood (nats)")
	plt.title("Collapsed vs Uncollapsed Matrix Factorization - Time")
	plt.legend(loc="lower right")
	all_times = np.concatenate([uc_dict["aisTimes"], uc_dict["raisTimes"], c_dict["aisTimes"], c_dict["raisTimes"]])
	plt.xlim(*pretty_xlim(min(all_times), max(all_times)))
	plt.savefig('experiments/mf/plots/times.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()