#!/bin/bash
echo $"script for generating fig 17"

if [ -d "${MICRO_OUT}/micro-compare-huron" ]; then
    echo "Directories for huron output exist"
else
    echo "Creating directory"
    mkdir ${MICRO_OUT}/micro-compare-huron
fi

# run the huron false sharing application
bash compare-huron-script.sh fslite huron $1

cd ${MICRO_OUT}/micro-compare-huron


cp -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron
cp -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual
cp -r ${MICRO_OUT}/micro-compare-huron/FS_MESI ${MICRO_OUT}/micro-compare-huron/FS_MESI
# generate the intermediate results for plots

cd ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking

# rename huron application
for i in $(seq 1 $i); do
    # perform operations on each folder
    # replace the following line with your desired operations
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/small/${i}/huron_ll_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/small/${i}/huron_bs_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/medium/${i}/huron_lt_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/medium/${i}/huron_rc_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/large/${i}/huron_sm_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/large/${i}/huron_lr_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/small/${i}/huron_ll ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/small/${i}/huron_ll_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/small/${i}/huron_bs ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/small/${i}/huron_bs_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/medium/${i}/huron_lt ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/medium/${i}/huron_lt_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/medium/${i}/huron_rc ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/medium/${i}/huron_rc_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/large/${i}/huron_sm ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/large/${i}/huron_sm_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_huron/large/${i}/huron_lr ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking/large/${i}/huron_lr_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr_man
done

# cleanup MESI manual manual fix application
for i in $(seq 1 $i); do
    # perform operations on each folder
    # replace the following line with your desired operations
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm_base
    mv -r ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr_man ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr_base
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr
done

# cleanup MESI Nonblocking protocol  application
for i in $(seq 1 $i); do
    # perform operations on each folder
    # replace the following line with your desired operations
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr_man
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_ll
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/small/${i}/huron_bs
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_lt
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/medium/${i}/huron_rc
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_sm
    rm -rf ${MICRO_OUT}/micro-compare-huron/MESI_Nonblocking_manual/large/${i}/huron_lr
done

# prcoess the stas to create csv
python3 src/main.py --tasks result --verbose 1 --protocol FS_MESI --outputDir micro-compare-huron

# insert the call to script for plot generation
python3 graph_script_artifact/plot-huron-comparison.py "${MICRO_RES}/micro-compare-huron/Stats_Avg.csv"