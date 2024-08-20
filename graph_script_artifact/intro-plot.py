# This script is for generating plots in the introduction for our MICRO24 submission.
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Diff csv file : Stat_formatted.csv, Stats_Avg.csv, Stats_Median.csv, Stats_Max.csv, Stats_Min.csv
PATH_CSV = "/home/prospar/prospar-micro-result/micro-manual-fix/Stats_Avg.csv"

PATH_CSV = str(sys.argv[1])
print(f"CSV file path: {PATH_CSV}")

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
KEY_LLC_GETX = "KEY_L2_CACHE_L1_GETX"
KEY_LLC_GET = "KEY_L2_CACHE_L1_GETS"
KEY_LLC_UPG = "KEY_L2_CACHE_L1_UPGRADE"
KEY_LLC_RQT  = "TOTAL_RQT_TO_LLC"
KEY_UP_ALL = "KEY_L2_CACHE_UP_ALL"
KEY_UP_DMD = "KEY_L2_CACHE_UP_DMD"
KEY_UP_EDS = "KEY_L2_CACHE_UP_EDS"
KEY_UP_MD = "KEY_L2_CACHE_UP_MD"

# vipin: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_RUNTIME = 6
IDX_MSG_VOL = 103  #98
IDX_MSG_COUNT = 104  #99
IDX_ENERGY_PAM = 58
IDX_ENERGY_SAM = 59
IDX_ENERGY_L1D = 60
IDX_ENERGY_LLC = 61
IDX_ENERGY_CPU2L1D = 62
IDX_ENERGY_FILL = 63
IDX_ENERGY_LEAKAGE = 64
IDX_LLC_GET = 36
IDX_LLC_GETX = 37
IDX_LLC_UPG = 39
IDX_UP_ALL = 96
IDX_UP_DMD = 97
IDX_UP_EDS = 98
IDX_UP_MD = 99

BENCH_NAMES = [
  "huron-boost-spinlock",
  "huron-lockless-toy",
  "huron-linear-reg",
  "huron-locked-toy",
  "huron-ref-count",
  "streamcluster",
  "ESTM-specfriendly-tree",  # "huron-lu-ncb", "huron-hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
  "huron-string-match"
]
'''
BS BoostSPINLOCK
LL lockless-toy
LR linear-reg
LT locked-toy
RC ref-count
SC streamcluster
SF ESTM-specfriendly-tree
SM string-match
'''
x_labels = [
  "BS",
  "LL",
  "LR",
  "LT",
  "RC",
  "SC",
  "SF",
  "SM",
  "geomean" 
]

bench_data = {}

# equally distribute the label locations along x axis
# index = np.arange(len(x_labels))
index = np.arange(0.0,9.0,1.0)
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
  fig.set_figheight(1)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 8.5
  ax.set_xticks(index + width / 2)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.6
  plt.ylim(0.9, MAX_HT)
  # index_y = np.arange(0.9, MAX_HT, 0.)
  ax.set_yticks(np.arange(1.0, MAX_HT, 0.2))
  # ax.set_yticklabels([0.9,1.0,1.1,1.2,1.3,1.4],fontsize=7)
  # ax.set_yticks(np.arange(1.0, MAX_HT, 0.1))
  plt.yticks(fontsize=8)
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
    # hatch='//',
    color=(0.3, 0.3, 0.3, 0.8))


  # Show labels over bars
  rects = ax.patches
  # labels = [f"label{i}" for i in range(len(rects))]
  for rect, label in zip(rects, manual_data):
    height = rect.get_height()
    if height > MAX_HT:
      height = MAX_HT
    # elif height == 0.0 and log_scale:
    #   height = 0.001
    # height = MAX_HT
    # print(height)
    ax.text(rect.get_x() + rect.get_width() / 2,
            height + 0.02,
            label,
            ha="center",
            va="bottom",
            size=7)

  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        print(row.index(KEY_MSG_VOL))
        print(row.index(KEY_ENERGY_PAM))
        print(row.index(KEY_UP_DMD))
        print(row.index(KEY_UP_ALL))
        print(row.index(KEY_UP_EDS))
        print(row.index(KEY_UP_MD))
        print(row.index(KEY_LLC_UPG))
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
        assert (row.index(KEY_LLC_GET) == IDX_LLC_GET)
        assert (row.index(KEY_LLC_GETX) == IDX_LLC_GETX)
        assert (row.index(KEY_LLC_UPG) == IDX_LLC_UPG)
        assert (row.index(KEY_UP_ALL) == IDX_UP_ALL)
        assert (row.index(KEY_UP_EDS) == IDX_UP_EDS)
        assert (row.index(KEY_UP_DMD) == IDX_UP_DMD)
        assert (row.index(KEY_UP_MD) == IDX_UP_MD)

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
        tmp[KEY_LLC_RQT] = str_to_float(row[IDX_LLC_GET]) + str_to_float(row[IDX_LLC_GETX])\
             + str_to_float(row[IDX_LLC_UPG]) + str_to_float(row[IDX_UP_ALL])\
              + str_to_float(row[IDX_UP_DMD]) + str_to_float(row[IDX_UP_EDS])\
                + str_to_float(row[IDX_UP_MD])
        # VIPIN: TODO: BYPASS the assert for repair and detect protocol
        assert (tmp[KEY_ENERGY_PAM] == 0 and tmp[KEY_ENERGY_SAM] == 0)
        if "manual" not in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]] = tmp
        else:
          bench_data[row[IDX_BENCH] + "-manual"] = tmp
      row_num += 1


