# This script is for generating plots in the introduction for our ASPLOS24 submission.
# python3 src/main.py --tasks result --verbose 1 --outputDir asplos24-intro
# python3 sb-intro-asplos24.py
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# PATH_CSV = "/home/swarnendu/prospar-exp-results/261123-asplos24-intro/Stat_formatted.csv"
# PATH_CSV = "/home/vipin/Documents/false-sharing-result/asplos-intro/Stat_formatted.csv"
# Diff csv file : Stat_formatted.csv, Stats_Avg.csv, Stats_Median.csv, Stats_Max.csv, Stats_Min.csv
PATH_CSV = "/home/vipin/Documents/false-sharing-result/micro-2024-result/result/micro-fs-acc/Stats_Avg.csv"

KEY_BENCH = "bench"
KEY_PROTOCOL = "protocol"
# KEY_RUNTIME = "KEY_SIM_TICKS"
# KEY_MSG_VOL = "KEY_TOTAL_MSG_VOL"
# KEY_MSG_COUNT = "KEY_TOTAL_MSG_COUNT"
# KEY_ENERGY_PAM = "KEY_TOTAL_PAM_ENERGY"
# KEY_ENERGY_SAM = "KEY_TOTAL_SAM_ENERGY"
# KEY_ENERGY_L1D = "KEY_TOTAL_L1D_ENERGY"
# KEY_ENERGY_LLC = "KEY_TOTAL_LLC_ENERGY"
# # KEY_ENERGY_CPU2L1D = "KEY_TOTAL_CPU_TO_L1_ENERGY"
# KEY_ENERGY_CPU2L1D = "KEY_CPU_TO_L1_ENERGY"
# KEY_ENERGY_FILL = "KEY_FILL_COHERENCE_ENERGY"
# KEY_TOTAL_LEAKAGE = "KEY_TOTAL_STATIC_LEAKAGE"
KEY_LLC_DEMAND_ACCESS = "KEY_L2_DEMAND_ACCESSES"
KEY_FS_ACCESSES = "KEY_FALSE_SHARING_ACC" 
KEY_L1D_HIT = "KEY_RUBY_L1D_DEMAND_HITS"
KEY_NON_FS_ACC="KEY_NON_FS_ACCESSES"
KEY_TOTAL_L1_ACC = "KEY_RUBY_L1D_DEMAND_ACCESSES"
# vipin: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
# IDX_RUNTIME = 6
# IDX_MSG_VOL =  101 #98
# IDX_MSG_COUNT = 102 #99
# IDX_ENERGY_PAM = 58
# IDX_ENERGY_SAM = 59
# IDX_ENERGY_L1D = 60
# IDX_ENERGY_LLC = 61
# IDX_ENERGY_CPU2L1D = 62
# IDX_ENERGY_FILL = 63
# IDX_ENERGY_LEAKAGE = 64
IDX_LLC_DEMAND_ACCESS = 133
IDX_FALSE_SHARING_ACC = 128
IDX_L1D_HIT = 104
IDX_TOTAL_L1D_ACC = 103
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
  "huron-boost-spinlock",
  "huron-lockless-toy",
  "huron-linear-reg",
  "huron-locked-toy",
  "huron-ref-count",
  "streamcluster",
  "ESTM-specfriendly-tree",  # "huron-lu-ncb", "huron-hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
  "huron-string-match"
]

x_labels = [
  "BS",
  "LL",
  "LR",
  "LT",
  "RC",
  "SC",
  "SF",
  "SM",
  "mean"  # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

bench_data = {}

# equally distribute the label locations along x axis
# index = np.arange(len(x_labels))
index = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25] #, 2.75, 3.25, 3.75, 4.25]
index1 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25] #, 2.75, 3.25, 3.75, 4.25]
# index1 = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25]
# index1 = [0.25, 1.25, 2.25, 3.25, 4.25, 5.25, 6.25, 7.25, 8.25]

width = 0.1  # the width of the bars

