# This script is for generating plots in the introduction for our MICRO24 submission.
# NOTE: Remember to update PATH_CSV if we have new data

import csv
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

BENCH_NAMES = [ 
  "BS", "LL","LR","LT","RC", "SM"
]

x_labels = [
  "BS", "LL","LR","LT","RC", "SM", "geomean"
]

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


def plot_data(huron_data, sheriff_data,  fslite_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(3.2, 1.6), dpi=120, facecolor='w', edgecolor='k')
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 6.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index-(width/2))
  ax.set_xticklabels(x_labels, fontsize=8)

  ax.set_ylabel(y_axis_label, fontsize=9)
  MAX_HT = 1.3
  plt.ylim(0.5, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - (3*width) / 2,
                  huron_data,
                  width,
                  label='Huron',
                  # hatch='//',
                  color=(0.3, 0.3, 0.3, 0.8))

  rects2 = ax.bar(
    index -(width/2),
    sheriff_data,
    width,
    align="center",
    label='Sheriff',
    # hatch='-',
    color=(0.6, 0.6, 0.6, 0.8))
  
  rects3 = ax.bar(
    index + (width/2),
    fslite_data,
    width,
    align="center",
    label='FSLite',
    # hatch='\\',
    color=(0.4, 0.4, 0.4, 0.8))

  # plt.axhline(y=1.0, color='k', linestyle='--')

  for bar, label in zip(rects1, huron_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() - bar.get_width() / 10, height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
  
  for bar, label in zip(rects2, sheriff_data):
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
  
  for bar, label in zip(rects3, fslite_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() + bar.get_width() , height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
  
  
  # for bars in [rects1, rects2, rects3]:
  #   for bar in bars:
  #       height = bar.get_height()
  #       if height > MAX_HT:
  #         height = MAX_HT
  #       ax.annotate('{}'.format(height),
  #                   xy=(bar.get_x() + bar.get_width() / 1.5, height),
  #                   xytext=(0, 3),  # 3 points vertical offset
  #                   textcoords="offset points",
  #                   ha='center', va='bottom',size=7)


  # fig.tight_layout()
  # plt.show()
  plt.legend(loc="lower left", ncol=3, fontsize=8)
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

def plot_data_huron(huron_data, fslite_data, y_axis_label, pdf_name, log_scale=False):
  fig = plt.figure(figsize=(3.2, 0.8), dpi=120, facecolor='w', edgecolor='k')
  ax = fig.add_axes([0, 0, 1, 1])
  index[-1] = 6.5
  # ax.set_xticks(index + width / 2)
  ax.set_xticks(index)
  ax.set_xticklabels(x_labels, fontsize=8)
  ax.set_yticks([0.6, 0.8, 1.0, 1.1])
  ax.set_yticklabels([0.6, 0.8, 1.0, 1.1],fontsize=8)
  ax.set_ylabel(y_axis_label, fontsize=8)
  MAX_HT = 1.1
  plt.ylim(0.6, MAX_HT)
  if log_scale:  # convert y-axis to Logarithmic scale
    plt.yscale("log")
    # Cannot set the minimum y-value to 0 on a log scale since log(0) is not defined
    plt.ylim(0.001, MAX_HT)

  ax.grid(axis='y', linestyle='dashed', linewidth=0.5)  # plot only horizontal grid lines
  ax.set_axisbelow(True)  # show grid lines behind bars

  rects1 = ax.bar(index - (width)/2,
                  huron_data,
                  width,
                  label='Huron',
                  # hatch='//',
                  color=(0.3, 0.3, 0.3, 0.8))
  
  rects3 = ax.bar(
    index+width/2,
    fslite_data,
    width,
    align="center",
    label='FSLite',
    # hatch='\\',
    color=(0.6, 0.6, 0.6, 0.8))

  plt.axhline(y=1.0, color='red', linestyle='--',label='Manual Fix', linewidth=0.5)

  for bar, label in zip(rects1, huron_data):
      height = bar.get_height()
      if height > MAX_HT:
        height = MAX_HT
      elif height == 1.0:
        continue
      ax.annotate('{}'.format(label),
                  xy=(bar.get_x() - bar.get_width() / 10, height-0.01),
                  xytext=(0, 3),  # 3 points vertical offset
                  textcoords="offset points",
                  ha='center', va='bottom',size=7,rotation=0)
  
  for bar, label in zip(rects3, fslite_data):
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
                  ha='center', va='bottom',size=7,rotation=0)

  plt.legend(loc="lower left", ncol=1, fontsize=7, labelspacing=0.01, borderpad=0.01 )
  fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
  plt.close()

def plot_time():
  #plot_data(huron_norm_times, sheriff_norm_times, fslite_norm_times, "Normalized execution \n  time", "plot-compare-huron.pdf")
  plot_data_huron(huron_speedup, fslite_speedup, "Speedup", "plot-huron-comparison.pdf")


def main():
  # read_csv_file()
  plot_time()

if __name__ == "__main__":
  main()
