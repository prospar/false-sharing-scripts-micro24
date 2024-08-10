#!/bin/bash

echo "Script for SAM exploration result"

if [ -d "${MICRO_OUT}/micro-reader-optimization" ] && [ -d "${MICRO_OUT}/micro-reader-optimization/FS_MESI" ]; then
    echo "Directories for fc-ic 32 expeirments exist"
else
    echo "Running the sam 256 experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.opt-reader ${MICRO_SCRIPT}/config.ini
    bash false-sharing-app-sam-script.sh false-sharing-app fslite ${1}
fi


if [ -d "${MICRO_OUT}/micro-false-sharing-app" ] && [ -d "${MICRO_OUT}/micro-micro-false-sharing-app/FS_MESI" ]; then
    echo "Directories for FS MESI with granularity 1 exist"
else
    echo "Running the fslite experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fslite-script.sh fslite false-sharing-app $1
fi

cp -r ${MICRO_OUT}/micro-reader-optimization/FS_MESI ${MICRO_OUT}/micro-reader-optimization/FS_MESI_Opt
cp -r ${MICRO_OUT}/micro-false-sharing-app/FS_MESI ${MICRO_OUT}/micro-reader-optimization/FS_MESI

# remove the streamcluster from the output directory
for i in {1..$1}
do
    rm -rf ${MICRO_OUT}/micro-reader-optimization/FS_MESI/large/${i}/streamcluster
done

cp ${MICRO_SCRIPT}/config-script/config.ini.opt-reader ${MICRO_SCRIPT}/config.ini
# generate the intermediate results for plots
python3 src/main.py --tasks result ---verbose 1 --protocol FS_MESI --outputDir micro-reader-optimization

# insert the call to script for plot generation
python3 src/graph_plotting_script/plot-opt-reader-study.py "${MICRO_RES}/micro-reader-optimization/Stats_Avg.csv"