#!/bin/bash

echo "Script for generating out-of-order result"

if [ -d "${MICRO_OUT}/micro-ooo-comparison" ]; then
    echo "Directories for out-of-order expeirments exist"
else
    echo "Creating directories the out-of-order experiments"
    cd ${MICRO_OUT}
    mkdir micro-ooo-comparison
    mkdir micro-se-o3
    mkdir micro-se-inorder
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    cd ${MICRO_SCRIPT}
fi
$MICRO_

if [ -d "${MICRO_OUT}/micro-se-o3" ] && [ -d "${MICRO_OUT}/micro-se-o3/FS_MESI" ] && [ -d "${MICRO_OUT}/micro-se-o3/MESI_Nonblocking" ] && [ -d "${MICRO_OUT}/micro-se-inorder/FS_MESI" ] && [ -d "${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking" ]; then
    echo "Directories for out-of-order experiments exist"
else
    echo "Run the script for out-of-order result"
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    bash out-of-order-result.sh parsec-app two-protocol $1
fi

if [ -d "${MICRO_OUT}/micro-ooo-comparison" ]; then
    echo "Directories for out-of-order comparison exist"
else
    echo "Creating directories the out-of-order experiments"
    mkdir micro-ooo-comparison
    cp ${MICRO_SCRIPT}/config-script/config.ini.32KB ${MICRO_SCRIPT}/config.ini
    cp ${MICRO_OUT}/micro-se-inorder/FS_MESI ${MICRO_OUT}/micro-ooo-comparison/FS_MESI
    cp ${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking ${MICRO_OUT}/micro-ooo-comparison/MESI_Nonblocking
    cp ${MICRO_OUT}/micro-se-o3/FS_MESI ${MICRO_OUT}/micro-ooo-comparison/FS_MESI_o3
    cp ${MICRO_OUT}/micro-se-o3/MESI_Nonblocking ${MICRO_OUT}/micro-ooo-comparison/MESI_Nonblocking_o3
fi

# generate the intermediate results for plots
python3 src/main.py --tasks result --verbose 1 --protocol MESI_Nonblocking --outputDir micro-ooo-comparsion --benchmark_type custom

# insert the call to script for plot generation
python3 graph_script_artifact/plot-ooo-comparison.py ${MICRO_RES}/micro-ooo-comparison/Stats_Avg.csv
echo "Out-of-order result completed"