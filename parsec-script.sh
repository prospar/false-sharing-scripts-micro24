#!/bin/bash

echo  "Running parsec experiments"

if [ $1 ] && [ $2 ];
then
    echo "launching experiment for parsec benchmarks"
    python3 src/main.py --tasks run --trials $3 --bench blackscholes --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench bodytrack --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench canneal --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench facesim --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench fluidanimate --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench swaptions --verbose 1 --protocol FS_MESI --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # echo "start detection protocol"
    # python3 src/main.py --tasks run --trials $3 --bench blackscholes --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench bodytrack --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench canneal --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench facesim --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench fluidanimate --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # # python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench swaptions --verbose 1 --protocol FS_MESI_DETECTION --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    echo "starting baseline protocol"
    python3 src/main.py --tasks run --trials $3 --bench blackscholes --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench bodytrack --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench canneal --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench facesim --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench fluidanimate --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    # python3 src/main.py --tasks run --trials $3 --bench streamcluster --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    python3 src/main.py --tasks run --trials $3 --bench swaptions --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-parsec --benchmark_type parsec
    echo "Completed experiments for parsec benchmarks"
else
    echo "arg not provided"
fi
