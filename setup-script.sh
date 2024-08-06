#!/bin/bash
echo  "Initializing the experimental setup "

if [ -d $MICRO_OUT ]; then
    echo "output directory exists"
else
    echo "output directory does not exist, creating"
    mkdir ${MICRO_OUT}
fi
cd ${MICRO_OUT}
bash scripts/dir-creation-script.sh

echo "Building the protocols"
cd ${MICRO_SCRIPT}
bash build-protocol-script.sh

echo "Extracting the image files"
cd ${MICRO_RESOURCE}/disk-images
bash extract-image-file.sh

cd ${MICRO_SCRIPT}
echo "Done Setting up the gem5 environment"