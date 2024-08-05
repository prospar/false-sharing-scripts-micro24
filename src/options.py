import os

from cfgparser import CFGParser
from constants import Constants


class Options(Constants):
    """This class encapsulates all the experimental properties."""

    def __init__(self, argv, di_options):
        self._tup_cmdLine = argv

        # Check for duplicates in bench
        self._li_benchmarks = list(set(di_options["bench"]))
        self._li_benchmarks.sort()

        self._li_tasks = list(di_options["tasks"])

        self._li_protocol: str = ''.join(di_options["protocol"])

        self._li_wlSizes = list(di_options["workloadSize"])
        self._li_wlSizes.sort()

        self._output: str = di_options["outputDir"]
        self.verbose: int = di_options["verbose"]
        self.numTrials: int = di_options["trials"]
        self.printOnly: bool = di_options["printOnly"]
        self.pruneFailed: bool = di_options["pruneFailed"]
        self.timeout: bool = di_options["timeout"]
        self.generateResults: bool = di_options["result"]
        self.debug: bool = di_options["debug"]
        self.benchmark_type = di_options["benchmark_type"]

        self._config = CFGParser(self)

        if self.verbose >= 2:
            self.printOptions()

    def getConfig(self):
        return self._config

    def getCmdListTuple(self) -> tuple:
        return self._tup_cmdLine

    def getExpCommand(self) -> str:
        """Return the EXP command line."""
        li_cmd = list(self.getCmdListTuple())
        li_cmd = li_cmd[1:]  # Leave out the script name
        str_cmdLine: str = (f"python3 {self.getFrameworkPath()}/{Options.RUN_SCRIPT_NAME} " +
                            " ".join(li_cmd))
        return str_cmdLine

    def getWorkloadSizesList(self) -> list:
        return self._li_wlSizes

    def getTasksList(self) -> list:
        return self._li_tasks

    def getProtocol(self) -> str:
        return self._li_protocol

    def getBenchmarksList(self) -> list:
        return self._li_benchmarks

    def getNumTrials(self) -> int:
        return self.numTrials

    def getExpOutputDir(self) -> str:
        return os.path.join(self._config.getExpOutputRoot(), self._output)

    def getExpResultsDir(self) -> str:
        return os.path.join(self._config.getExpResultsRoot(), self._output)

    def getVEnvDir(self) -> str:
        return os.path.abspath(self._config.getVEnv())

    def createRerunFile(self, op_dir_path: str):
        """Create a "rerun" command history file in op_dir_path."""
        with open(os.path.join(op_dir_path, "rerun"), "w", encoding="utf-8") as rerun:
            rerun.write(Options.BASH_SHEBANG + "\n\n")
            str_cmdLine: str = self.getExpCommand()
            rerun.write(str_cmdLine)
            rerun.close()

    def printOptions(self):
        print("Experiment options...\n"
              f"\tTasks: {self.getTasksList()}\n"
              f"\tProtocol: {self.getProtocol()}\n"
              f"\tBenchmark: {self.getBenchmarksList()}\n"
              f"\tWorkload sizes: {self.getWorkloadSizesList()}\n"
              f"\tOutput directory: {self.getExpOutputDir()}\n"
              f"\tTrials: {self.numTrials}\n"
              f"\tVerbosity: {self.verbose}\n"
              f"\tPrint-only: {self.printOnly}\n"
              f"\tGenerate results: {self.generateResults}\n"
              f"\tTimeout long runs: {self.timeout}"
              f"\tDebug gem5: {self.debug}")

    def isDebug(self):
        return self.debug
