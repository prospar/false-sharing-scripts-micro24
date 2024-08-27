#!/bin/bash

echo "Script for generating fig 14 of the paper: Applications with false sharing"

if [ -d "${MICRO_OUT}/micro-false-sharing-app" ] && [ -d "${MICRO_OUT}/micro-false-sharing-app/FS_MESI" ] && [ -d "${MICRO_OUT}/micro-false-sharing-app/FS_MESI_DETECTION"]; then
    echo "Directories for primary result of FSLite and FSDetect protocol exist"
else
    echo "Run the false-sharing-app-script.sh"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fslite-script.sh false-sharing-app fslite $1
    bash false-sharing-fsdetect-script.sh false-sharing-app fsdetect $1
fi

# copy the baseline result to manual fix output directory
if [ -d "${MICRO_OUT}/micro-baseline-32KB" ] && [ -d "${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking"]; then
    echo "Directories for 32 KB of MESI Nonblocking protocol exist"
    cp -r ${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking ${MICRO_OUT}/micro-false-sharing-app/MESI_Nonblocking
else
    echo "Run the baseline-32KB-script.sh"
    # cp scripts/baseline-32KB-script.sh .
    bash baseline-32KB-script.sh false-sharing-app mesi-nb $1
    cp -r ${MICRO_OUT}/micro-baseline-32KB/MESI_Nonblocking ${MICRO_OUT}/micro-false-sharing-app/MESI_Nonblocking
fi

# generate the intermediate results for plots
python3 src/main.py --tasks result --verbose 1 --protocol MESI_Nonblocking --outputDir micro-false-sharing-app --benchmark_type custom

# insert the call to script for plot generation
# TODO: check the below command, add two diff func call one for energy and one for performance
python3 graph_script_artifact/eval-fs-app-plot.py ${MICRO_RES}/micro-false-sharing-app/Stats_Avg.csv
echo "Primary result and fig script completed in graph plotting script folder"