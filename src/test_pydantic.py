from typing import List, Optional
from pydantic import BaseModel, Field, create_model

# 预定义的所有可能字段
all_fields = {
    "person": (Optional[List[str]], Field(default_factory=list)),
    "geographical_social_political": (Optional[List[str]], Field(default_factory=list)),
    "vehicle": (Optional[List[str]], Field(default_factory=list)),
    "organization": (Optional[List[str]], Field(default_factory=list)),
    "facility": (Optional[List[str]], Field(default_factory=list)),
    "weapon": (Optional[List[str]], Field(default_factory=list)),
    "location": (Optional[List[str]], Field(default_factory=list))
}

# 运行时定义的字段列表
a = ["location", "organization"]

# 使用a列表中的字段来创建一个动态的模型
# DynamicOutputModel = create_model(
#    "DynamicOutputModel",
#    **{field: all_fields[field] for field in a}
#)

tmp = {}
for field in a:
    tmp[field] = (Optional[List[str]], Field(default_factory=list))



DynamicOutputModel = create_model("DynamicOutputModel",**tmp)

# 使用示例数据创建模型实例
data = {
    "location": ["a place"],
    "organization": ["an organization"]
}

# 验证并输出
output = DynamicOutputModel(**data)
print(output.json(indent=2))
