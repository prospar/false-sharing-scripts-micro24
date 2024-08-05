# This script is for generating plots in the introduction for our ASPLOS24 submission.
# python3 src/main.py --tasks result --verbose 1 --outputDir asplos24-intro
# python3 sb-intro-asplos24.py
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


PATH_CSV = "/home/prospar/prospar-micro-result/micro-parsec/Stats_Avg.csv"
PATH_CSV = str(sys.argv[1])
KEY_BENCH = "bench"
KEY_PROTOCOL = "protocol"
KEY_RUNTIME = "KEY_SIM_TICKS"
KEY_MSG_VOL = "KEY_TOTAL_MSG_VOL"
KEY_MSG_COUNT = "KEY_TOTAL_MSG_COUNT"
KEY_ENERGY_PAM = "KEY_TOTAL_PAM_ENERGY"
KEY_ENERGY_SAM = "KEY_TOTAL_SAM_ENERGY"
KEY_ENERGY_L1D = "KEY_TOTAL_L1D_ENERGY"
KEY_ENERGY_LLC = "KEY_TOTAL_LLC_ENERGY"
# KEY_ENERGY_CPU2L1D = "KEY_TOTAL_CPU_TO_L1_ENERGY"
KEY_ENERGY_CPU2L1D = "KEY_CPU_TO_L1_ENERGY"
KEY_ENERGY_FILL = "KEY_FILL_COHERENCE_ENERGY"
KEY_TOTAL_LEAKAGE = "KEY_TOTAL_STATIC_LEAKAGE"

# vipin: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_RUNTIME = 6
IDX_MSG_VOL =  101 #98
IDX_MSG_COUNT = 102 #99
IDX_ENERGY_PAM = 60
IDX_ENERGY_SAM = 61
IDX_ENERGY_L1D = 62
IDX_ENERGY_LLC = 63
IDX_ENERGY_CPU2L1D = 64
IDX_ENERGY_FILL = 65
IDX_ENERGY_LEAKAGE = 66

# BENCH_NAMES = [
#   "feather-test1-small", "feather-test3-small", "feather-test4-small", "feather-test6-small",
#   "feather-test8-small", "feather-test9-small", "huron-boost-spinlock", "huron-hist",
#   "huron-linear-reg", "huron-locked-toy", "huron-lockless-toy", "huron-lu-ncb", "huron-ref-count",
#   "huron-string-match"
#   #, "SPIN-lazy-list"
# ]

BENCH_NAMES = [ 
  "blackscholes", "bodytrack", "canneal", "facesim", "fluidanimate", "swaptions"
]

x_labels = [
  "BL", "BO", "CA", "FA", "FL", "SW", "geomean"
]

bench_data = {}

# equally distribute the label locations along x axis
index = np.arange(len(x_labels))
index = np.arange(0.0,7.0,1.0)

width = 0.3  # the width of the bars

PRECISION = 2  # digits


def str_to_float(_inp: str) -> float:
  """Return float equivalent of the string, return zero if empty string.
    """
  _inp = _inp.strip()
  return float(_inp) if _inp else 0


def getColorsList():
  # mcolors = list(matplotlib.colors.cnames.keys())
  # CSS colours used from
  # https://matplotlib.org/3.3.0/gallery/color/named_colors.html
  return ['slategray', 'lightgrey', 'dimgray', 'darkgray', 'silver', 'y', 'k']


