import matplotlib.pyplot as plt
import numpy as np
import sys
from plotting.util import read_files_dict, pretty_xlim

def main():
	
	webppl_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_uc", sort="times", lang='webppl')
	webppl_c_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_c", sort="times", lang='webppl')
	stan_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_uc", sort="times", lang='stan')
	stan_c_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_c", sort="times", lang='stan')

	# ucDivSteps = uc_dict["aisSteps"]
	# ucDivMeans = uc_dict["raisMeans"] - uc_dict["aisMeans"]
	# ucDivLowers = uc_dict["raisLowers"] + uc_dict["aisUppers"]
	# ucDivUppers = uc_dict["raisUppers"] + uc_dict["aisLowers"]
	# plt.errorbar(ucDivSteps, ucDivMeans, np.array([ucDivLowers, ucDivUppers]), c='red', label='Uncollapsed')

	# cDivSteps = c_dict["aisSteps"]
	# cDivMeans = c_dict["raisMeans"] - c_dict["aisMeans"]
	# cDivLowers = c_dict["raisLowers"] + c_dict["aisUppers"]
	# cDivUppers = c_dict["raisUppers"] + c_dict["aisLowers"]
	# plt.errorbar(cDivSteps, cDivMeans, np.array([cDivLowers, cDivUppers]), c='blue', label='Collapsed')
		
	# plt.xlabel("HMC/No-U-Turn Steps")
	# plt.ylabel("Jeffreys Divergence (nats)")
	# plt.title("Collapsed vs Uncollapsed Matrix Factorization - Steps")
	# plt.legend(loc="upper right")
	# all_steps = np.concatenate([ucDivSteps, cDivSteps])
	# plt.xscale('log')
	# plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	# plt.savefig('experiments/mf/stan/plots/steps.pdf', format='pdf', dpi=1000)
	# plt.clf()
	
	# uc_dict = read_files_dict("experiments/mf/stan/results/output_uc", sort="times")
	# c_dict = read_files_dict("experiments/mf/stan/results/output_c", sort="times")
	# c_dict = {key:c_dict[key][:(c_trunc if c_trunc != 0 else len(c_dict[key]))] for key in c_dict}

	plt.errorbar(stan_uc_dict["aisTimes"], stan_uc_dict["aisMeans"], np.array([stan_uc_dict["aisLowers"], stan_uc_dict["aisUppers"]]), c='red', label='Stan (uncollapsed)')
	plt.errorbar(stan_uc_dict["raisTimes"], stan_uc_dict["raisMeans"], np.array([stan_uc_dict["raisLowers"], stan_uc_dict["raisUppers"]]), c='red')

	plt.errorbar(stan_c_dict["aisTimes"], stan_c_dict["aisMeans"], np.array([stan_c_dict["aisLowers"], stan_c_dict["aisUppers"]]), c='darkred', label='Stan (collapsed)')
	plt.errorbar(stan_c_dict["raisTimes"], stan_c_dict["raisMeans"], np.array([stan_c_dict["raisLowers"], stan_c_dict["raisUppers"]]), c='darkred')

	plt.errorbar(webppl_uc_dict["aisTimes"], webppl_uc_dict["aisMeans"], np.array([webppl_uc_dict["aisLowers"], webppl_uc_dict["aisUppers"]]), c='blue', label='Webppl (uncollapsed)')
	plt.errorbar(webppl_uc_dict["raisTimes"], webppl_uc_dict["raisMeans"], np.array([webppl_uc_dict["raisLowers"], webppl_uc_dict["raisUppers"]]), c='blue')

	plt.errorbar(webppl_c_dict["aisTimes"], webppl_c_dict["aisMeans"], np.array([webppl_c_dict["aisLowers"], webppl_c_dict["aisUppers"]]), c='darkblue', label='Webppl (collapsed)')
	plt.errorbar(webppl_c_dict["raisTimes"], webppl_c_dict["raisMeans"], np.array([webppl_c_dict["raisLowers"], webppl_c_dict["raisUppers"]]), c='darkblue')

	plt.legend()
	plt.show()

	# ucDivTimes = uc_dict["aisTimes"] + uc_dict["raisTimes"]
	# ucDivMeans = uc_dict["raisMeans"] - uc_dict["aisMeans"]
	# ucDivLowers = uc_dict["raisLowers"] + uc_dict["aisUppers"]
	# ucDivUppers = uc_dict["raisUppers"] + uc_dict["aisLowers"]
	# plt.errorbar(ucDivTimes, ucDivMeans, np.array([ucDivLowers, ucDivUppers]), c='red', label='Uncollapsed')

	# cDivTimes = c_dict["aisTimes"] + c_dict["raisTimes"]
	# cDivMeans = c_dict["raisMeans"] - c_dict["aisMeans"]
	# cDivLowers = c_dict["raisLowers"] + c_dict["aisUppers"]
	# cDivUppers = c_dict["raisUppers"] + c_dict["aisLowers"]
	# plt.errorbar(cDivTimes, cDivMeans, np.array([cDivLowers, cDivUppers]), c='blue', label='Collapsed')

	# plt.xlabel("Time (in sec)")
	# plt.ylabel("Jeffreys Divergence (nats)")
	# plt.title("Collapsed vs Uncollapsed Matrix Factorization - Time")
	# plt.legend(loc="upper right")
	# all_times = np.concatenate([ucDivTimes, cDivTimes])
	# plt.xscale('log')
	# plt.xlim(*pretty_xlim(min(all_times), max(all_times), scale='log'))
	# plt.savefig('experiments/mf/stan/plots/times.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()