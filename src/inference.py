import os
import sys
sys.path.append('./')
import json
import torch
from datasets import Dataset
from transformers import GenerationConfig

from args.parser import get_infer_args
from model.loader import load_model_and_tokenizer
from datamodule.preprocess import preprocess_dataset
from utils.general_utils import get_model_tokenizer_trainer, get_model_name
from utils.logging import get_logger
from tqdm import tqdm

import matplotlib.pyplot as plt
from collections import Counter
import datetime

# outlines
from typing import List, Optional
from pydantic import BaseModel, Field, create_model


if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except: 
    pass


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["WANDB_DISABLED"] = "true"

logger = get_logger(__name__)


def convert_datas2datasets(records):
    dataset_mapping = {'prompt':[], 'query':[], "response":[]}
    for record in records:
        dataset_mapping['prompt'].append(record['instruction'])
        dataset_mapping['query'].append(record.get('input', None))
        dataset_mapping['response'].append(record.get('output', 'test'))
    dataset = Dataset.from_dict(dataset_mapping)
    return dataset

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
    NEROutputModel = create_model("NEROutputModel", **tmp)
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
        arguments = {argue: (Optional[str], None) for argue in event["arguments"]}
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
    return OutputModel

def inference(model_args, data_args, training_args, finetuning_args, generating_args, inference_args):
    model_class, tokenizer_class, _ = get_model_tokenizer_trainer(model_args.model_name)
    logger.info(f"model_class:{model_class}\ntokenizer_class:{tokenizer_class}\n")


    # Load Outlines Model
    if inference_args.enable_outlines:
        import outlines
        config_kwargs = {
            "trust_remote_code": True,
            "cache_dir": model_args.cache_dir,
            "revision": model_args.model_revision,
        }
        tokenizer = tokenizer_class.from_pretrained(
            model_args.model_name_or_path,
            use_fast=model_args.use_fast_tokenizer,
            split_special_tokens=model_args.split_special_tokens,
            padding_side="left",
            **config_kwargs
        )

        model = outlines.models.transformers(
            model_args.model_name_or_path,
            device="cuda",# optional device argument, default is cpu
            # gpu_memory_utilization=0.7,
        )
        print(f"BOS:{tokenizer.bos_token_id},{tokenizer.bos_token}\tEOS:{tokenizer.eos_token_id},{tokenizer.eos_token}\tPAD:{tokenizer.pad_token_id},{tokenizer.pad_token}")
    else:
        model, tokenizer = load_model_and_tokenizer(
            model_class,
            tokenizer_class,
            model_args,
            finetuning_args,
            training_args.do_train,
            stage="sft"
        )
        model.to(device)
        print(f"BOS:{tokenizer.bos_token_id},{tokenizer.bos_token}\tEOS:{tokenizer.eos_token_id},{tokenizer.eos_token}\tPAD:{tokenizer.pad_token_id},{tokenizer.pad_token}")

    

    def evaluate(
        input_ids,
        generating_args,
        **kwargs,
    ):
        input_length = len(input_ids)
        input_ids = torch.tensor(input_ids, dtype=torch.long).unsqueeze(0)
        input_ids = input_ids.to(device)
        generation_config = GenerationConfig(
            temperature=generating_args.temperature,
            top_p=generating_args.top_p,
            top_k=generating_args.top_k,
            num_beams=generating_args.num_beams,
            max_new_tokens=generating_args.max_new_tokens,
            pad_token_id=tokenizer.pad_token_id,
            return_dict_in_generate=True,
            output_scores=True,
            **kwargs,
        )

        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                **kwargs,
            )
        generation_output = generation_output.sequences[0]
        generation_output = generation_output[input_length:]
        output = tokenizer.decode(generation_output, skip_special_tokens=True)
        return output,input_length,len(generation_output)



    def evaluate_outlines(
        record,
        generating_args,
        **kwargs,
    ):
        task = record['task']
        instruction = eval(record['instruction'])
        input = instruction['input']
        prompt = instruction['instruction']
        schema = instruction['schema']
        input_length = len(input) + len(prompt)
        OutputFormat = getFormat(schema,task)

        # import pdb;pdb.set_trace()
        generator = outlines.generate.json(model, OutputFormat)
        output = generator(prompt+"The input is as following:"+input)
        del generator
        return output.model_dump_json(),input_length,len(output.model_dump_json())

    records = []
    with open(inference_args.input_file, "r") as reader:
        for line in reader:
            data = json.loads(line)
            data["output"] = "test"
            records.append(data)
    predict_dataset = convert_datas2datasets(records)
    predict_dataset = preprocess_dataset(predict_dataset, tokenizer, data_args, training_args, finetuning_args.stage)


    input_length_list = []  # Recored the input length
    output_length_list = []  # Recored the output length
    with open(inference_args.output_file, 'w') as writer:
        if inference_args.enable_outlines:  #使用outlines
            for record in records:
                result, input_length, output_length = evaluate_outlines(record, generating_args)
                input_length_list.append(input_length)
                output_length_list.append(output_length)

                print(result)
                record['output'] = result
                writer.write(json.dumps(record, ensure_ascii=False) + '\n')
        else:
            for record, model_inputs in zip(records, predict_dataset["input_ids"]):
                result,input_length,output_length  = evaluate(model_inputs, generating_args)
                input_length_list.append(input_length)
                output_length_list.append(output_length)

                print(result)
                record['output'] = result
                writer.write(json.dumps(record, ensure_ascii=False)+'\n')

    #需要画图再解除注释
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # save_path = "../../fig/"+ timestamp
    # draw_figure(input_length_list, save_path+"_input.png")
    # draw_figure(output_length_list,save_path+"_output.png")


def draw_figure(data, save_path):
    # 使用 Counter 统计数字出现的次数
    frequency = Counter(data)
    # 提取数字和次数
    numbers = list(frequency.keys())
    counts = list(frequency.values())
    # 绘制条形统计图
    plt.figure(figsize=(60, 15))
    plt.bar(numbers, counts, color='skyblue', edgecolor='black')
    plt.title("Length of Sequence", fontsize=16)
    plt.xlabel("Length", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(numbers,rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    plt.savefig(save_path)




def main(args=None):
    model_args, data_args, training_args, finetuning_args, generating_args, inference_args = get_infer_args(args)
    # model_name映射
    model_args.model_name = get_model_name(model_args.model_name)
    inference(model_args, data_args, training_args, finetuning_args, generating_args, inference_args)
 



if __name__ == "__main__":
    main()