def plot_data(orig_data, manual_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(3.2, 1.6), dpi=120, facecolor='w', edgecolor='k')
  fig.set_figheight(1)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 6.5
  ax.set_xticks(index + width / 2)
  # ax.set_xticks(index )
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.05
  plt.ylim(0.8, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects2 = ax.bar(
    index + width / 2,
    manual_data,
    width,
    align="center",
    # label='Manual',
    # hatch='//',
    color=(0.3, 0.3, 0.3, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')
  for bar, label in zip(rects2, manual_data):# if bars == rects1 else manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      # elif height == 1.0:
      #   continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)

  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def plot_time_energy_data(runtime_data, energy_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(2.5, 0.6), dpi=120, facecolor='w', edgecolor='k')
  fig.set_figheight(0.6)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 6.5
  ax.set_xticks(index)
  # ax.set_xticks(index )
  
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel("Speedup", fontsize=7)
  MAX_HT = 1.02
  ax.set_yticks([0.98,1.0,1.02])
  ax.set_yticklabels([0.98,1.0,1.02],fontsize=7)
  ax.set_ylim(0.98, MAX_HT)
  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects2 = ax.bar(
    index - (width/2),
    runtime_data,
    width,
    # align="center",
    label='Speedup',
    # hatch='//',
    color=(0.6, 0.6, 0.6, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')
  for bar, label in zip(rects2, runtime_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() - bar.get_width()/4, height-0.003),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=6,rotation=0)

  #plotting energy data
  ax2 = ax.twinx()
  ax2.set_ylim(0.98, MAX_HT)
  ax2.set_yticks([0.98,1.0,1.02])
  ax2.set_yticklabels([0.98,1.0,1.02],fontsize=7)
  ax2.set_ylabel("Normalized \n energy", fontsize=7)

  rects3 = ax2.bar(
    index,
    energy_data,
    width,
    align="edge",
    label='Energy',
    # hatch='//',
    color=(0.8, 0.8, 0.8, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')
  for bar, label in zip(rects3, energy_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax2.annotate('{}'.format(label),
                  xy=((bar.get_x() + (bar.get_width()/2)+0.1) , height-0.008),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=6,rotation=0)
  # ax2.legend(loc='lower right', ncol=1, fontsize=6, frameon=False,labelspacing=0.01, borderpad=0.01)
  # ax.legend(loc='upper right', bbox_to_anchor=(1,0.85), ncol=1, fontsize=6, frameon=False,labelspacing=0.01, borderpad=0.01)

  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        assert (row.index(KEY_PROTOCOL) == IDX_PROTOCOL)
        assert (row.index(KEY_BENCH) == IDX_BENCH)
        assert (row.index(KEY_RUNTIME) == IDX_RUNTIME)
        assert (row.index(KEY_MSG_VOL) == IDX_MSG_VOL)
        assert (row.index(KEY_MSG_COUNT) == IDX_MSG_COUNT)
        assert (row.index(KEY_ENERGY_PAM) == IDX_ENERGY_PAM)
        assert (row.index(KEY_ENERGY_SAM) == IDX_ENERGY_SAM)
        assert (row.index(KEY_ENERGY_L1D) == IDX_ENERGY_L1D)
        assert (row.index(KEY_ENERGY_LLC) == IDX_ENERGY_LLC)
        assert (row.index(KEY_ENERGY_CPU2L1D) == IDX_ENERGY_CPU2L1D)
        assert (row.index(KEY_ENERGY_FILL) == IDX_ENERGY_FILL)
        assert (row.index(KEY_TOTAL_LEAKAGE) == IDX_ENERGY_LEAKAGE)

      elif row_num > 2:
        tmp = {}
        tmp[KEY_RUNTIME] = str_to_float(row[IDX_RUNTIME])
        tmp[KEY_MSG_VOL] = str_to_float(row[IDX_MSG_VOL])
        tmp[KEY_MSG_COUNT] = str_to_float(row[IDX_MSG_COUNT])
        tmp[KEY_ENERGY_L1D] = str_to_float(row[IDX_ENERGY_L1D])
        tmp[KEY_ENERGY_LLC] = str_to_float(row[IDX_ENERGY_LLC])
        tmp[KEY_ENERGY_PAM] = str_to_float(row[IDX_ENERGY_PAM])
        tmp[KEY_ENERGY_SAM] = str_to_float(row[IDX_ENERGY_SAM])
        tmp[KEY_ENERGY_CPU2L1D] = str_to_float(row[IDX_ENERGY_CPU2L1D])
        tmp[KEY_ENERGY_FILL] = str_to_float(row[IDX_ENERGY_FILL])
        tmp[KEY_TOTAL_LEAKAGE] = str_to_float(row[IDX_ENERGY_LEAKAGE])
        # VIPIN: BYPASS the assert for repair and detect protocol
        if "FS_MESI" not in row[IDX_PROTOCOL]:
          assert (tmp[KEY_ENERGY_PAM] == 0 and tmp[KEY_ENERGY_SAM] == 0)
        # VIPIN: adding protocol specific name to differentiate entry in map
        # if "FS_MESI_DETECTION" in row[IDX_PROTOCOL]:
          # bench_data[row[IDX_BENCH]+ "-detect"] = tmp
        if "FS_MESI" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp
        else:
          bench_data[row[IDX_BENCH]] = tmp
      row_num += 1

def plot_time_energy():
  #### Rutime bar:
  fs_abs_times = []
  bench_repair_abs_time = []
  for bench in BENCH_NAMES:
    bench_fs_run_time = bench_data[bench][KEY_RUNTIME]
    fs_abs_times.append(bench_fs_run_time)
    # detect protocol
    # bench_detect = bench + "-detect"
    # bench_detect_run_time = bench_data[bench_detect][KEY_RUNTIME]
    # bench_detect_abs_time.append(bench_detect_run_time)
    # repair protocol
    bench_repair = bench + "-repair"
    bench_repair_run_time = bench_data[bench_repair][KEY_RUNTIME]
    bench_repair_abs_time.append(bench_repair_run_time)

  fs_norm_times = [1 for x in fs_abs_times]
  # ealier n/d gives speedup, now d/n gives normalized value
  # detect_norm_times = [round(n / d, PRECISION) for n, d in zip(bench_detect_abs_time, fs_abs_times)]
  repair_norm_times = [round(n / d, PRECISION) for n, d in zip(bench_repair_abs_time, fs_abs_times)]
  fs_norm_times.append(1.0)
  geomean = np.prod(repair_norm_times) ** (1.0 / len(repair_norm_times))
  repair_norm_times.append(round(geomean,PRECISION))

  ### Energy bar
  fs_abs_energy = []
  # detect_abs_energy = []
  repair_abs_energy = []
  for bench in BENCH_NAMES:
    bench_fs_l1denergy = bench_data[bench][KEY_ENERGY_L1D]
    bench_fs_llcenergy = bench_data[bench][KEY_ENERGY_LLC]
    bench_fs_pamenergy = bench_data[bench][KEY_ENERGY_PAM]
    bench_fs_samenergy = bench_data[bench][KEY_ENERGY_SAM]
    bench_fs_cpu2l1denergy = bench_data[bench][KEY_ENERGY_CPU2L1D]
    bench_fs_fillenergy = bench_data[bench][KEY_ENERGY_FILL]
    bench_fs_staticleakage = bench_data[bench][KEY_TOTAL_LEAKAGE]
    # fs_abs_energy.append(bench_fs_l1denergy + bench_fs_llcenergy + bench_fs_pamenergy +
                        #  bench_fs_samenergy)
    fs_abs_energy.append( bench_fs_pamenergy + bench_fs_samenergy +
                         bench_fs_cpu2l1denergy + bench_fs_fillenergy +
                         bench_fs_staticleakage)

    bench_repair = bench + "-repair"
    bench_repair_l1denergy = bench_data[bench_repair][KEY_ENERGY_L1D]
    bench_repair_llcenergy = bench_data[bench_repair][KEY_ENERGY_LLC]
    bench_repair_pamenergy = bench_data[bench_repair][KEY_ENERGY_PAM]
    bench_repair_samenergy = bench_data[bench_repair][KEY_ENERGY_SAM]
    bench_repair_cpu2l1denergy = bench_data[bench_repair][KEY_ENERGY_CPU2L1D]
    bench_repair_fillenergy = bench_data[bench_repair][KEY_ENERGY_FILL]
    bench_repair_staticleakage = bench_data[bench_repair][KEY_TOTAL_LEAKAGE]
    repair_abs_energy.append(bench_repair_pamenergy + bench_repair_samenergy
                             + bench_repair_cpu2l1denergy + bench_repair_fillenergy
                             + bench_repair_staticleakage)

  fs_norm_energy = [1 for x in fs_abs_energy]

  # detect_norm_energy = [round(n / d, PRECISION) for n, d in zip(detect_abs_energy, fs_abs_energy)]

  repair_norm_energy = [round(n / d, PRECISION) for n, d in zip(repair_abs_energy, fs_abs_energy)]
  fs_norm_energy.append(1.0)
  geomean = np.prod(repair_norm_energy) ** (1.0 / len(repair_norm_energy))
  repair_norm_energy.append(round(geomean,PRECISION))

  plot_time_energy_data(repair_norm_times, repair_norm_energy, "--", "plot-parsec-runtime-energy.pdf")



def main():
  read_csv_file()
  plot_time_energy()


if __name__ == "__main__":
  main()
