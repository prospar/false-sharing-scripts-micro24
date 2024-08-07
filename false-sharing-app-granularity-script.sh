#!/bin/bash

echo  "Running huron false sharing granularity $3  experiment"

if [ $1 ] && [ $2 ];
then
    echo "Launching Granularity $3 experiments for applications with false sharing"
    # python3 src/main.py --tasks run --trials $4 --bench huron-lockless-toy --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small  --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-lockless-toy --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for lockles-toy completed"
    # python3 src/main.py --tasks run --trials $4 --bench huron-linear-reg --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-linear-reg --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for linear-reg completed"
    # python3 src/main.py --tasks run --trials $4 --bench huron-ref-count --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-ref-count --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for ref-count completed"
    # python3 src/main.py --tasks run --trials $4 --bench huron-boost-spinlock --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-boost-spinlock --verbose 1 --protocol FS_MESI --workloadSize small --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for boost spinlock completed"
    # python3 src/main.py --tasks run --trials $4 --bench huron-string-match --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-string-match --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for string match completed"
    # python3 src/main.py --tasks run --trials $4 --bench huron-locked-toy --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium  --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench huron-locked-toy --verbose 1 --protocol FS_MESI --workloadSize medium  --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for locked toy completed"
    # python3 src/main.py --tasks run --trials $4 --bench ESTM-specfriendly-tree --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium --outputDir micro-granularity-$3 --benchmark_type custom
    python3 src/main.py --tasks run --trials $4 --bench ESTM-specfriendly-tree --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-granularity-$3 --benchmark_type custom
    echo "Three protocol for ESTM-sftree completed"
    echo ":::::::::::::::: Granularity $3 experiments for false sharing applications ::::::::::::::::::"
else
    echo "arg not provided"
fi
