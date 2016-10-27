import matplotlib.pyplot as plt
import numpy as np
import sys
from plotting.util import read_files_dict, pretty_xlim

def main():
	
	webppl_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_uc", sort="times", lang='webppl')
	webppl_c_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_c", sort="times", lang='webppl')
	stan_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_uc", sort="times", lang='stan')
	stan_c_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_c", sort="times", lang='stan')

	plt.errorbar(stan_uc_dict["aisTimes"], stan_uc_dict["aisMeans"], np.array([stan_uc_dict["aisLowers"], stan_uc_dict["aisUppers"]]), c='red', label='Stan (uc)')
	plt.errorbar(stan_uc_dict["raisTimes"], stan_uc_dict["raisMeans"], np.array([stan_uc_dict["raisLowers"], stan_uc_dict["raisUppers"]]), c='red')

	plt.errorbar(stan_c_dict["aisTimes"], stan_c_dict["aisMeans"], np.array([stan_c_dict["aisLowers"], stan_c_dict["aisUppers"]]), c='maroon', label='Stan (c)')
	plt.errorbar(stan_c_dict["raisTimes"], stan_c_dict["raisMeans"], np.array([stan_c_dict["raisLowers"], stan_c_dict["raisUppers"]]), c='maroon')

	plt.errorbar(webppl_uc_dict["aisTimes"], webppl_uc_dict["aisMeans"], np.array([webppl_uc_dict["aisLowers"], webppl_uc_dict["aisUppers"]]), c='dodgerblue', label='WebPPL (uc)')
	plt.errorbar(webppl_uc_dict["raisTimes"], webppl_uc_dict["raisMeans"], np.array([webppl_uc_dict["raisLowers"], webppl_uc_dict["raisUppers"]]), c='dodgerblue')

	plt.errorbar(webppl_c_dict["aisTimes"], webppl_c_dict["aisMeans"], np.array([webppl_c_dict["aisLowers"], webppl_c_dict["aisUppers"]]), c='darkblue', label='WebPPL (c)')
	plt.errorbar(webppl_c_dict["raisTimes"], webppl_c_dict["raisMeans"], np.array([webppl_c_dict["raisLowers"], webppl_c_dict["raisUppers"]]), c='darkblue')

	plt.xlabel("Time (in sec)", fontsize='xx-large')
	plt.ylabel("Marginal log likelihood (nats)", fontsize='xx-large')
	plt.legend(loc='lower right', fontsize='x-large')
	all_times = np.concatenate([d[c] for d in [stan_c_dict, stan_uc_dict, webppl_c_dict, webppl_uc_dict] for c in ["aisTimes", "raisTimes"]])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_times), max(all_times), scale='log'))
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan-webppl/plots/bounds-times.pdf')
	plt.clf()

	ucDivStanTimes = stan_uc_dict["aisTimes"] + stan_uc_dict["raisTimes"]
	ucDivStanMeans = stan_uc_dict["raisMeans"] - stan_uc_dict["aisMeans"]
	ucDivStanLowers = stan_uc_dict["raisLowers"] + stan_uc_dict["aisUppers"]
	ucDivStanUppers = stan_uc_dict["raisUppers"] + stan_uc_dict["aisLowers"]
	plt.errorbar(ucDivStanTimes, ucDivStanMeans, np.array([ucDivStanLowers, ucDivStanUppers]), c='red', label='Stan (uc)')

	cDivStanTimes = stan_c_dict["aisTimes"] + stan_c_dict["raisTimes"]
	cDivStanMeans = stan_c_dict["raisMeans"] - stan_c_dict["aisMeans"]
	cDivStanLowers = stan_c_dict["raisLowers"] + stan_c_dict["aisUppers"]
	cDivStanUppers = stan_c_dict["raisUppers"] + stan_c_dict["aisLowers"]
	plt.errorbar(cDivStanTimes, cDivStanMeans, np.array([cDivStanLowers, cDivStanUppers]), c='maroon', label='Stan (c)')

	ucDivWebpplTimes = webppl_uc_dict["aisTimes"] + webppl_uc_dict["raisTimes"]
	ucDivWebpplMeans = webppl_uc_dict["raisMeans"] - webppl_uc_dict["aisMeans"]
	ucDivWebpplLowers = webppl_uc_dict["raisLowers"] + webppl_uc_dict["aisUppers"]
	ucDivWebpplUppers = webppl_uc_dict["raisUppers"] + webppl_uc_dict["aisLowers"]
	plt.errorbar(ucDivWebpplTimes, ucDivWebpplMeans, np.array([ucDivWebpplLowers, ucDivWebpplUppers]), c='dodgerblue', label='WebPPL (uc)')

	cDivWebpplTimes = webppl_c_dict["aisTimes"] + webppl_c_dict["raisTimes"]
	cDivWebpplMeans = webppl_c_dict["raisMeans"] - webppl_c_dict["aisMeans"]
	cDivWebpplLowers = webppl_c_dict["raisLowers"] + webppl_c_dict["aisUppers"]
	cDivWebpplUppers = webppl_c_dict["raisUppers"] + webppl_c_dict["aisLowers"]
	plt.errorbar(cDivWebpplTimes, cDivWebpplMeans, np.array([cDivWebpplLowers, cDivWebpplUppers]), c='darkblue', label='WebPPL (c)')

	plt.xlabel("Time (in sec)", fontsize='xx-large')
	plt.ylabel("Jeffreys divergence bound (nats)", fontsize='xx-large')
	plt.legend(loc='lower left', fontsize='x-large')
	all_times = np.concatenate([ucDivStanTimes, cDivStanTimes, ucDivWebpplTimes, cDivWebpplTimes])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_times), max(all_times), scale='log'))
	plt.yscale('log')
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan-webppl/plots/gaps-times.pdf', format='pdf', dpi=1000)
	plt.clf()

	webppl_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_uc", sort="steps", lang='webppl')
	webppl_c_dict = read_files_dict("experiments/mf/stan-webppl/results/webppl/output_c", sort="steps", lang='webppl')
	stan_uc_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_uc", sort="steps", lang='stan')
	stan_c_dict = read_files_dict("experiments/mf/stan-webppl/results/stan/output_c", sort="steps", lang='stan')

	plt.errorbar(stan_uc_dict["aisSteps"], stan_uc_dict["aisMeans"], np.array([stan_uc_dict["aisLowers"], stan_uc_dict["aisUppers"]]), c='red', label='Stan (uc)')
	plt.errorbar(stan_uc_dict["raisSteps"], stan_uc_dict["raisMeans"], np.array([stan_uc_dict["raisLowers"], stan_uc_dict["raisUppers"]]), c='red')

	plt.errorbar(stan_c_dict["aisSteps"], stan_c_dict["aisMeans"], np.array([stan_c_dict["aisLowers"], stan_c_dict["aisUppers"]]), c='maroon', label='Stan (c)')
	plt.errorbar(stan_c_dict["raisSteps"], stan_c_dict["raisMeans"], np.array([stan_c_dict["raisLowers"], stan_c_dict["raisUppers"]]), c='maroon')

	plt.errorbar(webppl_uc_dict["aisSteps"], webppl_uc_dict["aisMeans"], np.array([webppl_uc_dict["aisLowers"], webppl_uc_dict["aisUppers"]]), c='dodgerblue', label='WebPPL (uc)')
	plt.errorbar(webppl_uc_dict["raisSteps"], webppl_uc_dict["raisMeans"], np.array([webppl_uc_dict["raisLowers"], webppl_uc_dict["raisUppers"]]), c='dodgerblue')

	plt.errorbar(webppl_c_dict["aisSteps"], webppl_c_dict["aisMeans"], np.array([webppl_c_dict["aisLowers"], webppl_c_dict["aisUppers"]]), c='darkblue', label='WebPPL (c)')
	plt.errorbar(webppl_c_dict["raisSteps"], webppl_c_dict["raisMeans"], np.array([webppl_c_dict["raisLowers"], webppl_c_dict["raisUppers"]]), c='darkblue')

	plt.xlabel("Number of steps", fontsize='xx-large')
	plt.ylabel("Marginal log likelihood (nats)", fontsize='xx-large')
	plt.legend(loc='lower right', fontsize='large')
	all_steps = np.concatenate([d[c] for d in [stan_c_dict, stan_uc_dict, webppl_c_dict, webppl_uc_dict] for c in ["aisSteps", "raisSteps"]])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan-webppl/plots/bounds-steps.pdf')
	plt.clf()

	assert np.all(stan_uc_dict["aisSteps"] == stan_uc_dict["raisSteps"])
	ucDivStanSteps = stan_uc_dict["aisSteps"]
	ucDivStanMeans = stan_uc_dict["raisMeans"] - stan_uc_dict["aisMeans"]
	ucDivStanLowers = stan_uc_dict["raisLowers"] + stan_uc_dict["aisUppers"]
	ucDivStanUppers = stan_uc_dict["raisUppers"] + stan_uc_dict["aisLowers"]
	plt.errorbar(ucDivStanSteps, ucDivStanMeans, np.array([ucDivStanLowers, ucDivStanUppers]), c='red', label='Stan (uc)')

	assert np.all(stan_c_dict["aisSteps"] == stan_c_dict["raisSteps"])
	cDivStanSteps = stan_c_dict["aisSteps"]
	cDivStanMeans = stan_c_dict["raisMeans"] - stan_c_dict["aisMeans"]
	cDivStanLowers = stan_c_dict["raisLowers"] + stan_c_dict["aisUppers"]
	cDivStanUppers = stan_c_dict["raisUppers"] + stan_c_dict["aisLowers"]
	plt.errorbar(cDivStanSteps, cDivStanMeans, np.array([cDivStanLowers, cDivStanUppers]), c='maroon', label='Stan (c)')

	assert np.all(webppl_uc_dict["aisSteps"] == webppl_uc_dict["raisSteps"])
	ucDivWebpplSteps = webppl_uc_dict["aisSteps"]
	ucDivWebpplMeans = webppl_uc_dict["raisMeans"] - webppl_uc_dict["aisMeans"]
	ucDivWebpplLowers = webppl_uc_dict["raisLowers"] + webppl_uc_dict["aisUppers"]
	ucDivWebpplUppers = webppl_uc_dict["raisUppers"] + webppl_uc_dict["aisLowers"]
	plt.errorbar(ucDivWebpplSteps, ucDivWebpplMeans, np.array([ucDivWebpplLowers, ucDivWebpplUppers]), c='dodgerblue', label='WebPPL (uc)')

	assert np.all(webppl_c_dict["aisSteps"] == webppl_c_dict["raisSteps"])
	cDivWebpplSteps = webppl_c_dict["aisSteps"]
	cDivWebpplMeans = webppl_c_dict["raisMeans"] - webppl_c_dict["aisMeans"]
	cDivWebpplLowers = webppl_c_dict["raisLowers"] + webppl_c_dict["aisUppers"]
	cDivWebpplUppers = webppl_c_dict["raisUppers"] + webppl_c_dict["aisLowers"]
	plt.errorbar(cDivWebpplSteps, cDivWebpplMeans, np.array([cDivWebpplLowers, cDivWebpplUppers]), c='darkblue', label='WebPPL (c)')

	plt.xlabel("Number of steps", fontsize='xx-large')
	plt.ylabel("Jeffreys divergence bound (nats)", fontsize='xx-large')
	plt.legend(loc='lower left', fontsize='x-large')
	all_steps = np.concatenate([ucDivStanSteps, cDivStanSteps, ucDivWebpplSteps, cDivWebpplSteps])
	plt.xscale('log')
	plt.xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	plt.yscale('log')
	plt.tick_params(labelsize='xx-large')
	plt.tight_layout()
	plt.savefig('experiments/mf/stan-webppl/plots/gaps-steps.pdf', format='pdf', dpi=1000)

if __name__ == '__main__':
	main()