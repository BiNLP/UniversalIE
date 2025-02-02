python src/inference_gpt.py \
	--input_path "/scratch2/nlp/UIE/data/document/DocEE/IEPile_format/EE/test_iepile_guidelines.json"	\
	--output_path "/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/EE/DocEE/gpt-guidelines.json"	\
	--task EE


python ie2instruction/eval_func.py \
  --path1 /scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/EE/DocEE/gpt-guidelines.json \
  --task EE