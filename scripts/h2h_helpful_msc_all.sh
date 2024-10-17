# theanine/scripts/h2h_cc_theanine.sh
latest_version=$(ls ./outputs | grep -Eo 'msc_ver[0-9]+' | sort -V | tail -n 1)
if [ -z "$latest_version" ]; then
    new_version="msc_ver0"
else
    version_number=$(echo $latest_version | grep -Eo '[0-9]+')
    new_version="msc_ver$((version_number + 1))"
fi

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine_sample.json' './session_5/session_5/msc_comedy_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_helpful_comedy_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine_sample.json' './session_5/session_5/msc_memochat_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_helpful_memochat_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine_sample.json' './session_5/session_5/msc_ret_summary_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_helpful_ret_summary_mem" \

# python ./geval_h2h_helpful.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine_sample.json' './session_5/session_5/msc_ret_update_sample.json' \
#     --prompt './prompts/h2h_mem_helpful_ny.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_helpful_ret_update_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_sampled/msc_theanine_sampled.json' './session_5/session_5/msc_sampled/msc_comedy_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/msc_h2h_helpful_comedy_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_sampled/msc_theanine_sampled.json' './session_5/session_5/msc_sampled/msc_memochat_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/msc_h2h_helpful_memochat_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_sampled/msc_theanine_sampled.json' './session_5/session_5/msc_sampled/msc_ret_summary_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/msc_h2h_helpful_ret_summary_mem" \

python ./geval_h2h_helpful.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_sampled/msc_theanine_sampled.json' './session_5/session_5/msc_sampled/msc_ret_update_transform.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir "./outputs/$new_version/msc_h2h_helpful_ret_update_mem" \