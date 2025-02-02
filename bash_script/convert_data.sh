# NER
#python ie2instruction/convert_func.py \
#    --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/sample_train.json  \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/train.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/sample_train.json \
#    --language en \
#    --task NER \
#    --split_num 6 \
#    --random_sort \
#    --split train


# RE
python ie2instruction/convert_func.py \
    --src_path /home/chenzhb/Workspaces/Datasets/UIE/Re-DocRED/IEPile_format/NER/train.json  \
    --tgt_path /home/chenzhb/Workspaces/Datasets/UIE/ToyData/ner_train_to_test.json \
    --schema_path /home/chenzhb/Workspaces/Datasets/UIE/Re-DocRED/IEPile_format/NER/schema.json \
    --language en \
    --task NER \
    --split_num 10 \
    --random_sort \
    --split test


# EE
#python ie2instruction/convert_func.py \
#	  --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/sample_test.json \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/test.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/dataset_annotated/MUC3/schema_iepile.json \
#    --language en \
#    --task EE \
#    --split_num 4 \
#    --random_sort \
#    --split test
