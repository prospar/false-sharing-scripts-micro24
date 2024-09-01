import os
import sys
from typing import Set, List,Dict

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import re
import stats
import utils
import benchmarks
from constants import Constants

#FalseSharing: dumping stats as csv file
import csv

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


def _getOrderedProtocols(prot) -> List[str]:
    return [item for item in Constants.DESIRED_PROTOCOL_ORDER if item in prot]


def collectResults(options) -> list:
    """Walk the output directory, parse output files, identify valid/invalid results, and create
     a HTML container for logs."""
    validResSet = []  # list of dictionaries, with one dictionary representing one exp output

    num_total: int = 0
    num_valid: int = 0
    num_invalid: int = 0
    try:
        benchmarks_: Set[str] = set()
        protocols_: Set[str] = set()
        num_trials_: int = 0
        workloads_: Set[str] = set()

        for root, _, filenames in os.walk(options.getExpOutputDir()):
            for filename in filenames:
                if filename == Constants.STATS_FILE_NAME:
                    num_total += 1
                    path = os.path.join(root, filename)  # Path to one log file
                    if options.verbose > 1:
                        print(f"Parsing one experiment: {path}")
                    di_stats = stats.parseOneExperiment(root, path, options)
                    if di_stats["valid"]:
                        benchmarks_.add(di_stats[stats.KEY_BENCH])
                        protocols_.add(di_stats[stats.KEY_PROTOCOL])
                        num_trials_ = max(num_trials_, di_stats[stats.KEY_TRIAL])
                        workloads_.add(di_stats[stats.KEY_WS])
                        if options.verbose >= 3:
                            print(f"Stats extracted: {di_stats}")
                        num_valid += 1
                        validResSet.append(di_stats)
                    else:
                        print(f"Invalid log file: {path}")
                        num_invalid += 1
                    ## call for generating McPAT XML
                    # stats.gatherMcPATStats(root, path, options)
    finally:
        if options.verbose >= 1:
            print(f"Total number of log files: {num_total} Valid log files: {num_valid} "
                  f"Invalid log files: {num_invalid}")

    # Generate a success table
    html_str = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n"
                "<html lang=\"en\">\n\n")
    html_str += ("<table style=\"text-align: center; width: 90%;\" border=\"1\" cellpadding=\"2\""
                 "cellspacing=\"0\">\n\n<tbody>\n\n")
    # Generate the first row
    html_str += "<tr>\n<th></th>\n"

    for i in range(1, num_trials_ + 1):
        for prot_ in _getOrderedProtocols(protocols_):
            html_str += f"<th>tool={prot_} trial={str(i)}</th>\n"
    html_str += "</tr>\n\n"

    # Generate data corresponding to each benchmark, on one row
    for bench_ in benchmarks.getOrderedBenchmarks(benchmarks_):
        for ws_ in workloads_:
            present = True
            tmp_str: str = f"<tr>\n<td>bench={bench_}"
            if len(workloads_) > 1:
                tmp_str += f"<br>size={ws_}"
            tmp_str += ("</td>\n")
            for i in range(1, num_trials_ + 1):
                for prot_ in _getOrderedProtocols(protocols_):
                    # Construct the path to the output file
                    path = os.path.join(options.getExpOutputDir(), prot_, ws_, str(i), bench_)
                    if os.path.exists(path):
                        op_file = os.path.join(path, Constants.OUTPUT_FILE_NAME)
                        err_file = os.path.join(path, Constants.ERR_FILE_NAME)
                        stat_file = os.path.join(path, Constants.STATS_FILE_NAME)
                        # Check if the experiment passed or failed, re-parsing the output file
                        # seems faster than searching the list of all results
                        di_stats = stats.parseOneExperiment(path, stat_file, options)
                        # FalseSharing: formatting the privatization length stats
                        if di_stats["valid"]:
                            if prot_ == "FS_MESI_DETECTION":
                                # prvLenStatMap:Dict[str,Dict[str,List[PrivatizationStats]]] = 
                                # generatePrivatizationStats(path, op_file, options)
                                # for(key, value) in prvLenStatMap.items():
                                #     for instruction in value.keys():
                                #         print(f'{key} {len(value[instruction])}')
                                pass
                            elif prot_ == "FS_MESI":
                                # generateRepairPrivatizationStats(path, op_file, options)
                                pass
                        if di_stats["valid"]:
                            tmp_str += (f"<td><a href=\"{op_file}\" target="
                                        "><font color=green>OK</font></a>\n"
                                        f"<a href=\"{stat_file}\" target="
                                        "><font color=black>STATS</font></a></td>\n")
                            if options.verbose >= 3:
                                print(f"Stats extracted: {di_stats}")
                        else:
                            tmp_str += (f"<td><a href=\"{err_file}\"target="
                                        "><font color=red>ERR</font></a></td>\n")
                    else:
                        present = False
                        tmp_str += ("<td>--</td>\n")
            if present:  # Add to html output only if there is a trial
                html_str += tmp_str
        html_str += "</tr>\n\n"

    with open(os.path.join(options.getExpResultsDir(), "output.html"), "w",
              encoding="utf-8") as html_file:
        html_file.write(html_str)

    return [
        validResSet,
        benchmarks.getOrderedBenchmarks(benchmarks_),
        _getOrderedProtocols(protocols_)
    ]


