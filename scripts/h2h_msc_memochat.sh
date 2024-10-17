# theanine/scripts/h2h_cc_theanine.sh

version=$1
folder="con_msc_ver${version}"

python ./geval_h2h.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths '/home/intern/mjgwak/theanine/session_5/session_5/msc_sampled/msc_theanine_sampled.json' '/home/intern/mjgwak/theanine/session_5/session_5/msc_sampled/msc_memochat_transform.json' \
    --prompt './prompts/h2h_con.txt' \
    --save_dir "./outputs/${folder}/msc_h2h_memochat" \
    # --num_sample 59