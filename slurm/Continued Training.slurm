#!/bin/bash
#SBATCH -J IEPile                # 作业名为 xxx
#SBATCH -o IEPile.out           # 屏幕上的输出文件重定向到 xxx.out
#SBATCH -p HGX                   # 作业提交的分区为 HGX
#SBATCH --qos=lv0b               # 作业使用的 QoS 为 lv0b
#SBATCH -N 1                      # 作业申请 1 个节点
#SBATCH --ntasks-per-node=1       # 单节点启动的进程数为 1
#SBATCH --cpus-per-task=16        # 单任务使用的 CPU 核心数为 4
#SBATCH -t 5:00:00                # 任务运行的最长时间为5 小时
#SBATCH --gres=gpu:2              # 单个节点使用 2 块 GPU 卡
#SBATCH --mem=160G                  #--mem=<size[units]>：设定每个节点的内存大小，后缀可以为[K|M|G|T]，默认为MB
#SBATCH --account=research

# 设置运行环境
# module add /miniconda     # 添加 anaconda/3-5.0.0.1 模块

# 输入要执行的命令，例如 ./hello 或 python test.py 等
bash ../ft_scripts/llama2_ace05_continue.bash

