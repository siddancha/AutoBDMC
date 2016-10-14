import matplotlib.pyplot as plt
import numpy as np
import sys
from plotting.util import read_files_dict, pretty_xlim

def main():
	
	webppl_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_uc", sort="times", lang='webppl')
	webppl_c_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_c", sort="times", lang='webppl')
	stan_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_uc", sort="times", lang='stan')
	stan_c_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_c", sort="times", lang='stan')

	plt.errorbar(stan_uc_dict["aisTimes"], stan_uc_dict["aisMeans"], np.array([stan_uc_dict["aisLowers"], stan_uc_dict["aisUppers"]]), c='red', label='Stan (uncollapsed)')
	plt.errorbar(stan_uc_dict["raisTimes"], stan_uc_dict["raisMeans"], np.array([stan_uc_dict["raisLowers"], stan_uc_dict["raisUppers"]]), c='red')

	plt.errorbar(stan_c_dict["aisTimes"], stan_c_dict["aisMeans"], np.array([stan_c_dict["aisLowers"], stan_c_dict["aisUppers"]]), c='maroon', label='Stan (collapsed)')
	plt.errorbar(stan_c_dict["raisTimes"], stan_c_dict["raisMeans"], np.array([stan_c_dict["raisLowers"], stan_c_dict["raisUppers"]]), c='maroon')

	plt.errorbar(webppl_uc_dict["aisTimes"], webppl_uc_dict["aisMeans"], np.array([webppl_uc_dict["aisLowers"], webppl_uc_dict["aisUppers"]]), c='dodgerblue', label='WebPPL (uncollapsed)')
	plt.errorbar(webppl_uc_dict["raisTimes"], webppl_uc_dict["raisMeans"], np.array([webppl_uc_dict["raisLowers"], webppl_uc_dict["raisUppers"]]), c='dodgerblue')

	plt.errorbar(webppl_c_dict["aisTimes"], webppl_c_dict["aisMeans"], np.array([webppl_c_dict["aisLowers"], webppl_c_dict["aisUppers"]]), c='darkblue', label='WebPPL (collapsed)')
	plt.errorbar(webppl_c_dict["raisTimes"], webppl_c_dict["raisMeans"], np.array([webppl_c_dict["raisLowers"], webppl_c_dict["raisUppers"]]), c='darkblue')

	plt.xlabel("Time (in sec)")
	plt.ylabel("Marginal Log Likelihood (nats)")
	plt.title("Collapsed and Uncollapsed Matrix Factorization in Stan and WebPPL", fontsize=12)
	plt.legend(loc='lower right', prop={'size': 12})
	all_times = np.concatenate([d[c] for d in [stan_c_dict, stan_uc_dict, webppl_c_dict, webppl_uc_dict] for c in ["aisTimes", "raisTimes"]])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_times), max(all_times), scale='log'))
	plt.savefig('experiments/mf/stan-webppl/plots/bounds.pdf')
	plt.clf()

	ucDivStanTimes = stan_uc_dict["aisTimes"] + stan_uc_dict["raisTimes"]
	ucDivStanMeans = stan_uc_dict["raisMeans"] - stan_uc_dict["aisMeans"]
	ucDivStanLowers = stan_uc_dict["raisLowers"] + stan_uc_dict["aisUppers"]
	ucDivStanUppers = stan_uc_dict["raisUppers"] + stan_uc_dict["aisLowers"]
	plt.errorbar(ucDivStanTimes, ucDivStanMeans, np.array([ucDivStanLowers, ucDivStanUppers]), c='red', label='Stan (uncollapsed)')

	cDivStanTimes = stan_c_dict["aisTimes"] + stan_c_dict["raisTimes"]
	cDivStanMeans = stan_c_dict["raisMeans"] - stan_c_dict["aisMeans"]
	cDivStanLowers = stan_c_dict["raisLowers"] + stan_c_dict["aisUppers"]
	cDivStanUppers = stan_c_dict["raisUppers"] + stan_c_dict["aisLowers"]
	plt.errorbar(cDivStanTimes, cDivStanMeans, np.array([cDivStanLowers, cDivStanUppers]), c='maroon', label='Stan (collapsed)')

	ucDivWebpplTimes = webppl_uc_dict["aisTimes"] + webppl_uc_dict["raisTimes"]
	ucDivWebpplMeans = webppl_uc_dict["raisMeans"] - webppl_uc_dict["aisMeans"]
	ucDivWebpplLowers = webppl_uc_dict["raisLowers"] + webppl_uc_dict["aisUppers"]
	ucDivWebpplUppers = webppl_uc_dict["raisUppers"] + webppl_uc_dict["aisLowers"]
	plt.errorbar(ucDivWebpplTimes, ucDivWebpplMeans, np.array([ucDivWebpplLowers, ucDivWebpplUppers]), c='dodgerblue', label='WebPPL (uncollapsed)')

	cDivWebpplTimes = webppl_c_dict["aisTimes"] + webppl_c_dict["raisTimes"]
	cDivWebpplMeans = webppl_c_dict["raisMeans"] - webppl_c_dict["aisMeans"]
	cDivWebpplLowers = webppl_c_dict["raisLowers"] + webppl_c_dict["aisUppers"]
	cDivWebpplUppers = webppl_c_dict["raisUppers"] + webppl_c_dict["aisLowers"]
	plt.errorbar(cDivWebpplTimes, cDivWebpplMeans, np.array([cDivWebpplLowers, cDivWebpplUppers]), c='darkblue', label='WebPPL (collapsed)')

	plt.xlabel("Time (in sec)")
	plt.ylabel("Jeffreys Divergence (nats)")
	plt.title("Collapsed and Uncollapsed Matrix Factorization in Stan and WebPPL", fontsize=12)
	plt.legend(loc='upper right', prop={'size': 12})
	all_steps = np.concatenate([ucDivStanTimes, cDivStanTimes, ucDivWebpplTimes, cDivWebpplTimes])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	plt.savefig('experiments/mf/stan-webppl/plots/gaps.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()