PRECISION = 8  # digits


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
  fig = plt.figure(figsize=(2.5, 1), dpi=120, facecolor='w', edgecolor='k')
  ax = fig.add_axes([0, 0, 1, 1])

  ax.set_xticks(index + width / 2)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.05
  plt.ylim(0, MAX_HT)
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

  # ax.legend(x_labels)
  # leg = ax.get_legend()
  # leg.legendHandles[0].set_color(mcolors[0])
  # leg.legendHandles[1].set_color(mcolors[1])

  for bar, label in zip(rects2, manual_data):# if bars == rects1 else manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)


  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def plot_category_miss(y_axis_label, pdf_name, log_scale=False):
  fig,ax = plt.subplots(figsize=(3.5,1.01), facecolor='w', edgecolor='k')
  fig.set_figheight(1.01)

  # ax = fig.add_axes([0, 0, 1, 1])
  # index[-1] = 8.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=8, loc='center')
  MAX_HT = 1.05
  plt.ylim(0.8, MAX_HT)
  plt.yticks(fontsize=7)
  ax.set_yticks([0.8, 0.9, 1.0, ])
  # ax.set_yticklabels([0.8, 0.9, 1.0, 1.05],fontsize=7)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars
  # Filter out the message based on type

  _total_l1d_hit = [round(bench_data[bench][KEY_L1D_HIT]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_l1d_hit.append(np.mean(_total_l1d_hit))
  _total_l1d_hit_copy = []
  print(_total_l1d_hit)
  count = 0
  for i in range(len(_total_l1d_hit)):
    if _total_l1d_hit[i] == 0:
      _total_l1d_hit_copy.append(1)
      count += 1
    else:
      _total_l1d_hit_copy.append(_total_l1d_hit[i])
  # _total_l1d_hit.append(round(np.power(np.prod(_total_l1d_hit_copy), 1.0/(len(_total_l1d_hit_copy)-count)),PRECISION))

  _total_non_fs_acc= [round(bench_data[bench][KEY_NON_FS_ACC]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_non_fs_acc_copy = []
  _total_non_fs_acc.append(np.mean(_total_non_fs_acc))
  print(_total_non_fs_acc)
  count = 0
  for i in range(len(_total_non_fs_acc)):
    if _total_non_fs_acc[i] == 0:
      _total_non_fs_acc_copy.append(1)
      count += 1
    else:
      _total_non_fs_acc_copy.append(_total_non_fs_acc[i])
  # _total_non_fs_acc.append(round(np.power(np.prod(_total_non_fs_acc_copy), 1.0/(len(_total_non_fs_acc_copy)-count)),PRECISION))
  
  _total_fs_acc=[round(bench_data[bench][KEY_FS_ACCESSES]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_fs_acc.append(np.mean(_total_fs_acc))
  _total_fs_acc_copy = []
  print(_total_fs_acc)
  count = 0
  for i in range(len(_total_fs_acc)):
    if _total_fs_acc[i] == 0:
      _total_fs_acc_copy.append(1)
      count += 1
    else:
      _total_fs_acc_copy.append(_total_fs_acc[i])
  # _total_fs_acc.append(round(np.power(np.prod(_total_fs_acc_copy), 1.0/(len(_total_fs_acc_copy)-count)),PRECISION))

  rects1 = ax.bar(index1,
                  _total_l1d_hit,
                  width,
                  # label='L1D Demand Hits',
                  label='L1D Hits',
                  hatch='//',
                  color=(0.8, 0.8, 0.8, 0.8))
  _get_bar = ax.bar(index1,
                  _total_non_fs_acc,
                  width,
                  label='L1D Non-FS Misses',
                  bottom=_total_l1d_hit,
                  color=(0.2, 0.2, 0.2, 0.8))
  _upg_bar = ax.bar(index1,
                  _total_fs_acc,
                  width,
                  label='L1D FS Misses',
                  bottom=[sum(x) for x in zip(_total_l1d_hit, _total_non_fs_acc)],
                  color=(0.5, 0.5, 0.5, 0.8))

  # _total_md_bar = ax.bar(index1,
  #                 _total_md_data,
  #                 width,
  #                 label='TotalMD',
  #                 bottom=[sum(x) for x in zip(_getx_data, _get_data, _upg_data)],
  #                 color=(0.1, 0.9, 0.1, 0.8))
  handles,legend_labels = ax.get_legend_handles_labels()
  # plt.legend(loc='lower right', ncol=1, fontsize=6, frameon=True, borderpad=0.1, labelspacing=0.1, handlelength=1.5, handletextpad=0.5)
  ax.legend(handles[::-1], legend_labels[::-1], loc='lower right', ncol=1, fontsize=6, frameon=True, borderpad=0.1, labelspacing=0.1, handlelength=1.5, handletextpad=0.5)
  # plt.legend(loc='lower right', ncol=1, fontsize=6, frameon=True, borderpad=0.1, labelspacing=0.1, handlelength=1.5, handletextpad=0.5)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        print(row.index(KEY_LLC_DEMAND_ACCESS))
        print(row.index(KEY_FS_ACCESSES))
        print(row.index(KEY_L1D_HIT))
        print(row.index(KEY_TOTAL_L1_ACC))
        assert(row.index(KEY_LLC_DEMAND_ACCESS) == IDX_LLC_DEMAND_ACCESS)
        assert(row.index(KEY_FS_ACCESSES) == IDX_FALSE_SHARING_ACC)
        assert (row.index(KEY_PROTOCOL) == IDX_PROTOCOL)
        assert (row.index(KEY_BENCH) == IDX_BENCH)
        assert (row.index(KEY_L1D_HIT) == IDX_L1D_HIT)
        assert (row.index(KEY_TOTAL_L1_ACC) == IDX_TOTAL_L1D_ACC)
      elif row_num > 2:
        tmp = {}
        tmp[KEY_LLC_DEMAND_ACCESS] = str_to_float(row[IDX_LLC_DEMAND_ACCESS])
        tmp[KEY_FS_ACCESSES] = 2.0*str_to_float(row[IDX_FALSE_SHARING_ACC])
        tmp[KEY_L1D_HIT] = str_to_float(row[IDX_L1D_HIT])
        tmp[KEY_TOTAL_L1_ACC] = str_to_float(row[IDX_TOTAL_L1D_ACC])
        tmp[KEY_NON_FS_ACC] = tmp[KEY_LLC_DEMAND_ACCESS] - tmp[KEY_FS_ACCESSES]
        bench_data[row[IDX_BENCH]] = tmp
      row_num += 1

def plot_llc_access():
  access_share = []
  for bench in BENCH_NAMES:
    bench_llc_access = bench_data[bench][KEY_LLC_DEMAND_ACCESS]
    # print(bench, bench_llc_access)
    bench_fs_access = bench_data[bench][KEY_FS_ACCESSES]
    # print(bench, bench_fs_access)
    access_share.append(round(bench_fs_access / bench_llc_access, PRECISION))
  
  plot_data(access_share, access_share, "% of LLC \n demand accesses", "false-sharing-acc.pdf")
  

def main():
  read_csv_file()
  # plot_llc_access()
  plot_category_miss("Fraction of\n L1D accesses", "false-sharing-fraction.pdf", log_scale=False)


if __name__ == "__main__":
  main()
