import ast
import sys
import argparse

import utils
import benchmarks
from options import Options
from constants import Constants


def list_str(_str):
    return _str.split(',')


class CmdLineParser():
    """Helper class to parser command line arguments and perform limited sanity checks."""

    # helper class to enforce unique values with argparse
    # https://stackoverflow.com/questions/9376670/python-argparse-force-a-list-item-to-be-unique
    class __UniqueAppendAction(argparse.Action):

        def __call__(self, parser, namespace, values, option_string=None):
            unique_values = set(values)
            setattr(namespace, self.dest, unique_values)

    # SB: It is good to follow the order during building
    _allowedTasks = [
        "build_m5",
        "build_gem5",
        "build_bench",
        "run",
        "result",
        "email"  # Optional, send an email when the experiment is complete
    ]

    _allowedWorkloadSizes = ["test", "small", "medium", "large", "huge"]

    # FalseSharing:
    _allowedWorkloadTypes = ["parsec", "custom"]
    _allowedFSWorkloadSize = [
        "parsec: simsmall, simmedium, simlarge", "custom: mapping in image",
    ]

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog='false-sharing',
            description="Command line options for running false sharing experiments",
            conflict_handler="error",
            allow_abbrev=True)
        self._parser.add_argument("--tasks",
                                  "-t",
                                  help="Tasks to execute.",
                                  type=list_str,
                                  default=CmdLineParser._allowedTasks[0])

        # Only one protocol is allowed at a time because gem5 needs to be built with the
        # corresponding protocol
        self._parser.add_argument("--protocol",
                                  "-l",
                                  help="Protocol to execute.",
                                  type=list_str,
                                  default=Constants.DESIRED_PROTOCOL_ORDER[0])
        self._parser.add_argument("--trials",
                                  "-n",
                                  help="Number of trials, default is 1.",
                                  type=int,
                                  default=1)
        self._parser.add_argument("--outputDir",
                                  "-o",
                                  help="Output directory relative to EXP_OUTPUT_ROOT",
                                  default="temp")
        # 0: nothing, 1: important messages (e.g., errors, make output), 2: options/paths, 3:
        # everything
        self._parser.add_argument("--verbose",
                                  "-v",
                                  help="Verbosity level",
                                  default=1,
                                  type=int,
                                  choices=[0, 1, 2, 3])
        # vipin: a better approach for command line option of boolean type
        # https://stackoverflow.com/questions/50954491/python-argparse-how-to-pass-false-from-the-command-line
        self._parser.add_argument("--printOnly",
                                  "-p",
                                  help="Print the constructed commands, no execution",
                                  action='store_true')
        self._parser.add_argument("--bench", "-b", type=list_str, help="Benchmarks", default="none")
        self._parser.add_argument("--workloadSize",
                                  "-w",
                                  type=list_str,
                                  help="Size of the input to the application.",
                                  default=CmdLineParser._allowedWorkloadSizes[0])
        self._parser.add_argument("--result",
                                  "-r",
                                  help="Parse output and stats, and generate result",
                                  action='store_true')
        self._parser.add_argument("--pruneFailed",
                                  "-f",
                                  help="Remove benchmarks with all failed experiments for a tool",
                                  action='store_false')
        # default action for timeout is true, specify flag to disable timeout
        self._parser.add_argument(
            "--timeout",
            "-u",
            help="Use a timeout to kill long runs, specify option touse timeout",
            action='store_false')
        # default action for debug is false, specify flag to enable debugging
        self._parser.add_argument("--debug",
                                  "-d",
                                  help="Debug gem5, specify option to enable",
                                  action='store_true')
        # FalseSharing: support for FS mode
        self._parser.add_argument("--benchmark_type",
                                  "-bt",
                                  type=str,
                                  help="type to select the run script for FS mode",
                                  choices=CmdLineParser._allowedWorkloadTypes)
        self._parser.add_argument("--size",
                                  "-s",
                                  type=str,
                                  help="size for different benchmark suite applications",
                                  choices=CmdLineParser._allowedFSWorkloadSize[0])

    def parse(self, argv):
        # Parse options
        di_options = vars(self._parser.parse_args())

        # check whether to run all benchmark from a  group
        if (len(di_options["bench"]) == 1 and benchmarks.isBenchmarkGroup(di_options["bench"][0])):
            di_options["bench"] = benchmarks.returnAllBenchmarksFromGroup(di_options["bench"][0])

        options = Options(argv, di_options)

        # Sanity checks
        tasksList = options.getTasksList()
        for task in tasksList:
            if task not in CmdLineParser._allowedTasks:
                utils.raise_error(f"{task} is not a valid task!")

        if "result" not in tasksList:
            for bench in options.getBenchmarksList():
                if (not benchmarks.isFeatherBenchmark(bench) and
                        not benchmarks.isHuronBenchmark(bench) and
                        not benchmarks.isMicroBenchmark(bench) and
                        not benchmarks.isPARSECBenchmark(bench) and
                        not benchmarks.isSYNCHROBENCHBenchmark(bench)):
                    utils.raise_error(f"{bench} is not a valid benchmark!")

            prot: str = options.getProtocol()
            if prot not in Constants.DESIRED_PROTOCOL_ORDER:
                utils.raise_error(f"{options.getProtocol()} is not a valid protocol!")

        # If result is specified, it should be the only task
        if "result" in tasksList and len(tasksList) > 1:
            utils.raise_error("result task should be the only task!")

        # Only one protocol is allowed at a time, but we ignore the constraint if result task is
        # specified
        if "," in options.getProtocol():
            utils.raise_error("Note only one protocol is allowed at a time!")

        for ws in options.getWorkloadSizesList():
            if ws not in CmdLineParser._allowedWorkloadSizes:
                utils.raise_error(f"{ws} is not a valid workload size!")

        return options
