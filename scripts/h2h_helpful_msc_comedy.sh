# theanine/scripts/h2h_cc_theanine.sh
python ./geval_h2h_helpful.py \
    --memory_path './memory_file/msc_memory_file.json' \
    --input_paths './session_5/session_5/msc_theanine_sample.json' './session_5/session_5/msc_comedy_sample.json' \
    --prompt './prompts/h2h_mem_helpful_ny.txt' \
    --save_dir './outputs/msc_h2h_helpful_comedy_mem' \
    # --num_sample 59
