#!/bin/bash

echo "Verifying all folder and executable available...."

if [ -d "/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-benchmarks" ]; then
    echo "benchmarks folder exists"
else
    echo "benchmarks folder does not exist"
fi

if [ -d "/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-resources" ]; then
    echo "full system resources folder exists"
else
    echo "full system resources does not exist"
fi

if [ -d "/home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing" ]; then
    echo "gem5 source code folder exists"
else
    echo "gem5 source code folder does not exist"
fi

if [ -d "/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-resources/disk-images" ]; then
    echo "disk images folder exists"
else
    echo "disk images folder does not exist"
fi

if [ -f "/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-resources/disk-images/parsec-img.tar.xz" ]; then
    echo "parsec compress image exists"
else
    echo "parsec compress image does not exist"
fi

if [ -f "/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-resources/disk-images/custom-vm-img.tar.xz" ]; then
    echo "custom compress image exists"
else
    echo "custom compress image does not exist"
fi
echo "Direcotry structure is valid...."

perf_val=$(cat /proc/sys/kernel/perf_event_paranoid)
# check if perf_event_paranoid is set to -1
if [ $perf_val -eq -1 ]; then
    echo "perf_event_paranoid is set to -1"
else
    echo "set perf_event_paranoid to -1 by running the following command"
    echo "sudo sysctl -w kernel.perf_event_paranoid=-1"
fi

