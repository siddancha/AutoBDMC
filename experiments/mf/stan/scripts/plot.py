import matplotlib.pyplot as plt
import numpy as np
import sys
from plotting.util import read_files_dict, pretty_xlim

def main():
	uc_trunc = int(sys.argv[1]) if len(sys.argv) > 1 else 0 #8
	c_trunc = int(sys.argv[2]) if len(sys.argv) > 2 else 0  #-6
	
	uc_dict = read_files_dict("experiments/mf/stan/results/output_uc", sort="steps")
	c_dict = read_files_dict("experiments/mf/stan/results/output_c", sort="steps")
	uc_dict = {key:uc_dict[key][:(uc_trunc if uc_trunc != 0 else len(uc_dict[key]))] for key in uc_dict}
	
	ucDivSteps = uc_dict["aisSteps"]
	ucDivMeans = uc_dict["raisMeans"] - uc_dict["aisMeans"]
	ucDivLowers = uc_dict["raisLowers"] + uc_dict["aisUppers"]
	ucDivUppers = uc_dict["raisUppers"] + uc_dict["aisLowers"]
	plt.errorbar(ucDivSteps, ucDivMeans, np.array([ucDivLowers, ucDivUppers]), c='red', label='Uncollapsed')

	cDivSteps = c_dict["aisSteps"]
	cDivMeans = c_dict["raisMeans"] - c_dict["aisMeans"]
	cDivLowers = c_dict["raisLowers"] + c_dict["aisUppers"]
	cDivUppers = c_dict["raisUppers"] + c_dict["aisLowers"]
	plt.errorbar(cDivSteps, cDivMeans, np.array([cDivLowers, cDivUppers]), c='blue', label='Collapsed')
		
	plt.xlabel("No. of HMC/No-U-Turn steps", fontsize='xx-large')
	plt.ylabel("Jeffreys divergence (nats)", fontsize='xx-large')
	plt.legend(loc="upper right", fontsize='xx-large')
	all_steps = np.concatenate([ucDivSteps, cDivSteps])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan/plots/steps.pdf', format='pdf', dpi=1000)
	plt.clf()
	
	uc_dict = read_files_dict("experiments/mf/stan/results/output_uc", sort="times")
	c_dict = read_files_dict("experiments/mf/stan/results/output_c", sort="times")
	c_dict = {key:c_dict[key][:(c_trunc if c_trunc != 0 else len(c_dict[key]))] for key in c_dict}

	ucDivTimes = uc_dict["aisTimes"] + uc_dict["raisTimes"]
	ucDivMeans = uc_dict["raisMeans"] - uc_dict["aisMeans"]
	ucDivLowers = uc_dict["raisLowers"] + uc_dict["aisUppers"]
	ucDivUppers = uc_dict["raisUppers"] + uc_dict["aisLowers"]
	plt.errorbar(ucDivTimes, ucDivMeans, np.array([ucDivLowers, ucDivUppers]), c='red', label='Uncollapsed')

	cDivTimes = c_dict["aisTimes"] + c_dict["raisTimes"]
	cDivMeans = c_dict["raisMeans"] - c_dict["aisMeans"]
	cDivLowers = c_dict["raisLowers"] + c_dict["aisUppers"]
	cDivUppers = c_dict["raisUppers"] + c_dict["aisLowers"]
	plt.errorbar(cDivTimes, cDivMeans, np.array([cDivLowers, cDivUppers]), c='blue', label='Collapsed')

	plt.xlabel("Time (in sec)", fontsize='xx-large')
	plt.ylabel("Jeffreys divergence (nats)", fontsize='xx-large')
	plt.legend(loc="upper right", fontsize='xx-large')
	all_times = np.concatenate([ucDivTimes, cDivTimes])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_times), max(all_times), scale='log'))
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan/plots/times.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()