def getColorsList() -> List:
    # mcolors = list(matplotlib.colors.cnames.keys())
    # CSS colours used from
    # https://matplotlib.org/3.3.0/gallery/color/named_colors.html
    return ['slategray', 'lightgrey', 'dimgray', 'darkgray', 'silver', 'y', 'k']


def getColor():
    for item in ['r', 'g', 'b', 'c', 'm', 'y', 'k']:
        yield item


def generateStats(options, resultSet: list, o_benchs: list, o_protocols: list):
    """Generate stats tables."""
    workingRS = resultSet.copy()

    # print(f"keys: {list(workingRS[0].keys())}")
    # heading for csv files
    csv_heading = list(workingRS[0].keys())
    csv_heading1 = {}
    for t,v in stats.ALL_STATS_KEYS.items():
        csv_heading1[t]=v
    # contains stats for each trial
    csv_file = open("Stat_formatted.csv","w")
    file_writer = csv.DictWriter(csv_file, fieldnames=csv_heading)
    file_writer.writeheader()
    file_writer.writerow(csv_heading1)
    for i in range(len(workingRS)):
        file_writer.writerow(workingRS[i])
    csv_file.close()
    # FalseSharing: workingRS is list, where each ele contains all stats for a bechmarks 
    # dump the stats as CSV file
    # Generate a stats table
    html_str = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n"
                "<html lang=\"en\">\n\n")
    html_str += ("<table style=\"text-align: center; width: 90%;\" border=\"1\" cellpadding=\"2\""
                 "cellspacing=\"0\">\n\n<tbody>\n\n")
    # Generate the first row
    html_str += "<tr>\n<th></th>\n"

    for bench_ in o_benchs:
        for prot_ in o_protocols:
            html_str += f"<th>bench={bench_}\nprotocol={prot_}</th>\n"
    html_str += "</tr>\n\n"

    # Generate data corresponding to each stat key, on one row
    for key, val in stats.ALL_STATS_KEYS.items():
        html_str += f"<tr>\n<td>{val}</td>\n"
        for bench_ in o_benchs:
            for prot_ in o_protocols:
                di_known = {}
                di_known[stats.KEY_BENCH] = bench_
                di_known[stats.KEY_PROTOCOL] = prot_
                li_limit: list = utils.limit_to_dicts_with_dict(workingRS, di_known)
                stat_val: dict = utils.merge(li_limit, key)
                html_str += f"<td>{stat_val.get(key)}</td>\n"
        html_str += "</tr>\n\n"

    # FalseSharing: generate the csv file with avg of all trial
    avg_csv_file = open("Stats_Avg.csv","w")
    median_csv_file = open("Stats_Median.csv","w")
    min_csv_file = open("Stats_Min.csv","w")
    max_csv_file = open("Stats_Max.csv","w")

    file_writer = csv.DictWriter(avg_csv_file, fieldnames=csv_heading)
    file_writer.writeheader()
    file_writer.writerow(csv_heading1)
    file_writer_med = csv.DictWriter(median_csv_file, fieldnames=csv_heading)
    file_writer_med.writeheader()
    file_writer_med.writerow(csv_heading1)
    file_writer_min = csv.DictWriter(min_csv_file, fieldnames=csv_heading)
    file_writer_min.writeheader()
    file_writer_min.writerow(csv_heading1)
    file_writer_max = csv.DictWriter(max_csv_file, fieldnames=csv_heading)
    file_writer_max.writeheader()
    file_writer_max.writerow(csv_heading1)
    
    avg_stats:dict = {}
    median_stats:dict = {}
    min_stats:dict = {}
    max_stats:dict = {}

    for prot_ in o_protocols:
        for bench_ in o_benchs:
            avg_stats[stats.KEY_PROTOCOL] = prot_
            avg_stats[stats.KEY_BENCH] = bench_
            median_stats[stats.KEY_PROTOCOL] = prot_
            median_stats[stats.KEY_BENCH] = bench_
            min_stats[stats.KEY_PROTOCOL] = prot_
            min_stats[stats.KEY_BENCH] = bench_
            max_stats[stats.KEY_PROTOCOL] = prot_
            max_stats[stats.KEY_BENCH] = bench_

            for key, val in stats.ALL_STATS_KEYS.items():
                di_known = {}
                di_known[stats.KEY_BENCH] = bench_
                di_known[stats.KEY_PROTOCOL] = prot_
                li_limit: list = utils.limit_to_dicts_with_dict(workingRS, di_known)
                # for avg
                stat_val: dict = utils.merge(li_limit, key)
                avg_stats[key] = stat_val.get(key)
                # for median
                stat_val_med: dict = utils.merge(li_limit, key, mergeType=utils.MergeType.MERGE_MED)
                median_stats[key] = stat_val_med.get(key)
                # for min
                stat_val_min: dict = utils.merge(li_limit, key, mergeType=utils.MergeType.MERGE_MIN)
                min_stats[key] = stat_val_min.get(key)
                # for max
                stat_val_max: dict = utils.merge(li_limit, key, mergeType=utils.MergeType.MERGE_MAX)
                max_stats[key] = stat_val_max.get(key)
            file_writer.writerow(avg_stats)
            file_writer_med.writerow(median_stats)
            file_writer_min.writerow(min_stats)
            file_writer_max.writerow(max_stats)
    avg_csv_file.close()
    median_csv_file.close()
    min_csv_file.close()
    max_csv_file.close()

    with open(os.path.join(options.getExpResultsDir(), "stats.html"), "w",
              encoding="utf-8") as html_file:
        html_file.write(html_str)


