import matplotlib.pyplot as plt
import numpy as np
from plotting.util import read_files_dict, pretty_xlim
import sys

def display(ax, pos, data, color, label, hshift=0):
    shifted_pos = pos * (1.0 + hshift)
    bp = ax.boxplot(data, positions=shifted_pos, widths=0.1*shifted_pos, whis=3)
    for box in bp['boxes']:
        box.set(color=color)
    for whisker in bp['whiskers']:
        whisker.set(color=color)
    for cap in bp['caps']:
        cap.set(color=color)
    for median in bp['medians']:
        median.set(color=color)
    for flier in bp['fliers']:
        flier.set(markeredgecolor=color)
    ax.plot(pos, [np.median(d) for d in data], ls='-', color=color, label=label)

def main():
	SUBEXP = sys.argv[1]
	subexp_folder = str.format("experiments/real_data/{0}", SUBEXP)
	s_dict = read_files_dict(subexp_folder + "/results/synthetic")
	r_dict = read_files_dict(subexp_folder + "/results/real")
	
	fig, ax1 = plt.subplots()
	all_steps = np.concatenate([s_dict["aisSteps"], s_dict["raisSteps"], r_dict["aisSteps"]])
	
	display(ax1, s_dict["raisSteps"], s_dict["raisWeights"], color='darkred', label='simulated-RAIS')
	display(ax1, s_dict["aisSteps"], s_dict["aisWeights"], color='red', label='simulated-AIS')
	ax1.set_xlabel("Number of steps", fontsize='xx-large')
	ax1.set_ylabel("Log ML estimate", fontsize='xx-large')
	ax1.set_xlim(*pretty_xlim(0.9*min(all_steps), 1.1*max(all_steps), scale='log'))
	ax1.set_xscale('log')
	ax1.tick_params(labelsize='xx-large')
	for tl in ax1.get_yticklabels():
		tl.set_color('red')

	ax2 = ax1.twinx()
	display(ax2, r_dict["aisSteps"], r_dict["aisWeights"], color='blue', label='real-AIS', hshift=0.03)
	ax2.set_xlim(*pretty_xlim(0.9*min(all_steps), 1.1*max(all_steps), scale='log'))
	ax2.set_xscale('log')
	ax2.tick_params(labelsize='xx-large')
	for tl in ax2.get_yticklabels():
		tl.set_color('blue')

	# Alignment
	s_converge = max([np.median(row) for row in s_dict["aisWeights"]])
	r_converge = max([np.median(row) for row in r_dict["aisWeights"]])
	y1_low, y1_high = ax1.get_ylim()
	y2_low, y2_high = ax2.get_ylim()
	del_high = max(y1_high - s_converge, y2_high - r_converge)
	del_low = max(s_converge - y1_low, r_converge - y2_low)
	ax1.set_ylim(s_converge - del_low, s_converge + del_high)
	ax2.set_ylim(r_converge - del_low, r_converge + del_high)
	
	h1, l1 = ax1.get_legend_handles_labels()
	h2, l2 = ax2.get_legend_handles_labels()
	ax1.legend(h1 + h2, l1 + l2, loc="lower right", fontsize='x-large')
	plt.tight_layout()
	plt.show()

if __name__ == '__main__':
	main()