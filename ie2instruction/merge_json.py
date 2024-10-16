import json
from convert.utils.utils import stable_hash, write_to_json


# 定义文件路径
# json_ner = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/train_ner.json'
# json_re = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/train_re.json'
# json_ee = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format//train_ee.json'
# json_out = '/home/jiazixia/IEPile/data/ACE2005/IEPile_format/train.json'


json_ner = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test_ner.json'
json_re = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test_re.json'
json_ee = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test_ee.json'
json_out = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test.json'

# 读取JSON文件内容

combined_data = []

with open(json_ner, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))

with open(json_re, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))


with open(json_ee, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))


# 合并JSON数据
# 假设JSON的顶层是一个列表
# combined_data = data1 + data2 + data3

write_to_json(json_out,combined_data)

print(f"Data has been merged into {json_out}!")

