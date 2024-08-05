"""This module controls running all the tasks specified in the experiment."""

import os
import sys
import time
import signal
import subprocess
from typing import List

import utils
import result
import benchmarks
from constants import Constants


def runAllTasks(options):
    """Run all the tasks.  The order is pre-determined and important."""
    tasksList = options.getTasksList()

    # Setup root experimental output directory
    op_dir_root: str = options.getExpOutputDir()
    utils.check_and_create_dir(op_dir_root)
    options.createRerunFile(op_dir_root)

    if "build_bench" in tasksList:
        BuildBenchTask().build(options)

    if "build_gem5" in tasksList:
        BuildGem5Task().build(options)

    if "run" in tasksList:
        # RunTask().run(options)
        RunTask().run_fullsystem(options)

    if "result" in tasksList:
        ResultTask().result(options)

    if "email" in tasksList:
        EmailTask().email(options)

    if "build_m5" in tasksList:
        BuildM5Task().build(options)


def _isTerminated(pid: subprocess.Popen) -> bool:
    if pid.poll() is None:
        return False
    return True


def _areTerminated(pids: List[subprocess.Popen]) -> bool:
    for pid in pids:
        if pid.poll() is None:
            return False
    return True


class BaseTask(Constants):

    def __init__(self, tname: str):
        self._name = tname

    def _outputPrefix(self) -> str:
        return "[" + self._name + "]"

    def _printTaskInfoStart(self, options):
        if options.verbose >= 1:
            print(f"{self._outputPrefix()} Executing {self._name} task...")

    def _printTaskInfoEnd(self, options):
        if options.verbose >= 1:
            print(f"{self._outputPrefix()} Done executing {self._name} task...")


class BuildBenchTask(BaseTask):
    _TIMEOUT = 5

    def __init__(self):
        super().__init__("build_bench")

    def build(self, options):
        """Build all benchmarks provided in the command line."""
        self._printTaskInfoStart(options)
        try:
            cwd = os.getcwd()
            os.chdir(options.getConfig().getBenchRoot())

            cmdLine = f"mkdir -p build; cd build; rm -rf *; cmake .. -D GEM5_PATH={options.getConfig().getProjectRoot()}; cmake --build .;"
            if options.printOnly or options.verbose > 1:
                print(f"Build bench: {cmdLine}")

            if not options.printOnly:
                pid: subprocess.Popen = subprocess.Popen(["/bin/bash", "-c", cmdLine])
                while not _isTerminated(pid):
                    time.sleep(BuildBenchTask._TIMEOUT)
        finally:
            self._printTaskInfoEnd(options)
            os.chdir(cwd)


class BuildGem5Task(BaseTask):
    _TIMEOUT = 10

    def __init__(self):
        super().__init__("build_gem5")

    def build(self, options):
        self._printTaskInfoStart(options)
        prot: str = options.getProtocol()
        cfg = options.getConfig()
        try:
            cwd = os.getcwd()
            os.chdir(options.getConfig().getProjectRoot())

            # The Venv and the gem5 command should run in the same shell.
            # Enable the VENV
            cmdLine = f"source {options.getVEnvDir()}/bin/activate; "
            cmdLine += (
                f"scons build/X86_{prot}/gem5.opt -j{int(cfg.getNumCPUs()) + 1} --default=X86 PROTOCOL={prot} "
                "SLICC_HTML=False")

            if options.printOnly or options.verbose > 2:
                print(f"Build gem5 command line: {cmdLine}")
            if not options.printOnly:
                pid: subprocess.Popen = subprocess.Popen(["/bin/bash", "-c", cmdLine])
                while not _isTerminated(pid):
                    time.sleep(BuildGem5Task._TIMEOUT)
        finally:
            self._printTaskInfoEnd(options)
            os.chdir(cwd)


