import os
import configparser
from typing import Tuple

import utils
from constants import Constants


class CFGParser(Constants):

    _CONFIG: str = "config.ini"
    _tup_sections: Tuple[str, str, str] = ("PROJECT", "USER", "FS", "DISK_PATH",
                                            "SCRIPT_PATH", "KERNEL_PATH")
    _tup_allowedProjKeys: Tuple[str, str, str,
                                str] = ("FS_PROJECT_ROOT", "FS_BENCH_ROOT", "FS_VENV",
                                        "EXP_OUTPUT_ROOT", "EXP_RESULTS_ROOT", "FS_RESRC_ROOT")
    _tup_allowedUserKeys: Tuple[str, str] = ("USER", "EMAIL")
    _tup_allowedFSKeys: Tuple[str, str] = ("L2_SIZE", "TRACKING_WIDTH", "INV_THRESHOLD",
                                           "FETCH_THRESHOLD", "GLOBAL_ACT_SIZE", "ASSOC_ACT",
                                           "SIZE_OWN", "RESET_TICK", "NUM_CPUS", "FREQ", "CPU_TYPE",
                                           "CACHELINE_SIZE", "PRIMARY_MEM", "L1D_ASSOC", "L1D_SIZE",
                                           "L1I_ASSOC", "L1I_SIZE", "L2_ASSOC", "OPT_READERS",
                                           "CPU_FREQ", "CLK_FREQ", "DRAM_TYPE", "REPORT_PC",
                                           "ALLOW_MULTI_REPORT", "DISABLE_MD_COMM_OPT",
                                           "SATURATION_THRESHOLD", "HYSTERESIS_THRESHOLD")
    _tup_allowedDiskKeys: Tuple[str, str, str, str, str] = ("CUSTOM", "PARSEC", "SPEC", "NPB",  "GAP")

    _CUSTOM_BM_SHORTHAND = [
        "hist", "hist_man", "linear_reg", "linear_reg_man", "ref_count", "ref_count_man",
        "str_match", "str_match_man", "boost", "boost_man", "test1", "test1_man", "test2",
        "test3_man", "test3", "test4", "test4_man", "test5", "test6", "test6_man", "test7",
        "test8", "test8_man", "test9", "test9_man", "test10", "spectree", "false_sharing",
        "no_fs", "true_sharing", "prop_fs", "prop_ts", "both_fs_ts", "both_ts_fs",
        "rep_fs_ts_diff", "rep_ts_fs_same", "fs_ts_diff", "fs_ts_same", "false_sharing_char",
        "false_sharing_short", "false_sharing_long"
    ]

    _PARSEC_BM_SHORTHAND = [
        "blackscholes", "bodytrack", "canneal","facesim", "fluidanimate", "swaptions",
        "streamcluster", "streammanual"
    ]

    _BENCHMARK_SHORT_MAP = {
        "false-sharing": "false_sharing",
        "false-sharing-char": "false_sharing_char",
        "false-sharing-short": "false_sharing_short",
        "false-sharing-long": "false_sharing_long",
        "no-false-sharing": "no_fs",
        "true-sharing": "true_sharing",
        "both-false-and-true-sharing": "both_fs_ts",
        "both-true-and-false-sharing": "both_ts_fs",
        "proportional-ts": "prop_ts",
        "proportional-fs": "prop_fs",
        "repetitive-fs-ts-diffline": "rep_fs_ts_diff",
        "repetitive-fs-ts-sameline": "rep_fs_ts_same",
        "fs-ts-diffline": "fs_ts_diff",
        "fs-ts-sameline": "fs_ts_same",
        "huron_compile": "huron_compile",
        "huron-linear-reg": "linear_reg",
        "huron-linear-reg-manual": "linear_reg_man",
        "huron_lr": "huron_lr",
        "huron_lr_man": "huron_lr_man",
        "huron_lr_base": "huron_lr_base",
        "huron-ref-count": "ref_count",
        "huron-ref-count-manual": "ref_count_man",
        "huron_rc":"huron_rc",
        "huron_rc_man":"huron_rc_man",
        "huron_rc_base":"huron_rc_base",
        "huron-string-match": "str_match",
        "huron-string-match-manual": "str_match_man",
        "huron_sm": "huron_sm",
        "huron_sm_man": "huron_sm_man",
        "huron_sm_base": "huron_sm_base",
        "huron-boost-spinlock": "boost",
        "huron-boost-spinlock-manual": "boost_man",
        "huron_bs": "huron_bs",
        "huron_bs_man": "huron_bs_man",
        "huron_bs_base": "huron_bs_base",
        "huron-lockless-toy": "lockless_toy",
        "huron-lockless-toy-manual": "lockless_toy_man",
        "huron_ll": "huron_ll",
        "huron_ll_man": "huron_ll_man",
        "huron_ll_base": "huron_ll_base",
        "huron-locked-toy": "locked_toy",
        "huron-locked-toy-manual": "locked_toy_man",
        "huron_lt": "huron_lt",
        "huron_lt_man": "huron_lt_man",
        "huron_lt_base": "huron_lt_base",
        "ESTM-specfriendly-tree": "spectree",
        "ESTM-specfriendly-tree-man": "spectree_man",
        "feather-test1-small": "test1",
        "feather-test1-small-manual": "test1_man",
        "feather-test2-small": "test2",
        "feather-test3-small": "test3",
        "feather-test3-small-manual": "test3_man",
        "feather-test4-small": "test4",
        "feather-test4-small-manual": "test4_man",
        "feather-test5-small": "test5",
        "feather-test6-small": "test6",
        "feather-test6-small-manual": "test6_man",
        "feather-test7-small": "test7",
        "feather-test8-small": "test8",
        "feather-test8-small-manual": "test8_man",
        "feather-test9-small": "test9",
        "feather-test9-small-manual": "test9_man",
        "feather-test10-small": "test10",
        "blackscholes": "blackscholes",
        "bodytrack": "bodytrack",
        "canneal": "canneal",
        "facesim": "facesim",
        "fluidanimate": "fluidanimate",
        "swaptions": "swaptions",
        "streamcluster": "streamcluster",
        "streammanual": "streammanual",
    }

    def __init__(self, options):
        self._config = configparser.ConfigParser()
        config_path: str = options.getFrameworkPath() + os.sep + CFGParser._CONFIG
        if options.verbose > 2:
            print(f"Config file path: {config_path}")
        if not os.path.exists(config_path):
            utils.raise_error(f"{CFGParser._CONFIG} file missing in {config_path} directory.")
        self._config.read(config_path)
        self.sanityCheck()

    def sanityCheck(self):
        '''Check for missing sections.'''
        sections = self._config.sections()
        if len(sections) != len(CFGParser._tup_sections):
            utils.raise_error(f"{CFGParser._CONFIG} file contains incorrect number of sections!")

        for _section in sections:
            # if _section not in CFGParser._tup_sections:
            #     utils.raise_error(CFGParser._CONFIG, " file contains wrong section.")
            if _section == "PROJECT":
                for _key in self._config[_section]:
                    if _key.upper() not in CFGParser._tup_allowedProjKeys:
                        utils.raise_error(f"Invalid key {_key} in PROJECT section in CONFIG file!")
            elif _section == "USER":
                for _key in self._config[_section]:
                    if _key.upper() not in CFGParser._tup_allowedUserKeys:
                        utils.raise_error(f"Invalid key {_key} in USER section in CONFIG file!")
            elif _section == "FS":
                for _key in self._config[_section]:
                    if _key.upper() not in CFGParser._tup_allowedFSKeys:
                        utils.raise_error(f"Invalid key {_key} in FS section in CONFIG file!")
            elif _section == "DISK_PATH" or _section == "SCRIPT_PATH":
                for _key in self._config[_section]:
                    if _key.upper() not in  CFGParser._tup_allowedDiskKeys:
                        utils.raise_error(f"Invalid key {_key} in {_section} section in CONFIG file!")
            # elif _section == "KERNEL_PATH":
            #     for _key not in self._config[_section]:
            #         if _key.upper() in  CFGParser._tup_allowedDiskKeys:
            #             utils.raise_error(f"Invalid key {_key} in {_section} section in CONFIG file!")

    def getUser(self) -> str:
        return self._config["USER"]["USER"]

    def getEmail(self) -> str:
        return self._config["USER"]["EMAIL"]

    def getProjectRoot(self) -> str:
        return self._config["PROJECT"]["FS_PROJECT_ROOT"]

    def getBenchRoot(self) -> str:
        return self._config["PROJECT"]["FS_BENCH_ROOT"]

    def getExpOutputRoot(self) -> str:
        op_dir = self._config["PROJECT"]["EXP_OUTPUT_ROOT"]
        utils.check_and_create_dir(op_dir)
        return op_dir

    def getExpResultsRoot(self) -> str:
        op_dir = self._config["PROJECT"]["EXP_RESULTS_ROOT"]
        utils.check_and_create_dir(op_dir)
        return op_dir

    def getVEnv(self) -> str:
        venv_dir = self._config["PROJECT"]["FS_VENV"]
        if not os.path.exists(venv_dir):
            utils.raise_error(f"{venv_dir} does not exist!")
        return venv_dir

    def getL2Size(self) -> str:
        return self._config["FS"]["L2_SIZE"]

    def getTrackingWidth(self) -> int:
        return int(self._config["FS"]["TRACKING_WIDTH"])

    def getInvThreshold(self) -> int:
        return int(self._config["FS"]["INV_THRESHOLD"])

    def getFetchThreshold(self) -> int:
        return int(self._config["FS"]["FETCH_THRESHOLD"])

    def getGlobalActSize(self) -> int:
        return int(self._config["FS"]["GLOBAL_ACT_SIZE"])

    def getAssocACT(self) -> int:
        return int(self._config["FS"]["ASSOC_ACT"])

    def getOwnSize(self) -> int:
        return int(self._config["FS"]["SIZE_OWN"])

    def getResetTick(self) -> int:
        return self._config["FS"]["RESET_TICK"]

    def getNumCPUs(self) -> int:
        return self._config["FS"]["NUM_CPUS"]

    def getFreq(self) -> str:
        return self._config["FS"]["FREQ"]

    def getCPUType(self) -> str:
        return self._config["FS"]["CPU_TYPE"]

    def getCacheLineSize(self) -> int:
        return self._config["FS"]["CACHELINE_SIZE"]

    def getPrimaryMemSize(self) -> str:
        return self._config["FS"]["PRIMARY_MEM"]

    def getL1DAssoc(self) -> int:
        return self._config["FS"]["L1D_ASSOC"]

    def getL1DSize(self) -> str:
        return self._config["FS"]["L1D_SIZE"]

    def getL1IAssoc(self) -> int:
        return self._config["FS"]["L1I_ASSOC"]

    def getL1ISize(self) -> str:
        return self._config["FS"]["L1I_SIZE"]

    def getL2Assoc(self) -> int:
        return self._config["FS"]["L2_ASSOC"]

    def getOptReader(self) -> str:
        return self._config["FS"]["OPT_READERS"]

    def getReportPC(self) -> str:
        return self._config["FS"]["REPORT_PC"]

    def getCpuFreq(self) -> str:
        return self._config["FS"]["CPU_FREQ"]

    def getClkFreq(self) -> str:
        return self._config["FS"]["CLK_FREQ"]

    def getDRAMType(self) -> str:
        return self._config["FS"]["DRAM_TYPE"]

    # FalseSharing: return the parent directory with all config and resource file
    def getRsrcRoot(self) -> str:
        return self._config["PROJECT"]["FS_RESRC_ROOT"]

    def returnDiskPath(self, bench_type: str) -> str:
        disk_bench: str = self._config["DISK_PATH"][bench_type.upper()]
        return disk_bench

    def returnScriptPath(self, bench_type: str) -> str:
        script_path: str = self._config["SCRIPT_PATH"][bench_type.upper()]
        return script_path

    def getSaturationThreshold(self) -> int:
        return int(self._config["FS"]["SATURATION_THRESHOLD"])

    def getHysteresisThreshold(self) -> int:
        return int(self._config["FS"]["HYSTERESIS_THRESHOLD"])

    @staticmethod
    def isValidShortHand(bench_sh) -> bool:
        if (bench_sh in _CUSTOM_BM_SHORTHAND or 
                bench_sh in _PARSEC_BENCHMARKS ):
            return True
        return False

    def getBenchMarkShortHand(self, bench) -> str:
        # if CFGParser.isValidShortHand(bench):
        return CFGParser._BENCHMARK_SHORT_MAP[bench]
        # print ("Invalid benchmark name")
        # return ""
    
    def getDisableReportOnce(self) -> str:
        return self._config["FS"]["ALLOW_MULTI_REPORT"]
    
    def getDisableMDCommOpt(self) -> str:
        return self._config["FS"]["DISABLE_MD_COMM_OPT"]
    
    def returnLinuxKernelPath(self) -> str:
        return self._config["KERNEL_PATH"]["KERNEL"]
