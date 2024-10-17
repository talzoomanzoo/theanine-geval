# theanine/scripts/h2h_cc_theanine.sh
latest_version=$(ls ./outputs | grep -Eo 'cc_ver[0-9]+' | sort -V | tail -n 1)
if [ -z "$latest_version" ]; then
    new_version="cc_ver0"
else
    version_number=$(echo $latest_version | grep -Eo '[0-9]+')
    new_version="cc_ver$((version_number + 1))"
fi

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/cc_memory_file.json' \
#     --input_paths './session_5/session_5/cc_theanine_sample.json' './session_5/session_5/cc_comedy_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/cc_h2h_helpful_comedy_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/cc_memory_file.json' \
#     --input_paths './session_5/session_5/cc_theanine_sample.json' './session_5/session_5/cc_memochat_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/cc_h2h_helpful_memochat_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/cc_memory_file.json' \
#     --input_paths './session_5/session_5/cc_theanine_sample.json' './session_5/session_5/cc_ret_summary_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/cc_h2h_helpful_ret_summary_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/cc_memory_file.json' \
#     --input_paths './session_5/session_5/cc_theanine_sample.json' './session_5/session_5/cc_ret_update_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/cc_h2h_helpful_ret_update_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/cc_memory_file.json' \
    --input_paths './session_5/session_5/cc_sampled/cc_theanine_sampled.json' './session_5/session_5/cc_sampled/cc_comedy_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/cc_h2h_helpful_comedy_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/cc_memory_file.json' \
    --input_paths './session_5/session_5/cc_sampled/cc_theanine_sampled.json' './session_5/session_5/cc_sampled/cc_memochat_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/cc_h2h_helpful_memochat_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/cc_memory_file.json' \
    --input_paths './session_5/session_5/cc_sampled/cc_theanine_sampled.json' './session_5/session_5/cc_sampled/cc_ret_summary_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/cc_h2h_helpful_ret_summary_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/cc_memory_file.json' \
    --input_paths './session_5/session_5/cc_sampled/cc_theanine_sampled.json' './session_5/session_5/cc_sampled/cc_ret_update_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/cc_h2h_helpful_ret_update_mem" \