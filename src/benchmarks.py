from typing import List

_BENCHMARK_GROUP = ["huron", "feather", "parsec", "micro"]

_HURON_BENCHMARKS = [
    "huron-boost-spinlock", "huron-boost-spinlock-manual", "huron-ref-count",
    "huron-string-match", "huron-string-match-manual", "huron-linear-reg",
    "huron-linear-reg-manual", "huron-locked-toy", "huron-locked-toy-manual",
    "huron-lockless-toy", "huron-lockless-toy-manual", "huron-ref-count-manual",
    "huron_sm", "huron_rc", "huron_bs", "huron_lr", "huron_ll",
    "huron_lt", "huron_rc_man", "huron_bs_man", "huron_lr_man", "huron_ll_man",
    "huron_lt_man", "huron_rc_base", "huron_bs_base", "huron_lr_base", "huron_ll_base",
    "huron_lt_base", "huron_sm_base", "huron_sm_man", "huron_compile"
]


# feather-test*-small have same behavior as feather-test* with support to varying
# input size

_FEATHER_BENCHMARKS = [
    "feather-test1-small", "feather-test2-small", "feather-test3-small", "feather-test4-small",
    "feather-test5-small", "feather-test6-small", "feather-test7-small", "feather-test8-small",
    "feather-test9-small", "feather-test1-small-manual", "feather-test3-small-manual",
    "feather-test4-small-manual", "feather-test6-small-manual", "feather-test8-small-manual",
    "feather-test9-small-manual", "feather-test10-small"
]

_PARSEC_BENCHMARKS = [
    "blackscholes", "bodytrack", "canneal", "facesim", "fluidanimate",
    "swaptions", "streamcluster", "streammanual"
]


_MICROBENCHMARKS = [
    "false-sharing", "both-false-and-true-sharing", "both-true-and-false-sharing", "true-sharing",
    "no-false-sharing", "proportional-fs", "proportional-ts", "repetitive-fs-ts-diffline",
    "repetitive-fs-ts-sameline", "array-lock", "simulate-sleep", "false-sharing-char",
    "false-sharing-short", "false-sharing-long"
]



_SYNCHROBENCH_BENCHMARKS = [
    "ESTM-specfriendly-tree", "ESTM-specfriendly-tree-man"
]


# FalseSharing: Full system simulation options
_TYPE_BENCHMARK = ["parsec", "custom"]

