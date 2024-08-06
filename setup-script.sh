#!/bin/bash
echo  "Initializing the experimental setup "

echo "Creating the output directory"
cd /home/prospar/prospar-micro-output
bash scripts/dir-creation-script.sh

echo "Building the protocols"
cd /home/prospar/false-sharing-scripts-micro24
bash build-protocol-script.sh

echo "Extracting the image files"
cd /home/prospar/false-sharing-micro24/false-sharing-resources/disk-images
bash extract-image-file.sh

cd /home/prospar/false-sharing-scripts-micro24
echo "Done Setting up the gem5 environment"