def limitSuccessfulExps(options, resSet: list, o_benchmarks: list, o_protocols: list) -> list:
    """ Sanity check the number of valid experiments. All benchmarks should ideally have the
     same count. Find out the minimum number of valid trials across all benchmarks, ignore
     benchmarks which have zero valid trials for some tool."""

    workingRS: list = resSet.copy()
    li_sanity: dict = {}  # For debugging
    min_trials: int = sys.maxsize
    oc_benchs = o_benchmarks.copy()

    for bench_ in oc_benchs:
        li_toolcount: List = []
        min_bench_trials: int = sys.maxsize
        for tool_ in o_protocols:
            di_limit: dict = {}
            di_limit[stats.KEY_BENCH] = bench_
            di_limit[stats.KEY_PROTOCOL] = tool_
            li_ans: list = utils.limit_to_dicts_with_dict(workingRS, di_limit)
            min_bench_trials = min(min_bench_trials, len(li_ans))
            li_toolcount.append({tool_: len(li_ans)})
        if min_bench_trials > 0:
            min_trials = min(min_trials, min_bench_trials)
            li_sanity[bench_] = li_toolcount
        else:
            # Remove benchmarks for which at least one tool has zero valid trials
            if options.verbose >= 1:
                print(f"Removing trials of {bench_} since at least one tool has zero successful "
                      "experiments!")
            oc_benchs.remove(bench_)

    # min_trials gives us the number of useful trials, benchmarks is the list of pruned
    # benchmarks which succeeded
    try:
        assert len(oc_benchs) * min_trials * len(o_protocols) <= len(workingRS)
    except AssertionError as e:
        print(f"Number of remaining benchmarks: {len(oc_benchs)} Min trials: {min_trials}"
              f" Number of tools: {len(o_protocols)} Length of working RS: {len(workingRS)}")
        utils.raise_error(repr(e), stack=True)

    successfulRS: List = []
    for tool_ in o_protocols:
        for bench_ in oc_benchs:
            di_limit: dict = {}
            di_limit[stats.KEY_BENCH] = bench_
            di_limit[stats.KEY_PROTOCOL] = tool_
            li_ans: list = utils.limit_to_dicts_with_dict(workingRS, di_limit)
            assert len(li_ans) >= min_trials
            for i in range(min_trials):
                successfulRS.append(li_ans[i])

    try:
        assert len(oc_benchs) * min_trials * len(o_protocols) == len(successfulRS)
    except AssertionError:
        utils.raise_error(
            f"AssertionError: Number of benchmarks: {len(oc_benchs)} Number of tools: "
            f"{len(o_protocols)} Number of trials: {min_trials} Number of valid experiments: "
            f"{len(successfulRS)}")

    return [successfulRS, oc_benchs, min_trials]


