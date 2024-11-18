#!/bin/bash
#SBATCH -J UIE-EE-DocEE               # 作业名为 xxx
#SBATCH -o ./msg_out/Inf_ScratchDocRED_DocEE_EE.out         # 屏幕上的输出文件重定向到 xxx.out
#SBATCH -p HGX                   # 作业提交的分区为 HGX
#SBATCH --qos=lv0b               # 作业使用的 QoS 为 lv0b
#SBATCH -N 1                      # 作业申请 1 个节点
#SBATCH --ntasks-per-node=1       # 单节点启动的进程数为 1
#SBATCH --cpus-per-task=16        # 单任务使用的 CPU 核心数为 4
#SBATCH -t 48:00:00                # 任务运行的最长时间为5 小时
#SBATCH --gres=gpu:2              # 单个节点使用 2 块 GPU 卡
#SBATCH --mem=160G                  #--mem=<size[units]>：设定每个节点的内存大小，后缀可以为[K|M|G|T]，默认为MB
#SBATCH --account=research

# 设置运行环境
# module add /miniconda     # 添加 anaconda/3-5.0.0.1 模块

module add cuda11.8/toolkit/11.8.0


output_dir='/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/EE/DocEE/'
mkdir -p ${output_dir}

# 输入要执行的命令，例如 ./hello 或 python test.py 等
CUDA_VISIBLE_DEVICES=0,1 python ../../src/inference.py \
    --stage sft \
    --model_name_or_path '/scratch2/nlp/plm/Meta-Llama-3-8B-Instruct/' \
    --checkpoint_dir '/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/lora/llama3-8b-DocRED-Scratch/checkpoint-3244' \
    --model_name 'llama' \
    --template 'alpaca' \
    --do_predict \
    --input_file '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/iepile_test.json' \
    --output_file '/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/EE/DocEE/llama3-8b-DocRED-scratch.json' \
    --finetuning_type lora \
    --output_dir 'lora/test' \
    --predict_with_generate \
    --cutoff_len 512 \
    --bf16 \
    --max_new_tokens 300 \
	--load_best_model_at_end False

