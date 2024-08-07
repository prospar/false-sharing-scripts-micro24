#!/bin/bash

echo "Script for fc-ic result"

if [ -d "${MICRO_OUT}/micro-fc-ic-32" && -d "${MICRO_OUT}/micro-fc-ic-32/FS_MESI" ] ; then
    echo "Directories for fc-ic 32 expeirments exist"
else
    echo "Run the fc-ic-32 experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.fc-ic-32 ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fc-ic-script.sh false-sharing-app  repair-detect-protocol 32 $1
fi

# && -d "${MICRO_OUT}/micro-fc-ic-64"
if [ -d "${MICRO_OUT}/micro-fc-ic-64" && -d "${MICRO_OUT}/micro-fc-ic-64/FS_MESI" ] ; then
    echo "Directories for fc-ic 64 experiments exist"
else
    echo "Running the fc-ic-64 experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.fc-ic-64 ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fc-ic-script.sh false-sharing-app  repair-detect-protocol 64 $1
fi

if [ -d "${MICRO_OUT}/micro-false-sharing-app" && -d "${MICRO_OUT}/micro-micro-false-sharing-app/FS_MESI"] ; then
    echo "Directories for FS MESI with granularity 1 exist"
else
    echo "Running the fslite experiments"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash false-sharing-fslite-script.sh fslite false-sharing app $1
fi

cp -r ${MICRO_OUT}/micro-fc-ic-64/FS_MESI ${MICRO_OUT}/micro-fc-ic-output/FS_MESI_64
cp -r ${MICRO_OUT}/micro-fc-ic-32/FS_MESI ${MICRO_OUT}/micro-fc-ic-output/FS_MESI_32
cp -r ${MICRO_OUT}/micro-false-sharing-app/FS_MESI ${MICRO_OUT}/micro-fc-ic-output/FS_MESI

# remove the streamcluster from the output directory
for i in {1..$1}
do
    rm -rf ${MICRO_OUT}/micro-fc-ic-output/FS_MESI/large/${i}/streamcluster
done

cp ${MICRO_SCRIPT}/config-script/config.ini.fc-ic-32 ${MICRO_SCRIPT}/config.ini
# generate the intermediate results for plots
python3 src/main.py --tasks result ---verbose 1 --protocol FS_MESI --outputDir micro-fc-ic-output

# insert the call to script for plot generation
python3 src/graph_plotting_script/plot-fcic-study.py "${MICRO_RES}/micro-fc-ic-ouptut/Stats_Avg.csv"