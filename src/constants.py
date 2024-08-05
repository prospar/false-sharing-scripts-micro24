import os
import socket
from typing import List


class Constants():

    PRECISION_DIGITS: int = 3  # Number of digits after decimal
    PYTHON_EXEC: str = "python3"
    BASH_SHEBANG: str = "#!/bin/bash"
    RUN_SCRIPT_NAME: str = "src/main.py"

    OUTPUT_FILE_NAME: str = "output.txt"
    ERR_FILE_NAME: str = "error.txt"
    STATS_FILE_NAME: str = "stats.txt"
    BOOT_LOG_FILE_NAME: str = "system.pc.com_1.device"
    BASELINE_PROT_NAME: str = "MESI_Nonblocking"

    HAS_DISPLAY: bool = "DISPLAY" in os.environ
    if not HAS_DISPLAY:
        import matplotlib
        matplotlib.use("Agg")  # use a non-interactive backend

    HOSTNAME: str = socket.gethostname().split(".")[0].upper()

    # Allow MAX 2 days for a protocol
    TIMEOUT = (2 * 24 * 60 * 60)  # Kill experiment after these many seconds

    DESIRED_PROTOCOL_ORDER: List[str] = [
        "MESI_Two_Level", "MESI_Two_Level_Extended", "MESI_Nonblocking",
        "FS_MESI_DETECTION", "FS_MESI", "FS_MESI_Blocking",
        "FS_MESI_DETECTION_Blocking", "DETECT_MD", "MESI_Nonblocking_manual",
        "MESI_Nonblocking_40KB", "FS_MESI_DETECTION_gran2", "FS_MESI_DETECTION_gran4",
        "FS_MESI_DETECTION_gran8", "FS_MESI_gran2", "FS_MESI_gran4", "FS_MESI_gran8",
        "FS_MESI_256", "FS_MESI_DETECTION_256", "FS_MESI_Opt",
        "FS_MESI_32", "FS_MESI_64"
    ]

    @staticmethod
    def getFrameworkPath() -> str:
        _path: str = os.getenv("FS_FRAMEWORK")
        if _path is not None:
            return os.path.abspath(_path)
        return ""

    # FalseSharing: CONSTANTS for the energy calculations
    L1D_ENERGY_PER_READ = 3.83919  # in nJ
    L1D_ENERGY_PER_WRITE = 3.89143  # in nJ
    L1D_LEAKAGE_POWER = 223.004  # in mW
    # L1D_DATA AND TAG ARRAY
    # 1.23699nJ (data) , 0.0010053(tag) old value
    L1D_DATA_ARRAY_ENERGY_PER_ACCESS = 3.83774 # in nJ
    L1D_TAG_ARRAY_ENERGY_PER_ACCESS =  0.001453 # in nJ
    L1D_DATA_ARRAY_LEAKAGE_POWER = 220.986  # in mW
    L1D_TAG_ARRAY_LEAKAGE_POWER = 2.01732  # in mW

    LLC_ENERGY_PER_READ = 1.14093  #in nJ
    LLC_ENERGY_PER_WRITE = 1.15615  # in nJ
    LLC_LEAKAGE_POWER = 1250.99  # in mW
    # LLC DATA AND TAG ARRAY
    LLC_DATA_ARRAY_ENERGY_PER_ACCESS = 1.12974  # in nJ
    LLC_TAG_ARRAY_ENERGY_PER_ACCESS = 0.0111938  # in nJ
    LLC_DATA_ARRAY_LEAKAGE_POWER = 1158.27  # in mW
    LLC_TAG_ARRAY_LEAKAGE_POWER = 92.7189  # in mW

    PAM_ENERGY_PER_READ = 0.00421169  #in nJ
    PAM_ENERGY_PER_WRITE = 0.00271556  # in nJ
    PAM_LEAKAGE_POWER = 3.19931  # in mW

    # 0.32106 nJ per read energy if a single structure is used
    SAM_ENERGY_PER_READ =  0.0274765 #in nJ
    # 0.314917 nJ per write energy if a single structure is used
    SAM_ENERGY_PER_WRITE = 0.0284023# in nJ
    # 33.7605 mW leakage power if a single structure is used
    SAM_LEAKAGE_POWER = 15.1531 # in mW

    def calculateLLCEnergy():

        return Constants.LLC_ENERGY_PER_READ + Constants.LLC_ENERGY_PER_WRITE

    def calculateL1DEnergy():

        return Constants.L1D_ENERGY_PER_READ + Constants.L1D_ENERGY_PER_WRITE

    def calculatePAMEnergy():

        return Constants.PAM_ENERGY_PER_READ + Constants.PAM_ENERGY_PER_WRITE

    def calculateSAMEnergy():

        return Constants.SAM_ENERGY_PER_READ + Constants.SAM_ENERGY_PER_WRITE