def plot_time():
  fs_abs_times = []
  man_fix_abs_times = []
  for bench in BENCH_NAMES:
    bench_fs_run_time = bench_data[bench][KEY_RUNTIME]
    fs_abs_times.append(bench_fs_run_time)
    bench_man_fix = bench + "-manual"
    bench_man_fix_run_time = bench_data[bench_man_fix][KEY_RUNTIME]
    man_fix_abs_times.append(bench_man_fix_run_time)

  fs_norm_times = [1 for x in fs_abs_times]
  # ealier n/d gives speedup, now d/n gives normalized value
  man_fix_norm_times = [round(d / n, PRECISION) for n, d in zip(man_fix_abs_times, fs_abs_times)]
  geo_mean_time = round(np.power(np.prod(man_fix_norm_times), 1.0 / len(man_fix_norm_times)),
                        PRECISION)
  fs_norm_times.append(1.0)
  man_fix_norm_times.append(geo_mean_time)
  plot_data(fs_norm_times, man_fix_norm_times, "Speedup", "figure-2-runtime.pdf")


def plot_traffic_vol():
  fs_abs_traffic = []
  man_fix_abs_traffic = []
  for bench in BENCH_NAMES:
    bench_fs_traffic = bench_data[bench][KEY_MSG_VOL]
    fs_abs_traffic.append(bench_fs_traffic)
    bench_man_fix = bench + "-manual"
    bench_man_fix_traffic = bench_data[bench_man_fix][KEY_MSG_VOL]
    man_fix_abs_traffic.append(bench_man_fix_traffic)

  fs_norm_traffic = [1 for x in fs_abs_traffic]
  man_fix_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(man_fix_abs_traffic, fs_abs_traffic)
  ]
  geo_mean_vol = round(np.power(np.prod(man_fix_norm_traffic), 1.0 / len(man_fix_norm_traffic)),
                       PRECISION)
  fs_norm_traffic.append(1.0)
  man_fix_norm_traffic.append(geo_mean_vol)
  plot_data(fs_norm_traffic, man_fix_norm_traffic, "Normalized on-chip traffic \n(bytes)",
            "figure-2-traffic-vol.pdf", True)


