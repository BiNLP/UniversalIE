output_dir='/home/chenzhb/Workspaces/UniversalIE/results/NER/DWIE/'
mkdir -p ${output_dir}

statistic_file="/home/chenzhb/Workspaces/UniversalIE/statistic/DWIE/NER_split6/"
mkdir -p ${statistic_file}

# 输入要执行的命令，例如 ./hello 或 python test.py 等
CUDA_VISIBLE_DEVICES=0,1 python ../../src/inference.py \
    --stage sft \
    --model_name_or_path '/home/chenzhb/Workspaces/LLMs/Meta-Llama-3-8B-Instruct/' \
    --checkpoint_dir '/home/chenzhb/Workspaces/UniversalIE/lora/llama3-8b-ALL-drop50/checkpoint-3000/' \
    --model_name 'llama' \
    --template 'alpaca' \
    --do_predict \
    --input_file '/home/chenzhb/Workspaces/Datasets/UIE/DWIE/IEPile_format/NER/test.json' \
    --output_file '/home/chenzhb/Workspaces/UniversalIE/results/NER/DWIE/llama3-8b-drop-50.json' \
    --finetuning_type lora \
    --output_dir 'lora/test' \
    --predict_with_generate \
    --cutoff_len 6000 \
    --bf16 \
    --max_new_tokens 3000 \
	--load_best_model_at_end False \
    --statistic_len True \
    --statistic_file ${statistic_file}

