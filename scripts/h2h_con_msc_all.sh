# theanine/scripts/h2h_cc_theanine.sh
latest_version=$(ls ./outputs | grep -Eo 'con_msc_ver[0-9]+' | sort -V | tail -n 1)
if [ -z "$latest_version" ]; then
    new_version="con_msc_ver0"
else
    version_number=$(echo $latest_version | grep -Eo '[0-9]+')
    new_version="con_msc_ver$((version_number + 1))"
fi

python ./geval_h2h.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_theanine.json' './session_5/session_5/msc_comedy_transform.json' \
    --prompt './prompts/h2h_con.txt' \
    --save_dir "./outputs/$new_version/msc_h2h_comedy" \

# python ./geval_h2h.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine.json' './session_5/session_5/msc_memochat_transform.json' \
#     --prompt './prompts/h2h_con.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_memochat" \

# python ./geval_h2h.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine.json' './session_5/session_5/msc_ret_summary_transform.json' \
#     --prompt './prompts/h2h_con.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_ret_summary" \

# python ./geval_h2h.py \
#     --memory_path './memory_file/msc_memory_file.json' \
#     --input_paths './session_5/session_5/msc_theanine.json' './session_5/session_5/msc_ret_update_transform.json' \
#     --prompt './prompts/h2h_con.txt' \
#     --save_dir "./outputs/$new_version/msc_h2h_ret_update" \