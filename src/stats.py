import os
import xml.etree.ElementTree as ET

import utils
from constants import Constants
from benchmarks import isSYNCHROBENCHBenchmark

GEM5_TOTAL_STATS = {
    "KEY_SIM_TICKS": "sim_ticks",
    "KEY_SIM_TIME": "sim_seconds",
    "KEY_NET_BYTE_CONTROL": "system.caches.network.msg_byte.Control",
    "KEY_NET_BYTE_REQ_CONTROL": "system.caches.network.msg_byte.Request_Control",
    "KEY_NET_BYTE_RSP_CONTROL": "system.caches.network.msg_byte.Response_Control",
    "KEY_NET_BYTE_RSP_DATA": "system.caches.network.msg_byte.Response_Data",
    "KEY_NET_BYTE_WB_CONTROL": "system.caches.network.msg_byte.Writeback_Control",
    "KEY_NET_BYTE_WB_DATA": "system.caches.network.msg_byte.Writeback_Data",
    "KEY_NET_BYTE_METADATA": "system.caches.network.msg_byte.Metadata",
    "KEY_NET_COUNT_CONTROL": "system.caches.network.msg_count.Control",
    "KEY_NET_COUNT_REQ_CONTROL": "system.caches.network.msg_count.Request_Control",
    "KEY_NET_COUNT_RSP_CONTROL": "system.caches.network.msg_count.Response_Control",
    "KEY_NET_COUNT_RSP_DATA": "system.caches.network.msg_count.Response_Data",
    "KEY_NET_COUNT_WB_CONTROL": "system.caches.network.msg_count.Writeback_Control",
    "KEY_NET_COUNT_WB_DATA": "system.caches.network.msg_count.Writeback_Data",
    "KEY_NET_COUNT_METADATA": "system.caches.network.msg_count.Metadata",

    # energy stats
    "KEY_SYS_TOTAL_ENERGY": "system.energy_total",  # total energy of the system
    "KEY_TOTAL_PAM_ENERGY": "system.caches.PAM.energy",  # PAM energy, dummy entries later populated
    "KEY_TOTAL_SAM_ENERGY": "system.caches.SAM.energy",  # SAM energy, dummy entries later populated
    "KEY_TOTAL_L1D_ENERGY": "system.caches.L1D.energy",  # L1D energy, dummy entries later populated
    "KEY_TOTAL_LLC_ENERGY": "system.caches.LLC.energy",  # LLC energy, dummy entries later populated
    # FalseSharig: new stats after 23 Nov 2023
    "KEY_CPU_TO_L1_ENERGY": "system.caches.cpu_lid_energy", # dummy entry
    "KEY_FILL_COHERENCE_ENERGY": "system.caches.fill_coherence_energy", # dummy entry
    "KEY_TOTAL_STATIC_LEAKAGE":"system.caches.total_static_leakage", # dummy entry
    "KEY_LLC_STATIC_LEAKAGE":"system.caches.LLC.static_leakage", # dummy entry
    "KEY_LLC_DYNAMIC_ENERGY":"system.caches.LLC.dynamic_energy", # dummy entry
    # TODO: SB: Do we have L1i cache stats? Should we include instruction cache for energy computation?

    # stats added for energy calculation
    "KEY_L1_CACHE_TOTAL_READ": "system.caches.L1Cache_Controller.Load::total",  # L1DCache read
    "KEY_L1_CACHE_TOTAL_WRITE": "system.caches.L1Cache_Controller.Store::total",  # L1DCache write
    "KEY_L1_CACHE_DATA":
    "system.caches.L1Cache_Controller.Data::total",  # L1 Cache data/tag array write
    "KEY_L1_CACHE_DATA_FROM_L1":
    "system.caches.L1Cache_Controller.DataS_fromL1::total",  # L1 Cache data/tag array write
    "KEY_L1_CACHE_DATA_EXCLUSIVE": "system.caches.L1Cache_Controller.Data_Exclusive::total",
    "KEY_L1_CACHE_DATA_ALL_ACKS": "system.caches.L1Cache_Controller.Data_all_Acks::total",
    "KEY_L1_CACHE_DATA_ALL_ACKS_UNBLOCK":
    "system.caches.L1Cache_Controller.Data_all_Acks_Unblock::total",
    "KEY_L1_CACHE_DATA_ALL_ACKS_RMW": "system.caches.L1Cache_Controller.Data_all_Acks_RMW::total",
    "KEY_L1_CACHE_DATA_ALL_ACKS_UNBLOCK_RMW":
    "system.caches.L1Cache_Controller.Data_all_Acks_Unblock_RMW::total",
    "KEY_L1_CACHE_ACK": "system.caches.L1Cache_Controller.Ack::total",  # L1 Cache ack
    "KEY_L1_CACHE_ACK_ALL": "system.caches.L1Cache_Controller.Ack_all::total",  # L1 Cache ACK ALL
    "KEY_L1_CACHE_ACK_ALL_RMW":
    "system.caches.L1Cache_Controller.Ack_all_RMW::total",  # L1 Cache ACK ALL RMW
    "KEY_L1_CACHE_FWD_GETS":
    "system.caches.L1Cache_Controller.Fwd_GETS::total",  # L1 Cache FWD GETS
    "KEY_L1_CACHE_FWD_GETX":
    "system.caches.L1Cache_Controller.Fwd_GETX::total",  # L1 Cache FWD GETX
    "KEY_L1_CACHE_INV": "system.caches.L1Cache_Controller.Inv::total",  # L1 Cache INV
    "KEY_L1_CACHE_REPLACEMENT":
    "system.caches.L1Cache_Controller.L1_Replacement::total",  # L1 Cache INV
    "KEY_L1_CACHE_WB_ACK":
    "system.caches.L1Cache_Controller.WB_Ack::total",  # L1 Cache writeback ack
    "KEY_L1_CACHE_RMW_RD_STORE":
    "system.caches.L1Cache_Controller.RMW_Read_STORE::total",  # L1 Cache RMW read store
    "KEY_L1_CACHE_RMW_WR_STORE":
    "system.caches.L1Cache_Controller.RMW_Write_STORE::total",  # L1 Cache RMW write store ack
    "KEY_L1_CACHE_PEN_S":
    "system.caches.L1Cache_Controller.Pen_GetS::total",  # L1 Cache pending load
    "KEY_L1_CACHE_PEN_X":
    "system.caches.L1Cache_Controller.Pen_GetX::total",  # L1 Cache pending store

    # Addtional updates for repair protocol
    "KEY_L1_CACHE_CH_PRV_LD":
    "system.caches.L1Cache_Controller.CH_PRV_LD::total",  # L1 Cache PRV load check
    "KEY_L1_CACHE_CH_PRV_ST":
    "system.caches.L1Cache_Controller.CH_PRV_ST::total",  # L1 Cache PRV store check
    "KEY_L1_CACHE_NC_PRV":
    "system.caches.L1Cache_Controller.NC_PRV::total",  # L1 Cache No conflict ack
    "KEY_L1_CACHE_TR_PRV":
    "system.caches.L1Cache_Controller.TR_PRV::total",  # L1 Cache trigger privatization
    "KEY_L1_CACHE_ACK_EMD": "system.caches.L1Cache_Controller.Ack_EMD::total",  # L1 Cache ack emd
    "KEY_L1_CACHE_INV_PRV": "system.caches.L1Cache_Controller.Inv_PRV::total",  # L1 Cache INV
    "KEY_L1_CACHE_REPLACEMENT_S":
    "system.caches.L1Cache_Controller.L1_Replacement_S::total",  # L1 Cache INV
    #TODO: Add the stats for tag read for MD comm
    "KEY_L1_REPLACEMENT_S_STATE": "system.caches.L1Cache_Controller.S.L1_Replacement::total",
    "KEY_L1_REPLACEMENT_E_STATE": "system.caches.L1Cache_Controller.E.L1_Replacement::total",
    "KEY_L1_REPLACEMENT_M_STATE": "system.caches.L1Cache_Controller.M.L1_Replacement::total",
    "KEY_L1_INV_S_STATE": "system.caches.L1Cache_Controller.S.Inv::total",
    "KEY_L1_INV_E_STATE": "system.caches.L1Cache_Controller.E.Inv::total",
    "KEY_L1_INV_M_STATE": "system.caches.L1Cache_Controller.M.Inv::total",
    "KEY_L1_INV_SM_STATE": "system.caches.L1Cache_Controller.SM.Inv::total",
    "KEY_L1_FWDX_E_STATE": "system.caches.L1Cache_Controller.E.Fwd_GETX::total",
    "KEY_L1_FWDS_E_STATE": "system.caches.L1Cache_Controller.E.Fwd_GETS::total",
    "KEY_L1_FWDX_M_STATE": "system.caches.L1Cache_Controller.M.Fwd_GETX::total",
    "KEY_L1_FWDS_M_STATE": "system.caches.L1Cache_Controller.M.Fwd_GETS::total",
    "KEY_L1_CACHE_WR_ST_X": "system.caches.L1Cache_Controller.Write_Store_PenX::total",
    "KEY_L1_CACHE_WR_ST_S": "system.caches.L1Cache_Controller.Write_Store_PenS::total",

    # TODO: SB: Are the following for the repair protocol or detection?
    "KEY_L2_CACHE_MEM_DATA": "system.caches.L2Cache_Controller.Mem_Data::total",  # LLC write
    "KEY_L2_CACHE_MEM_Ack": "system.caches.L2Cache_Controller.Mem_Ack::total", # LLC write
    "KEY_L2_CACHE_WB_DATA":
        "system.caches.L2Cache_Controller.WB_Data::total",  # LLC tag and data array read/write
    "KEY_L2_CACHE_L1_PUTX": "system.caches.L2Cache_Controller.L1_PUTX::total",  # LLC writeback
    "KEY_L2_CACHE_L1_GETX": "system.caches.L2Cache_Controller.L1_GETX::total",  # LLC write
    "KEY_L2_CACHE_L1_GETS": "system.caches.L2Cache_Controller.L1_GETS::total",  # LLC read
    "KEY_L2_CACHE_L1_UPGRADE": "system.caches.L2Cache_Controller.L1_UPGRADE::total",  # LLC upgrade
    "KEY_L2_CACHE_WB_CLEAN": "system.caches.L2Cache_Controller.WB_Data_Clean::total",  # LLC write
    "KEY_L2_CACHE_ACK": "system.caches.L2Cache_Controller.Ack::total",  # LLC ACK
    "KEY_L2_CACHE_ACK_ALL": "system.caches.L2Cache_Controller.Ack_all::total",  # LLC ACK ALL
    "KEY_L2_CACHE_UNBLOCK": "system.caches.L2Cache_Controller.Unblock::total",
    "KEY_L2_CACHE_EXCLUSIVE_UNBLOCK": "system.caches.L2Cache_Controller.Exclusive_Unblock::total",
    "KEY_L2_CACHE_REPLACEMENT": "system.caches.L2Cache_Controller.L2_Replacement::total",
    "KEY_L2_CACHE_REPLACEMENT_CLEAN": "system.caches.L2Cache_Controller.L2_Replacement_clean::total",

    # Additional event for repair protocol at LLC
    "KEY_L2_CACHE_LAST_WB": "system.caches.L2Cache_Controller.Last_WB::total",
    "KEY_L2_CACHE_LAST_WB_R": "system.caches.L2Cache_Controller.Last_WB_R::total",
    "KEY_L2_CACHE_LAST_WB_NR": "system.caches.L2Cache_Controller.Last_WB_NR::total",
    "KEY_L2_CACHE_LAST_WB_EX": "system.caches.L2Cache_Controller.Last_WB_EX::total",
    "KEY_L2_CACHE_LAST_PUTX": "system.caches.L2Cache_Controller.Last_PUTX::total",
    "KEY_L2_CACHE_WB_DATA_S": "system.caches.L2Cache_Controller.WB_DATA_S::total",
    "KEY_L2_CACHE_WB_DATA_M": "system.caches.L2Cache_Controller.WB_DATA_M::total",
    "KEY_L2_CACHE_PRV_WB": "system.caches.L2Cache_Controller.PRV_WB::total",
    "KEY_L2_CACHE_PRV_WB_DATA": "system.caches.L2Cache_Controller.PRV_WB_DATA::total",
    "KEY_L2_CACHE_GA_ACK": "system.caches.L2Cache_Controller.GA_ACK::total",
    "KEY_L2_CACHE_UP_ALL": "system.caches.L2Cache_Controller.UP_All::total",
    "KEY_L2_CACHE_UP_DMD": "system.caches.L2Cache_Controller.UP_DMD::total",
    "KEY_L2_CACHE_UP_EDS": "system.caches.L2Cache_Controller.UP_EDS::total",
    "KEY_L2_CACHE_UP_MD": "system.caches.L2Cache_Controller.UP_MD::total",
    "KEY_L2_CACHE_TR_PRV": "system.caches.L2Cache_Controller.TR_PRV::total",
    "KEY_L2_CACHE_TE_PRV": "system.caches.L2Cache_Controller.TE_PRV::total",
    "KEY_L2_CACHE_TE_CNFT_S": "system.caches.L2Cache_Controller.TE_CNFT_S::total",
    # new stats
    "KEY_TOTAL_MSG_VOL": "system.network.total_msg_vol",
    "KEY_TOTAL_MSG_COUNT": "system.network.total_msg_count"
}

