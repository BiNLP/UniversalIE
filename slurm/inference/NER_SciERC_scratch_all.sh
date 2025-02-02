output_dir='/home/chenzhb/Workspaces/UniversalIE/results/NER/SciERC/'
mkdir -p ${output_dir}

# 输入要执行的命令，例如 ./hello 或 python test.py 等
CUDA_VISIBLE_DEVICES=0,1 python ../../src/inference.py \
    --stage sft \
    --model_name_or_path '/home/chenzhb/Workspaces/LLMs/Meta-Llama-3-8B-Instruct/' \
    --model_name 'llama' \
    --template 'alpaca' \
    --do_predict \
    --input_file '/home/chenzhb/Workspaces/Datasets/UIE/SciERC/IEPile_format/NER/test_iepile.json' \
    --output_file '/home/chenzhb/Workspaces/UniversalIE/results/NER/SciERC/llama3-8b.json' \
    --finetuning_type lora \
    --output_dir 'lora/test' \
    --predict_with_generate \
    --cutoff_len 512 \
    --bf16 \
    --max_new_tokens 300 \
	  --load_best_model_at_end False


python ../../ie2instruction/eval_func.py \
  --path1 /home/chenzhb/Workspaces/UniversalIE/results/NER/SciERC/llama3-8b.json \
  --task NER

