#!/bin/bash

echo "Script for introduction result"
if [ -d "${MICRO_OUT}/micro-baseline-32KB" && -d "${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking"] ; then
    echo "Directories for 32 KB of MESI Nonblocking protocol exist"
else
    echo "Run the baseline-32KB-script.sh"
    cp config-script/config.ini.32KB config.ini
    bash baseline-32KB-script.sh false-sharing-app $1
fi

if [ -d "${MICRO_OUT}/micro-manual-fix" && -d "${MICRO_OUT}/micro-manual-fix/MESI_Nonblocking_manual"] ; then
    echo "Directories for manual fix of MESI Nonblocking protocol exist"
else
    echo "Running the manual-fix-script.sh"
    bash manual-fix-script.sh manualfix-false-sharing-app $1
fi

# copy the baseline result to manual fix output directory
cp -r ${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking ${MICRO_OUT}/micro-manual-fix/MESI_Nonblocking

# generate the intermediate results for plots
python3 src/main.py --tasks result --trials 1 --bench huron-false-sharing --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-manual-fix --benchmark_type custom

# insert the call to script for plot generation
python3 src/graph_plotting_script/intro-plot.py /home/prospar/prospar-micro-result/micro-manual-fix/Stats_Avg.csv
