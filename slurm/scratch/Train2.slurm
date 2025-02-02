#!/bin/bash
#SBATCH -J IEPile_Training                # 作业名为 xxx
#SBATCH -o ./msg_out/IEPile_Scratch_DocEE.out           # 屏幕上的输出文件重定向到 xxx.out
#SBATCH -p DGX                   # 作业提交的分区为 HGX
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

# 输入要执行的命令，例如 ./hello 或 python test.py 等
output_dir='/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/lora/llama3-8b-DocEE-Scratch'
mkdir -p ${output_dir}
CUDA_VISIBLE_DEVICES="0,1" torchrun --nproc_per_node=2 --master_port=1287 ../src/finetune.py \
    --do_train \
	--do_eval \
    --overwrite_output_dir \
    --model_name_or_path '/scratch2/nlp/plm/Meta-Llama-3-8B-Instruct/' \
    --stage 'sft' \
    --model_name 'llama' \
    --template 'alpaca' \
    --train_file '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/iepile_train.json' \
    --valid_file '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/iepile_dev.json' \
    --val_set_size 100 \
    --output_dir=${output_dir} \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --preprocessing_num_workers 16 \
    --num_train_epochs 5 \
    --learning_rate 5e-5 \
    --max_grad_norm 0.5 \
    --optim "adamw_torch" \
    --max_source_length 400 \
    --cutoff_len 700 \
    --max_target_length 300 \
    --evaluation_strategy "epoch" \
    --save_strategy "epoch" \
    --save_total_limit 1 \
    --lora_r 16 \
    --lora_alpha 32 \
    --lora_dropout 0.05 \
	--run_name 'DocEE_Scratch' \
	--report_to 'wandb' \
	--logging_step 2 \
    --bf16
