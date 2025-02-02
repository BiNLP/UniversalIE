python src/inference_gpt.py \
	--input_path "/scratch2/nlp/UIE/data/document/Re-DocRED/IEPile_format/NER/test_iepile_guidelines.json"	\
	--output_path "/scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/NER/ReDocRED/gpt-guidelines.json"	\
	--task NER


python ie2instruction/eval_func.py \
  --path1 /scratch2/nlp/chenzhenbin/Workspaces/UniversalIE/results/NER/ReDocRED/gpt-guidelines.json \
  --task NER