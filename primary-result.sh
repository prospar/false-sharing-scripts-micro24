#!/bin/bash

echo "Script for generating fig 14 of the paper: Applications with false sharing"
if [ -d "/home/prospar/prospar-micro-output/micro-false-sharing-app" && -d "/home/prospar/prospar-micro-output/micro-false-sharing-app/FS_MESI" && -d "/home/prospar/prospar-micro-output/micro-false-sharing-app/FS_MESI_DETECTION"] ; then
    echo "Directories for primary result of FSLite and FSDetect protocol exist"
else
    echo "Run the false-sharing-app-script.sh"
    bash false-sharing-app-script.sh false-sharing-app fslite-fsdetect 
fi

# copy the baseline result to manual fix output directory
if [ -d "/home/prospar/prospar-micro-output/micro-baseline-32KB" && -d "/home/prospar/prospar-micro-output/micro-baseline-32KB/MESI_Nonblocking"] ; then
    echo "Directories for 32 KB of MESI Nonblocking protocol exist"
    cp -r /home/prospar/prospar-micro-output/micro-baseline-32KB/MESI_Nonblocking /home/prospar/prospar-micro-output/micro-false-sharing-app/MESI_Nonblocking
else
    echo "Run the baseline-32KB-script.sh"
    # cp scripts/baseline-32KB-script.sh .
    bash baseline-32KB-script.sh false-sharing-app mesi-nb 1
    cp -r /home/prospar/prospar-micro-output/micro-baseline-32KB/MESI_Nonblocking /home/prospar/prospar-micro-output/micro-false-sharing-app/MESI_Nonblocking
fi

# generate the intermediate results for plots
python3 src/main.py --tasks result --trials 1 --bench huron-false-sharing --verbose 1 --protocol MESI_Nonblocking --workloadSize small  --outputDir micro-false-sharing-app --benchmark_type custom

# insert the call to script for plot generation
# TODO: check the below command, add two diff func call one for energy and one for performance
python3 src/graph_plotting_script/eval-fs-app.py /home/prospar/prospar-micro-result/micro-false-sharing-app/Stats_Avg.csv
echo "Primary result and fig script completed"