#LLaMA-Factory 微调Qwen2.5VL 链接  https://zhuanlan.zhihu.com/p/1903485169010210107
# swanlab API Key : wFExi1nV5osUmt0EpAMAs
# 命令 nohup python car_train.py > app.log 2>&1 &

import os,csv
import torch
torch.cuda.empty_cache()
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
torch.backends.cudnn.benchmark = True
from datasets import Dataset
from modelscope import snapshot_download, AutoTokenizer
from swanlab.integration.transformers import SwanLabCallback
from qwen_vl_utils import process_vision_info
from peft import LoraConfig, TaskType, get_peft_model, PeftModel
from transformers import (
    TrainingArguments,Qwen2_5_VLForConditionalGeneration,
    Trainer,
    DataCollatorForSeq2Seq,
    Qwen2VLForConditionalGeneration,
    AutoProcessor,DefaultDataCollator
)
import swanlab
import json

def process_func(example):
    """
    将数据集进行预处理
    """
    MAX_LENGTH = 8192
    input_ids, attention_mask, labels = [], [], []
    conversation = example["conversations"]
    input_content = conversation[0]["value"]
    output_content = conversation[1]["value"]
    file_path = input_content.split("<|vision_start|>")[1].split("<|vision_end|>")[0]  # 获取图像路径
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": f"{file_path}",
                    "resized_height": 280,
                    "resized_width": 280,
                },
                {"type": "text", "text": "Dcar Yes:"},
            ],
        }
    ]
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )  # 获取文本

    image_inputs, video_inputs = [], []
    try:
        image_inputs, video_inputs = process_vision_info(messages)  # 获取预处理后的图像和视频数据
    except OSError as e:
        if "image file is truncated" in str(e):
            print(f"Warning: Skipping truncated image: {file_path}")
            image_inputs = [torch.zeros((3, 224, 224))]  # 使用一个零张量作为占位符
        else:
            raise e
    # 处理 video_inputs 为空的情况，如果为空则设置为 None
    if not video_inputs:
        video_inputs = None

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = {key: value.tolist() for key, value in inputs.items()} # tensor -> list, 为了方便拼接
    instruction = inputs

    response = tokenizer(f"{output_content}", add_special_tokens=False)

    input_ids = (
        instruction["input_ids"][0] + response["input_ids"] + [tokenizer.pad_token_id]
    )

    attention_mask = instruction["attention_mask"][0] + response["attention_mask"] + [1]
    labels = (
        [-100] * len(instruction["input_ids"][0])
        + response["input_ids"]
        + [tokenizer.pad_token_id]
    )
    if len(input_ids) > MAX_LENGTH:  # 做一个截断
        input_ids = input_ids[:MAX_LENGTH]
        attention_mask = attention_mask[:MAX_LENGTH]
        labels = labels[:MAX_LENGTH]

    input_ids = torch.tensor(input_ids)
    attention_mask = torch.tensor(attention_mask)
    labels = torch.tensor(labels)
    inputs['pixel_values'] = torch.tensor(inputs['pixel_values'])
    inputs['image_grid_thw'] = torch.tensor(inputs['image_grid_thw']).squeeze(0)  # 由（1,h,w)变换为（h,w）
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels,
            "pixel_values": inputs['pixel_values'], "image_grid_thw": inputs['image_grid_thw']}


def predict(messages, model):
    # 准备推理
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # 生成输出
    generated_ids = model.generate(**inputs, max_new_tokens=64)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    
    return output_text[0]


# 在modelscope上下载Qwen2-VL模型到本地目录下
#model_dir = snapshot_download("./mm", cache_dir="./", revision="master")

# 使用Transformers加载模型权重
tokenizer = AutoTokenizer.from_pretrained("./Qwen", use_fast=False, trust_remote_code=True)
processor = AutoProcessor.from_pretrained("./Qwen")

