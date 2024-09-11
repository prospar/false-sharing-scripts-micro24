#!/bin/bash

echo "Script for Baseline 128KB result"
if [ -d "${MICRO_OUT}/micro-baseline-32KB" ] && [ -d "${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking" ]; then
    echo "Directories for 32 KB of MESI Nonblocking protocol exist"
else
    echo "Run the baseline-32KB-script.sh"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash baseline-32KB-script.sh false-sharing-app $1
fi

if [ -d "${MICRO_OUT}/micro-baseline-128KB" ] && [ -d "${MICRO_OUT}/micro-baseline-128KB/MESI_Nonblocking" ]; then
    echo "Directories for 128KB of MESI Nonblocking protocol exist"
else
    echo "Run the baseline-128KB-script.sh"
    cp ${MICRO_SCRIPT}/config-script/config.ini.128KB ${MICRO_SCRIPT}/config.ini
    bash baseline-128KB-script.sh false-sharing-app $1
fi


# copy the baseline result to manual fix output directory
cp -r ${MICRO_OUT}/micro-baseline-128KB/MESI-Nonblocking ${MICRO_OUT}/micro-baseline-128KB/MESI_Nonblocking_128KB
cp -r ${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking ${MICRO_OUT}/micro-baseline-128KB/MESI_Nonblocking

# generate the intermediate results for plots
python3 src/main.py --tasks result --verbose 1 --outputDir micro-baseline-128KB --benchmark_type custom

# insert the call to script for plot generation
python3 src/graph_plotting_script/intro-plot.py ${MICRO_RES}/micro-baseline-128KB/Stats_Avg.csv