class RunTask(BaseTask):

    _TIMEOUT = 10

    def __init__(self):
        super().__init__("run_fullsystem")

    def _getBenchOptions(self, bench: str, ws: str, options) -> str:
        if ws == "test":
            return benchmarks.TEST_OPTIONS.get(bench)
        elif ws == "small":
            return benchmarks.SMALL_OPTIONS.get(bench)
        elif ws == "medium":
            return benchmarks.MEDIUM_OPTIONS.get(bench)
        elif ws == "large":
            return benchmarks.LARGE_OPTIONS.get(bench)
        elif ws == "huge":
            return benchmarks.HUGE_OPTIONS.get(bench)

    # https://stackoverflow.com/questions/15535240/how-to-write-to-stdout-and-to-log-file-simultaneously-with-popen/15535389#15535389
    # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true

    def run_fullsystem(self, options):
        self._printTaskInfoStart(options)
        cfg = options.getConfig()
        try:
            cwd = os.getcwd()
            # need to fix path based on each benchmarks image
            benchmark_type = options.benchmark_type
            resource_root: str = cfg.getRsrcRoot()
            linux_ker_path:str= cfg.returnLinuxKernelPath()
            kernel_path: str = f"{resource_root}/{linux_ker_path}"
            path_disk: str = cfg.returnDiskPath(benchmark_type)
            disk_path: str = f"{resource_root}/{path_disk}"
            bench_root: str = cfg.getBenchRoot()
            config_script: str = f"{cfg.returnScriptPath(benchmark_type)}"

            os.chdir(bench_root)

            prot: str = options.getProtocol()
            wsSizes: List[str] = options.getWorkloadSizesList()

            gem5_path: str = cfg.getProjectRoot()
            cmd_prefix: str = (f"{gem5_path}/build/X86_{prot}/gem5.opt ")

            # change the config path based on benchmarks
            cmd_suffix: str = (f"{resource_root}/{config_script} --ruby "
                               f"--cpu_type={cfg.getCPUType()} "
                               f"--num_cpus={cfg.getNumCPUs()} "
                               f"--cacheline_size={cfg.getCacheLineSize()} "
                               f"--l1d_assoc={cfg.getL1DAssoc()} "
                               f"--l1d_size={cfg.getL1DSize()} "
                               f"--l1i_assoc={cfg.getL1IAssoc()} "
                               f"--l1i_size={cfg.getL1ISize()} "
                               f"--l2_assoc={cfg.getL2Assoc()} "
                               f"--l2_size={cfg.getL2Size()} "
                               f"--tracking_width={cfg.getTrackingWidth()} "
                               f"--inv_threshold={cfg.getInvThreshold()} "
                               f"--fetch_threshold={cfg.getFetchThreshold()} "
                               f"--global_act_size={cfg.getGlobalActSize()} "
                               f"--size_own={cfg.getOwnSize()} "
                               f"--kernel={kernel_path} "
                               f"--disk={disk_path} "
                               f"--mem_sys={prot} "
                               f"--cpu_freq={cfg.getCpuFreq()} "
                               f"--clk_freq={cfg.getClkFreq()} "
                               f"--dram_type={cfg.getDRAMType()} "
                               f"--saturation_threshold={cfg.getSaturationThreshold()} "
                               f"{cfg.getOptReader()} "
                               f"{cfg.getReportPC()} "
                               f"{cfg.getDisableReportOnce()} "
                               f"{cfg.getDisableMDCommOpt()} ")
            # FalseSharing: Added for reader optimization
            for ws in wsSizes:
                for trial in range(1, options.getNumTrials() + 1):
                    for bench in options.getBenchmarksList():
                        curr_exp_path = f"{options.getExpOutputDir()}/{prot}/{ws}/{trial}/{bench}/"
                        if options.verbose > 2:
                            print(f"Create experiment directory: {curr_exp_path}")
                        utils.check_and_create_dir(curr_exp_path)

                        # Form command line
                        cmdLine = cmd_prefix
                        cmdLine += f"--outdir={curr_exp_path} "
                        cmdLine += cmd_suffix
                        cmdLine += f" --size=\"{self._getBenchOptions(bench, ws, options)}\" "
                        cmdLine += f" --benchmark=\"{cfg.getBenchMarkShortHand(bench)}\" "
                        if options.printOnly or options.verbose > 2:
                            print(f"Run command: {cmdLine}")

                        if not options.printOnly:
                            OUTFILE: str = os.path.join(curr_exp_path, RunTask.OUTPUT_FILE_NAME)
                            ERRFILE: str = os.path.join(curr_exp_path, RunTask.ERR_FILE_NAME)

                            with open(OUTFILE, "w") as outfile, open(ERRFILE, "w") as errfile:
                                pid: subprocess.Popen = subprocess.Popen(
                                    ["/bin/bash", "-c", cmdLine],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    preexec_fn=os.setsid,
                                    universal_newlines=True)
                                if options.timeout:
                                    try:
                                        outs, errs = pid.communicate(timeout=RunTask.TIMEOUT)
                                    except subprocess.TimeoutExpired:
                                        # Does not work, possibly because of the launched shell
                                        # pid.kill()
                                        os.killpg(os.getpgid(pid.pid), signal.SIGTERM)
                                        outs, errs = pid.communicate()
                                else:
                                    outs, errs = pid.communicate()
                                if outs is not None:
                                    for line in outs:
                                        sys.stdout.write(line)
                                        outfile.write(line)
                                if errs is not None:
                                    for line in errs:
                                        sys.stderr.write(line)
                                        errfile.write(line)
                                # SB: There is a timeout option for wait(). Is
                                # that simpler than what we have implemented?
                                pid.wait()
                            while not _isTerminated(pid):
                                time.sleep(RunTask._TIMEOUT)
                        else:
                            print(f"Run command: {cmdLine}")
        finally:
            self._printTaskInfoEnd(options)
            os.chdir(cwd)


