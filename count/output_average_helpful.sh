#!/bin/bash

version=$1

# folder1_path="./outputs/con_msc_ver${version}"
# folder2_path="./outputs/con_cc_ver${version}"

folder1_path="/home/intern/namyoung/theanine/outputs/msc_ver${version}"
folder2_path="/home/intern/namyoung/theanine/outputs/cc_ver${version}"

# Check if the folders exist
if [ ! -d "$folder1_path" ]; then
    echo "Error: Folder $folder1_path does not exist."
    exit 1
fi

if [ ! -d "$folder2_path" ]; then
    echo "Error: Folder $folder2_path does not exist."
    exit 1
fi

# Run the output_average.py script with the provided folders and output file name
# python ./count/output_average.py con_msc_ver${version} con_cc_ver${version} ver${version}.json
python count/output_average.py msc_ver${version} cc_ver${version} ver${version}.json