def generateOutput(options, resSet: list, o_benchmarks: list, o_protocols: list, min_trials: int):
    """Generate performance plots."""
    # Copy resultsSet so as to have a backup
    workingRS: list = resSet.copy()

    _generateAbsPlot(options, workingRS, o_benchmarks, o_protocols, min_trials)
    if len(o_protocols) > 1:
        _generateNormPlot(options, workingRS, o_benchmarks, o_protocols, min_trials)


def _generateAbsPlot(options, workingRS: list, benchmarks: List[str], protocols: List[str],
                     num_trials: int):
    ordered_prots = _getOrderedProtocols(protocols)

    di_baseline: dict = {}
    di_baseline[stats.KEY_PROTOCOL] = Constants.BASELINE_PROT_NAME
    cfgObj = options.getConfig()
    di_baseline[stats.KEY_PROTOCOL] = cfgObj.getBaselineProtocol()

    for key in stats.ALL_STATS_KEYS:
        li_y_labels = []
        li_abs_data = []
        for bench in benchmarks:
            li_bench = []
            for prot in ordered_prots:  # Order is important
                di_known = {}
                di_known[stats.KEY_BENCH] = bench
                di_known[stats.KEY_PROTOCOL] = prot
                li_limit = utils.limit_to_dicts_with_dict(workingRS, di_known)
                if options.pruneFailed:
                    assert len(li_limit) == num_trials
                di_key = utils.merge(li_limit, key)
                di_known = dict(di_known, **di_key)  # Union the two dictionaries
                li_bench.append(di_key.get(key))
                li_abs_data.append(di_known)
            li_y_labels.append(li_bench)

        try:
            assert len(benchmarks) * len(ordered_prots) == len(li_abs_data)
            assert len(benchmarks) == len(li_y_labels)
        except AssertionError:
            print(f"AssertionError: Number of benchmarks: {len(benchmarks)} Number of protocols: "
                  f"{len(ordered_prots)} Number of trials: {num_trials} Length after merging valid "
                  f"experiments: {len(li_abs_data)} Number of valid y labels: {len(li_y_labels)}")
            sys.exit()

        # Now plot the data in li_data

        x_labels = list(benchmarks)
        index = np.arange(len(x_labels))

        gap = 0.8 / len(ordered_prots)

        fig = plt.figure(figsize=(12, 5), dpi=120, facecolor='w', edgecolor='k')
        ax = fig.add_axes([0, 0, 1, 1])

        ax.set_xticks(index + (len(ordered_prots) / 2 * gap) - (gap / 2))
        ax.set_xticklabels(x_labels, rotation=90, fontsize=9)
        ax.set_ylabel(stats.ALL_STATS_KEYS.get(key), fontsize=12)

        flat_list = [item for sublist in li_y_labels for item in sublist]
        text_start = max(flat_list) / 100 if max(flat_list) > 1000 else 1

        mcolors = getColorsList()
        for i, row in enumerate(li_y_labels):
            X = np.arange(len(row))
            plt.bar(i + X * gap,
                    row,
                    width=gap,
                    color=mcolors[0:len(row) % len(mcolors)],
                    align="center")
            for x in row:
                plt.text(i + X[row.index(x)] * gap - 0.2 * gap,
                         text_start,
                         s='%.2f' % x,
                         rotation=90,
                         fontsize=8)

        ax.set_title(f"Absolute Plot for {key}")
        ax.autoscale(tight=True)
        ax.legend(ordered_prots)
        leg = ax.get_legend()
        # FalseSharing: the following code is used to set the color of the legend
        # vipin: resulting error therefore commenting for now
        # for x in range(len(ordered_prots)):
        # leg.legendHandles[x].set_color(mcolors[x])
        fig.savefig(f"Abs_{key}.pdf", bbox_inches='tight', format="pdf")
        plt.close()


