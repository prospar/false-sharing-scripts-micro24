#!/bin/bash

cd  /home/prospar/micro-virtualenv/gem5-fs-resources/disk-images

if [ -f "./parsec-img.tar.xz" ]; then
    echo "parsec-img.tar.xz exists"
else
    echo "parsec-img.tar.xz does not exist"
fi
if [ -f "./custom-vm-img.tar.xz" ]; then
    echo "custom-vm-img.tar.xz exists"
else
    echo "custom-vm-img.tar.xz does not exist"
fi
tar -xf parsec-img.tar.xz
tar -xf custom-vm-img.tar.xz

echo "extracted parsec-img.tar.xz and custom-vm-img.tar.xz"
#rm parsec-img.tar.xz
#rm custom-vm-img.tar.xz