import random
import json
from convert.utils.utils import stable_hash, write_to_json


# 定义文件路径
json_input = '/home/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/test.json'
json_out = '/home/chenzhenbin/Workspaces/IEPile/data/ACE2005/IEPile_format/dev.json'
# 读取JSON文件内容

combined_data = []

with open(json_input, 'r', encoding='utf-8') as f:
    flag = 0
    index = random.sample(range(1,len(f.readlines())-1),100)
    print("Selected sample ids:",index)
    

with open(json_input, 'r', encoding='utf-8') as f:
    for line in f:
        if flag in index:
            print(flag)
            combined_data.append(json.loads(line))
        flag+=1    



# 合并JSON数据
# 假设JSON的顶层是一个列表
# combined_data = data1 + data2 + data3
write_to_json(json_out,combined_data)

print(f"Data has been merged into {json_out}!")