GEM5_PER_CORE_STATS = {
    "KEY_RUBY_L1D_DEMAND_HITS": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_hits"
    },
    "KEY_RUBY_L1D_DEMAND_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_misses"
    },
    "KEY_RUBY_L1D_DEMAND_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_accesses"
    },
    "KEY_RUBY_L1I_DEMAND_HITS": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Icache.demand_hits"
    },
    "KEY_RUBY_L1I_DEMAND_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Icache.demand_misses"
    },
    "KEY_RUBY_L1I_DEMAND_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Icache.demand_accesses"
    },
    "KEY_RUBY_L1D_PAM_READ": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_read_pm"
    },
    "KEY_RUBY_L1D_PAM_WRITE": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_write_pm"
    },
    "KEY_RUBY_PRV_READ": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_prv_read"
    },
    "KEY_RUBY_PRV_WRITE": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_prv_write"
    },
    "KEY_RUBY_PAM_EVC_M": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.evc_owner"
    },
    "KEY_RUBY_PAM_EVC_S": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.evc_shared"
    },
    "KEY_RUBY_PRV_RPLC": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.prv_line_replacement"
    },
    "KEY_MD_CONTROL_MD_MSG": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.control_metadata_msg",
    },
    "KEY_MD_MD_MSG": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.metadata_msg"
    },
    "KEY_MD_EVIC_MD_MSG": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.eviction_metadata_msg"
    },
    "KEY_MD_TOTAL_MD_MSG": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.total_metadata_msg"
    },
    "KEY_SAM_ENTRY_EVIC": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.sam_eviction"
    },
    "KEY_LINE_PRIVATIZE": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.prv_line"
    },
    "KEY_SUCC_PRV_LINE": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.succ_prv_line"
    },
    "KEY_TERM_IMM": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.immediate_termination"
    },
    "KEY_TERM_CNFT": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.term_cnft"
    },
    "KEY_TERM_DIR_EV": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.term_dir_ev"
    },
    "KEY_TERM_SAM_EV": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.term_sam_ev"
    },
    "KEY_TOTAL_TERM": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.total_term"
    },
    "KEY_SAM_LD": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.total_sam_read"
    },  # SAM read
    "KEY_SAM_ST": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.total_sam_write"
    },  # SAM write
    "KEY_EVC_PRV_LINE": {
        "prefix": "system.caches.controllers",
        "suffix": "FSGlobalACTData.evc_prv_line"
    },
    "KEY_PRV_TS_BIT":{
        "prefix":"system.caches.controllers",
        "suffix":"FSGlobalACTData.prv_ts_bit"
    },
    "KEY_PRV_HYS_CNT":{
        "prefix":"system.caches.controllers",
        "suffix":"FSGlobalACTData.prv_hys_cnt"
    },
    "KEY_L2_DEMAND_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L2cache.demand_accesses"
    },
    "KEY_L2_DEMAND_HITS": {
        "prefix": "system.caches.controllers",
        "suffix": "L2cache.demand_hits"
    },
    "KEY_L2_DEMAND_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L2cache.demand_misses"
    },
    "KEY_COMMITTED_INSTS": {
        "prefix": "system.timingCpu",
        "suffix": "committedInsts"
    },
    "KEY_FALSE_SHARING_ACC": {
        "prefix": "system.caches.controllers",
        "suffix": "total_false_sharing_accesses"
    }
}

