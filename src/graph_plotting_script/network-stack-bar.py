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
# PATH_CSV = "/home/vipin/Documents/false-sharing-result/micro-2024-result/result/custom/Stats_Avg.csv"
PATH_CSV = "/home/vipin/Documents/false-sharing-result/micro-2024-result/result/app-fs/Stats_Avg.csv"

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
KEY_TOTAL_MD = "KEY_MD_TOTAL_MD_MSG"
KEY_EVICTION_MD = "KEY_MD_EVIC_MD_MSG"
KEY_CONTROL_MD = "KEY_MD_CONTROL_MD_MSG"
KEY_MD_DATA_MSG = "KEY_MD_MD_MSG"
# vipin: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_RUNTIME = 6
IDX_MSG_VOL =  103 #98
IDX_MSG_COUNT = 104 #99
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
IDX_TOTAL_MD = 125
IDX_EVICTION_MD = 124
IDX_CONTROL_MD = 122
IDX_MD_DATA_MSG = 123
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
  "mean"  # "lu-ncb", "hist" #"MUTEX-hashtable", "SPIN-lazy-list", "MUTEX-lazy-list", "SPIN-hashtable"
]

STACK_KEY:list=[KEY_LLC_GETX,KEY_LLC_GET,KEY_LLC_UPG,KEY_TOTAL_MD,\
                  KEY_EVICTION_MD,KEY_CONTROL_MD,KEY_MD_DATA_MSG]
bench_data = {}

# equally distribute the label locations along x axis
index = [0.4, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4, 8.4]
index_1 = [0.2, 1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2]
# index_1 = np.arange(0.2,8.2,1)
index1 = [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3]
# index1 = np.arange(0.3,8.3,1)
index2 = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
# index2 = np.arange(0.5,8.5,1)
width = 0.2  # the width of the bars

PRECISION = 3  # digits


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


