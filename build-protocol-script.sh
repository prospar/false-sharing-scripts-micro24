#!/bin/bash

# cd /home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing

echo "Building all three protocols"
python3 src/main.py --tasks build_gem5 --trials 1 --bench false-sharing --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-result --benchmark_type custom
if [ -f "/home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing/build/X86_MESI_Nonblocking/gem5.opt" ]; then
    echo "MESI Nonblocking build successful"
else
    echo "MESI Nonblocking build failed"
fi
python3 src/main.py --tasks build_gem5 --trials 1 --bench false-sharing --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small  --outputDir micro-result --benchmark_type custom
if [ -f "/home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing/build/X86_FS_MESI_DETECTION/gem5.opt" ]; then
    echo "FS MESI Detection build successful"
else
    echo "FS Detect build failed"
fi
python3 src/main.py --tasks build_gem5 --trials 1 --bench false-sharing --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-results --benchmark_type custom
if [ -f "/home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing/build/X86_FS_MESI/gem5.opt" ]; then
    echo "FS MESI build successful"
else
    echo "FS MESI build failed"
fi

# cd /home/prospar/micro-virtualenv/false-sharing-scripts-micro24