#!/bin/bash

echo  "Running huron false sharing application started"

if [ $1 ] && [ $2 ];
then
    echo "HURON false sharing set for all three protocol"
    # huron binaries
    python3 src/main.py --tasks run --trials $3 --bench huron_ll --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_bs --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lt --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_rc --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_sm --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lr --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    # manual fix version of huron
    python3 src/main.py --tasks run --trials $3 --bench huron_ll_man --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_bs_man --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lt_man --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_rc_man --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_sm_man --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lr_man --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    # original application with false sharing
    python3 src/main.py --tasks run --trials $3 --bench huron_ll_base --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_bs_base --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lt_base --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_rc_base --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_sm_base --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lr_base --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    # our repair protocol
    python3 src/main.py --tasks run --trials $3 --bench huron_ll_base --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_bs_base --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lt_base --verbose 1 --protocol FS_MESI --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_rc_base --verbose 1 --protocol FS_MESI --workloadSize medium  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_sm_base --verbose 1 --protocol FS_MESI --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron_lr_base --verbose 1 --protocol FS_MESI --workloadSize large  --outputDir micro-compare-huron --benchmark_type custom
    echo "::::::::::::::::ALL experiments for huron comparison completed::::::::::::::::::"
else
    echo "arg not provided"
fi

