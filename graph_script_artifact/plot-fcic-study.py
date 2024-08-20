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
PATH_CSV = "/home/prospar/prospar-micro-result/micro-fc-ic-ouptut/Stats_Avg.csv"
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
IDX_MSG_VOL =  103 #98
IDX_MSG_COUNT = 104 #99
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
  "geomean"  # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

bench_data = {}

# equally distribute the label locations along x axis
index = np.arange(len(x_labels))
index = np.arange(0.0,8.0,1.0)


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
  fig = plt.figure(figsize=(3, 0.5), dpi=120, facecolor='w', edgecolor='k')
  fig.set_figheight(0.5)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 8.2
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=8)
  MAX_HT = 1.05
  plt.ylim(0.9, MAX_HT)
  ax.set_yticks([0.9, 0.95, 1.0, 1.05])
  ax.set_yticklabels([0.9, 0.95,1.0, 1.05],fontsize=8)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - width/2,
                  orig_data,
                  width,
                  label='32',
                  # hatch='x',
                  color=(0.3, 0.3, 0.3, 0.8))

  rects2 = ax.bar(
    index ,
    manual_data,
    width,
    align="edge",
    label='64',
    # hatch='//',
    color=(0.7, 0.7, 0.7, 0.8))

  for bar, label in zip(rects1, orig_data):# if bars == rects1 else manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0 or height == 0.95:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() - bar.get_width() / 3, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)


  for bar, label in zip(rects2, manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      elif height == 1.03:
        height = height+0.02
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 1, height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
      # else:
      #   ax.annotate('{}'.format(label),
      #             xy=(bar.get_x() + bar.get_width() / 2, height-0.01),
      #             xytext=(0, 3),  # 3 points vertical offset
      #             textcoords="offset points",
      #             ha='center', va='bottom',size=7,rotation=0)  
  # fig.tight_layout()
  # plt.show()
  plt.legend(loc='lower right', ncol=2, fontsize=7, handletextpad=0.5)
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
        if "FS_MESI_32" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+ "-fc32"] = tmp
        elif "FS_MESI_64" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-fc64"] = tmp
        else:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp

        # if "manual" not in row[IDX_PROTOCOL]:
        #   bench_data[row[IDX_BENCH]] = tmp
        # else:
        #   bench_data[row[IDX_BENCH]+"-manual"] = tmp
      row_num += 1


def plot_time():
  fs_abs_times = []
  bench_fc32_abs_time = []
  bench_fc64_abs_time = []
  for bench in BENCH_NAMES:
    # print(bench)
    bench_base = bench + "-repair"
    bench_fs_run_time = bench_data[bench_base][KEY_RUNTIME]
    fs_abs_times.append(bench_fs_run_time)
    # fc32 protocol
    bench_fc32 = bench + "-fc32"
    bench_fc32_run_time = bench_data[bench_fc32][KEY_RUNTIME]
    bench_fc32_abs_time.append(bench_fc32_run_time)
    # fc64 protocol
    bench_fc64 = bench + "-fc64"
    bench_fc64_run_time = bench_data[bench_fc64][KEY_RUNTIME]
    bench_fc64_abs_time.append(bench_fc64_run_time)

  fs_norm_times = [1 for x in fs_abs_times]
  fs_norm_times.append(1.0)
  # ealier n/d gives speedup, now d/n gives normalized value
  fc32_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_fc32_abs_time, fs_abs_times)]
  fc64_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_fc64_abs_time, fs_abs_times)]  
  geo_mean_time = round(np.power(np.prod(fc32_norm_times), 1.0/len(fc32_norm_times)),PRECISION)
  
  # print(fc64_norm_times)
  fc32_norm_times.append(geo_mean_time)
  geo_mean_time = round(np.power(np.prod(fc64_norm_times), 1.0/len(fc64_norm_times)),PRECISION) 
  fc64_norm_times.append(geo_mean_time)
  plot_data(fc32_norm_times, fc64_norm_times, "Speedup", "figure-16-run-time.pdf")


def main():
  read_csv_file()
  # print(bench_data)
  plot_time()
  # plot_traffic_vol()
  # plot_traffic_count()
  # plot_energy()


if __name__ == "__main__":
  main()