def plot_data(orig_data:dict, y_axis_label, pdf_name, log_scale=False):
  fig,ax = plt.subplots(figsize=(3,2), facecolor='w', edgecolor='k')
  fig.set_figheight(2)
  # ax = fig.add_axes([0, 0, 1, 1])
  # index[-1] = 8.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)
  index12 = np.arange(0, 1.5, 0.2)
  ax.set_yticks(index12)
  ax.set_ylabel(y_axis_label, fontsize=7)
  MAX_HT = 1.5
  plt.ylim(0, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars
  # Filter out the message based on type
  _getx_data=[round(bench_data[bench][KEY_LLC_GETX]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _getx_mean = round(np.mean(_getx_data),PRECISION)
  _getx_data.append(_getx_mean)
  _getx_data_detect=[round(bench_data[bench+"-detect"][KEY_LLC_GETX]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _getx_data_detect_mean = round(np.mean(_getx_data_detect),PRECISION)
  _getx_data_detect.append(_getx_data_detect_mean)

  _getx_data_repair=[round(bench_data[bench+"-repair"][KEY_LLC_GETX]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _getx_data_repair_mean = round(np.mean(_getx_data_repair),PRECISION)
  _getx_data_repair.append(_getx_data_repair_mean)

  _get_data=[round(bench_data[bench][KEY_LLC_GET]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _get_data_mean = round(np.mean(_get_data),PRECISION)
  _get_data.append(_get_data_mean)

  _get_data_detect=[round(bench_data[bench+"-detect"][KEY_LLC_GET]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _get_data_detect_mean = round(np.mean(_get_data_detect),PRECISION)
  _get_data_detect.append(_get_data_detect_mean)

  _get_data_repair=[round(bench_data[bench+"-repair"][KEY_LLC_GET]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _get_data_repair_mean = round(np.mean(_get_data_repair),PRECISION)
  _get_data_repair.append(_get_data_repair_mean)

  _upg_data=[round(bench_data[bench][KEY_LLC_UPG]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _upg_data_mean = round(np.mean(_upg_data),PRECISION)
  _upg_data.append(_upg_data_mean)

  _upg_data_detect=[round(bench_data[bench+"-detect"][KEY_LLC_UPG]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _upg_data_detect_mean = round(np.mean(_upg_data_detect),PRECISION)
  _upg_data_detect.append(_upg_data_detect_mean)

  _upg_data_repair=[round(bench_data[bench+"-repair"][KEY_LLC_UPG]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _upg_data_repair_mean = round(np.mean(_upg_data_repair),PRECISION)
  _upg_data_repair.append(_upg_data_repair_mean)

  _total_md_data_detect=[round(bench_data[bench+"-detect"][KEY_TOTAL_MD]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _total_md_data_detect_mean = round(np.mean(_total_md_data_detect),PRECISION)
  _total_md_data_detect.append(_total_md_data_detect_mean)

  _total_md_data_repair=[round(bench_data[bench+"-repair"][KEY_TOTAL_MD]/orig_data[bench],PRECISION) for bench in BENCH_NAMES]
  _total_md_data_repair_mean = round(np.mean(_total_md_data_repair),PRECISION)
  _total_md_data_repair.append(_total_md_data_repair_mean)
  
  rects3 = ax.bar(index_1,
                  _getx_data,
                  width,
                  label='GetX',
                  hatch='//',
                  color=(0.9, 0.9, 0.9, 0.8))
  _get_bar = ax.bar(index_1,
                  _get_data,
                  width,
                  label='Get',
                  bottom=_getx_data,
                  color=(0.2, 0.2, 0.2, 0.8))
  _upg_bar = ax.bar(index_1,
                  _upg_data,
                  width,
                  label='Upg',
                  hatch='-',
                  bottom=[sum(x) for x in zip(_getx_data, _get_data)],
                  color=(0.7, 0.7, 0.7, 0.8))
  # label for baseline
  count = 0
  for r1,r2,r3 in zip(rects3, _get_bar, _upg_bar):
    if count < len(BENCH_NAMES):
      count += 1
      continue
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    plt.text(r1.get_x() + r1.get_width() / 2., h1+h2+h3+0.03, 'B', ha='center', va='center', fontsize=6, color='black')


  rects1 = ax.bar(index1,
                  _getx_data_detect,
                  width,
                  # label='GetX',
                  align="edge",
                  color=(0.9, 0.9, 0.9, 0.8),
                  edgecolor='black', linewidth=0.02)
  _get_bar_detect = ax.bar(index1 ,
                  _get_data_detect,
                  width,
                  # label='Get',
                  align="edge",
                  bottom=_getx_data_detect,
                  color=(0.2, 0.2, 0.2, 0.8),
                  edgecolor='black', linewidth=0.02)
  _upg_bar_detect = ax.bar(index1,
                  _upg_data_detect,
                  width,
                  # label='Upgrade',
                  align="edge",
                  bottom=[sum(x) for x in zip(_getx_data_detect, _get_data_detect)],
                  color=(0.7, 0.7, 0.7, 0.8),
                  edgecolor='black', linewidth=0.02)
  _total_md_bar_detect = ax.bar(index1,
                  _total_md_data_detect,
                  width,
                  label='Metadata',
                  align="edge",
                  bottom=[sum(x) for x in zip(_getx_data_detect, _get_data_detect, _upg_data_detect)],
                  color=(0.4, 0.4, 0.4, 0.8),
                  edgecolor='black', linewidth=0.02) 
  count = 0
  for r1,r2,r3,r4 in zip(rects1, _get_bar_detect, _upg_bar_detect, _total_md_bar_detect):
    if count < len(BENCH_NAMES):
      count += 1
      continue
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    h4 = r4.get_height()
    plt.text(r1.get_x() + r1.get_width() / 2., h1+h2+h3+h4+0.03, 'D', ha='center', va='center', fontsize=6, color='black')

  
  rects2 = ax.bar( index2 ,
    _getx_data_repair,
    width,
    align="edge",
    # label='GetX',
    hatch='//',
    color=(0.9, 0.9, 0.9, 0.8))
  _get_bar_repair = ax.bar( index2,
    _get_data_repair,
    width,
    align="edge",
    # label='Get',
    bottom=_getx_data_repair,
    color=(0.2, 0.2, 0.2, 0.8))
  _upg_bar_repair = ax.bar(
    index2,
    _upg_data_repair,
    width,
    align="edge",
    # label='Upgrade',
    bottom=[sum(x) for x in zip(_getx_data_repair, _get_data_repair)],
                  color=(0.7, 0.7, 0.7, 0.8))
  _total_md_bar_repair = ax.bar( index2,
    _total_md_data_repair,
    width,
    align="edge",
    # label='TotalMD',
    bottom=[sum(x) for x in zip(_getx_data_repair, _get_data_repair, _upg_data_repair)],
    color=(0.4, 0.4, 0.4, 0.8))
  count = 0
  for r1,r2,r3,r4 in zip(rects2, _get_bar_repair, _upg_bar_repair, _total_md_bar_repair):
    if count < len(BENCH_NAMES):
      count += 1
      continue
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    h4 = r4.get_height()
    plt.text(r1.get_x() + r1.get_width() / 2., h1+h2+h3+h4+0.03, 'L', ha='center', va='center', fontsize=6, color='black')
    count += 1
    if count:
      break

  plt.legend(loc='upper center', ncol=4, fontsize=6, frameon=False,labelspacing=0.01, borderpad=0.01)
  plt.text(0.45, 0.82, 'B:Baseline, D:FSDetect, L:FSLite', ha='center', va='center', fontsize=6, color='black', transform=ax.transAxes)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def plot_metadata_category(abs_traffic:dict, y_axis_label, pdf_name, log_scale=False):
  fig,ax = plt.subplots( facecolor='w', edgecolor='k')
  fig.set_figheight(1.5)
  # ax = fig.add_axes([0, 0, 1, 1])
  # index[-1] = 8.5
  # ax.set_xticks(index + width / 2)
  metadata_index = [0.4, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4, 8.4]
  metadata_index1 = [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3]

  ax.set_xticks(metadata_index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=8)
  ax.set_yticks(np.arange(0, 0.4, 0.1))
  MAX_HT = 0.4
  plt.ylim(0, MAX_HT)

  plt.yticks(fontsize=8)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars
  # Filter out the message based on type

  _total_md_data_detect = [round(bench_data[bench+"-detect"][KEY_TOTAL_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _total_md_data_detect_mean = round(np.mean(_total_md_data_detect),PRECISION)
  _total_md_data_detect_copy = []
  count = 0
  for i in range(len(_total_md_data_detect)):
    if _total_md_data_detect[i] == 0:
      _total_md_data_detect_copy.append(1)
      count += 1
    else:
      _total_md_data_detect_copy.append(_total_md_data_detect[i])
  # _total_md_data_detect.append(round(np.power(np.prod(_total_md_data_detect_copy), 1.0/(len(_total_md_data_detect_copy)-count)),PRECISION))
  _total_md_data_detect.append(_total_md_data_detect_mean)

  _total_md_data_repair=[round(bench_data[bench+"-repair"][KEY_TOTAL_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _total_md_data_repair_mean = round(np.mean(_total_md_data_repair),PRECISION)
  _total_md_data_repair_copy = []
  count = 0
  for i in range(len(_total_md_data_repair)):
    if _total_md_data_repair[i] == 0:
      _total_md_data_repair_copy.append(1)
      count += 1
    else:
      _total_md_data_repair_copy.append(_total_md_data_repair[i])
  # _total_md_data_repair.append(round(np.power(np.prod(_total_md_data_repair_copy), 1.0/(len(_total_md_data_repair_copy)-count)),PRECISION))
  _total_md_data_repair.append(_total_md_data_repair_mean)

  _eviction_md_data_detect= [round(bench_data[bench+"-detect"][KEY_EVICTION_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _eviction_md_data_detect_mean = round(np.mean(_eviction_md_data_detect),PRECISION)
  _eviction_md_data_detect_copy = []
  count = 0
  for i in range(len(_eviction_md_data_detect)):
    if _eviction_md_data_detect[i] == 0:
      _eviction_md_data_detect_copy.append(1)
      count += 1
    else:
      _eviction_md_data_detect_copy.append(_eviction_md_data_detect[i])
  # _eviction_md_data_detect.append(round(np.power(np.prod(_eviction_md_data_detect_copy), 1.0/(len(_eviction_md_data_detect_copy)-count)),PRECISION))
  _eviction_md_data_detect.append(_eviction_md_data_detect_mean)

  _eviction_md_data_repair=[round(bench_data[bench+"-repair"][KEY_EVICTION_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _eviction_md_data_repair_mean = round(np.mean(_eviction_md_data_repair),PRECISION)
  _eviction_md_data_repair_copy = []
  count = 0
  for i in range(len(_eviction_md_data_repair)):
    if _eviction_md_data_repair[i] == 0:
      _eviction_md_data_repair_copy.append(1)
      count += 1
    else:
      _eviction_md_data_repair_copy.append(_eviction_md_data_repair[i])
  # _eviction_md_data_repair.append(round(np.power(np.prod(_eviction_md_data_repair_copy), 1.0/(len(_eviction_md_data_repair_copy)-count)),PRECISION))
  _eviction_md_data_repair.append(_eviction_md_data_repair_mean)

  _control_md_data_detect=[round(bench_data[bench+"-detect"][KEY_CONTROL_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _control_md_data_detect_mean = round(np.mean(_control_md_data_detect),PRECISION)
  _control_md_data_detect.append(_control_md_data_detect_mean)

  _control_md_data_repair=[round(bench_data[bench+"-repair"][KEY_CONTROL_MD]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _control_md_data_repair_mean = round(np.mean(_control_md_data_repair),PRECISION)
  _control_md_data_repair_copy = []
  count = 0
  for i in range(len(_control_md_data_repair)):
    if _control_md_data_repair[i] == 0:
      _control_md_data_repair_copy.append(1)
      count += 1
    else:
      _control_md_data_repair_copy.append(_control_md_data_repair[i])
  # _control_md_data_repair.append(round(np.power(np.prod(_control_md_data_repair_copy), 1.0/(len(_control_md_data_repair_copy)-count)),PRECISION))
  _control_md_data_repair.append(_control_md_data_repair_mean)
  _md_data_msg_data_detect=[round(bench_data[bench+"-detect"][KEY_MD_DATA_MSG]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _md_data_msg_data_detect_mean = round(np.mean(_md_data_msg_data_detect),PRECISION)
  _md_data_msg_data_detect_copy = []
  count = 0
  for i in range(len(_md_data_msg_data_detect)):
    if _md_data_msg_data_detect[i] == 0:
      _md_data_msg_data_detect_copy.append(1)
      count += 1
    else:
      _md_data_msg_data_detect_copy.append(_md_data_msg_data_detect[i])
  # _md_data_msg_data_detect.append(round(np.power(np.prod(_md_data_msg_data_detect_copy), 1.0/(len(_md_data_msg_data_detect_copy)-count)),PRECISION))
  _md_data_msg_data_detect.append(_md_data_msg_data_detect_mean)

  _md_data_msg_data_repair=[round(bench_data[bench+"-repair"][KEY_MD_DATA_MSG]/abs_traffic[bench],PRECISION) for bench in BENCH_NAMES]
  _md_data_msg_data_repair_mean = round(np.mean(_md_data_msg_data_repair),PRECISION)
  _md_data_msg_data_repair_copy = []
  count = 0
  for i in range(len(_md_data_msg_data_repair)):
    if _md_data_msg_data_repair[i] == 0:
      _md_data_msg_data_repair_copy.append(1)
      count += 1
    else:
      _md_data_msg_data_repair_copy.append(_md_data_msg_data_repair[i])
  # _md_data_msg_data_repair.append(round(np.power(np.prod(_md_data_msg_data_repair_copy), 1.0/(len(_md_data_msg_data_repair_copy)-count)),PRECISION))
  _md_data_msg_data_repair.append(_md_data_msg_data_repair_mean)

  rects1 = ax.bar(metadata_index1,
                  _eviction_md_data_detect,
                  width,
                  label='Eviction MD',
                  color=(0.1, 0.1, 0.9, 0.8))
  _get_bar = ax.bar(metadata_index1,
                  _control_md_data_detect,
                  width,
                  label='Control MD',
                  bottom=_eviction_md_data_detect,
                  color=(0.9, 0.1, 0.1, 0.8))
  _upg_bar = ax.bar(metadata_index1,
                  _md_data_msg_data_detect,
                  width,
                  label='MD Data',
                  bottom=[sum(x) for x in zip(_eviction_md_data_detect, _control_md_data_detect)],
                  color=(0.1, 0.9, 0.1, 0.8))
  rects2 = ax.bar(metadata_index,
                  _eviction_md_data_repair,
                  width,
                  # label='Eviction MD',
                  align="edge",
                  color=(0.1, 0.1, 0.9, 0.8))
  _get_bar = ax.bar(metadata_index,
                  _control_md_data_repair,
                  width,
                  # label='Control MD',
                  align="edge",
                  bottom=_eviction_md_data_repair,
                  color=(0.9, 0.1, 0.1, 0.8))
  _upg_bar = ax.bar(metadata_index,
                  _md_data_msg_data_repair,
                  width,
                  # label='MD Data',
                  align="edge",
                  bottom=[sum(x) for x in zip(_eviction_md_data_repair, _control_md_data_repair)],
                  color=(0.1, 0.9, 0.1, 0.8))
  # _total_md_bar = ax.bar(index1,
  #                 _total_md_data,
  #                 width,
  #                 label='TotalMD',
  #                 bottom=[sum(x) for x in zip(_getx_data, _get_data, _upg_data)],
  #                 color=(0.1, 0.9, 0.1, 0.8))
  
  plt.legend(loc='best', ncol=3, fontsize=7)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        # print(row.index(KEY_TOTAL_MD))
        # print(row.index(KEY_EVICTION_MD))
        # print(row.index(KEY_CONTROL_MD))
        # print(row.index(KEY_MD_DATA_MSG))
        # print(row.index(KEY_LLC_GETX))
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
        assert (row.index(KEY_TOTAL_MD) == IDX_TOTAL_MD)
        assert (row.index(KEY_EVICTION_MD) == IDX_EVICTION_MD)
        assert (row.index(KEY_CONTROL_MD) == IDX_CONTROL_MD)
        assert (row.index(KEY_MD_DATA_MSG) == IDX_MD_DATA_MSG)
      elif row_num > 2:
        tmp = {}
        # tmp[KEY_RUNTIME] = str_to_float(row[IDX_RUNTIME])
        # tmp[KEY_MSG_VOL] = str_to_float(row[IDX_MSG_VOL])
        # tmp[KEY_MSG_COUNT] = str_to_float(row[IDX_MSG_COUNT])
        # tmp[KEY_ENERGY_L1D] = str_to_float(row[IDX_ENERGY_L1D])
        # tmp[KEY_ENERGY_LLC] = str_to_float(row[IDX_ENERGY_LLC])
        # tmp[KEY_ENERGY_PAM] = str_to_float(row[IDX_ENERGY_PAM])
        # tmp[KEY_ENERGY_SAM] = str_to_float(row[IDX_ENERGY_SAM])
        # tmp[KEY_ENERGY_CPU2L1D] = str_to_float(row[IDX_ENERGY_CPU2L1D])
        # tmp[KEY_ENERGY_FILL] = str_to_float(row[IDX_ENERGY_FILL])
        # tmp[KEY_TOTAL_LEAKAGE] = str_to_float(row[IDX_ENERGY_LEAKAGE])
        # tmp[KEY_LLC_RQT] = str_to_float(row[IDX_LLC_GET]) + str_to_float(row[IDX_LLC_GETX])\
        #      + str_to_float(row[IDX_LLC_UPG]) + str_to_float(row[IDX_UP_ALL])\
        #       + str_to_float(row[IDX_UP_DMD]) + str_to_float(row[IDX_UP_EDS])\
        #         + str_to_float(row[IDX_UP_MD])
        tmp[KEY_TOTAL_MD] = round(str_to_float(row[IDX_TOTAL_MD]))
        tmp[KEY_EVICTION_MD] = round(str_to_float(row[IDX_EVICTION_MD]),0)
        tmp[KEY_CONTROL_MD] = round(str_to_float(row[IDX_CONTROL_MD]),0)
        tmp[KEY_MD_DATA_MSG] =round(str_to_float(row[IDX_MD_DATA_MSG]),0)
        tmp[KEY_LLC_GETX] = round(str_to_float(row[IDX_LLC_GETX]))
        tmp[KEY_LLC_GET] = round(str_to_float(row[IDX_LLC_GET]))
        tmp[KEY_LLC_UPG] = round(str_to_float(row[IDX_LLC_UPG]))
        # VIPIN: adding protocol specific name to differentiate entry in map
        if "FS_MESI_DETECTION" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+ "-detect"] = tmp
        elif "FS_MESI" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp
        else:
          bench_data[row[IDX_BENCH]] = tmp
      row_num += 1


# FalseSharing: stack bar for each protocol
def plot_traffic_vol_stack_bar(fs_abs_traffic:dict):
  plot_data(fs_abs_traffic,  "Normalized fraction of\n network msg count",
            "fs-apps-traffic-stack-bar.pdf", False)

def main():
  read_csv_file()
  fs_abs_traffic:dict = {}

  for bench in BENCH_NAMES:
    total_msg_count_baseline = 0.0
    total_msg_count_detect = 0.0
    total_msg_count_repair = 0.0
    for _msg_key in [KEY_TOTAL_MD, KEY_LLC_GET, KEY_LLC_UPG, KEY_LLC_GETX]:
      total_msg_count_baseline += bench_data[bench][_msg_key]
      total_msg_count_detect += bench_data[bench+"-detect"][_msg_key]
      total_msg_count_repair += bench_data[bench+"-repair"][_msg_key]
    fs_abs_traffic[bench] = total_msg_count_baseline
    fs_abs_traffic[bench+"-detect"] = total_msg_count_detect
    fs_abs_traffic[bench+"-repair"] = total_msg_count_repair
  
  plot_traffic_vol_stack_bar(fs_abs_traffic)
  # plot_metadata_category(fs_abs_traffic,"Normalized fraction of\n each metadata message category", "fs-apps-metadata-stack-bar.pdf")

if __name__ == "__main__":
  main()
