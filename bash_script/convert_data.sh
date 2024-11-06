## NER
#python ie2instruction/convert_func.py \
#    --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/NER/SciERC/sample_test.json  \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/NER/SciERC/iepile_test.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/NER/SciERC/schema.json \
#    --language en \
#    --task NER \
#    --split_num 6 \
#    --random_sort \
#    --split test


## RE
#python ie2instruction/convert_func.py \
#    --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/RE/SciERC/sample_test.json  \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/RE/SciERC/iepile_test.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/RE/SciERC/schema.json \
#    --language en \
#    --task RE \
#    --split_num 4 \
#    --random_sort \
#    --split test


# EE
python ie2instruction/convert_func.py \
	--src_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/dev.json \
    --tgt_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/iepile_dev.json \
    --schema_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/schema.json \
    --language en \
    --task EE \
    --split_num 4 \
    --random_sort \
    --split train

# EE
python ie2instruction/convert_func.py \
	--src_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/Wikievents/dev.json \
    --tgt_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/Wikievents/iepile_dev.json \
    --schema_path /home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/Wikievents/schema.json \
    --language en \
    --task EE \
    --split_num 4 \
    --random_sort \
    --split train