#for parec sim-dev
TEST_OPTIONS = {
    # microbenchmark
    "false-sharing": "18",
    "false-sharing-char": "18",
    "false-sharing-short": "18",
    "false-sharing-long": "18",
    "both-false-and-true-sharing": "18",
    "both-true-and-false-sharing": "18",
    "true-sharing": "18",
    "no-false-sharing": "18",
    "repetitive-fs-ts-diffline": "18",
    "repetitive-fs-ts-sameline": "18",
    "proportional-fs": "18",
    "proportional-ts": "18",
    "fs-ts-diffline": "18",
    "fs-ts-sameline": "18",
    #parsec
    "blackscholes": "simsmall", 
    "bodytrack": "simsmall",
    "canneal": "simsmall",
    "facesim": "simsmall",
    "fluidanimate": "simsmall",
    "swaptions": "simsmall",
    "streamcluster": "simsmall",
    "streammanual": "simsmall",
    # feather microbm
    "feather-test1-small": "18",
    "feather-test1-small-manual": "18",
    "feather-test2-small": "18",
    "feather-test3-small": "18",
    "feather-test3-small-manual": "18",
    "feather-test4-small": "18",
    "feather-test4-small-manual": "18",
    "feather-test5-small": "18",
    "feather-test6-small": "18",
    "feather-test6-small-manual": "18",
    "feather-test7-small": "18",
    "feather-test8-small": "18",
    "feather-test8-small-manual": "18",
    "feather-test9-small": "18",
    "feather-test9-small-manual": "18",
    "feather-test10-small": "18",
    "huron-boost-spinlock": "1000",  # huron benchmarks
    "huron-boost-spinlock-manual": "1000",
    "huron_bs": "1000", # huron comparison
    "huron_bs_man": "1000", # huron comparison
    "huron_bs_base": "1000", # huron comparison
    "huron_compile":"10",
    "huron-ref-count": "12",
    "huron-ref-count-manual": "12",
    "huron_rc": "12", # huron comparison
    "huron_rc_man": "12", # huron comparison
    "huron_rc_base": "12", # huron comparison
    "huron-string-match":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt",
    "huron-string-match-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt",
    "huron_sm":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron_sm_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron_sm_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron-linear-reg":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt",
    "huron-tmi-boost-refcount": "",
    "huron-linear-reg-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt",
    "huron_lr":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron_lr_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron_lr_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_50KB.txt", # huron comparison
    "huron-locked-toy": "11",
    "huron-locked-toy-manual": "11",
    "huron_lt": "11", # huron comparison
    "huron_lt_man": "11", # huron comparison
    "huron_lt_base": "11", # huron comparison
    "huron-lockless-toy": "11",
    "huron-lockless-toy-manual": "11",
    "huron_ll": "11", # huron comparison
    "huron_ll_man": "11", # huron comparison
    "huron_ll_base": "11", # huron comparison
    "ESTM-specfriendly-tree": "-t 4 -d 1500 -S 2147483647 -i 256 -r 2147483647 -u 20",
    "ESTM-specfriendly-tree-man": "-t 4 -d 1500 -S 2147483647 -i 256 -r 2147483647 -u 20"
}

SMALL_OPTIONS = {
    # microbenchmarks
    "false-sharing": "18",
    "false-sharing-char": "18",
    "false-sharing-short": "18",
    "false-sharing-long": "18",
    "both-false-and-true-sharing": "18",
    "both-true-and-false-sharing": "18",
    "true-sharing": "18",
    "no-false-sharing": "18",
    "repetitive-fs-ts-diffline": "18",
    "repetitive-fs-ts-sameline": "18",
    "proportional-fs": "18",
    "proportional-ts": "18",
    "fs-ts-diffline": "18",
    "fs-ts-sameline": "18",
    # parsec benchmarks
    "blackscholes": "simsmall",
    "bodytrack": "simsmall",
    "canneal": "simsmall",
    "facesim": "simsmall",
    "fluidanimate": "simsmall",
    "swaptions": "simsmall",
    "streamcluster": "simsmall",
    "streammanual": "simsmall",
    # feather microbenchmarks
    "feather-test1-small": "20",
    "feather-test1-small-manual": "20",
    "feather-test2-small": "20",
    "feather-test3-small": "20",
    "feather-test3-small-manual": "20",
    "feather-test4-small": "20",
    "feather-test4-small-manual": "20",
    "feather-test5-small": "20",
    "feather-test6-small": "20",
    "feather-test6-small-manual": "20",
    "feather-test7-small": "20",
    "feather-test8-small": "20",
    "feather-test8-small-manual": "20",
    "feather-test9-small": "20",
    "feather-test9-small-manual": "20",
    "feahter-test10-small": "20",
    "huron-boost-spinlock": "10000",  # huron benchmarks
    "huron-boost-spinlock-manual": "10000",
    "huron_bs": "10000", # huron comparison
    "huron_bs_man": "10000", # huron comparison
    "huron_bs_base": "10000", # huron comparison
    "huron_compile":"10",
    "huron-ref-count": "16",
    "huron-ref-count-manual": "16",
    "huron_rc": "16", # huron comparison
    "huron_rc_man": "16", # huron comparison
    "huron_rc_base": "16", # huron comparison
    "huron-string-match":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt",
    "huron-string-match-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt",
    "huron_sm":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron_sm_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron_sm_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron-linear-reg":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt",
    "huron-linear-reg-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt",
    "huron_lr":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron_lr_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron_lr_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_100KB.txt", # huron comparison
    "huron-locked-toy": "16",
    "huron-locked-toy-manual": "16",
    "huron_lt": "16", # huron comparison
    "huron_lt_man": "16", # huron comparison
    "huron_lt_base": "16", # huron comparison
    "huron-lockless-toy": "16",
    "huron-lockless-toy-manual": "16",
    "huron_ll": "16", # huron comparison
    "huron_ll_man": "16", # huron comparison
    "huron_ll_base": "16", # huron comparison
    # sychrobench benchmarks
    "ESTM-specfriendly-tree": "-t 4 -d 2000 -S 2147483647 -i 256 -r 2147483647 -u 20",
    "ESTM-specfriendly-tree-man": "-t 4 -d 2000 -S 2147483647 -i 256 -r 2147483647 -u 20",
}

