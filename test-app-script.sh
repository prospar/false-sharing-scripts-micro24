#!/bin/bash

echo  "Running false sharing application started"

if [ $1 ] && [ $2 ];
then
    echo "false sharing set for all three protocol"
    python3 src/main.py --tasks run --trials 1 --bench false-sharing --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-test-app --benchmark_type custom
    python3 src/main.py --tasks run --trials 1 --bench false-sharing --verbose 1 --protocol FS_MESI_DETECTION --workloadSize small  --outputDir micro-test-app --benchmark_type custom
    python3 src/main.py --tasks run --trials 1 --bench false-sharing --verbose 1 --protocol FS_MESI --workloadSize small  --outputDir micro-test-app --benchmark_type custom
    echo "Three protocol for lockles-toy completed"
    echo "::::::::::::::::COMPLETED::::::::::::::::::"
else
    echo "arg not provided"
fi

echo "generating final csv for stats"
python3 src/main.py --tasks result --verbose 1 --protocol FS_MESI --outputDir micro-test-app
echo "Done with csv generation"
if [ -f "${MICRO_RES}/micro-test-app/Stats_Avg.csv" ]; then
    echo "Stats files generated successfully"
else
    echo "Stats_Avg.csv not generated, report the issue"
fi
