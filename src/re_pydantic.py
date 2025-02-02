from typing import List, Optional, Dict
from pydantic import BaseModel, Field, create_model

# 定义单个关系的结构
class RelationItem(BaseModel):
    subject: str
    object: str

# 定义给定的schema
schema = ["place lived", "company", "children", "location contains"]

# 使用schema列表中的关系名称，动态生成输出模型
# 所有字段都是一个List[RelationItem]类型，默认是空列表
DynamicOutputModel = create_model(
    "DynamicOutputModel",
    **{relation: (Optional[List[RelationItem]], Field(default_factory=list)) for relation in schema}
)

# 示例数据
data = {
    "place lived": [{"subject": "Sheldon Whitehouse", "object": "Rhode Island"}],
    "company": [],
    "children": [],
    "location contains": []
}

# 创建模型实例并输出
output = DynamicOutputModel(**data)
print(output.json(indent=2))
