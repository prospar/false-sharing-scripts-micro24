# This script is for generating plots in the introduction for our MICRO24 submission.

# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# Diff csv file : Stat_formatted.csv, Stats_Avg.csv, Stats_Median.csv, Stats_Max.csv, Stats_Min.csv
PATH_CSV = "/home/prospar/prospar-micro-result/micro-false-sharing-app/Stats_Avg.csv"

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
# PROSPAR: these indexex changes due to addition of new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_RUNTIME = 6
IDX_MSG_VOL =  103 #98
IDX_MSG_COUNT = 104 #99
IDX_ENERGY_PAM = 59
IDX_ENERGY_SAM = 60
IDX_ENERGY_L1D = 61
IDX_ENERGY_LLC = 62
IDX_ENERGY_CPU2L1D = 63
IDX_ENERGY_FILL = 64
IDX_ENERGY_LEAKAGE = 65
IDX_LLC_GET = 37
IDX_LLC_GETX = 38
IDX_LLC_UPG = 40
IDX_UP_ALL = 96
IDX_UP_DMD = 97
IDX_UP_EDS = 98
IDX_UP_MD = 99
IDX_TOTAL_MD = 125
IDX_EVICTION_MD = 124
IDX_CONTROL_MD = 122
IDX_MD_DATA_MSG = 123


BENCH_NAMES = [
  "false-sharing"
]

x_labels = [
  "FS",
  "geomean"
]

bench_data = {}

# equally distribute the label locations along x axis
index = np.arange(0.0,2.0,1.0)
# index = np.arange(len(x_labels))

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
  fig = plt.figure(figsize=(3.0, 1.6), dpi=120, facecolor='w', edgecolor='k')
  fig.set_figheight(1)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 8.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.6
  plt.ylim(0.9, MAX_HT)
  ax.set_yticks(np.arange(1.0, MAX_HT, 0.2))
  # ax.set_yticklabels([0.9, 1.0, 1.1],fontsize=8)
  plt.yticks(fontsize=8)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - width/2,
                  orig_data,
                  width,
                  label='FSDetect',
                  # hatch='x',
                  color=(0.3, 0.3, 0.3, 0.8))

  rects2 = ax.bar(
    index ,
    manual_data,
    width,
    align="edge",
    label='FSLite',
    # hatch='//',
    color=(0.7, 0.7, 0.7, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')
  # for bars in [rects1, rects2]:
  for bar, label in zip(rects1, orig_data):# if bars == rects1 else manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 10, height-0.02),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
  for bar, label in zip(rects2, manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
        ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
      elif height == 1.0:
        continue
      else:
        ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)  

  plt.legend(loc='upper right', ncol=2, fontsize=7, borderaxespad=0.0, columnspacing=0.5, labelspacing=0.1)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()


def plot_energy_data(orig_data, manual_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(3.2, 1), dpi=120, facecolor='w', edgecolor='k')
  fig.set_figheight(1)
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 8.5
  width = 0.2  # the width of the bars
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, rotation=0, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.1
  plt.ylim(0.2, MAX_HT)
  ax.set_yticks(np.arange(0.25, MAX_HT, 0.25))
  # ax.set_yticklabels([0.9, 1.0, 1.1],fontsize=8)
  plt.yticks(fontsize=7)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - width/2,
                  orig_data,
                  width,
                  label='FSDetect',
                  # hatch='x',
                  color=(0.3, 0.3, 0.3, 0.8))

  rects2 = ax.bar(
    index ,
    manual_data,
    width,
    align="edge",
    label='FSLite',
    # hatch='//',
    color=(0.7, 0.7, 0.7, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')
  # for bars in [rects1, rects2]:
  for bar, label in zip(rects1, orig_data):# if bars == rects1 else manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 10, height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
  for bar, label in zip(rects2, manual_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
        ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() / 2, height-0.02),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
      elif height == 1.0:
        continue
      # elif height == 1.01:
      #   height = 1.
      else:
        ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() , height-0.05),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)  

  plt.legend(loc='lower right', ncol=1, fontsize=7, borderaxespad=0.0, columnspacing=0.5, labelspacing=0.1)
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
        assert (row.index(KEY_TOTAL_MD) == IDX_TOTAL_MD)
        assert (row.index(KEY_EVICTION_MD) == IDX_EVICTION_MD)
        assert (row.index(KEY_CONTROL_MD) == IDX_CONTROL_MD)
        assert (row.index(KEY_MD_DATA_MSG) == IDX_MD_DATA_MSG)
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
        # PROSPAR: BYPASS the assert for repair and detect protocol
        if "FS_MESI" not in row[IDX_PROTOCOL]:
          assert (tmp[KEY_ENERGY_PAM] == 0 and tmp[KEY_ENERGY_SAM] == 0)
        # PROSPAR: adding protocol specific name to differentiate entry in map
        if "FS_MESI_DETECTION" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+ "-detect"] = tmp
        elif "FS_MESI" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp
        else:
          bench_data[row[IDX_BENCH]] = tmp

        # if "manual" not in row[IDX_PROTOCOL]:
        #   bench_data[row[IDX_BENCH]] = tmp
        # else:
        #   bench_data[row[IDX_BENCH]+"-manual"] = tmp
      row_num += 1