MEDIUM_OPTIONS = {
    # microbenchmark
    "false-sharing": "20",
    "false-sharing-char": "20",
    "false-sharing-short": "20",
    "false-sharing-long": "20",
    "both-false-and-true-sharing": "20",
    "both-true-and-false-sharing": "20",
    "true-sharing": "20",
    "no-false-sharing": "20",
    "repetitive-fs-ts-diffline": "20",
    "repetitive-fs-ts-sameline": "20",
    "proportional-fs": "20",
    "proportional-ts": "20",
    "fs-ts-diffline": "20",
    "fs-ts-sameline": "20",
    # parsec benchmarks
    "blackscholes": "simmedium",
    "bodytrack": "simmedium",
    "canneal": "simmedium",
    "facesim": "simmedium",
    "fluidanimate": "simmedium",
    "swaptions": "simmedium",
    "streamcluster": "simmedium",
    "streammanual": "simmedium",
    # feather microbm
    "feather-test1-small": "24",
    "feather-test1-small-manual": "24",
    "feather-test2-small": "24",
    "feather-test3-small": "24",
    "feather-test3-small-manual": "24",
    "feather-test4-small": "24",
    "feather-test4-small-manual": "24",
    "feather-test5-small": "24",
    "feather-test6-small": "24",
    "feather-test6-small-manual": "24",
    "feather-test7-small": "24",
    "feather-test8-small": "22",
    "feather-test8-small-manual": "22",
    "feather-test9-small": "24",
    "feather-test9-small-manual": "24",
    "feather-test10-small": "22",
    "huron-boost-spinlock": "50000",  # huron benchmarks
    "huron-boost-spinlock-manual": "50000",
    "huron_bs": "50000", # huron comparison
    "huron_bs_man": "50000", # huron comparison
    "huron_bs_base": "50000", # huron comparison
    "huron_compile":"10",
    "huron-ref-count": "18",
    "huron-ref-count-manual": "18",
    "huron_rc": "18", # huron comparison
    "huron_rc_man": "18", # huron comparison
    "huron_rc_base": "18", # huron comparison
    "huron-string-match":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt",
    "huron-string-match-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt",
    "huron_sm":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron_sm_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron_sm_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron-linear-reg":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt",
    "huron-linear-reg-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt",
    "huron_lr":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron_lr_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron_lr_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_1MB.txt", # huron comparison
    "huron-locked-toy": "18",
    "huron-locked-toy-manual": "18",
    "huron_lt": "18", # huron comparison
    "huron_lt_man": "18", # huron comparison
    "huron_lt_base": "18", # huron comparison
    "huron-lockless-toy": "18",
    "huron-lockless-toy-manual": "18",
    "huron_ll": "18", # huron comparison
    "huron_ll_man": "18", # huron comparison
    "huron_ll_base": "18", # huron comparison
    # sychrobench benchmarks
    "ESTM-specfriendly-tree": "-t 4 -d 4000 -S 2147483647 -i 256 -r 2147483647 -u 20",
    "ESTM-specfriendly-tree-man": "-t 4 -d 4000 -S 2147483647 -i 256 -r 2147483647 -u 20",
}

