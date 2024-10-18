from typing import List, Optional, Dict
from pydantic import BaseModel, Field, create_model

# 定义基础事件模型
class EventArgument(BaseModel):
    pass

# 根据schema动态生成事件模型
def generate_event_model(schema):
    # 存储所有事件类型
    event_fields = {}
    
    for event in schema:
        event_type = event["event_type"]
        arguments = {arg: (Optional[str], "NAN") for arg in event["arguments"]}
        
        # 定义嵌套的Arguments模型
        ArgumentsModel = create_model(
            f"{event_type.capitalize()}Arguments",
            **arguments
        )
        
        # 定义事件模型，包括trigger和arguments
        EventModel = create_model(
            f"{event_type.capitalize()}Event",
            trigger=(Optional[str], "NAN"),
            arguments=(ArgumentsModel, ArgumentsModel())
        )
        
        # 最后将其添加到主模型字段中
        event_fields[event_type] = (Optional[List[EventModel]], Field(default_factory=list))
    
    # 创建最终的输出模型类
    OutputModel = create_model("OutputModel", **event_fields)
    return OutputModel

# 定义事件schema
schema = [
    {"event_type": "elect", "trigger": True, "arguments": ["place", "entity", "person"]},
    {"event_type": "start position", "trigger": True, "arguments": ["place", "entity", "person"]},
    {"event_type": "die", "trigger": True, "arguments": ["place", "agent", "instrument", "victim"]},
    {"event_type": "extradite", "trigger": True, "arguments": ["agent", "destination", "person"]}
]

# 使用schema生成事件输出模型
OutputModel = generate_event_model(schema)

# 创建测试数据
data = {
    "elect": [
        {
            "trigger": "re - election",
            "arguments": {
                "place": "NAN",
                "entity": "NAN",
                "person": "Putin"
            }
        }
    ],
    "start position": [],
    "die": [],
    "extradite": []
}

# 验证并输出
output = OutputModel(**data)
print(output.json(indent=2))

