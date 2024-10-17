#!/bin/bash

# # Check if the correct number of arguments is provided
# if [ "$#" -ne 3 ]; then
#     echo "Usage: $0 <input_file> <reference_files> <output_dir>"
#     exit 1
# fi

base_dir=/home/intern/mjgwak/theanine/session_5/session_5
dataset=cc
# Assign arguments to variables
INPUT_FILE=${dataset}_theanine.json
REFERENCE_FILES_1=${dataset}_ret_update_transform.json
REFERENCE_FILES_2=${dataset}_ret_summary_transform.json
REFERENCE_FILES_3=${dataset}_memochat_transform.json
REFERENCE_FILES_4=${dataset}_comedy_transform.json

OUTPUT_DIR=${dataset}_sampled
CSV_FILE=/home/intern/mjgwak/theanine/session_5/session_5/ours_rg.csv

# Run the sampling.py script with the provided arguments
python sampling.py ${base_dir}/${INPUT_FILE} ${base_dir}/${REFERENCE_FILES_1} ${base_dir}/${REFERENCE_FILES_2} ${base_dir}/${REFERENCE_FILES_3} ${base_dir}/${REFERENCE_FILES_4} ${base_dir}/${OUTPUT_DIR} ${dataset} ${CSV_FILE}