def plot_time():
  fs_abs_times = []
  bench_detect_abs_time = []
  bench_repair_abs_time = []
  for bench in BENCH_NAMES:
    # print(bench)
    # print(bench_data)
    bench_fs_run_time = bench_data[bench][KEY_RUNTIME]
    fs_abs_times.append(bench_fs_run_time)
    # detect protocol
    bench_detect = bench + "-detect"
    bench_detect_run_time = bench_data[bench_detect][KEY_RUNTIME]
    bench_detect_abs_time.append(bench_detect_run_time)
    # repair protocol
    bench_repair = bench + "-repair"
    bench_repair_run_time = bench_data[bench_repair][KEY_RUNTIME]
    bench_repair_abs_time.append(bench_repair_run_time)

  fs_norm_times = [1 for x in fs_abs_times]
  fs_norm_times.append(1.0)
  # ealier n/d gives speedup, now d/n gives normalized value
  detect_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_detect_abs_time, fs_abs_times)]
  repair_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_repair_abs_time, fs_abs_times)]  
  geo_mean_time = round(np.power(np.prod(detect_norm_times), 1.0/len(detect_norm_times)),PRECISION)
  
  print(repair_norm_times)
  detect_norm_times.append(geo_mean_time)
  geo_mean_time = round(np.power(np.prod(repair_norm_times), 1.0/len(repair_norm_times)),PRECISION) 
  repair_norm_times.append(geo_mean_time)
  plot_data(detect_norm_times, repair_norm_times, "Speedup", "test-app-run-time.pdf")


def plot_traffic_vol():
  fs_abs_traffic = []
  detect_abs_traffic = []
  repair_abs_traffic = []
  for bench in BENCH_NAMES:
    bench_fs_traffic = bench_data[bench][KEY_MSG_VOL]
    fs_abs_traffic.append(bench_fs_traffic)
    bench_detect = bench + "-detect"
    bench_detect_traffic = bench_data[bench_detect][KEY_MSG_VOL]
    detect_abs_traffic.append(bench_detect_traffic)
    # repair protocol
    bench_repair = bench + "-repair"
    bench_repair_traffic = bench_data[bench_repair][KEY_MSG_VOL]
    repair_abs_traffic.append(bench_repair_traffic)

  fs_norm_traffic = [1 for x in fs_abs_traffic]
  detect_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(detect_abs_traffic, fs_abs_traffic)
  ]
  geo_mean_vol = round(np.power(np.prod(detect_norm_traffic), 1.0/len(detect_norm_traffic)),PRECISION)
  fs_norm_traffic.append(1.0)
  detect_norm_traffic.append(geo_mean_vol)
  repair_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(repair_abs_traffic, fs_abs_traffic)
  ]
  geo_mean_vol = round(np.power(np.prod(repair_norm_traffic), 1.0/len(repair_norm_traffic)),PRECISION)
  repair_norm_traffic.append(geo_mean_vol)
  plot_data(detect_norm_traffic, repair_norm_traffic,  "Normalized on-chip traffic \n(bytes)",
            "test-app-traffic-vol.pdf")


def plot_traffic_count():
  fs_abs_traffic = []
  detect_abs_traffic = []
  repair_abs_traffic = []
  for bench in BENCH_NAMES:
    # bench_fs_traffic = bench_data[bench][KEY_MSG_COUNT]
    bench_fs_traffic = bench_data[bench][KEY_LLC_RQT]
    fs_abs_traffic.append(bench_fs_traffic)
    bench_detect = bench + "-detect"
    # bench_detect_traffic = bench_data[bench_detect][KEY_MSG_COUNT]
    bench_detect_traffic = bench_data[bench_detect][KEY_LLC_RQT]
    detect_abs_traffic.append(bench_detect_traffic)
    # repair protocol
    bench_repair = bench + "-repair"
    # bench_repair_traffic = bench_data[bench_repair][KEY_MSG_COUNT]
    bench_repair_traffic = bench_data[bench_repair][KEY_LLC_RQT]
    repair_abs_traffic.append(bench_repair_traffic)

  fs_norm_traffic = [1 for x in fs_abs_traffic]
  detect_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(detect_abs_traffic, fs_abs_traffic)
  ]
  count = 0
  for i in range(len(detect_norm_traffic)):
    if detect_norm_traffic[i] == 0:
      detect_norm_traffic[i] = 1
      count+=1
  geo_mean_count = round(np.power(np.prod(detect_norm_traffic), 1.0/(len(detect_norm_traffic)-count)),PRECISION)
  fs_norm_traffic.append(1.0)
  detect_norm_traffic.append(geo_mean_count)
  repair_norm_traffic = [
    round(n / d, PRECISION) for n, d in zip(repair_abs_traffic, fs_abs_traffic)
  ]
  count = 0
  for i in range(len(repair_norm_traffic)):
    if repair_norm_traffic[i] == 0:
      repair_norm_traffic[i] = 1
      count += 1
  geo_mean_count = round(np.power(np.prod(repair_norm_traffic), 1.0/(len(repair_norm_traffic)-count)),PRECISION)
  repair_norm_traffic.append(geo_mean_count)
  plot_data(detect_norm_traffic, repair_norm_traffic, "Normalized on-chip traffic \n(messages)",
            "test-app-traffic.pdf")