def _generateNormPlot(options, workingRS, benchmarks, protocols, num_trials):
    normRS = workingRS.copy()  # Make a copy so that norm does not overwrite the original data
    ordered_prots = _getOrderedProtocols(protocols)
    # ordered_tools_names = _getOrderedProtocolNames(tools)

    di_baseline = {}
    cfgObj = options.getConfig()
    # _baseline_prot = Constants.BASELINE_PROT_NAME
    _baseline_prot = cfgObj.getBaselineProtocol()
    di_baseline[stats.KEY_PROTOCOL] = _baseline_prot

    for key in stats.ALL_STATS_KEYS:
        li_norm_data = []  # Contains normalized data for key
        li_y_data = []  # Contains the list of normalized values passed to matplotlib
        li_CI_data = []  # Contains the list of CI (confidence interval) for li_y_data

        # First average of trials for every (bench x tool) combination
        for bench in benchmarks:
            li_bench = []
            for prot in ordered_prots:  # Order is important
                di_known = {}
                di_known[stats.KEY_BENCH] = bench
                di_known[stats.KEY_PROTOCOL] = prot
                li_limit: list = utils.limit_to_dicts_with_dict(normRS, di_known)
                if options.pruneFailed:
                    assert len(li_limit) == num_trials
                di_key = utils.merge(li_limit, key)
                di_known = dict(di_known, **di_key)  # Union the two dictionaries
                di_known['CI'] = utils.merge(li_limit, key, utils.MergeType.MERGE_CI)
                li_bench.append(di_known)

            # Normalize data and add to y label data structure
            norm: float = utils.limit_to_dicts_with_dict(li_bench, di_baseline)[0].get(key)

            li_bench_y_data = []
            li_bench_CI_data = []
            for entry_ in li_bench:
                try:
                    entry_[key] = entry_[key] / norm
                    entry_["CI"] = entry_["CI"][key] / norm
                except ZeroDivisionError:
                    entry_[key] = 0
                    entry_["CI"] = 0
                li_bench_y_data.append(entry_[key])
                li_bench_CI_data.append(entry_["CI"])
            li_norm_data.extend(li_bench)
            li_y_data.append(li_bench_y_data)
            li_CI_data.append(li_bench_CI_data)
        try:
            assert len(benchmarks) * len(ordered_prots) == len(li_norm_data)
            assert len(benchmarks) == len(li_y_data)
        except AssertionError:
            print(f"AssertionError: Number of benchmarks: {len(benchmarks)} Number of tools: "
                  f"{len(ordered_prots)} Number of trials: {num_trials} Length after merging valid "
                  f"experiments: {len(li_norm_data)}")
            sys.exit()

        # Create geomean data
        li_geomean = []
        for prot_ in ordered_prots:
            di_known: dict = {}
            di_known[stats.KEY_PROTOCOL] = prot_
            li_limit: list = utils.limit_to_dicts_with_dict(li_norm_data, di_known)
            di_key = utils.merge(li_limit, key, utils.MergeType.MERGE_GEOMEAN)
            li_geomean.append(di_key.get(key))
        li_y_data.append(li_geomean)
        x_labels = list(benchmarks + ["geomean"])
        index = np.arange(len(x_labels))

        assert len(li_y_data[0]) == len(ordered_prots)
        gap = 0.8 / (len(ordered_prots) - 1)

        fig = plt.figure(figsize=(12, 3), dpi=120, facecolor='w', edgecolor='k')
        ax = fig.add_axes([0, 0, 1, 1])

        ax.set_xticks(index + ((len(ordered_prots) - 1) / 2 * gap) - (gap / 2))
        # FalseSharing: rotation old value 30, fontsize old value 12 
        ax.set_xticklabels(x_labels, rotation=90, fontsize=8)
        ax.set_ylabel(stats.ALL_STATS_KEYS.get(key), fontsize=10)

        mcolors = getColorsList()
        skip = False
        for i, row in enumerate(li_y_data):
            # FalseSharing: replaced by _baseline_prot
            if row[ordered_prots.index(_baseline_prot)] == 0:
                skip = True
                continue
            try:
                row = [x / row[ordered_prots.index(_baseline_prot)] for x in row]
            except ZeroDivisionError:
                utils.raise_error("ZeroDivisionError")
            row = row[1:]
            X = np.arange(len(row))
            # Following "If" condition is used to check if its geomean bars, do not plot confidence
            # interval for geomean.
            if (i == len(li_y_data) - 1):
                plt.bar(i + X * gap,
                        row,
                        width=gap,
                        color=mcolors[0:(len(row)) % len(mcolors)],
                        align="center")
            else:
                plt.bar(i + X * gap,
                        row,
                        width=gap,
                        color=mcolors[0:(len(row)) % len(mcolors)],
                        align="center",
                        capsize=5,
                        yerr=li_CI_data[i][1:])
            for x in row:
                plt.text(i + X[row.index(x)] * gap - 0.25 * gap,
                         1.2,
                         s='%.2f' % x,
                         rotation=90,
                         fontsize=8)

        if not skip:
            # ax.set_title(f"Normalized Plot for {INT_KEYS_Y_LABELS.get(key)}")
            # ax.autoscale(tight=True)
            ax.legend(ordered_prots[1:])
            leg = ax.get_legend()
            for x in range(len(ordered_prots) - 1):
                try:
                    leg.legend_handles[x].set_color(mcolors[x])
                except IndexError:
                    utils.raise_error("IndexError")
            plt.ylim(0, 13)
            fig.savefig(f"Norm_{key}.pdf", bbox_inches='tight', format="pdf")
            plt.close()