def plot_traffic_count():
  fs_abs_traffic = []
  man_fix_abs_traffic = []
  for bench in BENCH_NAMES:
    # bench_fs_traffic = bench_data[bench][KEY_MSG_COUNT]
    bench_fs_traffic = bench_data[bench][KEY_LLC_RQT]
    fs_abs_traffic.append(bench_fs_traffic)
    bench_man_fix = bench + "-manual"
    # bench_man_fix_traffic = bench_data[bench_man_fix][KEY_MSG_COUNT]
    bench_man_fix_traffic = bench_data[bench_man_fix][KEY_LLC_RQT]
    man_fix_abs_traffic.append(bench_man_fix_traffic)

  fs_norm_traffic = [1 for x in fs_abs_traffic]
  man_fix_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(man_fix_abs_traffic, fs_abs_traffic)
  ]
  count=0
  for i in range(len(man_fix_norm_traffic)):
    if man_fix_norm_traffic[i] == 0:
      man_fix_norm_traffic[i] = 1
      count+=1
  geo_mean_count = round(np.power(np.prod(man_fix_norm_traffic), 1.0 / (len(man_fix_norm_traffic)-1)),
                         PRECISION)
  fs_norm_traffic.append(1.0)
  man_fix_norm_traffic.append(geo_mean_count)
  plot_data(fs_norm_traffic, man_fix_norm_traffic, "Normalized on-chip traffic \n(messages)",
            "fiogure-2-traffic-count.pdf")


# TODO: stack plot for using diff energy component
# fill energy, cpu2l1d energy, pam energy, sam energy, leakage energy
# will cover all energy components
# do not consider L1D and LLC energy
def plot_energy():
  fs_abs_energy = []
  man_fix_abs_energy = []
  for bench in BENCH_NAMES:
    bench_fs_l1denergy = bench_data[bench][KEY_ENERGY_L1D]
    bench_fs_llcenergy = bench_data[bench][KEY_ENERGY_LLC]
    bench_fs_pamenergy = bench_data[bench][KEY_ENERGY_PAM]
    bench_fs_samenergy = bench_data[bench][KEY_ENERGY_SAM]
    bench_fs_cpu2l1denergy = bench_data[bench][KEY_ENERGY_CPU2L1D]
    bench_fs_fillenergy = bench_data[bench][KEY_ENERGY_FILL]
    bench_fs_staticleakage = bench_data[bench][KEY_TOTAL_LEAKAGE]
    # fs_abs_energy.append(bench_fs_l1denergy + bench_fs_llcenergy + bench_fs_pamenergy +
    fs_abs_energy.append(bench_fs_pamenergy + bench_fs_samenergy + bench_fs_cpu2l1denergy +
                         bench_fs_fillenergy + bench_fs_staticleakage)
    bench_man_fix = bench + "-manual"
    bench_man_fix_l1denergy = bench_data[bench_man_fix][KEY_ENERGY_L1D]
    bench_man_fix_llcenergy = bench_data[bench_man_fix][KEY_ENERGY_LLC]
    bench_man_fix_pamenergy = bench_data[bench_man_fix][KEY_ENERGY_PAM]
    bench_man_fix_samenergy = bench_data[bench_man_fix][KEY_ENERGY_SAM]
    bench_man_fix_cpu2l1denergy = bench_data[bench_man_fix][KEY_ENERGY_CPU2L1D]
    bench_man_fix_fillenergy = bench_data[bench_man_fix][KEY_ENERGY_FILL]
    bench_man_fix_staticleakage = bench_data[bench_man_fix][KEY_TOTAL_LEAKAGE]
    # man_fix_abs_energy.append(bench_man_fix_l1denergy + bench_man_fix_llcenergy +
    man_fix_abs_energy.append(bench_man_fix_pamenergy + bench_man_fix_samenergy +
                              bench_man_fix_cpu2l1denergy + bench_man_fix_fillenergy +
                              bench_man_fix_staticleakage)
  fs_norm_energy = [1 for x in fs_abs_energy]
  man_fix_norm_energy = [round(n / d, PRECISION) for n, d in zip(man_fix_abs_energy, fs_abs_energy)]
  geo_mean_energy = round(np.power(np.prod(man_fix_norm_energy), 1.0 / len(man_fix_norm_energy)),
                          PRECISION)
  fs_norm_energy.append(1.0)
  man_fix_norm_energy.append(geo_mean_energy)
  plot_data(fs_norm_energy, man_fix_norm_energy, "Normalized energy usage", "figure-2-energy.pdf")
  #TODO: add code for stack plot


def main():
  read_csv_file()
  # print(bench_data)
  plot_time()
  # plot_traffic_vol()
  # plot_traffic_count()
  # plot_energy()


if __name__ == "__main__":
  main()
