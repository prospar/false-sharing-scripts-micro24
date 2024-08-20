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
PATH_CSV = "/home/prospar/prospar-micro-result/micro-baseline-40KB/Stats_Avg.csv"
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
IDX_ENERGY_PAM = 58
IDX_ENERGY_SAM = 59
IDX_ENERGY_L1D = 60
IDX_ENERGY_LLC = 61
IDX_ENERGY_CPU2L1D = 62
IDX_ENERGY_FILL = 63
IDX_ENERGY_LEAKAGE = 64

'''
Application with FS
Locked-Toy        - LT
Lockless-Toy      - LL
Linear-Regression - LR
String-Match      - SM
Boost-Spinlock    - BS
ESTM-SFtree       - SF
Reference-Count   - RC
StreamCluster     - SC

Application W/O FS

Blackscholes - BL
Swaptions    - SW
Bodytrack    - BO
Canneal      - CA
Facesim      - FA
Fluidanimate - FL

'''

BENCH_NAMES = [
  "huron-boost-spinlock", "huron-ref-count", "huron-string-match", "huron-linear-reg", "huron-locked-toy",
  "huron-lockless-toy", "streamcluster", "ESTM-specfriendly-tree", # "huron-lu-ncb", "huron-hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
  "blackscholes", "bodytrack", "canneal", "facesim", "fluidanimate", "swaptions"
]

x_labels = [
  "BS", "RC", "SM", "LR", "LT",
  "LL", "SC", "SF", "BL", "BO", "CA",
  "FA", "FL", "SW", "GM" # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

bench_data = {}

# equally distribute the label locations along x axis
index = np.arange(len(x_labels))

width = 0.35  # the width of the bars

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
  ax = fig.add_axes([0, 0, 1, 1])

  ax.set_xticks(index + width / 2)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.1
  plt.ylim(0, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  # rects1 = ax.bar(index - width / 2,
  #                 fs_version_time,
  #                 width,
  #                 label='FSversion',
  #                 hatch='/',
  #                 color=(0.1, 0.1, 0.1, 0.1))

  rects2 = ax.bar(
    index + width / 2,
    manual_data,
    width,
    align="center",
    # label='Manual',
    hatch='x',
    color=(0.5, 0.5, 0.5, 0.7))

  # plt.axhline(y=1.0, color='k', linestyle='--')

  # ax.legend(x_labels)
  # leg = ax.get_legend()
  # leg.legendHandles[0].set_color(mcolors[0])
  # leg.legendHandles[1].set_color(mcolors[1])

  # Show labels over bars
  rects = ax.patches
  # labels = [f"label{i}" for i in range(len(rects))]
  for rect, label in zip(rects, manual_data):
    height = rect.get_height()
    if height > MAX_HT:
      height = MAX_HT
    # elif height == 0.0 and log_scale:
    #   height = 0.001
    # print(height)
    ax.text(rect.get_x() + rect.get_width() / 2,
            height + 0.03,
            label,
            ha="center",
            va="bottom",
            size=7, rotation=0)
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
        # VIPIN: TODO: BYPASS the assert for repair and detect protocol
        assert (tmp[KEY_ENERGY_PAM] == 0 and tmp[KEY_ENERGY_SAM] == 0)
        if "40KB" not in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]] = tmp
        else:
          bench_data[row[IDX_BENCH]+"-40KB"] = tmp
      row_num += 1


def plot_time():
  fs_abs_times = []
  man_fix_abs_times = []
  for bench in BENCH_NAMES:
    bench_fs_run_time = bench_data[bench][KEY_RUNTIME]
    fs_abs_times.append(bench_fs_run_time)
    bench_man_fix = bench + "-40KB"
    bench_man_fix_run_time = bench_data[bench_man_fix][KEY_RUNTIME]
    man_fix_abs_times.append(bench_man_fix_run_time)

  fs_norm_times = [1 for x in fs_abs_times]
  # ealier n/d gives speedup, now d/n gives normalized value
  man_fix_norm_times = [round(n / d, PRECISION) for n, d in zip(man_fix_abs_times, fs_abs_times)]
  geo_mean_time = round(np.power(np.prod(man_fix_norm_times), 1.0/len(man_fix_norm_times)),PRECISION)
  fs_norm_times.append(1.0)
  man_fix_norm_times.append(geo_mean_time)
  plot_data(fs_norm_times, man_fix_norm_times, "Speedup", "figure-baseline40KB-run-time.pdf")

def main():
  read_csv_file()
  # print(bench_data)
  plot_time()


if __name__ == "__main__":
  main()
