CUDA_VISIBLE_DEVICES=0,1 python src/inference.py \
    --stage sft \
    --model_name_or_path '/scratch2/nlp/plm/Llama-2-13b-chat-hf/' \
    --checkpoint_dir '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/lora/llama2-13b-ace05-continue/checkpoint-2695' \
    --model_name 'llama' \
    --template 'llama2' \
    --do_predict \
    --input_file '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/zjunlp/iepile/IE-en/RE/ADE_corpus/test.json' \
    --output_file 'results/llama2-13b-continue_re.json' \
    --finetuning_type lora \
    --output_dir 'lora/test' \
    --predict_with_generate \
    --cutoff_len 512 \
    --bf16 \
    --max_new_tokens 300 
