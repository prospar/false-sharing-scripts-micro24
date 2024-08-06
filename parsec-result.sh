#!/bin/bash

echo "Script for generating fig 15 of the paper : PARSEC result "
# && -d "${MICRO_OUT}/micro-parsec/FS_MESI_DETECTION"
if [ -d "${MICRO_OUT}/micro-parsec" && -d "${MICRO_OUT}/micro-parsec/FS_MESI" && -d "${MICRO_OUT}/micro-parsec/MESI_Nonblocking" ] ; then
    echo "Directories for parsec result of all three protcol exist"
else
    echo "Run the false-sharing-app-script.sh"
    bash parsec-script.sh parsec-app three-protocol $1
fi

# generate the intermediate results for plots
python3 src/main.py --tasks result --trials 1 --bench huron-false-sharing --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-parsec --benchmark_type custom

# insert the call to script for plot generation
# TODO: check the below command, add two diff func call one for energy and one for performance
python3 src/graph_plotting_script/parsec-plot.py ${MICRO_RES}/micro-parsec/Stats_Avg.csv
echo "Parsec result and fig script completed"