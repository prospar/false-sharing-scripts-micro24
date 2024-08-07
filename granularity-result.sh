#!/bin/bash

echo "Script for granularity result"

# && -d "${MICRO_OUT}/micro-granularity-2/FS_MESI_DETECTION"
if [ -d "${MICRO_OUT}/micro-granularity-2" && -d "${MICRO_OUT}/micro-granularity-32/FS_MESI" ] ; then
    echo "Directories for granularity 2 expeirments exist"
else
    echo "Running granualrity-2 experiments"
    cp ${MICRO_SCRIPT}/scripts/config.ini.tw-2 ${MICRO_SCRIPT}/config.ini
    bash false-sharing-granularity-script.sh fslite false-sharing-app 2 $1
fi

# && -d "${MICRO_OUT}/micro-granularity-2/FS_MESI_DETECTION"
if [ -d "${MICRO_OUT}/micro-granularity-4" && -d "${MICRO_OUT}/micro-granularity-4/FS_MESI" ] ; then
    echo "Directories for granularity 4 expeirments exist"
else
    echo "Run the granularity-4 experiment"
    cp ${MICRO_SCRIPT}/scripts/config.ini.tw-4 ${MICRO_SCRIPT}/config.ini
    bash false-sharing-granularity-script.sh fslite false-sharing-app 4 $1
fi

if [ -d "${MICRO_OUT}/micro-granularity-output" ]; then
    echo "Directories for granularity output exist"
else
    echo "Creating directory"
    mkdir ${MICRO_OUT}/micro-granularity-output
fi


# copy the baseline result to manual fix output directory
cp -r ${MICRO_OUT}/micro-granularity-2/FS_MESI ${MICRO_OUT}/micro-granularity-output/FS_MESI_2
cp -r ${MICRO_OUT}/micro-granularity-4/FS_MESI ${MICRO_OUT}/micro-granularity-output/FS_MESI_4
if [ -d ${MICRO_OUT}/micro-false-sharing-app/FS_MESI ]; then 
    echo "False Sharing app result with granularity 1 exists"
else
    echo "running FS MESI with granularity 1"
    cp ${MICRO_SCRIPT}/scripts/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fslite-script.sh fslite false-sharing-app $1
fi

cp ${MICRO_SCRIPT}/scripts/config.ini.tw-4 ${MICRO_SCRIPT}/config.ini
cp -r ${MICRO_OUT}/micro-false-sharing-app/FS_MESI ${MICRO_OUT}/micro-granularity-output/FS_MESI

# generate the intermediate results for plots
python3 src/main.py --tasks result --verbose 1 --protocol FS_MESI --outputDir micro-granularity-output

# insert the call to script for plot generation
python3 src/graph_plotting_script/plot-granularity-study.py "${MICRO_RES}/micro-granularity-output/Stats_Avg.csv"