GEM5_PC_STATS_SUM = {
    "KEY_COMMITTED_INSTS": "system.timingcpu.committedInsts",
    "KEY_FALSE_SHARING_ACC": "system.caches.false_sharing_accesses",
    "KEY_RUBY_L1D_DEMAND_HITS": "system.caches.controllers.L1Dcache.demand_hits",
    "KEY_RUBY_L1D_DEMAND_MISSES": "system.caches.controllers.L1Dcache.demand_misses",
    "KEY_RUBY_L1D_DEMAND_ACCESSES": "system.caches.controllers.L1Dcache.demand_accesses",
    "KEY_RUBY_L1I_DEMAND_HITS": "system.caches.controllers.L1Icache.demand_hits",
    "KEY_RUBY_L1I_DEMAND_MISSES": "system.caches.controllers.L1Icache.demand_misses",
    "KEY_RUBY_L1I_DEMAND_ACCESSES": "system.caches.controllers.L1Icache.demand_accesses",
    "KEY_L2_DEMAND_ACCESSES": "system.caches.controllers.L2cache.demand_accesses",
    "KEY_L2_DEMAND_HITS": "system.caches.controllers.L2cache.demand_hits",
    "KEY_L2_DEMAND_MISSES": "system.caches.controllers.L2cache.demand_misses",
    "KEY_RUBY_L1D_PAM_WRITE": "system.caches.controllers.OptionalOwnAccessMetadata.total_write_pm",
    "KEY_RUBY_L1D_PAM_READ": "system.caches.controllers.OptionalOwnAccessMetadata.total_read_pm",
    "KEY_RUBY_PRV_WRITE": "system.caches.controllers.OptionalOwnAccessMetadata.total_prv_write",
    "KEY_RUBY_PRV_READ": "system.caches.controllers.OptionalOwnAccessMetadata.total_prv_read",
    "KEY_RUBY_PAM_EVC_M": "system.caches.controllers.OptionalOwnAccessMetadata.evc_owner",
    "KEY_RUBY_PAM_EVC_S": "system.caches.controllers.OptionalOwnAccessMetadata.evc_shared",
    "KEY_RUBY_PRV_RPLC": "system.caches.controllers.OptionalOwnAccessMetadata.prv_line_replacement",
    "KEY_MD_CONTROL_MD_MSG": "system.caches.controllers.FSGlobalACTData.control_metadata_msg",
    "KEY_MD_MD_MSG": "system.caches.controllers.FSGlobalACTData.metadata_msg",
    "KEY_MD_EVIC_MD_MSG": "system.caches.controllers.FSGlobalACTData.eviction_metadata_msg",
    "KEY_MD_TOTAL_MD_MSG": "system.caches.controllers.FSGlobalACTData.total_metadata_msg",
    "KEY_SAM_ENTRY_EVIC": "system.caches.controllers.FSGlobalACTData.sam_eviction",
    "KEY_LINE_PRIVATIZE": "system.caches.controllers.FSGlobalACTData.prv_line",
    "KEY_SUCC_PRV_LINE": "system.caches.controllers.FSGlobalACTData.succ_prv_line",
    "KEY_TERM_IMM": "system.caches.controllers.FSGlobalACTData.immediate_termination",
    "KEY_TERM_CNFT": "system.caches.controllers.FSGlobalACTData.term_cnft",
    "KEY_TERM_DIR_EV": "system.caches.controllers.FSGlobalACTData.term_dir_ev",
    "KEY_TERM_SAM_EV": "system.caches.controllers.FSGlobalACTData.term_sam_ev",
    "KEY_TOTAL_TERM": "system.caches.controllers.FSGlobalACTData.total_term",
    "KEY_SAM_LD": "system.caches.controllers.FSGlobalACTData.total_sam_read",
    "KEY_SAM_ST": "system.caches.controllers.FSGlobalACTData.total_sam_write",
    "KEY_EVC_PRV_LINE": "system.caches.controllers.FSGlobalACTData.eviction_prv_line",
    "KEY_PRV_TS_BIT": "system.caches.controllers.FSGlobalACTData.prv_ts_bit",
    "KEY_PRV_HYS_CNT": "system.caches.controllers.FSGlobalACTData.prv_hys_cnt"
}

# Union of all keys
ALL_STATS_KEYS = {**GEM5_TOTAL_STATS, **GEM5_PC_STATS_SUM}

KEY_PROTOCOL = "protocol"
KEY_WS = "workloadsize"
KEY_TRIAL = "trial"
KEY_BENCH = "bench"


