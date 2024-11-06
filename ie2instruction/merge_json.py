import json
from convert.utils.utils import stable_hash, write_to_json


# 定义文件路径
# json_ner = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/dev_ner.json'
# json_re = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/dev_re.json'
# json_ee = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format//dev_ee.json'
# json_out = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/dev.json'


#json_ner = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/NER/SciERC/iepile_test.json'
#json_re = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/RE/SciERC/iepile_test.json'
#json_ee = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/dev_ee.json'
#json_out = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/mixup/SciERC/test.json'

json1 = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/mixup/DocRED/test.json'
json2 = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/mixup/SciERC/test.json'
json3 = '/home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/DocEE-en/iepile_test.json'
json4 = '/home/chenzhenbin/Workspaces/datasets/iepile_format_data/EE/Wikievents/iepile_test.json'
json_out = '/scratch2/nlp/chenzhenbin/Workspaces/datasets/iepile_format_data/mixup/test.json'

# 读取JSON文件内容

combined_data = []

with open(json1, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))

with open(json2, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))

with open(json3, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))

with open(json4, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))
#with open(json_ee, 'r', encoding='utf-8') as f:
#    for line in f:
#        combined_data.append(json.loads(line))


# 合并JSON数据
# 假设JSON的顶层是一个列表
# combined_data = data1 + data2 + data3

write_to_json(json_out,combined_data)

print(f"Data has been merged into {json_out}!")