# TODO: stack plot for using diff energy component 
# fill energy, cpu2l1d energy, pam energy, sam energy, leakage energy
# will cover all energy components
# do not consider L1D and LLC energy
def plot_energy():
  fs_abs_energy = []
  man_fix_abs_energy = []
  detect_abs_energy = []
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
    fs_abs_energy.append( bench_fs_pamenergy + bench_fs_samenergy +
                         bench_fs_cpu2l1denergy + bench_fs_fillenergy +
                         bench_fs_staticleakage)
    bench_detect = bench + "-detect"
    bench_detect_l1denergy = bench_data[bench_detect][KEY_ENERGY_L1D]
    bench_detect_llcenergy = bench_data[bench_detect][KEY_ENERGY_LLC]
    bench_detect_pamenergy = bench_data[bench_detect][KEY_ENERGY_PAM]
    bench_detect_samenergy = bench_data[bench_detect][KEY_ENERGY_SAM]
    bench_detect_cpu2l1denergy = bench_data[bench_detect][KEY_ENERGY_CPU2L1D]
    bench_detect_fillenergy = bench_data[bench_detect][KEY_ENERGY_FILL]
    bench_detect_staticleakage = bench_data[bench_detect][KEY_TOTAL_LEAKAGE]
    # detect_abs_energy.append(bench_detect_l1denergy + bench_detect_llcenergy +
    detect_abs_energy.append(bench_detect_pamenergy + bench_detect_samenergy
                             + bench_detect_cpu2l1denergy + bench_detect_fillenergy
                              + bench_detect_staticleakage)
    bench_repair = bench + "-repair"
    bench_repair_l1denergy = bench_data[bench_repair][KEY_ENERGY_L1D]
    bench_repair_llcenergy = bench_data[bench_repair][KEY_ENERGY_LLC]
    bench_repair_pamenergy = bench_data[bench_repair][KEY_ENERGY_PAM]
    bench_repair_samenergy = bench_data[bench_repair][KEY_ENERGY_SAM]
    bench_repair_cpu2l1denergy = bench_data[bench_repair][KEY_ENERGY_CPU2L1D]
    bench_repair_fillenergy = bench_data[bench_repair][KEY_ENERGY_FILL]
    bench_repair_staticleakage = bench_data[bench_repair][KEY_TOTAL_LEAKAGE]
    # repair_abs_energy.append(bench_repair_l1denergy + bench_repair_llcenergy +
    repair_abs_energy.append(bench_repair_pamenergy + bench_repair_samenergy
                             + bench_repair_cpu2l1denergy + bench_repair_fillenergy
                             + bench_repair_staticleakage)

  fs_norm_energy = [1 for x in fs_abs_energy]
  detect_norm_energy = [round(n / d, PRECISION) for n, d in zip(detect_abs_energy, fs_abs_energy)]
  geo_mean_energy = round(np.power(np.prod(detect_norm_energy), 1.0/len(detect_norm_energy)),PRECISION)
  detect_norm_energy.append(geo_mean_energy)

  repair_norm_energy = [round(n / d, PRECISION) for n, d in zip(repair_abs_energy, fs_abs_energy)]
  geo_mean_energy = round(np.power(np.prod(repair_norm_energy), 1.0/len(repair_norm_energy)),PRECISION)
  repair_norm_energy.append(geo_mean_energy)
  fs_norm_energy.append(1.0)

  plot_energy_data(detect_norm_energy, repair_norm_energy, "Normalized energy \n usage", "test-app-energy.pdf")



def main():
  read_csv_file()
  plot_time()
  plot_energy() # use different range, so run one at a time

if __name__ == "__main__":
  main()
