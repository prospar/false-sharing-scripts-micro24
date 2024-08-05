#!/bin/bash

echo  "Running false sharing application started"

if [ $1 ] && [ $2 ];
then
    echo "false sharing set for all three protocol"
    # python3 src/main.py --tasks run --trials $3 --bench huron-lockless-toy --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-lockless-toy --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small  --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-lockless-toy --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for lockles-toy completed"
    # python3 src/main.py --tasks run --trials $3 --bench huron-linear-reg --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-linear-reg --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-linear-reg --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for linear-reg completed"
    # python3 src/main.py --tasks run --trials $3 --bench huron-ref-count --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-ref-count --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-ref-count --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for ref-count completed"
    # python3 src/main.py --tasks run --trials $3 --bench huron-boost-spinlock --verbose 1 --protocol MESI_Nonblocking --workloadSize small --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-boost-spinlock --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-boost-spinlock --verbose 1 --protocol FS_MESI --workloadSize small --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for boost spinlock completed"
    # python3 src/main.py --tasks run --trials $3 --bench huron-string-match --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-string-match --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-string-match --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for string match completed"
    # python3 src/main.py --tasks run --trials $3 --bench huron-locked-toy --verbose 1 --protocol MESI_Nonblocking --workloadSize medium  --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-locked-toy --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium  --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench huron-locked-toy --verbose 1 --protocol FS_MESI --workloadSize medium  --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for locked toy completed"
    # python3 src/main.py --tasks run --trials $3 --bench ESTM-specfriendly-tree --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench ESTM-specfriendly-tree --verbose 1 --protocol FS_MESI_DETECTION --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    python3 src/main.py --tasks run --trials $3 --bench ESTM-specfriendly-tree --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-false-sharing-app --benchmark_type custom
    echo "Three protocol for ESTM specfriendly tree completed"
    # python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-false-sharing-app --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-false-sharing-app --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-false-sharing-app --benchmark_type parsec
    echo "::::::::::::::::COMPLETED::::::::::::::::::"
else
    echo "arg not provided"
fi

