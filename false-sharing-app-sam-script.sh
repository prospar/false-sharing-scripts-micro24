#!/bin/bash

echo  "Running false sharing application started"

if [ $1 ];
then
    echo "false sharing set for all applications with 256 SAM entry"
    python3 src/main.py --tasks run --trials $3 --bench huron-lockless-toy --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol for lockles-toy completed"
    python3 src/main.py --tasks run --trials $3 --bench huron-linear-reg --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for linear-reg completed"
    python3 src/main.py --tasks run --trials $3 --bench huron-ref-count --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for ref-count completed"
    python3 src/main.py --tasks run --trials $3 --bench huron-boost-spinlock --verbose 1 --protocol FS_MESI --workloadSize small --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for boost spinlock completed"
    python3 src/main.py --tasks run --trials $3 --bench huron-string-match --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for string match completed"
    python3 src/main.py --tasks run --trials $3 --bench huron-locked-toy --verbose 1 --protocol FS_MESI --workloadSize medium  --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for locked toy completed"
    python3 src/main.py --tasks run --trials $3 --bench ESTM-specfriendly-tree --verbose 1 --protocol FS_MESI --workloadSize medium --outputDir micro-sam --benchmark_type custom
    echo "FS_MESI protocol with 256 SAM entry for ESTM specfriendly tree completed"
    echo "::::::::::::::::COMPLETED::::::::::::::::::"
else
    echo "arg not provided"
fi