LARGE_OPTIONS = {
    # microbenchmark
    "false-sharing": "21",
    "false-sharing-char": "21",
    "false-sharing-short": "21",
    "false-sharing-long": "21",
    "both-false-and-true-sharing": "21",
    "both-true-and-false-sharing": "21",
    "true-sharing": "21",
    "no-false-sharing": "21",
    "repetitive-fs-ts-diffline": "21",
    "repetitive-fs-ts-sameline": "21",
    "proportional-fs": "21",
    "proportional-ts": "21",
    "fs-ts-diffline": "21",
    "fs-ts-sameline": "21",
    "blackscholes": "simlarge",  # parsec benchmarks
    "bodytrack": "simlarge",
    "canneal": "simlarge",
    "facesim": "simlarge",
    "fluidanimate": "simlarge",
    "swaptions": "simlarge",
    "streamcluster": "simlarge",
    "streammanual": "simlarge",
    # feather microbm
    "feather-test1-small": "24",
    "feather-test1-small-manual": "24",
    "feather-test2-small": "24",
    "feather-test3-small": "26",
    "feather-test3-small-manual": "26",
    "feather-test4-small": "25",
    "feather-test4-small-manual": "25",
    "feather-test5-small": "24",
    "feather-test6-small": "25",
    "feather-test6-small-manual": "25",
    "feather-test7-small": "24",
    "feather-test8-small": "25",
    "feather-test8-small-manual": "25",
    "feather-test9-small": "26",
    "feather-test9-small-manual": "26",
    "feather-test10-small": "24",
    "huron-boost-spinlock": "100000",  # huron benchmarks
    "huron-boost-spinlock-manual": "100000",
    "huron_bs": "100000", # huron comparison
    "huron_bs_man": "100000", # huron comparison
    "huron_bs_base": "100000", # huron comparison
    "huron_compile":"10",
    "huron-ref-count": "20",
    "huron-ref-count-manual": "20",
    "huron_rc": "20", # huron comparison
    "huron_rc_man": "20", # huron comparison
    "huron_rc_base": "20", # huron comparison
    "huron-string-match":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt",
    "huron-string-match-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt",
    "huron_sm":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron_sm_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron_sm_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron-linear-reg":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt",
    "huron-linear-reg-manual": "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt",
    "huron_lr":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron_lr_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron_lr_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_8MB.txt", # huron comparison
    "huron-locked-toy": "19",
    "huron-locked-toy-manual": "19",
    "huron_lt": "19", # huron comparison
    "huron_lt_man": "19", # huron comparison
    "huron_lt_base": "19", # huron comparison
    "huron-lockless-toy": "19",
    "huron-lockless-toy-manual": "19",
    "huron_ll": "19", # huron comparison
    "huron_ll_man": "19", # huron comparison
    "huron_ll_base": "19", # huron comparison
    # sychrobench benchmarks
    "ESTM-specfriendly-tree": "-t 4 -d 5000 -S 2147483647 -i 256 -r 2147483647 -u 20",
    "ESTM-specfriendly-tree-man": "-t 4 -d 5000 -S 2147483647 -i 256 -r 2147483647 -u 20"
}
# native input for parsec are skipped,
HUGE_OPTIONS = {
    # microbenchmark
    "false-sharing": "24",
    "false-sharing-char": "24",
    "false-sharing-short": "24",
    "false-sharing-long": "24",
    "both-false-and-true-sharing": "24",
    "both-true-and-false-sharing": "24",
    "true-sharing": "24",
    "no-false-sharing": "24",
    "repetitive-fs-ts-diffline": "24",
    "repetitive-fs-ts-sameline": "24",
    "proportional-fs": "24",
    "proportional-ts": "24",
    "fs-ts-diffline": "24",
    "fs-ts-sameline": "24",
    "blackscholes": "simlarge",  # parsec benchmarks
    "bodytrack": "simlarge",
    "canneal": "simlarge",
    "facesim": "simlarge",
    "fluidanimate": "simlarge",
    "swaptions": "simlarge",
    "streamcluster": "simlarge",
    "streammanual": "simlarge",
    # feather microbm
    "feather-test1-small": "28",
    "feather-test1-small-manual": "28",
    "feather-test2-small": "32",
    "feather-test3-small": "28",
    "feather-test3-small-manual": "28",
    "feather-test4-small": "28",
    "feather-test4-small-manual": "28",
    "feather-test5-small": "28",
    "feather-test6-small": "28",
    "feather-test6-small-manual": "28",
    "feather-test7-small": "28",
    "feather-test8-small": "28",
    "feather-test8-small-manual": "28",
    "feather-test9-small": "28",
    "feather-test9-small-manual": "28",
    "feather-test10-small": "28",
    "huron-boost-spinlock": "1000000",  # huron benchmarks
    "huron-boost-spinlock-manual": "1000000",
    "huron_bs": "1000000", # huron comparison
    "huron_bs_man": "1000000", # huron comparison
    "huron_bs_base": "1000000", # huron comparison
    "huron_compile":"10",
    "huron-ref-count": "21",
    "huron-ref-count-manual": "21",
    "huron_rc": "21", # huron comparison
    "huron_rc_man": "21", # huron comparison
    "huron_rc_base": "21", # huron comparison
    "huron-string-match":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt",
    "huron-string-match-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt",
    "huron_sm":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron_sm_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron_sm_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron-linear-reg":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt",
    "huron-tmi-boost-refcount": "",
    "huron-linear-reg-manual":
    "/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt",
    "huron_lr":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron_lr_man":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron_lr_base":"/home/gem5/false-sharing-benchmarks/bench_input/huron/linear_reg/key_file_32MB.txt", # huron comparison
    "huron-locked-writer": "17",
    "huron-locked-toy": "20",
    "huron-locked-toy-manual": "20",
    "huron_lt": "20", # huron comparison
    "huron_lt_man": "20", # huron comparison
    "huron_lt_base": "20", # huron comparison
    "huron-lockless-toy": "20",
    "huron-lockless-toy-manual": "20",
    "huron_ll": "20", # huron comparison
    "huron_ll_man": "20", # huron comparison
    "huron_ll_base": "20", # huron comparison
    # sychrobench benchmarks
    "ESTM-specfriendly-tree": "-t 4 -d 10000 -S 2147483647 -i 256 -r 2147483647 -u 20",
    "ESTM-specfriendly-tree-man": "-t 4 -d 10000 -S 2147483647 -i 256 -r 2147483647 -u 20"
}


