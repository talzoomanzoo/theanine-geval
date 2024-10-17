# theanine/scripts/h2h_cc_theanine.sh
python ./geval_h2h_helpful.py \
    --memory_path './memory_file/cc_memory_file.json' \
    --input_paths './session_5/session_5/cc_theanine_sample.json' './session_5/session_5/cc_comedy_sample.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir './outputs/cc_h2h_helpful_comedy_mem' \
    # --num_sample 59