# FalseSharing: privatization stats for repair protocol
class PrvLenStat:
    _startTick:int=0
    # _prvLen:int=0
    
    def __init__(self, startTick: int, prvLen: int):
        self._startTick = startTick
        self._prvLen = prvLen
    
    def getStartTick(self):
        return self._startTick
    
    def getPrvLen(self):
        return self._prvLen
    pass

# FalseSharing: the stat designed for detect protocol, later can be extended to REPAIR protocol
class PrivatizationStats:
    """A class to store privatization stats."""
    _reportedTicks:List[int]=[]
    _count:int=0
    # _lenPrivatization:int=0
    def __init__(self, startTick: int):
        self._reportedTicks.append(startTick)
        self._count = 1

    def updateTickList(self, startTick:int):
        self._reportedTicks.append(startTick)

# read the output.txt file and format the privatization length stats
# to generate the report of privatization episodes.
def generatePrivatizationStats(op_path: str, op_file: str, options):#->Dict[str,Dict[str,List[PrivatizationStats]]]:
    """Generate privatization stats."""
    prvLenMap:Dict[str,Dict[str, List[PrivatizationStats]]]={}
    prvStatLog:str="DetectPrvStat.log"
    logPath:str=os.path.join(op_path, prvStatLog)
    
    with open(op_file, 'r') as file:
        for line in file:
            # check if line contains "identified for "
            if "participates in false sharing repair" in line \
                and re.search(r'0x[A-Fa-f0-9]+', line):
                splitStr = line.split(sep=' ')
                blockNum:str = splitStr[2]
                involvedInst:str = splitStr[6]
                startTick:int = int(splitStr[-1])
                if(blockNum not in prvLenMap.keys()):                                     
                        firstInst:PrivatizationStats = PrivatizationStats(startTick)
                        prvLenMap[blockNum] = {}
                        prvLenMap[blockNum][involvedInst] = []
                        prvLenMap[blockNum][involvedInst].append(firstInst)
                else: # block present, check if involvedInst is present
                    if involvedInst not in prvLenMap[blockNum].keys():
                        firstReport:PrivatizationStats = PrivatizationStats(startTick)
                        prvLenMap[blockNum][involvedInst]=[]
                        prvLenMap[blockNum][involvedInst].append(firstReport)
                    else: # block and involvedInst present, update the tick list
                        prvLenMap[blockNum][involvedInst].append(PrivatizationStats(startTick))
    with open(logPath, 'w') as file:
        for(key, value) in prvLenMap.items():
            file.write(f'{key} {len(value)} ')
            for instruction in value.keys():
                file.write(f'{instruction}:{len(value[instruction])} ')
            file.write('\n')
    # return prvLenMap

