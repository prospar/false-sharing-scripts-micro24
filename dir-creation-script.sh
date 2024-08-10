#!/bin/bash

echo "Creating directories for micro-results"

cd ${MICRO_OUT}
mkdir micro-baseline-32KB
mkdir micro-manual-fix
mkdir micro-introduction
mkdir micro-false-sharing-app
mkdir micro-parsec
mkdir micro-fc-ic-32
mkdir micro-fc-ic-64
mkdir micro-fc-ic-output
mkdir micro-granularity-2
mkdir micro-granularity-4
mkdir micro-granularity-output
mkdir micro-sam
mkdir micro-reader-optimization
mkdir micro-baseline-40KB
mkdir micro-se-o3
mkdir micro-se-inorder
mkdir micro-ooo-comparison
echo "Directories created for micro-results"
cd ${MICRO_SCRIPT}