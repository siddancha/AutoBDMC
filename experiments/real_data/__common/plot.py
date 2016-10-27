import matplotlib.pyplot as plt
import numpy as np
from plotting.util import read_files_dict, pretty_xlim
import sys

def main():
	SUBEXP = sys.argv[1]
	subexp_folder = str.format("experiments/real_data/{0}", SUBEXP)
	s_dict = read_files_dict(subexp_folder + "/results/synthetic")
	r_dict = read_files_dict(subexp_folder + "/results/real")
	
	fig, ax1 = plt.subplots()
	all_steps = np.concatenate([s_dict["aisSteps"], s_dict["raisSteps"], r_dict["aisSteps"]])
	
	ax1.errorbar(s_dict["raisSteps"], s_dict["raisMeans"], np.array([s_dict["raisLowers"], s_dict["raisUppers"]]), c='darkred', label='synthetic-RAIS')
	ax1.errorbar(s_dict["aisSteps"], s_dict["aisMeans"], np.array([s_dict["aisLowers"], s_dict["aisUppers"]]), c='red', label='synthetic-AIS')
	ax1.set_xlabel("Number of steps", fontsize='xx-large')
	ax1.set_ylabel("Log ML estimate", fontsize='xx-large')
	ax1.set_xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	ax1.set_xscale('log')
	ax1.tick_params(labelsize='xx-large')
	for tl in ax1.get_yticklabels():
		tl.set_color('red')

	ax2 = ax1.twinx()
	ax2.errorbar(r_dict["aisSteps"], r_dict["aisMeans"], np.array([s_dict["aisLowers"], s_dict["aisUppers"]]), c='blue', label='real-AIS')
	ax2.set_xlim(*pretty_xlim(min(all_steps), max(all_steps), scale='log'))
	ax2.set_xscale('log')
	ax2.tick_params(labelsize='xx-large')
	for tl in ax2.get_yticklabels():
		tl.set_color('blue')

	# Alignment
	s_converge = s_dict["raisMeans"].min()
	r_converge = r_dict["aisMeans"].max()
	y1_low, y1_high = ax1.get_ylim()
	y2_low, y2_high = ax2.get_ylim()
	del_high = max(y1_high - s_converge, y2_high - r_converge)
	del_low = max(s_converge - y1_low, r_converge - y2_low)
	ax1.set_ylim(s_converge - del_low, s_converge + del_high)
	ax2.set_ylim(r_converge - del_low, r_converge + del_high)
	
	h1, l1 = ax1.get_legend_handles_labels()
	h2, l2 = ax2.get_legend_handles_labels()
	ax1.legend(h1 + h2, l1 + l2, loc="lower right", fontsize='xx-large')
	plt.tight_layout()
	plt.savefig(subexp_folder + "/plots/plot.pdf", format='pdf', dpi=1000)

if __name__ == '__main__':
	main()