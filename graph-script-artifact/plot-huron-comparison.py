# This script is for generating plots in the introduction for our MICRO24 submission.
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

BENCH_NAMES = [ 
  "huron_bs_base", "huron_ll_base","huron_lr_base","huron_lt_base","huron_rc_base", "huron_sm_base"
]

x_labels = [
  "BS", "LL","LR","LT","RC", "SM", "geomean"
]


PATH_CSV = "/home/prospar/prospar-micro-result/micro-compare-huron/Stats_Avg.csv"
PATH_CSV = str(sys.argv[1])
KEY_BENCH = "bench"
KEY_PROTOCOL = "protocol"
KEY_RUNTIME = "KEY_SIM_TICKS"

# vipin: these indices might changes if adding new stats
IDX_PROTOCOL = 0
IDX_BENCH = 3
IDX_RUNTIME = 6



# FalseSharing: huron numbers from native run w.r.t. manual fix


# these value are consistent with the labels 1:1 mapping
repair_speedup = [
  1.003103237, 0.979336317, 0.9894833579, 1.103398809, 1.27691981, 0.9949700632, 1.052928035
]
fslite_speedup = [round(x, 2) for x in repair_speedup]
huron_speedup_base = [ 
  1.146409959, 0.9408919496, 1.213145641, 1.097842429, 0.6955125894, 0.9171459236, 0.9855515575
]
huron_speedup = [round(x, 2) for x in huron_speedup_base]

# equally distribute the label locations along x axis
# index = np.arange(len(x_labels))
# print(index)
index = np.arange(0.0,7.0,1)

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


def read_csv_file():
  with open(PATH_CSV, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    row_num = 1
    for row in reader:
      if row_num == 1:
        print(row.index(KEY_PROTOCOL))
        print(row.index(KEY_BENCH))
        print(row.index(KEY_RUNTIME))
        assert (row.index(KEY_PROTOCOL) == IDX_PROTOCOL)
        assert (row.index(KEY_BENCH) == IDX_BENCH)
        assert (row.index(KEY_RUNTIME) == IDX_RUNTIME)

      elif row_num > 2:
        tmp = {}
        tmp[KEY_RUNTIME] = str_to_float(row[IDX_RUNTIME])

        # VIPIN: adding protocol specific name to differentiate entry in map
        if "_manual" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+ "-manual"] = tmp
        elif "FS_MESI" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-repair"] = tmp
        elif "_huron" in row[IDX_PROTOCOL]:
          bench_data[row[IDX_BENCH]+"-huron"] = tmp
        else:
          bench_data[row[IDX_BENCH]] = tmp
      row_num += 1



# HURON data from clang compiler
def plot_clang_data_huron(manual_data_clang, huron_data_clang, fslite_data_clang, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(3.2, 0.8), dpi=120, facecolor='w', edgecolor='k')
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 6.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, fontsize=8)
  ax.set_yticks([0.9, 1.1, 1.3,1.4])
  ax.set_yticklabels([0.9, 1.1, 1.3,1.4],fontsize=8)
  ax.set_ylabel(y_axis_label, fontsize=8)
  MAX_HT = 1.4
  plt.ylim(0.9, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - (width),
                  manual_data_clang,
                  width,
                  label='Manual',
                  hatch='//',
                  color=(0.2, 0.2, 0.2, 0.8))
  
  rects2 = ax.bar(
    index,
    huron_data_clang,
    width,
    align="center",
    label='Huron',
    # hatch='\',
    color=(0.5, 0.5, 0.5, 0.8))


  rects3 = ax.bar(
    index+width,
    fslite_data_clang,
    width,
    align="center",
    label='FSLite',
    hatch='\\',
    color=(0.8, 0.8, 0.8, 0.8))

  plt.axhline(y=1.0, color='red', linestyle='--',label='Baseline', linewidth=0.5)

  for bar, label in zip(rects1, manual_data_clang):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() - bar.get_width() / 10, height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=90)
  
  for bar, label in zip(rects2, huron_data_clang):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      elif height == 1.05:
        height = 1.0
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width()/2 , height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=90)

  for bar, label in zip(rects3, fslite_data_clang):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      elif height == 1.05:
        height = 1.0
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() , height),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=90)

  plt.legend(loc="center right", ncol=2, fontsize=7, labelspacing=0.01, borderpad=0.01 )
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

def plot_time():
  bench_abs_times = []
  bench_manual_abs_time = []
  bench_repair_abs_time = []
  bench_huron_abs_time = []
  for bench in BENCH_NAMES:
    
    bench_fs_run_time = bench_data[bench][KEY_RUNTIME]
    bench_abs_times.append(bench_fs_run_time)
    # detect protocol
    bench_manual = bench + "-manual"
    bench_manual_run_time = bench_data[bench_manual][KEY_RUNTIME]
    bench_manual_abs_time.append(bench_manual_run_time)
    # repair protocol
    bench_repair = bench + "-repair"
    bench_repair_run_time = bench_data[bench_repair][KEY_RUNTIME]
    bench_repair_abs_time.append(bench_repair_run_time)
    # huron protocol
    bench_huron = bench + "-huron"
    bench_huron_run_time = bench_data[bench_huron][KEY_RUNTIME]
    bench_huron_abs_time.append(bench_huron_run_time)
  bench_norm_times = [1 for x in bench_abs_times]
  bench_norm_times.append(1.0)
  # ealier n/d gives speedup, now d/n gives normalized value
  manual_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_manual_abs_time, bench_abs_times)]
  repair_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_repair_abs_time, bench_abs_times)]
  huron_norm_times = [round(d / n, PRECISION) for n, d in zip(bench_huron_abs_time, bench_abs_times)]
  geo_mean_time = round(np.power(np.prod(manual_norm_times), 1.0/len(manual_norm_times)),PRECISION)
  manual_norm_times.append(geo_mean_time)
  geo_mean_time = round(np.power(np.prod(repair_norm_times), 1.0/len(repair_norm_times)),PRECISION) 
  repair_norm_times.append(geo_mean_time)
  geo_mean_time = round(np.power(np.prod(huron_norm_times), 1.0/len(huron_norm_times)),PRECISION)
  huron_norm_times.append(geo_mean_time)


  plot_clang_data_huron(manual_norm_times, huron_norm_times, repair_norm_times, "Speedup", "plot-huron-comparison.pdf")



def main():
  read_csv_file()
  plot_time()

if __name__ == "__main__":
  main()
