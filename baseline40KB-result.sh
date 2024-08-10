#!/bin/bash

echo "Script for Baseline 40KB result"
if [ -d "${MICRO_OUT}/micro-baseline-32KB" ] && [ -d "${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking" ]; then
    echo "Directories for 32 KB of MESI Nonblocking protocol exist"
else
    echo "Run the baseline-32KB-script.sh"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash baseline-32KB-script.sh false-sharing-app $1
fi

if [ -d "${MICRO_OUT}/micro-baseline-40KB" ] && [ -d "${MICRO_OUT}/micro-baseline-40KB/MESI_Nonblocking" ]; then
    echo "Directories for 40 KB of MESI Nonblocking protocol exist"
else
    echo "Run the baseline-40KB-script.sh"
    cp ${MICRO_SCRIPT}/config-script/config.ini.40KB ${MICRO_SCRIPT}/config.ini
    bash baseline-40KB-script.sh false-sharing-app $1
fi


# copy the baseline result to manual fix output directory
cp -r ${MICRO_OUT}/micro-baseline-40KB/MESI-Nonblocking ${MICRO_OUT}/micro-baseline-40KB/MESI_Nonblocking_40KB
cp -r ${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking ${MICRO_OUT}/micro-baseline-40KB/MESI_Nonblocking

# generate the intermediate results for plots
python3 src/main.py --tasks result --verbose 1 --outputDir micro-baseline-40KB --benchmark_type custom

# insert the call to script for plot generation
python3 src/graph_plotting_script/intro-plot.py ${MICRO_RES}/micro-baseline-40KB/Stats_Avg.csv