def parseOneExperiment(root: str, path: str, options) -> dict:
    """Parse one output file."""
    di_stats = {}

    # exp_log contains the log for each experiment
    exp_log = os.path.join(root, Constants.BOOT_LOG_FILE_NAME)
    exp_ops = root.replace(options.getExpOutputDir(), "")
    parts = exp_ops.split(os.sep)
    parts = list(filter(None, parts))
    assert len(parts) == 4

    di_stats[KEY_PROTOCOL] = parts[0]
    di_stats[KEY_WS] = parts[1]
    di_stats[KEY_TRIAL] = int(parts[2])
    di_stats[KEY_BENCH] = parts[3]

    valid = False
    pc_stats = {}
    total_msg_bytes = 0
    total_msg_count = 0
    with open(path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            line = line.strip()

            for skey, sval in GEM5_TOTAL_STATS.items():
                if sval in line:
                    assert line.startswith(sval)
                    suffix = line.replace(sval, "").strip()  # Creates a copy of the string
                    stat_val = suffix[:suffix.find("#")].strip()  # Check and remove comment
                    if '#' not in line:  # few stats do not contain '#' comment
                        str_part = line.split()
                        stat_val = str_part[1]
                    di_stats[skey] = float(stat_val)
                    # TODO: update sim to throughput for synchrobench applications
                    if isSYNCHROBENCHBenchmark(di_stats[KEY_BENCH]):
                        if skey == "KEY_SIM_TICKS":
                            di_stats[skey] = updateSimTickByTxsPerSec(exp_log)

                    if 'network.msg_byte' in sval:
                        total_msg_bytes += int(stat_val)
                    elif 'network.msg_count' in sval:
                        total_msg_count += int(stat_val)

            for skey, sval in GEM5_PER_CORE_STATS.items():
                if sval["prefix"] in line and sval["suffix"] in line:
                    if '#' not in line:
                        # TODO: SB: You can do "assert False"
                        hashCommentNotPresent = False
                        assert (hashCommentNotPresent)
                    suffix = line[line.find(sval["suffix"]) + len(sval["suffix"]):].strip()
                    if suffix is not None:
                        stat_val = suffix[:suffix.find("#")].strip()
                        # skey = sval["prefix"] + "." + sval["suffix"]
                        pc_stats[skey] = pc_stats.get(skey, 0) + float(stat_val)

            if "---------- End Simulation Statistics   ----------" in line:
                valid = True
            di_stats["valid"] = valid

    # SB: This is not important, but iterating is faster using keys() method. List comprehension is
    # Pythonic but may be difficult to comprehend.
    for skey, sval in GEM5_TOTAL_STATS.items():
        if skey not in di_stats:
            di_stats[skey] = 0

    # FalseSharing: initialize the unpopulated stats to 0 for compatability
    for skkey, skval in GEM5_PER_CORE_STATS.items():
        if skkey not in pc_stats:
            pc_stats[skkey] = 0

    # added the total count for N/W traffic as key
    di_stats["KEY_TOTAL_MSG_VOL"] = total_msg_bytes
    di_stats["KEY_TOTAL_MSG_COUNT"] = total_msg_count

    # the assertion fails for baseline MESI as it does not contain stats for
    # PAM and SAM table.
    # TODO: SB: You can enable the assert conditionally based on the protocol
    '''
    try:
        assert len(GEM5_TOTAL_STATS) == (len(di_stats) - 7)
    except AssertionError:
        utils.raise_error(f"AssertionError: {path} \n#GEM5_TOTAL_STATS: {len(GEM5_TOTAL_STATS)} "
                          f"{len(di_stats)} \n{di_stats}")

    try:
        assert len(GEM5_PER_CORE_STATS) == len(pc_stats)
    except AssertionError:
        utils.raise_error(f"AssertionError: {path} \n#GEM5_PER_CORE_STATS: "
                          f"{len(GEM5_PER_CORE_STATS)} \n{pc_stats}")
    '''

    # FalseSharing: Energy calculations for L1D cache
    # All load/store hit will access the tag to find the block,
    # the operation will access the data array
    l1d_data_array_read = di_stats["KEY_L1_CACHE_FWD_GETS"] + di_stats["KEY_L1_CACHE_TOTAL_READ"] +\
        di_stats["KEY_L1_CACHE_REPLACEMENT"] + di_stats["KEY_L1_CACHE_FWD_GETX"]

    # RMW_Read_Store and RMW_Write_Store will access the data array twice
    l1d_data_array_write = di_stats["KEY_L1_CACHE_DATA_FROM_L1"] + di_stats["KEY_L1_CACHE_DATA"] +\
            di_stats["KEY_L1_CACHE_TOTAL_WRITE"] + di_stats["KEY_L1_CACHE_DATA_EXCLUSIVE"] +\
            di_stats["KEY_L1_CACHE_DATA_ALL_ACKS"] + di_stats["KEY_L1_CACHE_DATA_ALL_ACKS_UNBLOCK"] +\
            di_stats["KEY_L1_CACHE_DATA_ALL_ACKS_UNBLOCK_RMW"] + di_stats["KEY_L1_CACHE_DATA_ALL_ACKS_RMW"] +\
            di_stats["KEY_L1_CACHE_DATA_EXCLUSIVE"] + di_stats["KEY_L1_CACHE_PEN_S"] +\
            di_stats["KEY_L1_CACHE_PEN_X"]+ di_stats["KEY_L1_CACHE_ACK_ALL"]

    # According to discussion on 27-Nov-2023: energy further classified as
    # cpu-2-l1d and fill+ coherence energy
    cpu2l1d_access_energy = ((2*di_stats["KEY_L1_CACHE_TOTAL_WRITE"] + di_stats["KEY_L1_CACHE_TOTAL_READ"])\
                * Constants.L1D_DATA_ARRAY_ENERGY_PER_ACCESS)/1000000

    l1d_tag_array_read = l1d_data_array_read + di_stats["KEY_L1_CACHE_WB_ACK"] +\
        di_stats["KEY_L1_CACHE_ACK"] +\
        di_stats["KEY_L1_CACHE_REPLACEMENT_S"]

    l1d_tag_array_write = l1d_data_array_write + di_stats["KEY_L1_CACHE_INV"]

    pam_array_read = 0.0
    pam_array_write = 0.0
    # Compute additional writes and read for detection protocol
    # FSDetect will read tag array while sending the metadata
    if (di_stats[KEY_PROTOCOL] == "FS_MESI_DETECTION"):
        l1d_tag_array_read = l1d_tag_array_read + di_stats["KEY_L1_REPLACEMENT_S_STATE"] +\
        di_stats["KEY_L1_REPLACEMENT_E_STATE"] + di_stats["KEY_L1_REPLACEMENT_M_STATE"] +\
        di_stats["KEY_L1_INV_S_STATE"] + di_stats["KEY_L1_INV_E_STATE"] +\
        di_stats["KEY_L1_INV_M_STATE"] + di_stats["KEY_L1_INV_SM_STATE"] +\
        di_stats["KEY_L1_FWDX_E_STATE"] + di_stats["KEY_L1_FWDS_E_STATE"] +\
        di_stats["KEY_L1_FWDX_M_STATE"] + di_stats["KEY_L1_FWDS_M_STATE"] +\
        di_stats["KEY_L1_CACHE_WR_ST_X"] + di_stats["KEY_L1_CACHE_WR_ST_S"]
    elif (di_stats[KEY_PROTOCOL] == "FS_MESI"):
        l1d_tag_array_read = l1d_tag_array_read + di_stats["KEY_L1_REPLACEMENT_S_STATE"] +\
        di_stats["KEY_L1_REPLACEMENT_E_STATE"] + di_stats["KEY_L1_REPLACEMENT_M_STATE"] +\
        di_stats["KEY_L1_INV_S_STATE"] + di_stats["KEY_L1_INV_E_STATE"] +\
        di_stats["KEY_L1_INV_M_STATE"] + di_stats["KEY_L1_INV_SM_STATE"] +\
        di_stats["KEY_L1_FWDX_E_STATE"] + di_stats["KEY_L1_FWDS_E_STATE"] +\
        di_stats["KEY_L1_FWDX_M_STATE"] + di_stats["KEY_L1_FWDS_M_STATE"] +\
        di_stats["KEY_L1_CACHE_WR_ST_X"] + di_stats["KEY_L1_CACHE_WR_ST_S"]

    pam_array_read = pam_array_read + 0.0
    pam_array_write = pam_array_write + 0.0

    # new computation for L1D energy according  to 23 Nov discussion
    # in nJ, converted to mJ by dividing by 10^6
    l1d_dyn_energy = ((Constants.L1D_DATA_ARRAY_ENERGY_PER_ACCESS*(l1d_data_array_read +\
                2*l1d_data_array_write)) + (Constants.L1D_TAG_ARRAY_ENERGY_PER_ACCESS*(l1d_tag_array_read+\
                2*l1d_tag_array_write)))/1000000 
    # in mJ
    l1d_static_leakage = ((di_stats["KEY_SIM_TICKS"])*\
                (Constants.L1D_DATA_ARRAY_LEAKAGE_POWER +Constants.L1D_TAG_ARRAY_LEAKAGE_POWER))

    l1d_total_energy = l1d_dyn_energy + l1d_static_leakage

    # incorrect multiplying twice data array energy
    # di_stats["KEY_CPU_TO_L1_ENERGY"] = cpu2l1d_access_energy*Constants.L1D_DATA_ARRAY_ENERGY_PER_ACCESS
    di_stats["KEY_CPU_TO_L1_ENERGY"] = cpu2l1d_access_energy

    # FalseSharing: stats for L1D energy
    di_stats["KEY_TOTAL_L1D_ENERGY"] = l1d_total_energy

    llc_total_write = di_stats["KEY_L2_CACHE_WB_DATA"] + di_stats["KEY_L2_CACHE_MEM_DATA"]+\
                di_stats["KEY_L2_CACHE_L1_PUTX"]

    if (di_stats[KEY_PROTOCOL] == "FS_MESI"):
        repair_protocol_writes = di_stats["KEY_L2_CACHE_LAST_WB"] +\
         di_stats["KEY_L2_CACHE_LAST_WB_R"] + di_stats["KEY_L2_CACHE_LAST_WB_NR"] +\
         di_stats["KEY_L2_CACHE_LAST_WB_EX"] + di_stats["KEY_L2_CACHE_LAST_PUTX"] +\
         di_stats["KEY_L2_CACHE_WB_DATA_S"] + di_stats["KEY_L2_CACHE_WB_DATA_M"] +\
         di_stats["KEY_L2_CACHE_PRV_WB"] + di_stats["KEY_L2_CACHE_PRV_WB_DATA"]
        llc_total_write = llc_total_write + repair_protocol_writes

    # GETS, GETX, PUTX, replacement req will update data array
    llc_data_array_read = di_stats["KEY_L2_CACHE_L1_GETS"] + di_stats["KEY_L2_CACHE_L1_GETX"] +\
            di_stats["KEY_L2_CACHE_REPLACEMENT"]

    llc_data_array_write = di_stats["KEY_L2_CACHE_WB_DATA"] + di_stats["KEY_L2_CACHE_MEM_DATA"] +\
        di_stats["KEY_L2_CACHE_L1_PUTX"]

    # access updating tag array
    llc_tag_array_read = llc_data_array_read + di_stats["KEY_L2_CACHE_ACK"] + di_stats["KEY_L2_CACHE_ACK_ALL"] +\
        di_stats["KEY_L2_CACHE_EXCLUSIVE_UNBLOCK"] + di_stats["KEY_L2_CACHE_UNBLOCK"] + di_stats["KEY_L2_CACHE_WB_CLEAN"]

    llc_tag_array_write = llc_data_array_read + llc_data_array_write
    # original formula for energy calculation: read_energy*(num_read+num_write) + write_energy*num_write
    llc_tag_energy = (Constants.LLC_TAG_ARRAY_ENERGY_PER_ACCESS *
                      (2 * llc_tag_array_write + llc_tag_array_read))
    llc_data_energy = (Constants.LLC_DATA_ARRAY_ENERGY_PER_ACCESS *
                       (2 * llc_data_array_write + llc_data_array_read))

    llc_dyn_energy = (llc_data_energy + llc_tag_energy)/1000000
    llc_static_leakage = (Constants.LLC_LEAKAGE_POWER * (di_stats["KEY_SIM_TICKS"]))
    llc_total_energy = llc_dyn_energy + llc_static_leakage
    di_stats["KEY_LLC_STATIC_LEAKAGE"] = llc_static_leakage
    di_stats["KEY_LLC_DYNAMIC_ENERGY"] = llc_dyn_energy
    di_stats["KEY_TOTAL_LLC_ENERGY"] = llc_total_energy

    di_stats["KEY_FILL_COHERENCE_ENERGY"] = (l1d_dyn_energy + llc_total_energy)- di_stats["KEY_CPU_TO_L1_ENERGY"] 
    # FalseSharing: leakgae in mW energy= mW*s->mJ 
    di_stats["KEY_TOTAL_STATIC_LEAKAGE"] = l1d_static_leakage + llc_static_leakage

    if ("FS_MESI" in di_stats[KEY_PROTOCOL]):

        di_stats["KEY_TOTAL_PAM_ENERGY"] = (Constants.PAM_ENERGY_PER_READ*(pc_stats["KEY_RUBY_L1D_PAM_READ"] +pc_stats["KEY_RUBY_L1D_PAM_WRITE"])\
                        + Constants.PAM_ENERGY_PER_WRITE * pc_stats["KEY_RUBY_L1D_PAM_WRITE"] +\
                        + (Constants.PAM_LEAKAGE_POWER * (di_stats["KEY_SIM_TICKS"])*1000000))/1000000
        # write of SAM structure also counted reads of SAM
        di_stats["KEY_TOTAL_SAM_ENERGY"] = (Constants.SAM_ENERGY_PER_READ*(pc_stats["KEY_SAM_LD"] + pc_stats["KEY_SAM_ST"])\
                    + Constants.SAM_ENERGY_PER_WRITE * pc_stats["KEY_SAM_ST"] +\
                    + (Constants.SAM_LEAKAGE_POWER * (di_stats["KEY_SIM_TICKS"])*1000000))/1000000
    else:
        di_stats["KEY_TOTAL_PAM_ENERGY"] = 0.0
        di_stats["KEY_TOTAL_SAM_ENERGY"] = 0.0
    di_stats = {**di_stats, **pc_stats}
    return di_stats

"""Update the simulation time by transactions per second."""
def updateSimTickByTxsPerSec(exp_log: str)-> float:
    with open(exp_log, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            line = line.strip()
            if "#txs" in line:
                parts = line.split()
                return (1/float(parts[3][1:]))


'''
# unused now but can be helpful for future work
############################
# STATS for energy numbers #
############################
int_inst = ["No_OpClass", "IntAlu", "IntMult", "IntDiv", "IprAccess"]
float_inst = [
    "Float", "FloatMult", "FloatDiv", "FloatMultAcc", "FloatCmp", "FloatCvt", "FloatSqrt",
    "FloatMisc"
]
load_inst = ["MemRead", "InstPrefetch", "FloatMemRead"]
store_inst = ["MemWrite", "FloatMemWrite"]

GEM5_ENERGY_STATS = {
    "KEY_CPU_TOTAL_CYCLES": {
        "prefix": "system.cpu",
        "suffix": "numCycles"
    },
    "KEY_CPU_IDLE_CYCLES": {
        "prefix": "system.cpu",
        "suffix": "idleCycles"
    },
    "KEY_CORE_TOTAL_INSTRUCTIONS": {
        "prefix": "system.cpu",
        "suffix": "iq.iqInstsIssued"
    },  # total_instructions
    "KEY_CORE_FU_INSTRUCTIONS": {
        "prefix": "system.cpu",
        "suffix": "iq.FU_type_0"
    },  #all_instructions_types
    # "KEY_CORE_FP_INSTRUCTIONS" :{
    #     "prefix": "system.cpu",
    #     "suffix": "FloatAdd FloatCmp FloatCvt FloatMult FloatDiv FloatSqrt"
    # },#fp_instructions
    "KEY_CORE_BRANCH_INSTRUCTIONS": {
        "prefix": "system.timingCpu",
        "suffix": "branchPred.condPredicted"
    },  #branch_instructions
    "KEY_CORE_BRANCH_MISPREDICTIONS": {
        "prefix": "system.timingCpu",
        "suffix": "branchPred.condIncorrect"
    },  #branch_mispredictions
    "KEY_CORE_BTB_READ_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "branchPred.lookups"
    },  # branchPred.lookups
    "KEY_CORE_BTB_WRITES_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "commit.branches"
    },  # commit_branches
    "KEY_CORE_COMMITTED_INSTRUCTIONS": {
        "prefix": "system.timingCpu",
        "suffix": "commit.committedInsts"
    },  #committed_instructions
    "KEY_CORE_COMMITTED_INT_INSTRUCTIONS": {
        "prefix": "system.timingCpu",
        "suffix": "commit.int_insts"
    },  #committed_int_instructions
    "KEY_CORE_COMMITTED_FP_INSTRUCTIONS": {
        "prefix": "system.timingCpu",
        "suffix": "commit.fp_insts"
    },  #committed_fp_instructions
    "KEY_CORE_ROB_READS": {
        "prefix": "system.timingCpu",
        "suffix": "rob.rob_reads"
    },  #ROB_reads
    "KEY_CORE_ROB_WRITES": {
        "prefix": "system.timingCpu",
        "suffix": "rob.rob_writes"
    },  #ROB_writes
    "KEY_CORE_RENAME_READS": {
        "prefix": "system.timingCpu",
        "suffix": "rename.int_rename_lookups"
    },  #rename_reads
    "KEY_CORE_FP_RENAME_READS": {
        "prefix": "system.timingCpu",
        "suffix": "rename.fp_rename_lookups"
    },  #fp_rename_reads,
    "KEY_CORE_RENAME_LOOKUPS": {
        "prefix": "system.timingCpu",
        "suffix": "rename.RenameLookups"
    },  #rename_lokups
    "KEY_CORE_RENAME_OPERANDS": {
        "prefix": "system.timingCpu",
        "suffix": "rename.RenamedOperands"
    },  #fp_rename_writes
    "KEY_CORE_INST_WINDOW_READS": {
        "prefix": "system.timingCpu",
        "suffix": "iq.int_inst_queue_reads"
    },  #inst_window_reads
    "KEY_CORE_INST_WINDOW_WRITES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.int_inst_queue_writes"
    },  #inst_window_writes
    "KEY_CORE_INST_WAKEUP_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.int_inst_queue_wakeup_accesses"
    },  #inst_window_wakeup_accesses
    "KEY_CORE_FP_INST_WINDOW_READS": {
        "prefix": "system.timingCpu",
        "suffix": "iq.fp_inst_queue_reads"
    },  #fp_inst_window_reads
    "KEY_CORE_FP_INST_WINDOW_WRITES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.fp_inst_queue_writes"
    },  #fp_inst_window_writes
    "KEY_CORE_FP_INST_WAKEUP_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.fp_inst_queue_wakeup_accesses"
    },  #fp_inst_window_wakeup_accesses
    "KEY_CORE_INT_REGFILE_READS": {
        "prefix": "system.timingCpu",
        "suffix": "int_regfile_reads"
    },  #int_regfile_reads
    "KEY_CORE_INT_REGFILE_WRITES": {
        "prefix": "system.timingCpu",
        "suffix": "int_regfile_writes"
    },  #_regfile_writes
    "KEY_CORE_FLOAT_REGFILE_READS": {
        "prefix": "system.timingCpu",
        "suffix": "fp_regfile_reads"
    },  #fp_regfile_reads
    "KEY_CORE_FLOAT_REGFILE_WRITES": {
        "prefix": "system.timingCpu",
        "suffix": "fp_regfile_writes"
    },  #fp_regfile_writes
    "KEY_CORE_FUNCTION_CALLS": {
        "prefix": "system.timingCpu",
        "suffix": "commit.function_calls"
    },  #function_calls
    "KEY_CORE_CONTEXT_SWITCHES": {
        "prefix": "system.timingCpu",
        "suffix": "workload.numSyscalls"
    },  #context_switches
    "KEY_CORE_IALU_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.int_alu_accesses"
    },  #ialu_accesses
    "KEY_CORE_FPU_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "iq.fp_alu_accesses"
    },  #fpu_accesses
    #mul_accesses, cdb_alu_accesses, cdb_mul_accesses, cdb_fpu_accesses set to 0
    "KEY_CORE_ITLB_WRITE_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "itb.wrAccesses"
    },  #itb.wrAccesses
    "KEY_CORE_ITLB_WRITE_MISSES": {
        "prefix": "system.timingCpu",
        "suffix": "itb.wrMisses"
    },  #itb.wrMisses
    "KEY_CORE_ITLB_READ_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "itb.rdAccesses"
    },  #itb.rdAccesses
    "KEY_CORE_ITLB_READ_MISSES": {
        "prefix": "system.timingCpu",
        "suffix": "itb.rdMisses"
    },  #itb.rdMisses
    "KEY_CORE_ICACHE_READ_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Icache.demand_accesses"
    },  #icahce.ReadReq_accesses
    "KEY_CORE_ICACHE_READ_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Icache.demand_misses"
    },  #icahce.ReadReq_misses
    "KEY_CORE_DTLB_WRITE_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "dtb.wrAccesses"
    },  #dtb.wrAccesses
    "KEY_CORE_DTLB_WRITE_MISSES": {
        "prefix": "system.timingCpu",
        "suffix": "dtb.wrMisses"
    },  #dtb.wrMisses
    "KEY_CORE_DTLB_READ_ACCESSES": {
        "prefix": "system.timingCpu",
        "suffix": "dtb.rdAccesses"
    },  #dtb.rdAccesses
    "KEY_CORE_DTLB_READ_MISSES": {
        "prefix": "system.timingCpu",
        "suffix": "dtb.rdMisses"
    },  #dtb.rdMisses
    "KEY_CORE_DCACHE_READ_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_accesses"
    },  #dcache.ReadReq_accesses
    "KEY_CORE_DCACHE_READ_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_misses"
    },  #dcache.ReadReq_misses
    "KEY_CORE_DCACHE_WRITE_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_hits"  #use demand_accesses or not
    },  #dcache.WriteReq_accesses
    "KEY_CORE_DCACHE_WRITE_MISSES": {
        "prefix": "system.caches.controllers",
        "suffix": "L1Dcache.demand_misses"
    },  #dcache.WriteReq_misses
    "KEY_CORE_DCACHE_CONFLICTS": {
        "prefix": "system.caches.controllers",
        "suffix": "dcache.tags.Replacement"
    },  #dcache.
    "KEY_PAM_READ_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_read_pm"
    },  #OptionalOwnAccessMetadata.total_read_pm
    "KEY_PAM_WRITE_ACCESSES": {
        "prefix": "system.caches.controllers",
        "suffix": "OptionalOwnAccessMetadata.total_write_pm"
    },  #OptionalOwnAccessMetadata.total_write_pm
}

GEM5_ENERGY_SYSTEM_STATS = {
    # stats for energy consumption of system
    "KEY_L1DIR_TOTAL_LOAD": "system.caches.L1Cache_Controller.Load::total",
    "KEY_L1DIR_TOTAL_STORE": "system.caches.L1Cache_Controller.Store::total",
    "KEY_L1DIR_READ_MISSES": "system.caches.L1Cache_Controller.I.Load::total",
    "KEY_L1DIR_WRITE_I": "system.caches.L1Cache_Controller.I.Store::total",
    "KEY_L1DIR_WRITE_S": "system.caches.L1Cache_Controller.S.Store::total",
    "KEY_L1DIR_CONFLICT": "system.caches.L1Cache_Controller.L1_Replacement::total",
    "KEY_SAM_READ": "system.caches.controllers5.FSGlobalACTData.total_sam_read",
    "KEY_SAM_WRITE": "system.caches.controllers5.FSGlobalACTData.total_sam_write",
    "KEY_L2CACHE_DEMAND_ACCESSES": "system.caches.controllers.L2cache.demand_accesses",
    "KEY_L2CACHE_DEMAND_HITS": "system.caches.controllers.L2cache.demand_hits",
    "KEY_L2CACHE_DEMAND_MISSES": "system.caches.controllers.L2cache.demand_misses",
    "KEY_MEM_READS": "system.mem_ctrls.num_reads::total",
    "KEY_MEM_WRITES": "system.mem_ctrls.num_writes::total"
}

ALL_ENERGY_STATS = {**GEM5_ENERGY_SYSTEM_STATS, **GEM5_ENERGY_STATS}


def gatherMcPATStats(root: str, path: str, options):

    exp_ops = root.replace(options.getExpOutputDir(), "")
    parts = exp_ops.split(os.sep)
    parts = list(filter(None, parts))
    assert len(parts) == 4

    protocol_name = parts[0]  # protocol
    input_size = parts[1]  # input-size
    iter_num = int(parts[2])  # iteration
    bench_name = parts[3]  # benchmark
    mcPAT_stats = {}
    with open(path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            line = line.strip()
            for skey, sval in GEM5_ENERGY_SYSTEM_STATS.items():
                if sval in line:
                    suffix = line.replace(sval, "").strip()
                    stat_val = suffix[:suffix.find("#")].strip()
                    if '#' not in line:  # few stats do not contain '#' comment
                        str_part = line.split()
                        stat_val = str_part[1]
                    mcPAT_stats[skey] = stat_val.strip()

            for skey, sval in GEM5_ENERGY_STATS.items():
                if sval["prefix"] in line and sval["suffix"] in line:
                    ## handle FU_type_0 in different way
                    suffix = line[line.find(sval["suffix"]) + len(sval["suffix"]):].strip()

                    if ("FU_type_0" in line):
                        if '#' not in line:
                            hashCommentNotPresent = False
                            assert (hashCommentNotPresent)
                        stat_val = suffix[:suffix.find("#")].strip().split()
                        if any(word in line for word in int_inst):
                            mcPAT_stats["KEY_CORE_INT_INSTRUCTIONS"] = mcPAT_stats.get("KEY_CORE_INT_INSTRUCTIONS", 0) \
                                                                    + int(stat_val[1])
                        elif any(word in line for word in float_inst):
                            mcPAT_stats["KEY_CORE_FP_INSTRUCTIONS"] = mcPAT_stats.get("KEY_CORE_FP_INSTRUCTIONS", 0) \
                                                                    + int(stat_val[1])
                        elif any(word in line for word in load_inst):
                            mcPAT_stats["KEY_CORE_LOAD_INSTRUCTIONS"] = mcPAT_stats.get("KEY_CORE_LOAD_INSTRUCTIONS",0)\
                            + int(stat_val[1])
                        elif any(word in line for word in store_inst):
                            mcPAT_stats["KEY_CORE_STORE_INSTRUCTIONS"] = mcPAT_stats.get("KEY_CORE_STORE_INSTRUCTIONS",0)\
                            + int(stat_val[1])
                    else:
                        suffix = line[line.find(sval["suffix"]) + len(sval["suffix"]):].strip()
                        if suffix is not None:
                            stat_val = suffix[:suffix.find("#")].strip()
                            mcPAT_stats[skey] = mcPAT_stats.get(skey, 0) + int(stat_val)

            if "---------- End Simulation Statistics   ----------" in line:
                valid = True

    # For energy stats: using pcacti now
    #### gem5 populate stat number
    for stat_key, stat_val in ALL_ENERGY_STATS.items():
        if stat_key not in mcPAT_stats:
            mcPAT_stats[stat_key] = str(0)

    # write the parsed stats to file
    filename = f"{options.getExpResultsDir()}/{bench_name}-{input_size}-{protocol_name}-{iter_num}.energy_stats"
    # parseXML(mcPAT_stats, root, path, options, f"{protocol_name}.xml")

    pass

'''

'''
# iterate over all children of root -> child.attrib['name']
# 1:system 2:L1Directory0 3:L2Directory0 4:L20 -> modify update values
# 5:noc0 6:mc 7:niu 8:pcie 9: flashc
# All config parameter will remain unmodified across all protocol
# except for PAM and SAM configuration
'''
# Unused now
'''
def parseXML(stats_map, parentFolder: str, path: str, options, inputXML:str):

    exp_ops = parentFolder.replace(options.getExpOutputDir(), "")
    parts = exp_ops.split(os.sep)
    parts = list(filter(None, parts))
    assert len(parts) == 4
    protocol_name = parts[0] # protocol
    input_size = parts[1] # input-size
    iter_num = int(parts[2]) # iteration
    bench_name = parts[3] # benchmark

    #construct
    curr_dir = os.getcwd()
    tree = ET.parse(f"{curr_dir}/src/mcpat/template/{inputXML}")
    # start one level compoenent
    root = tree.getroot()

    for child in root:
        indent = "\t"
        for children in child:
            #modifying theXML parsing
            # if modify any param
            if(children.attrib['name'] == 'number_of_cores'):
                children.attrib['value'] = str(8)

            # update stat for total, idle and busy cycles
            if(children.attrib['name'] == 'total_cycles'):
                children.attrib['value'] = str(stats_map["KEY_CPU_TOTAL_CYCLES"])

            if(children.attrib['name'] == 'idle_cycles'):
                children.attrib['value'] = str(stats_map["KEY_CPU_IDLE_CYCLES"])

            if(children.attrib['name'] == 'busy_cycles'):
                children.attrib['value'] = str(stats_map["KEY_CPU_TOTAL_CYCLES"]-\
                                            stats_map["KEY_CPU_IDLE_CYCLES"])

            # systemc.core0 component
            if (children.attrib['name'] == 'core0'):
                # iterate over system component to modify its children
                for sys_child in children:

                    # system.core.branch_predictor no change to config, update stats
                    if (sys_child.attrib['name'] == 'PBT'):
                        pass # update if required to parse/update any value

                    # system.core.itlb stats update
                    if (sys_child.attrib['name'] == 'itlb'):
                        for itlb_child in sys_child:
                            if (itlb_child.attrib['name'] == 'total_accesses'):
                                itlb_child.attrib['value'] = str(stats_map["KEY_CORE_ITLB_READ_ACCESSES"]+\
                                                                stats_map["KEY_CORE_ITLB_WRITE_ACCESSES"])
                            if (itlb_child.attrib['name'] == 'total_misses'):
                                itlb_child.attrib['value'] = str(stats_map["KEY_CORE_ITLB_READ_MISSES"]+\
                                                                stats_map["KEY_CORE_ITLB_WRITE_MISSES"])
                            if (itlb_child.attrib['name'] == 'conflicts'):
                                itlb_child.attrib['value'] = str(0)# can be initialized with number of replacements
                        # print("ITLB stats update")


                    # system.core.icache stats update
                    if (sys_child.attrib['name'] == 'icache'):
                        # icache_config, buffer_size unchanged
                        for icache_child in sys_child:
                            if (icache_child.attrib['name'] == 'read_accesses'):
                                icache_child.attrib['value'] = str(stats_map["KEY_CORE_ICACHE_READ_ACCESSES"])
                            if (icache_child.attrib['name'] == 'read_misses'):
                                icache_child.attrib['value'] = str(stats_map["KEY_CORE_ICACHE_READ_MISSES"])
                            if (icache_child.attrib['name'] == 'conflicts'):
                                icache_child.attrib['value'] = str(0)# can be initialized with number of replacements
                        # print("Icache stats update")

                    # system.core.dtlb stats update
                    if (sys_child.attrib['name'] == 'dtlb'):
                        for dtlb_child in sys_child:
                            if (dtlb_child.attrib['name'] == 'total_accesses'):
                                dtlb_child.attrib['value'] = str(stats_map["KEY_CORE_DTLB_READ_ACCESSES"]+\
                                                                stats_map["KEY_CORE_DTLB_WRITE_ACCESSES"])
                            if (dtlb_child.attrib['name'] == 'total_misses'):
                                dtlb_child.attrib['value'] = str(stats_map["KEY_CORE_DTLB_READ_MISSES"]+\
                                                                stats_map["KEY_CORE_DTLB_WRITE_MISSES"])
                            if (dtlb_child.attrib['name'] == 'conflicts'):
                                dtlb_child.attrib['value'] = str(0)# can be initialized with number of replacements
                        # print("DTLB stats update")

                    # system.core.dcache stats update
                    if (sys_child.attrib['name'] == 'dcache'):
                        for dcache_child in sys_child:
                            if (dcache_child.attrib['name'] == 'read_accesses'):
                                dcache_child.attrib['value'] = str(stats_map["KEY_CORE_DCACHE_READ_ACCESSES"])
                            if (dcache_child.attrib['name'] == 'write_accesses'):
                                dcache_child.attrib['value'] = str(stats_map["KEY_CORE_DCACHE_WRITE_ACCESSES"])
                            if (dcache_child.attrib['name'] == 'read_misses' ):
                                dcache_child.attrib['value'] = str(stats_map["KEY_CORE_DCACHE_READ_MISSES"])
                            if (dcache_child.attrib['name'] == 'write_misses'):
                                dcache_child.attrib['value'] = str(stats_map["KEY_CORE_DCACHE_WRITE_MISSES"])
                            if (dcache_child.attrib['name'] == 'conflicts'):
                                dcache_child.attrib['value'] = str(0)
                        # print("Dcache stats update")

                    # system.core.pam private access metadata table
                    if (sys_child.attrib['name'] == 'pam'):
                        for pam_child in sys_child:
                            if (pam_child.attrib['name'] == 'total_accesses'):
                                pam_child.attrib['value'] = str(stats_map["KEY_PAM_READ_ACCESSES"]+\
                                                                stats_map["KEY_PAM_WRITE_ACCESSES"])
                            if (pam_child.attrib['name'] == 'read_accesses'):
                                pam_child.attrib['value'] = str(stats_map["KEY_PAM_READ_ACCESSES"])
                            if (pam_child.attrib['name'] == 'write_accesses'):
                                pam_child.attrib['value'] = str(stats_map["KEY_PAM_WRITE_ACCESSES"])
                        # print("PAM stats update")

                    # system.core.btb
                    if (sys_child.attrib['name'] == 'BTB'):
                        for btb_child in sys_child:
                            if (btb_child.attrib['name'] == 'read_accesses'):
                                btb_child.attrib['value'] = str(stats_map["KEY_CORE_BTB_READ_ACCESSES"])
                            if (btb_child.attrib['name'] == 'write_accesses'):
                                btb_child.attrib['value'] = str(stats_map["KEY_CORE_BTB_WRITES_ACCESSES"])
                        # print("BTB stats update")

                    if (sys_child.attrib['name']=='ROB_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_ROB_READS"])
                    if (sys_child.attrib['name']=='ROB_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_ROB_WRITES"])
                    if (sys_child.attrib['name']=='rename_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_RENAME_READS"])
                    if (sys_child.attrib['name']=='rename_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_RENAME_OPERANDS"]*
                                (stats_map["KEY_CORE_RENAME_READS"]//stats_map["KEY_CORE_RENAME_LOOKUPS"]))
                    if (sys_child.attrib['name']=='fp_rename_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FP_RENAME_READS"])
                    if (sys_child.attrib['name']=='fp_rename_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_RENAME_OPERANDS"]*
                                (stats_map["KEY_CORE_FP_RENAME_READS"]//stats_map["KEY_CORE_RENAME_LOOKUPS"]))
                    if (sys_child.attrib['name']=='inst_window_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INST_WINDOW_READS"])
                    if (sys_child.attrib['name']=='inst_window_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INST_WINDOW_WRITES"])
                    if (sys_child.attrib['name']=='inst_window_wakeup_accesses'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INST_WAKEUP_ACCESSES"])
                    if (sys_child.attrib['name']=='fp_inst_window_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FP_INST_WINDOW_READS"])
                    if (sys_child.attrib['name']=='fp_inst_window_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FP_INST_WINDOW_WRITES"])
                    if (sys_child.attrib['name']=='fp_inst_window_wakeup_accesses'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FP_INST_WAKEUP_ACCESSES"])
                    if (sys_child.attrib['name']=='int_regfile_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INT_REGFILE_READS"])
                    if (sys_child.attrib['name']=='int_regfile_writes'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INT_REGFILE_WRITES"])
                    if (sys_child.attrib['name']=='float_regfile_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FLOAT_REGFILE_READS"])
                    if (sys_child.attrib['name']=='float_regfile_reads'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FLOAT_REGFILE_WRITES"])
                    if (sys_child.attrib['name']=='functions_calls'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FUNCTION_CALLS"])
                    if (sys_child.attrib['name']=='context_switches'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_CONTEXT_SWITCHES"])
                    if (sys_child.attrib['name']=='ilau_accesses'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_IALU_ACCESSES"])
                    if (sys_child.attrib['name']=='fpu_accesses'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FPU_ACCESSES"])
                    if (sys_child.attrib['name']=='mul_accesses'):
                        sys_child.attrib['value'] = str(0)#stats_map["KEY_CORE_MUL_ACCESSES"])
                    if (sys_child.attrib['name']=='cdb_alu_accesses'):
                        sys_child.attrib['value'] = str(0)
                    if (sys_child.attrib['name']=='cdb_mul_accesses'):
                        sys_child.attrib['value'] = str(0)
                    if (sys_child.attrib['name']=='cdb_fpu_accesses'):
                        sys_child.attrib['value'] = str(0)
                    if (sys_child.attrib['name']== 'total_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_TOTAL_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'int_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_INT_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'fp_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_FP_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'branch_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_BRANCH_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'branch_mispredictions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_BRANCH_MISPREDICTIONS"])
                    if (sys_child.attrib['name']== 'load_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_LOAD_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'store_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_STORE_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'committed_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_COMMITTED_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'committed_int_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_COMMITTED_INT_INSTRUCTIONS"])
                    if (sys_child.attrib['name']== 'committed_fp_instructions'):
                        sys_child.attrib['value'] = str(stats_map["KEY_CORE_COMMITTED_FP_INSTRUCTIONS"])

            # parsing of core stats completed

            if (children.attrib['name'] == 'L1Directory0'):
                for dir_child in children:
                    if (dir_child.attrib['name'] == 'read_accesses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L1DIR_TOTAL_LOAD"]+\
                                                    stats_map["KEY_L1DIR_TOTAL_STORE"])
                    if (dir_child.attrib['name'] == 'read_misses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L1DIR_READ_MISSES"])
                    if (dir_child.attrib['name'] == 'write_accesses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L1DIR_TOTAL_STORE"])
                    if (dir_child.attrib['name'] == 'write_misses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L1DIR_WRITE_I"]+\
                                                        stats_map["KEY_L1DIR_WRITE_S"])
                    if (dir_child.attrib['name'] == 'conflicts'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L1DIR_CONFLICT"])
                # print ("L1 Directory stats update")


            # if (children.attrib['name'] == 'L1Directory0'):
            #     for dir_child in children:
            #         if (dir_child.attrib['name'] == 'read_accesses'):
            #             dir_child.attrib['value'] = str('dir_read_acc')
            #         if (dir_child.attrib['name'] == 'read_misses'):
            #             dir_child.attrib['value'] = str('dir_read_miss')
            #         if (dir_child.attrib['name'] == 'write_accesses'):
            #             dir_child.attrib['value'] = str('dir_write_acc')
            #         if (dir_child.attrib['name'] == 'write_misses'):
            #             dir_child.attrib['value'] = str('dir_write_miss')
            #         if (dir_child.attrib['name'] == 'conflicts'):
            #             dir_child.attrib['value'] = str('icnflt')
            #     print("L1 Dir stats update")

            # system.L2Directory
            if (children.attrib['name'] == 'L2Directory0'):
                for dir_child in children:
                    if (dir_child.attrib['name'] == 'read_accesses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_ACCESSES"])
                    if (dir_child.attrib['name'] == 'read_misses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_MISSES"])
                    if (dir_child.attrib['name'] == 'write_accesses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_HITS"])
                    if (dir_child.attrib['name'] == 'write_misses'):
                        dir_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_MISSES"])
                    if (dir_child.attrib['name'] == 'conflicts'):
                        dir_child.attrib['value'] = str(0)
                    if (dir_child.attrib['name'] == 'sam'):
                        for sam_child in dir_child:
                            if (sam_child.attrib['name'] == 'total_accesses'):
                                sam_child.attrib['value'] = str(stats_map["KEY_SAM_READ"]+\
                                                                stats_map["KEY_SAM_WRITE"])
                            if (sam_child.attrib['name'] == 'read_accesses'):
                                sam_child.attrib['value'] = str(stats_map["KEY_SAM_READ"])
                            if (sam_child.attrib['name'] == 'write_accesses'):
                                sam_child.attrib['value'] = str(stats_map["KEY_SAM_WRITE"])
                            if (sam_child.attrib['name'] == 'sam_config'):
                                # addd code to update the sam size
                                pass
                # print("L2 Dir stats update")

            # system.L20
            if (children.attrib['name'] == 'L20'):
                for l2cache_child in children:
                    if (l2cache_child.attrib['name'] == 'read_accesses'):
                        l2cache_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_ACCESSES"])
                    if (l2cache_child.attrib['name'] == 'read_misses'):
                        l2cache_child.attrib['value'] = str(0)
                    if (l2cache_child.attrib['name'] == 'write_accesses'):
                        l2cache_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_HITS"])
                    if (l2cache_child.attrib['name'] == 'write_misses'):
                        l2cache_child.attrib['value'] = str(stats_map["KEY_L2CACHE_DEMAND_MISSES"])
                    if (l2cache_child.attrib['name'] == 'conflicts'):
                        l2cache_child.attrib['value'] = str(0)
                # print("L2 cache stats update")

            #memory controller
            if (children.attrib['name'] == 'mc'):
                for memcntrl_child in children:
                    if(memcntrl_child.attrib['name'] == 'memory_accesses'):
                        memcntrl_child.attrib['value'] = str(stats_map["KEY_MEM_READS"]+\
                                                            stats_map["KEY_MEM_WRITES"])
                    if(memcntrl_child.attrib['name'] == 'memory_reads'):
                        memcntrl_child.attrib['value'] = str(stats_map["KEY_MEM_READS"])
                    if(memcntrl_child.attrib['name'] == 'memory_writes'):
                        memcntrl_child.attrib['value'] = str(stats_map["KEY_MEM_WRITES"])
                # print("Mem controller update")

    # DATA parsing and update done, write file
    tree.write(f"{options.getExpResultsDir()}/{bench_name}-{input_size}-{protocol_name}-{iter_num}.xml")
'''
