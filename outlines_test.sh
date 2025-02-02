module add cuda11.8/toolkit/11.8.0

output_dir='/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/NER/ReDocRED/'
mkdir -p ${output_dir}

# 输入要执行的命令，例如 ./hello 或 python test.py 等
python ./src/inference.py \
    --stage sft \
    --model_name_or_path '/scratch2/nlp/plm/Meta-Llama-3-8B-Instruct/' \
    --model_name 'llama' \
    --template 'alpaca' \
    --do_predict \
    --input_file '/scratch2/nlp/UIE/data/document/Re-DocRED/IEPile_format/NER/test_iepile.json' \
    --output_file '/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/NER/ReDocRED/llama3-8b-outlines.json' \
    --finetuning_type lora \
    --output_dir 'lora/test' \
    --predict_with_generate \
    --cutoff_len 512 \
    --bf16 \
    --max_new_tokens 300 \
	  --load_best_model_at_end False \
	  --enable_outlines True