class ResultTask(BaseTask):

    def __init__(self):
        super().__init__("result")

    def result(self, options):
        self._printTaskInfoStart(options)
        try:
            cwd = os.getcwd()
            if options.printOnly:
                print("Print-only option is set. Maybe turn it off?")
            else:
                utils.check_and_create_dir(options.getExpResultsDir())
                [resultSet, o_benchmarks, o_protocols] = result.collectResults(options)
                validResSet: list = resultSet
                oc_benchs: list = o_benchmarks
                min_trials: int = 0
                if options.pruneFailed:
                    # The following method call removes benchmarks for which there is no successful
                    # trial of a tool
                    [validResSet, oc_benchs,
                     min_trials] = result.limitSuccessfulExps(options, resultSet, o_benchmarks,
                                                              o_protocols)
                os.chdir(options.getExpResultsDir())
                options.createRerunFile(options.getExpResultsDir())
                result.generateStats(options, validResSet, oc_benchs, o_protocols)
                result.generateOutput(options, validResSet, oc_benchs, o_protocols, min_trials)
        finally:
            self._printTaskInfoEnd(options)
            os.chdir(cwd)


class EmailTask(BaseTask):
    """Send an email notification to the user once an experiment is complete."""

    def __init__(self):
        super().__init__("email")

    def email(self, options):
        self._printTaskInfoStart(options)
        self._printTaskInfoEnd(options)
        super().__init__("email")

    def email(self, options):
        self._printTaskInfoStart(options)
        self._printTaskInfoEnd(options)
        self._printTaskInfoEnd(options)


class BuildM5Task(BaseTask):

    _TIMEOUT = 5

    def __init__(self):
        super().__init__("build_m5")

    def build(self, options):
        """Build m5 library for gem5 stats reset."""
        self._printTaskInfoStart(options)
        cfg = options.getConfig()
        try:
            cwd = os.getcwd()
            os.chdir(f"{cfg.getProjectRoot()}/util/m5")

            cmdLine = "scons build/x86/out/m5"
            if options.printOnly or options.verbose > 1:
                print(f"Build m5: {cmdLine}")

            if not options.printOnly:
                pid: subprocess.Popen = subprocess.Popen(["/bin/bash", "-c", cmdLine])
                while not _isTerminated(pid):
                    time.sleep(BuildM5Task._TIMEOUT)
        finally:
            self._printTaskInfoEnd(options)
            os.chdir(cwd)