def isMicroBenchmark(bench) -> bool:
    return bench in _MICROBENCHMARKS


def isHuronBenchmark(bench) -> bool:
    return bench in _HURON_BENCHMARKS


def isFeatherBenchmark(bench) -> bool:
    return bench in _FEATHER_BENCHMARKS


def isPARSECBenchmark(bench) -> bool:
    return bench in _PARSEC_BENCHMARKS


def isSYNCHROBENCHBenchmark(bench) -> bool:
    return bench in _SYNCHROBENCH_BENCHMARKS

def getOrderedBenchmarks(benchs) -> List[str]:
    DESIRED_BENCH_ORDER = _MICROBENCHMARKS + _FEATHER_BENCHMARKS + _HURON_BENCHMARKS + _PARSEC_BENCHMARKS + _SYNCHROBENCH_BENCHMARKS
    return [item for item in DESIRED_BENCH_ORDER if item in benchs]


def isBenchmarkGroup(bench) -> bool:
    if bench in _BENCHMARK_GROUP:
        return True
    return False


def returnAllBenchmarksFromGroup(bench) -> List[str]:
    if bench == "huron":
        return _HURON_BENCHMARKS
    if bench == "feather":
        return _FEATHER_BENCHMARKS
    if bench == "parsec":
        return _PARSEC_BENCHMARKS
    if bench == "micro":
        return _MICROBENCHMARKS
