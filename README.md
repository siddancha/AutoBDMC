# AutoBDMC
<b>AutoBDMC</b> is a tool based on <a href=http://arxiv.org/pdf/1511.02543v1.pdf>bidirectional Monte Carlo</a> to accurately evaluate and
bound log likelihoods of synthetic data via annealed importance sampling in an automated fashion by integrating it with probabilisitic
programming languages, such as Stan and WebPPL.

This repository contains an implementation of this tool in Stan (and WebPPL), as well as experiments that validate the use of this tool
and demonstrate scientific findings produced by it.

## Instructions
Each experiment is represented by a subfolder in the "experiments" folder. To run an experiment from scratch, run
```sh
bash experiments/<EXP_NAME>/scripts/main.sh [--run] [--parallel] [--clean]
```
<ol>
<li><code>--run</code><br>
To actually run the experiment.<br>

<li><code>--parallel</code><br>
An experiment consists of a set of independent jobs, which are run serially by default. If you have access to a CPU cluster with <a href=http://www.gnu.org/software/parallel>GNU parallel</a> installed, you can use this flag to parallelize the
jobs.<br>

<li><code>--clean</code><br>
The script generates data files, exact-sample files, job lists, results and plots. Use this flag to delete all generated files and clean the directory, in order to re-run the experiment. <em>Caution</em>: all unsaved work will be lost.
</ol>

Example: <code>bash experiments/mf/scripts/main.sh --run --parallel</code>

After the script finishes execution, generated plots will be available in experiments/<i>EXP_NAME</i>/plots.