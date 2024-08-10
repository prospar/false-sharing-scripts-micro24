#!/bin/bash

echo  "Running applications with the 40KB baseline"

if [ $1 ];
then
    echo "HURON application for MESI Nonblocking protocol"
    python3 src/main.py --tasks run --trials $2 --bench huron-lockless-toy --verbose 1 --protocol MESI_Nonblocking --workloadSize small --outputDir micro-baseline-40KB --benchmark_type custom
    python3 src/main.py --tasks run --trials $2 --bench huron-linear-reg --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type custom
    python3 src/main.py --tasks run --trials $2 --bench huron-ref-count --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-baseline-40KB --benchmark_type custom
    python3 src/main.py --tasks run --trials $2 --bench huron-boost-spinlock --verbose 1 --protocol MESI_Nonblocking --workloadSize small --outputDir micro-baseline-40KB --benchmark_type custom
    python3 src/main.py --tasks run --trials $2 --bench huron-string-match --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type custom
    python3 src/main.py --tasks run --trials $2 --bench huron-locked-toy --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-baseline-40KB --benchmark_type custom
    echo "HURON application for 40KB baseline completed"
    python3 src/main.py --tasks run --trials $2 --bench ESTM-specfriendly-tree --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-baseline-40KB --benchmark_type custom
    echo "Synchrobench for 40KB baseline completed"
    python3 src/main.py --tasks run --trials $2 --bench streamcluster --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type parsec
    python3 src/main.py --tasks run --trials $2 --bench canneal --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type parsec
    echo "PARSEC kernels for 40KB baseline completed"
    python3 src/main.py --tasks run --trials $2 --bench blackscholes --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-baseline-40KB --benchmark_type parsec
    python3 src/main.py --tasks run --trials $2 --bench bodytrack --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-baseline-40KB --benchmark_type parsec
    python3 src/main.py --tasks run --trials $2 --bench facesim --verbose 1 --protocol MESI_Nonblocking --workloadSize large  --outputDir micro-baseline-40KB --benchmark_type parsec
    python3 src/main.py --tasks run --trials $2 --bench fluidanimate --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type parsec
    python3 src/main.py --tasks run --trials $2 --bench swaptions --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-baseline-40KB --benchmark_type parsec
    echo "PARSEC apps for 40KB baseline completed"
else
    echo "arg not provided"
fi

