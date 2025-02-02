import json
from convert.utils.utils import stable_hash, write_to_json


json1 = '/home/chenzhb/Workspaces/Datasets/UIE/DWIE/IEPile_format/NER/dev.json'
json2 = '/home/chenzhb/Workspaces/Datasets/UIE/DWIE/IEPile_format/RE/dev.json'
json3 = '/home/chenzhb/Workspaces/Datasets/UIE/Re-DocRED/IEPile_format/NER/dev_iepile.json'
json4 = '/home/chenzhb/Workspaces/Datasets/UIE/Re-DocRED/IEPile_format/RE/dev_iepile.json'
json5 = "/home/chenzhb/Workspaces/Datasets/UIE/SciERC/IEPile_format/NER/dev_iepile.json"
json6 = "/home/chenzhb/Workspaces/Datasets/UIE/SciERC/IEPile_format/RE/dev_iepile.json"

json_out = '/home/chenzhb/Workspaces/Datasets/UIE/mixup/dev_iepile.json'

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

with open(json5, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))

with open(json6, 'r', encoding='utf-8') as f:
    for line in f:
        combined_data.append(json.loads(line))


write_to_json(json_out,combined_data)

print(f"Data has been merged into {json_out}!")

