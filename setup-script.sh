#!/bin/bash
echo  "Initializing the experimental setup "

echo "Creating the output directory"
cd /home/prospar/prospar-micro-output
bash scripts/dir-creation-script.sh

echo "Building the protocols"
bash build-protocol-script.sh

echo "Extracting the image files"
bash extract-image-file.sh