model = Qwen2_5_VLForConditionalGeneration.from_pretrained("./Qwen", device_map="auto", trust_remote_code=True,)
model.enable_input_require_grads()  # 开启梯度检查点时，要执行该方法

# 处理数据集：读取json文件
# 拆分成训练集和测试集，保存为data_vl_train.json和data_vl_test.json

train_ds = Dataset.from_json("data_vl.json")
train_dataset = train_ds.map(process_func)

# 配置LoRA
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False,  # 训练模式
    r=64,  # Lora 秩
    lora_alpha=16,  # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.05,  # Dropout 比例
    bias="none",
)

# 获取LoRA模型
peft_model = get_peft_model(model, config)

# 配置训练参数
args = TrainingArguments(
    output_dir="./output/Qwen2.5-VL-3B",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,
    logging_steps=10,
    logging_first_step=5,
    num_train_epochs=1,
    save_steps=100,
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True,
    report_to="none",
)
        
# 设置SwanLab回调
swanlab_callback = SwanLabCallback(
    project="Dcar",
    workspace="1352744183",
    experiment_name="qwen2.5-vl-Dcar1000",
    config={
        "model": "https://modelscope.cn/models/Qwen/Qwen2.5-VL-3B-Instruct",
        "dataset": "https://modelscope.cn/datasets/modelscope/coco_2014_caption/quickstart",
        "github": "https://github.com/datawhalechina/self-llm",
        "prompt": f"请你分析一下此图片为汽车的内饰图片还是外饰图片,是什么点位类型、是什么点位名称",
        "train_data_number": 4267,
        "lora_rank": 64,
        "lora_alpha": 16,
        "lora_dropout": 0.1,
    },
)
""" A100训练的
args = TrainingArguments(
  output_dir="./output",
  per_device_train_batch_size=24,    # 拉大一点
  gradient_accumulation_steps=2,     # 减少累积
  bf16=True,
  fp16=False,
  gradient_checkpointing=True,       # 如果显存吃紧，就开；不吃紧可关
  deepspeed="ds_stage3.json",        # 深度零冗余 offload（选配）
  dataloader_num_workers=12,
  dataloader_pin_memory=True,
  prefetch_factor=4,
  optim="adamw_torch",
  logging_steps=10,
  save_steps=100,
  report_to="none",
)"""


# 配置Trainer
trainer = Trainer(
    model=peft_model,
    args=args,
    train_dataset=train_dataset,
    data_collator=DefaultDataCollator(return_tensors="pt", padding=True),
    callbacks=[swanlab_callback],
)

# 开启模型训练
trainer.train()

# ====================测试模式===================
# 配置测试参数
val_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=True,  # 训练模式
    r=64,  # Lora 秩
    lora_alpha=16,  # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.05,  # Dropout 比例
    bias="none",
)

# 获取测试模型
val_peft_model = PeftModel.from_pretrained(model, model_id="/data/checkpoint-228", config=val_config)

# 读取测试数据
with open("Dcar_1000_test.json", "r") as f:
    test_dataset = json.load(f)
OUT_CSV    = 'predictions.csv'
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 写入表头
    writer.writerow(['item', 'prediction'])


    for item in os.listdir('/data/test_images'):
        print(item)
        #input_image_prompt = item["conversations"][0]["value"]
    # 去掉前后的<|vision_start|>和<|vision_end|>
    
    #origin_image_path = input_image_prompt.split("<|vision_start|>")[1].split("<|vision_end|>")[0]
    #print('origin_image_path:',origin_image_path) 
        messages = [{
        "role": "user", 
        "content": [
            {
            "type": "image", 
            "image": f"/data/test_images/{item}"
            },
            {
            "type": "text",
            "text": "Dcar Yes:"
            }
        ]}]
    
        response = predict(messages, val_peft_model)
        print("item:",item ,'predict:',response)
        writer.writerow([item, response])
print(f"写入完成，见文件 {OUT_CSV}")
