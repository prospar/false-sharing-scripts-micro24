# This script is for generating plots in the introduction for our ASPLOS24 submission.
# python3 src/main.py --tasks result --verbose 1 --outputDir asplos24-intro
# python3 sb-intro-asplos24.py
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# Diff csv file : Stat_formatted.csv, Stats_Avg.csv, Stats_Median.csv, Stats_Max.csv, Stats_Min.csv
PATH_CSV = "/home/prospar/prospar-micro-result/micro-reader-optimization/Stats_Avg.csv"
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
IDX_ENERGY_PAM = 72
IDX_ENERGY_SAM = 73
IDX_ENERGY_L1D = 74
IDX_ENERGY_LLC = 75
IDX_ENERGY_CPU2L1D = 76
IDX_ENERGY_FILL = 77
IDX_ENERGY_LEAKAGE = 78

# BENCH_NAMES = [
#   "feather-test1-small", "feather-test3-small", "feather-test4-small", "feather-test6-small",
#   "feather-test8-small", "feather-test9-small", "huron-boost-spinlock", "huron-hist",
#   "huron-linear-reg", "huron-locked-toy", "huron-lockless-toy", "huron-lu-ncb", "huron-ref-count",
#   "huron-string-match"
#   #, "SPIN-lazy-list"
# ]
#   "huron-boost-spinlock", "huron-ref-count", "streamcluster", "ESTM-specfriendly-tree"
BENCH_NAMES = [
  "huron-boost-spinlock",
  "huron-lockless-toy",
  "huron-linear-reg",
  "huron-locked-toy",
  "huron-ref-count",
  # "streamcluster",
  "ESTM-specfriendly-tree",  # "huron-lu-ncb", "huron-hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
  "huron-string-match"
]

x_labels = [
  "BS",
  "LL",
  "LR",
  "LT",
  "RC",
  # "SC",
  "SF",
  "SM",
  "mean"  # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

bench_data = {}

# equally distribute the label locations along x axis
index = np.arange(len(x_labels))

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

  ax.set_xticks(index + width / 2)
  # ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.05
  plt.ylim(0.7, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  # rects1 = ax.bar(index - width/2,
  #                 orig_data,
  #                 width,
  #                 label='FSversion',
  #                 hatch='x',
  #                 color=(0.4, 0.4, 0.4, 0.6))

  rects2 = ax.bar(
    index ,
    manual_data,
    width,
    align="edge",
    label='Manual',
    hatch='X',
    color=(0.6, 0.6, 0.6, 0.4))

  # plt.axhline(y=1.0, color='k', linestyle='--')

  rects = ax.patches
  # labels = [f"label{i}" for i in range(len(rects))]
  # for rect, label in zip(rects, orig_data):
  #   height = rect.get_height()
  #   if height > MAX_HT:
  #     height = MAX_HT
  #   # elif height == 0.0 and log_scale:
  #   #   height = 0.001
  #   # print(height)
  #   ax.text(rect.get_x() + rect.get_width()/3 ,
  #           height + 0.01,
  #           label,
  #           ha="center",
  #           va="baseline",
  #           size=7,
  #           rotation=0)



  # Show labels over bars
  rects3 = ax.patches
  # labels = [f"label{i}" for i in range(len(rects))]
  for rect, label in zip(rects3, manual_data):
    height = rect.get_height()
    if height > MAX_HT:
      height = MAX_HT
    # elif height == 0.0 and log_scale:
    #   height = 0.001
    # print(height)
    ax.text(rect.get_x() + rect.get_width()/2,
            height + 0.01,
            label,
            ha="center",
            va="baseline",
            size=7,
            rotation=0)
  # fig.tight_layout()
  # plt.show()

  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        print(row.index(KEY_ENERGY_PAM))
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
        #   bench_data[row[IDX_BENCH]+ "-detect"] = tmp
        if "FS_MESI_Opt" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair-opt"] = tmp
        elif "FS_MESI" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp
        # else:
        #   bench_data[row[IDX_BENCH]] = tmp

        # if "manual" not in row[IDX_PROTOCOL]:
        #   bench_data[row[IDX_BENCH]] = tmp
        # else:
        #   bench_data[row[IDX_BENCH]+"-manual"] = tmp
      row_num += 1


def plot_time():

  bench_repair_abs_time = []
  bench_repair_opt_abs_time = []
  for bench in BENCH_NAMES:

    # repair protocol
    bench_repair = bench + "-repair"
    bench_repair_run_time = bench_data[bench_repair][KEY_RUNTIME]
    bench_repair_abs_time.append(bench_repair_run_time)

    #repair protocol sam 256
    bench_repair_opt = bench + "-repair-opt"
    bench_repair_opt_run_time = bench_data[bench_repair_opt][KEY_RUNTIME]
    bench_repair_opt_abs_time.append(bench_repair_opt_run_time)
 
  # ealier n/d gives speedup, now d/n gives normalized value
  repair_norm_times = [1.0 for x in bench_repair_abs_time]
  # detect_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_detect_abs_time, fs_abs_times)]
  repair_sam_norm_times = [round(n / d, PRECISION) for n, d in zip(bench_repair_opt_abs_time, bench_repair_abs_time)]  
  # geo_mean_time = round(np.power(np.prod(detect_norm_times), 1.0/len(detect_norm_times)),PRECISION)
  repair_norm_times.append(1.0)
  # detect_norm_times.append(geo_mean_time)
  geo_mean_time = round(np.power(np.prod(repair_sam_norm_times), 1.0/len(repair_sam_norm_times)),PRECISION) 
  repair_sam_norm_times.append(geo_mean_time)
  plot_data(repair_norm_times, repair_sam_norm_times, "Speedup", "figure-opt-reader-run-time.pdf")

def main():
  read_csv_file()
  # print(bench_data)
  plot_time()


if __name__ == "__main__":
  main()
