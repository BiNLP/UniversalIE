import os
import sys
sys.path.append('./')
import json

import re
from utils.logging import get_logger
from tqdm import tqdm

from typing import List, Optional
from pydantic import BaseModel, Field, create_model

import argparse
from openai import AzureOpenAI

logger = get_logger(__name__)


REGION = "eastus"
MODEL = "gpt-4o-2024-08-06"
API_KEY = "02cbec6d675e4827c0c32c6965751cab"
API_BASE = "https://api.tonggpt.mybigai.ac.cn/proxy"
ENDPOINT = f"{API_BASE}/{REGION}"
client = AzureOpenAI( api_key=API_KEY, api_version="2024-08-01-preview", azure_endpoint=ENDPOINT, )

def getFormat(schema_list, task):
    if task == 'NER':
        return NERFormat(schema_list)
    elif task == 'RE':
        return REFormat(schema_list)
    elif task == 'EE':
        return EEFormat(schema_list)

def NERFormat(schema):
    tmp = {}
    for field in schema:
        tmp[field] = (Optional[List[str]], Field(default_factory=list))
    NEROutputModel = create_model("NEROutputModel",**tmp)
    return NEROutputModel


def REFormat(schema):
    class RelationItem(BaseModel):
        subject: str
        object: str
    
    REOutputModel = create_model(
        "REOutputModel",
        **{relation: (Optional[List[RelationItem]], Field(default_factory=list)) for relation in schema}
    )
    return REOutputModel 


# 根据schema动态生成事件模型
def EEFormat(schema):
    # 存储所有事件类型
    event_fields = {}

    for event in schema:
        event_type = event["event_type"]
        arguments = {argue: (Optional[str],None) for argue in event["arguments"]}

        # 定义嵌套的Arguments模型
        ArgumentsModel = create_model(
            f"{event_type.capitalize()}Arguments",
            **arguments
        )

        # 定义事件模型，包括trigger和arguments
        EventModel = create_model(
            f"{event_type.capitalize()}Event",
            trigger=(Optional[str], None),
            # arguments=(ArgumentsModel, ArgumentsModel())
            arguments=(Optional[ArgumentsModel], None)
        )

        # 最后将其添加到主模型字段中
        event_fields[event_type] = (Optional[List[EventModel]], Field(default_factory=list))

    # 创建最终的输出模型类
    OutputModel = create_model("OutputModel", **event_fields)
    # example_data = {
    #     "Transport": [
    #         {
    #             "trigger": "shipment",
    #             "arguments": {
    #                 "Time-Starting": "2023-10-01T08:00:00Z",
    #                 "Org": "DHL",
    #                 "Destination": "New York",
    #                 "Defendant": "John Doe",
    #                 "Price": "1000 USD",
    #
    #                 "Prosecutor": "Attorney General",
    #
    #                 "Victim": "N/A",
    #                 "Time-At-Beginning": "2023-10-01T07:30:00Z",
    #                 "Time-Within": "2023-10-01",
    #                 "Person": "Jane Smith",
    #                 "Instrument": "Truck",
    #                 "Adjudicator": "Judge Judy",
    #                 "Beneficiary": "XYZ Corp",
    #                 "Recipient": "Bob's Electronics",
    #                 "Sentence": "N/A",
    #                 "Artifact": "Package",
    #                 "Time-Ending": "2023-10-01T12:00:00Z",
    #                 "Plaintiff": "N/A",
    #                 "Position": "Manager",
    #                 "Giver": "DHL",
    #                 "Entity": "DHL",
    #                 "Crime": "N/A",
    #                 "Attacker": "N/A",
    #                 "Time-After": "2023-10-01T12:00:00Z",
    #                 "Money": "1000 USD",
    #                 "Time-Holds": "2023-10-01T10:00:00Z",
    #                 "Time-Before": "2023-10-01T07:00:00Z",
    #                 "Origin": "Los Angeles",
    #                 "Vehicle": "Van",
    #                 "Seller": "DHL",
    #                 "Time-At-End": "2023-10-01T12:00:00Z",
    #                 "Target": "New York"
    #             }
    #         }
    #     ], "Elect": [],  "Nominate": [], "Start-Position": [], "Attack": [], "End-Position": []}
    # schema_instance = OutputModel(**example_data)
    # print(schema_instance.json(indent=4))
    return OutputModel


def getResponse(prompt, text, schema_list, task):
    # import pdb;pdb.set_trace()
    # Format = getFormat(schema_list, task)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": f"{prompt}" },
            {"role": "user", "content": f"{text}"},
        ],
        response_format= getFormat(schema_list, task),
    )

    message = completion.choices[0].message
    if message.parsed:
        # print(message.parsed.json())
        return message.parsed.json()
    else:
        print("=============== GPT-4o Parses Failed! ===========")
        return []

def inference(args):
    records = []
    with open(args.input_path, "r") as reader:
        for line in reader:
            data = json.loads(line)
            data["output"] = "test"
            records.append(data)
    
    with open(args.output_path, 'w') as writer:
        for data in tqdm(records):
            # import pdb;pdb.set_trace()
            if args.task == 'EE':
                data_dict = eval(re.sub("true", "True", data['instruction']))  # 解决schema里面有true的问题，但没有这个变量
            else:
                data_dict = eval(data['instruction'])
            prompt = data_dict['instruction']
            text = data_dict['input']
            schema_list = data_dict['schema']
            result = getResponse(prompt, text, schema_list, args.task)
            print(result)
            data['output'] = result
            writer.write(json.dumps(data, ensure_ascii=False)+'\n') 


def main(args=None):
    parser = argparse.ArgumentParser(description='Please give the argument that GPT-4o need!')
    parser.add_argument("-i","--input_path", type=str, help="The IEPile format data path.")
    parser.add_argument("-o","--output_path", type=str, help="The predict result save path.")
    parser.add_argument("-t","--task", type=str, choices=['NER','RE','EE'], help="NER/RE/EE")
    args = parser.parse_args()
    inference(args)
 

if __name__ == "__main__":
    main()
