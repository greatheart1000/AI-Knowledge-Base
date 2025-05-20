import os
import csv
from PIL import Image
import torch

# —— 1. 环境变量，减小碎片
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
torch.backends.cudnn.benchmark = True

# —— 2. 预加载：tokenizer/processor
from transformers import AutoTokenizer, AutoProcessor, Qwen2_5_VLForConditionalGeneration
from peft import LoraConfig, PeftModel
from qwen_vl_utils import process_vision_info

tokenizer = AutoTokenizer.from_pretrained(
    "/root/autodl-tmp/Qwen", use_fast=False, trust_remote_code=True
)
# 这里给 processor 指定 min/max pixels，统一输入尺寸，减小显存峰值
processor = AutoProcessor.from_pretrained(
    "/root/autodl-tmp/Qwen",
    min_pixels=256*28*28,
    max_pixels=1280*28*28,
)

# —— 3. 加载 base 模型（8bit + fp16 + offload + 自动 device_map）
base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "/root/autodl-tmp/Qwen",
    device_map="auto",       # 自动切分 CPU/GPU
    torch_dtype=torch.float16, 
    load_in_8bit=True,       # bitsandbytes 8-bit 量化
    offload_folder="offload",# offload 文件夹（必要时将部分权重置于磁盘/CPU）
    trust_remote_code=True,
)

# —— 4. 加载 LoRA 权重（同样 fp16 + device_map）
val_config = LoraConfig(
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    inference_mode=True,
    r=64, lora_alpha=16, lora_dropout=0.05,
    bias="none",
)
model = PeftModel.from_pretrained(
    base_model,
    "./output/Qwen2.5-VL-3B/checkpoint-1536",
    torch_dtype=torch.float16,
    device_map="auto",
)

# —— 5. 推理准备
model.eval()                # 关闭 Dropout
torch.cuda.empty_cache()    # 清理潜在显存碎片

def predict_one(image_path, text_prompt):
    """
    给定一张图和一段文字 prompt，返回生成结果
    """
    # 5.1 构造 messages，然后提取 vision/text inputs
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": image_path},
            {"type": "text",  "text": text_prompt}
        ]
    }]
    # 5.2 生成模板化的输入文本（不立即 token 化）
    chat_text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # 5.3 处理图像/视频，并调用 processor 生成 tensors
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[chat_text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device, torch.float16)

    # 5.4 真正推理：no_grad + 关闭 KV Cache + 控制长度
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=64,   # ⬅️ 严格控制生成长度
            use_cache=False,     # ⬅️ 关闭 KV cache，减少显存峰值
            do_sample=False      # ⬅️ 如果允许，greedy 也稍微省点算力
        )

    # 5.5 截断掉 prompt，decode 并返回
    # generated: [batch_size, seq_len]，batch_size=1
    gen_ids = generated[0][ inputs["input_ids"].size(1) : ]
    return processor.decode(
        gen_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

# —— 6. 批量推理并写 CSV
OUT_CSV = "predictions.csv"
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["item", "prediction"])

    prompt_text = "该图是汽车的内饰图片,请你判断该图片显示的点位类型、点位名称是什么"
    test_dir = "/root/autodl-tmp/test_images"

    for fname in sorted(os.listdir(test_dir)):
        img_path = os.path.join(test_dir, fname)
        # 逐张推理
        pred = predict_one(img_path, prompt_text)
        print(f"{fname} -> {pred}")
        writer.writerow([fname, pred])

print("推理完成，结果见", OUT_CSV)


# 在两个V100上推理的代码

import os, csv
import torch
from PIL import Image
from transformers import (
    AutoTokenizer, AutoProcessor,
    Qwen2_5_VLForConditionalGeneration
)
from peft import LoraConfig, PeftModel
from qwen_vl_utils import process_vision_info

# 1. 环境 & 显存碎片控制
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
torch.backends.cudnn.benchmark = True

# 2. 量化策略：4bit 更省，8bit 兼容性好
use_4bit = False       # 切换到 True 可试 4bit
use_8bit = True        # 如果不启 4bit，请启用 8bit

# 3. tokenizer + processor
tokenizer = AutoTokenizer.from_pretrained(
    "/root/autodl-tmp/Qwen",
    use_fast=False,
    trust_remote_code=True
)
processor = AutoProcessor.from_pretrained(
    "/root/autodl-tmp/Qwen",
    min_pixels=256*28*28,
    max_pixels=1280*28*28,
)

# 4. 两卡显存预算（各 32GB，留点系统／碎片余量）
max_mem = {
    "0": "30GiB",  # 第一张 V100
    "1": "30GiB",  # 第二张 V100
    "cpu": "64GiB" # 如果 offload，需要给 CPU 足够空间
}

# 5. 加载 Base Model：半精度 + 量化 + 自动拆卡 + Offload
base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "/root/autodl-tmp/Qwen",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    load_in_4bit=use_4bit,
    load_in_8bit=use_8bit and not use_4bit,
    device_map="auto",
    max_memory=max_mem,
    offload_folder="offload",       # 可选：指定 offload 临时目录
    offload_state_dict=True,        # off载部分权重到 CPU
)

# 6. 加载 LoRA 权重
val_config = LoraConfig(
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj","k_proj","v_proj","o_proj",
        "gate_proj","up_proj","down_proj"
    ],
    inference_mode=True,
    r=64, lora_alpha=16, lora_dropout=0.05,
    bias="none",
)
model = PeftModel.from_pretrained(
    base_model,
    "./output/Qwen2.5-VL-3B/checkpoint-1536",
    torch_dtype=torch.float16,
    device_map="auto",
    max_memory=max_mem,
)

# 7. 推理准备
model.eval()
torch.cuda.empty_cache()

def predict_one(image_path: str, prompt_text: str) -> str:
    # 构造消息
    messages = [{
        "role":"user","content":[
            {"type":"image","image":image_path},
            {"type":"text","text":prompt_text}
        ]
    }]
    # 生成 template 文本
    chat_text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    # 视觉预处理 + Tensor
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[chat_text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to(model.device, torch.float16)

    # no_grad + 关 cache + 控制长度
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=64,
            use_cache=False,
            do_sample=False
        )

    # 去掉 prompt 部分并 decode
    out_ids = generated[0][ inputs["input_ids"].size(1): ]
    return processor.decode(
        out_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )

# 8. 批量推理 & 写 CSV
OUT_CSV = "predictions.csv"
prompt_text = "该图是汽车的内饰图片,请你判断该图片显示的点位类型、点位名称是什么"
test_dir = "/root/autodl-tmp/test_images"

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["item","prediction"])
    for fn in sorted(os.listdir(test_dir)):
        img_path = os.path.join(test_dir, fn)
        pred = predict_one(img_path, prompt_text)
        print(f"{fn} -> {pred}")
        writer.writerow([fn, pred])

print("推理完成，结果写入", OUT_CSV)
