#!/bin/bash

echo "Script for SAM exploration result"

if [ -d "${MICRO_OUT}/micro-sam" ] && [ -d "${MICRO_OUT}/micro-sam/FS_MESI" ]; then
    echo "Directories for fc-ic 32 expeirments exist"
else
    echo "Running the sam 256 experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.sam256 ${MICRO_SCRIPT}/config.ini
    bash false-sharing-app-sam-script.sh false-sharing-app fslite ${1}
fi


if [ -d "${MICRO_OUT}/micro-false-sharing-app" ] && [ -d "${MICRO_OUT}/micro-micro-false-sharing-app/FS_MESI" ]; then
    echo "Directories for FS MESI with granularity 1 exist"
else
    echo "Running the fslite experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fslite-script.sh fslite false-sharing-app $1
fi

cp -r ${MICRO_OUT}/micro-sam/FS_MESI ${MICRO_OUT}/micro-sam/FS_MESI_256
cp -r ${MICRO_OUT}/micro-false-sharing-app/FS_MESI ${MICRO_OUT}/micro-sam/FS_MESI

# remove the streamcluster from the output directory
for i in {1..$1}
do
    rm -rf ${MICRO_OUT}/micro-sam/FS_MESI/large/${i}/streamcluster
done

cp ${MICRO_SCRIPT}/config-script/config.ini.sam256 ${MICRO_SCRIPT}/config.ini
# generate the intermediate results for plots
python3 src/main.py --tasks result ---verbose 1 --protocol FS_MESI --outputDir micro-sam

# insert the call to script for plot generation
python3 graph_script_artifact/plot-sam-study.py "${MICRO_RES}/micro-sam/Stats_Avg.csv"