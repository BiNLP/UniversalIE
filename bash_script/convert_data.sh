


## NER
#file="CrossNER_politics"
#python ie2instruction/convert_func.py \
#    --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/NER/${file}/sample_test.json \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/NER/${file}/test.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/NER/${file}/schema.json \
#    --language en \
#    --task NER \
#    --split_num 9 \
#    --random_sort \
#    --split test



## RE
#file="semval-RE"
#python ie2instruction/convert_func.py \
#    --src_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/RE/${file}/sample_test.json \
#    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/RE/${file}/test.json \
#    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/datasets/Sentence-IE/RE/${file}/schema.json \
#    --language en \
#    --task RE \
#    --split_num 5 \
#    --random_sort \
#    --split test

# EE
#file="PHEE"
python ie2instruction/convert_func.py \
    --src_path /scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/sample_ee.json \
    --tgt_path /scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test_ee_new.json \
    --schema_path /scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/schema_ee_new.json \
    --language en \
    --task EE \
    --split_num 4 \
    --random_sort \
    --split test


