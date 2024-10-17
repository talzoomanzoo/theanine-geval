#!/bin/bash

dataset=$1
version=$2

# Construct the folder path
folder_path="/home/intern/namyoung/theanine/outputs/${dataset}_ver${version}"

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder $folder_path does not exist."
    exit 1
fi

# Loop through each subdirectory in the folder path
for subdir in "$folder_path"/*/; do
    # Extract the subdir name
    subdir_name=$(basename "$subdir")
    # Run the output_count.py script for each subdirectory with count_results named after the subdir
    python count/output_count.py "$subdir" "${folder_path}/${subdir_name}_count_results.json"
done