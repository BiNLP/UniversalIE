import torch

from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, GenerationConfig
from peft import PeftModel



def merge(model_name_or_path:str, checkpoint_dir:str, save_path:str):
    config_kwargs = {
        "model_name": 'llama',
        "cache_dir": None,
        "use_fast_tokenizer": True,
        "trust_remote_code": True,
        "use_auth_token": False,
        "model_revision": 'main',
        # "split_special_tokens" : False,
        "bits": 16,
        "adam8bit": False,
        "double_quant": True,
        "quant_type": "nf4",
        "checkpoint_dir": None,
        "revision": "main",
    }
    # 载入预训练模型
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        use_fast = True,
        split_special_tokens = False,
        padding_side="left",
        **config_kwargs
    )
    print("Tokenizer Load Success!")
    config = AutoConfig.from_pretrained(model_name_or_path, **config_kwargs)
    # Load and prepare pretrained models (without valuehead).
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        config=config,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        revision='main',
    )
    print('origin config =', model.config)
    # 模型合并
    # ckpt_list = ["checkpoint-1000", "checkpoint-2000", "checkpoint-3000"]
    # for checkpoint in ckpt_list:
    #     print('Merge checkpoint: {}'.format(checkpoint))
    #     model = PeftModel.from_pretrained(model, os.path.join(lora_model, checkpoint))
    #     model = model.merge_and_unload()
    # print('merge config =', model.config)
    print('Merge checkpoint: {}'.format(checkpoint_dir))
    model = PeftModel.from_pretrained(model, checkpoint_dir)
    model = model.merge_and_unload()
    print('merge config =', model.config)


    print(f"Saving the target model to {save_path}")
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

if __name__ == '__main__':
    model_name_or_path = '/scratch2/nlp/plm/Meta-Llama-3-8B-Instruct/'
    checkpoint_dir = '/scratch2/nlp/chenzhenbin/Workspaces/LLMs/llama3-8b-iepile-lora'
    save_path = '/scratch2/nlp/chenzhenbin/Workspaces/LLMs/llama3-8b-iepile-lora-merged'
    merge(model_name_or_path, checkpoint_dir, save_path)