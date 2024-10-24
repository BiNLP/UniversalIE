from typing import List, Dict, Any, Type
from pydantic import BaseModel, create_model, ValidationError

# 动态生成的 schema 作为输入
schema = [
    {"event_type": "elect", "trigger": True, "arguments": ["place", "entity", "person"]},
    {"event_type": "start position", "trigger": True, "arguments": ["place", "entity", "person"]}
]


# 创建每个事件的子模型
def create_event_model(event_name: str, arguments: List[str]) -> Type[BaseModel]:
    # 创建 Arguments 模型类，使用 provided arguments 生成字段
    arguments_fields = {arg: (str, ...) for arg in arguments}

    # 动态生成 Arguments 模型
    ArgumentsModel = create_model(f"{event_name}_Arguments", **arguments_fields)

    # 创建事件的详细模型，包括 trigger 和 arguments
    EventDetailModel = create_model(
        f"{event_name}_Detail",
        trigger=(str, ...),  # trigger 是字符串类型
        arguments=(ArgumentsModel, ...)  # arguments 是我们刚生成的 ArgumentsModel
    )
    return EventDetailModel


# 创建主模型，包含所有事件类型
def create_main_model(schema: List[Dict[str, Any]]) -> Type[BaseModel]:
    event_fields = {}

    for event in schema:
        event_type = event["event_type"]
        # 将 event_type 转换为适合 Python 命名的字段
        event_field_name = event_type.replace(" ", "_")
        arguments = event["arguments"]

        # 为每个事件生成子模型
        EventDetailModel = create_event_model(event_field_name, arguments)

        # 将事件字段添加到主模型中，类型为 List[EventDetailModel]
        event_fields[event_type] = (List[EventDetailModel], [])

    # 动态生成主模型
    MainModel = create_model("DynamicEventSchema", **event_fields)
    return MainModel


# 创建主模型
DynamicEventSchema = create_main_model(schema)

# 示例数据（符合目标格式）
example_data = {
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
    "start position": []
}

# 数据验证
try:
    schema_instance = DynamicEventSchema(**example_data)
    print(schema_instance.json(indent=4))
except ValidationError as e:
    print("Validation error:", e)