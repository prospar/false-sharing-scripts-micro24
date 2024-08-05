# useful link for reference: https://matplotlib.org/3.3.4/gallery/index.html

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Update the list of benchmarks
x_labels = ['hist-med', 'lr-med', 'str-mat-med', 'ref-count', 'spinlock']

PRECISION = 3  # digits

# label along y-axis
# y_labels = [0, 0.5, 1, 1.05]

# equally distribute the label locations along x axis
index = np.arange(len(x_labels))

width = 0.35  # the width of the bars


def plot_data(orig_data, manual_data, y_axis_label, pdf_name):
    fig = plt.figure(figsize=(4, 2), dpi=120, facecolor='w', edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_xticks(index + width / 2)
    ax.set_xticklabels(x_labels, rotation=30, fontsize=8)

    ax.set_ylabel(y_axis_label, fontsize=10)
    plt.ylim(0, 1.1)

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
        # hatch='o',
        color=(0.2, 0.2, 0.2, 0.7))

    plt.axhline(y=1.0, color='k', linestyle='--')

    # ax.legend(x_labels)
    # leg = ax.get_legend()
    # leg.legendHandles[0].set_color(mcolors[0])
    # leg.legendHandles[1].set_color(mcolors[1])

    # fig.tight_layout()
    # plt.show()

    fig.savefig(pdf_name, bbox_inches='tight', format="pdf")
    plt.close()


def plot_time():
    # Value are normalized to execution w.r.t false sharing version
    fs_version_time = [1 for x in x_labels]

    manual_fix_time = [0.9357804966, 0.3612873858, 0.988772333, 0.4258604738, 0.938965831]
    manual_fix_time = [round(num, PRECISION) for num in manual_fix_time]

    plot_data(fs_version_time, manual_fix_time, "Normalized execution time", "plot-runtime.pdf")


def plot_traffic_vol():
    fs_msg_vol = [8765817928, 16034691816, 1393743488, 11421463672, 49484120]
    fs_msg_vol = [num / num for num in fs_msg_vol]

    man_msg_vol = [3810778704, 513011784, 507212728, 2529120, 957016]
    man_msg_vol = [round(man_msg_vol[i] / fs_msg_vol[i], PRECISION) for i in range(len(x_labels))]

    plot_data(fs_msg_vol, man_msg_vol, "Normalized on-chip traffic \n(bytes)",
              "plot-traffic-vol.pdf")


def plot_traffic_count():
    fs_msg_count = [380480089, 719334677, 57667208, 461526207, 2048803]
    fs_msg_count = [num / num for num in fs_msg_count]

    man_msg_count = [157394042, 20856329, 20084887, 98508, 26323]
    man_msg_count = [
        round(man_msg_count[i] / fs_msg_count[i], PRECISION) for i in range(len(x_labels))
    ]

    plot_data(fs_msg_count, man_msg_count, "Normalized on-chip traffic \n(messages)",
              "plot-traffic-count.pdf")


def plot_energy():
    pass


def main():
    plot_time()
    plot_traffic_vol()
    plot_traffic_count()
    plot_energy()


def getColorsList():
    # mcolors = list(matplotlib.colors.cnames.keys())
    # CSS colours used from
    # https://matplotlib.org/3.3.0/gallery/color/named_colors.html
    return ['slategray', 'lightgrey', 'dimgray', 'darkgray', 'silver', 'y', 'k']


if __name__ == "__main__":
    main()
