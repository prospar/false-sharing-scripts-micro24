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
PATH_CSV = "/home/vipin/Documents/false-sharing-result/micro-2024-result/result/app-fs/Stats_Avg.csv"

KEY_BENCH = "bench"
KEY_PROTOCOL = "protocol"
KEY_SAM_LD = "KEY_SAM_LD"
KEY_SAM_ST = "KEY_SAM_ST" 
KEY_SAM_EVIC = "KEY_SAM_ENTRY_EVIC"
# vipin: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_SAM_LD = 134
IDX_SAM_ST = 135
IDX_SAM_EVIC = 126
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
  "huron-lockless-toy", "streamcluster" , "ESTM-specfriendly-tree"
]

x_labels = [
  "BS", "RC", "SM", "LR", "LT",
  "LL", "SC", "SF", "geomean" # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

bench_data = {}

# equally distribute the label locations along x axis
# index = np.arange(len(x_labels))
index = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25] #, 2.75, 3.25, 3.75, 4.25]
index1 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25] #, 2.75, 3.25, 3.75, 4.25]

width = 0.1  # the width of the bars

PRECISION = 5  # digits


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

def plot_data( manual_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(2.5, 1), dpi=120, facecolor='w', edgecolor='k')
  ax = fig.add_axes([0, 0, 1, 1])

  ax.set_xticks(index)
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


  rects2 = ax.bar(
    index,
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
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)


  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

'''
def plot_sam_eviction(y_axis_label, pdf_name, log_scale=False):
  fig,ax = plt.subplots(figsize=(3.5,2), facecolor='w', edgecolor='k')
  fig.set_figheight(1.5)

  # ax = fig.add_axes([0, 0, 1, 1])
  # index[-1] = 8.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=8)
  MAX_HT = 1.05
  plt.ylim(0.7, MAX_HT)
  plt.yticks(fontsize=8)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars
  # Filter out the message based on type

  _total_l1d_hit = [round(bench_data[bench][KEY_SAM_ST]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_l1d_hit_copy = []
  print(_total_l1d_hit)
  count = 0
  for i in range(len(_total_l1d_hit)):
    if _total_l1d_hit[i] == 0:
      _total_l1d_hit_copy.append(1)
      count += 1
    else:
      _total_l1d_hit_copy.append(_total_l1d_hit[i])
  _total_l1d_hit.append(round(np.power(np.prod(_total_l1d_hit_copy), 1.0/(len(_total_l1d_hit_copy)-count)),PRECISION))

  _total_non_fs_acc= [round(bench_data[bench][KEY_NON_FS_ACC]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_non_fs_acc_copy = []
  print(_total_non_fs_acc)
  count = 0
  for i in range(len(_total_non_fs_acc)):
    if _total_non_fs_acc[i] == 0:
      _total_non_fs_acc_copy.append(1)
      count += 1
    else:
      _total_non_fs_acc_copy.append(_total_non_fs_acc[i])
  _total_non_fs_acc.append(round(np.power(np.prod(_total_non_fs_acc_copy), 1.0/(len(_total_non_fs_acc_copy)-count)),PRECISION))
  
  _total_fs_acc=[round(bench_data[bench][KEY_FS_ACCESSES]/bench_data[bench][KEY_TOTAL_L1_ACC],PRECISION) for bench in BENCH_NAMES]
  _total_fs_acc_copy = []
  print(_total_fs_acc)
  count = 0
  for i in range(len(_total_fs_acc)):
    if _total_fs_acc[i] == 0:
      _total_fs_acc_copy.append(1)
      count += 1
    else:
      _total_fs_acc_copy.append(_total_fs_acc[i])
  _total_fs_acc.append(round(np.power(np.prod(_total_fs_acc_copy), 1.0/(len(_total_fs_acc_copy)-count)),PRECISION))

  rects1 = ax.bar(index1,
                  _total_l1d_hit,
                  width,
                  label='L1D Demand Hits',
                  color=(0.1, 0.1, 0.9, 0.8))
  _get_bar = ax.bar(index1,
                  _total_non_fs_acc,
                  width,
                  label='L1D Non-FS Misses',
                  bottom=_total_l1d_hit,
                  color=(0.9, 0.1, 0.1, 0.8))
  _upg_bar = ax.bar(index1,
                  _total_fs_acc,
                  width,
                  label='L1D FS Misses',
                  bottom=[sum(x) for x in zip(_total_l1d_hit, _total_non_fs_acc)],
                  color=(0.1, 0.9, 0.1, 0.8))

  # _total_md_bar = ax.bar(index1,
  #                 _total_md_data,
  #                 width,
  #                 label='TotalMD',
  #                 bottom=[sum(x) for x in zip(_getx_data, _get_data, _upg_data)],
  #                 color=(0.1, 0.9, 0.1, 0.8))
  
  plt.legend(loc='lower center', ncol=2, fontsize=7)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()
'''

def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        print(row.index(KEY_SAM_LD))
        print(row.index(KEY_SAM_ST))
        print(row.index(KEY_SAM_EVIC))

        assert(row.index(KEY_SAM_LD) == IDX_SAM_LD)
        assert(row.index(KEY_SAM_ST) == IDX_SAM_ST)
        assert (row.index(KEY_SAM_EVIC) == IDX_SAM_EVIC)
        assert (row.index(KEY_BENCH) == IDX_BENCH)
        assert (row.index(KEY_PROTOCOL) == IDX_PROTOCOL)
      elif row_num > 2:
        tmp = {}
        tmp[KEY_SAM_LD] = str_to_float(row[IDX_SAM_LD])
        tmp[KEY_SAM_ST] = 2.0*str_to_float(row[IDX_SAM_ST])
        tmp[KEY_SAM_EVIC] = str_to_float(row[IDX_SAM_EVIC])
        bench_data[row[IDX_BENCH]] = tmp
      row_num += 1

def plot_sam_eviction():
  sam_evictions = []
  for bench in BENCH_NAMES:
    sam_store = bench_data[bench][KEY_SAM_ST]
    sam_load = bench_data[bench][KEY_SAM_LD]
    sam_evictions.append(round(bench_data[bench][KEY_SAM_EVIC]/(sam_store + sam_load), PRECISION)*100.0)
    count =0
  print(sam_evictions)
  sam_evictions_copy=[]
  for i in range(len(sam_evictions)):
    if sam_evictions[i] == 0:
      sam_evictions_copy.append(1)
      # sam_evictions[i]=1
      count+=1
    else:
      sam_evictions_copy.append(sam_evictions[i])
  print(round(np.power(np.prod(sam_evictions), 1.0/(len(sam_evictions)-count)),PRECISION))
  sam_evictions.append(round(np.power(np.prod(sam_evictions_copy), 1.0/(len(sam_evictions)-count)),PRECISION))


  print(sam_evictions) 
  plot_data(sam_evictions, "% of SAM \n evictions", "sam-eviction-percentage.pdf")
  

def main():
  read_csv_file()
  plot_sam_eviction()


if __name__ == "__main__":
  main()