def generateRepairPrivatizationStats(op_path: str, op_file: str, options):
    """Generate privatization stats."""
    prvLenMap:Dict[str,Dict[str, List[PrivatizationStats]]]={}
    prvStatLog:str="RepairPrvStat.log"
    logPath:str=os.path.join(op_path, prvStatLog)
    print("op_path:", op_path)
    print("op_file:", op_file)
    with open(op_file, 'r') as file:
        for line in file:
            # check if line contains "identified for "
            if "participates in false sharing repair" in line \
                and re.search(r'0x[A-Fa-f0-9]+', line):
                splitStr = line.split(sep=' ')
                blockNum:str = splitStr[2]
                involvedInst:str = splitStr[6]
                startTick:int = int(splitStr[-1])
                if(blockNum not in prvLenMap.keys()):                                     
                        firstInst:PrivatizationStats = PrivatizationStats(startTick)
                        prvLenMap[blockNum] = {}
                        prvLenMap[blockNum][involvedInst] = []
                        prvLenMap[blockNum][involvedInst].append(firstInst)
                else: # block present, check if involvedInst is present
                    if involvedInst not in prvLenMap[blockNum].keys():
                        firstReport:PrivatizationStats = PrivatizationStats(startTick)
                        prvLenMap[blockNum][involvedInst]=[]
                        prvLenMap[blockNum][involvedInst].append(firstReport)
                    else: # block and involvedInst present, update the tick list
                        prvLenMap[blockNum][involvedInst].append(PrivatizationStats(startTick))
    pass
