#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 16:59
# @Author  : caijian
# @File    : get_images.py
# @Software: PyCharm
import requests
import threading
import os
import re
import pandas as pd
from urllib.parse import urlparse
import time

def download_image(url, save_dir, max_retries=3, retry_delay=5, timeout=30):
    """下载单个图片，文件名取自 URL 的最后一部分，带有重试机制和更长的超时"""
    for i in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功

            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            filepath = os.path.join(save_dir, filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"成功下载: {url} -> {filepath} (尝试次数: {i+1})")
            return  # 下载成功，退出重试循环
        except requests.exceptions.RequestException as e:
            print(f"下载失败 (尝试 {i+1}/{max_retries}): {url} - {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
        print(f"下载多次失败: {url}")

def download_images_multithreaded(urls, save_dir, num_threads=5):
    """多线程下载图片"""
    os.makedirs(save_dir, exist_ok=True)
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url, save_dir))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("所有图片下载完成！")

if __name__ == "__main__":
    excel_file = "test.csv"  # 将你的 CSV 文件名替换为实际的文件名
    save_directory = "downloaded_images_last_part"  # 指定保存图片的文件夹
    url_column = "url"  # 指定包含图片 URL 的列名
    num_threads = 10  # 可以调整线程数量
    max_retries = 3   # 下载失败后的最大重试次数
    retry_delay = 5   # 重试之间的等待时间（秒）
    timeout = 30      # 下载超时时间（秒）

    try:
        df = pd.read_csv(excel_file)
        if url_column not in df.columns:
            print(f"错误：CSV 文件中找不到名为 '{url_column}' 的列。")
        else:
            image_urls = df[url_column].tolist()
            download_images_multithreaded(image_urls, save_directory, num_threads)
    except FileNotFoundError:
        print(f"错误：找不到文件 '{excel_file}'。")
    except Exception as e:
        print(f"发生错误: {e}")

查看images文件夹有多少张图片的脚本
import os
import sys

# 默认要查看的文件夹路径
# 你也可以在运行脚本时通过命令行参数指定路径
DEFAULT_FOLDER_PATH = './images' # 根据你的实际文件夹名称修改这里

def count_files_in_folder(folder_path):
    """
    计算指定文件夹中的文件和子文件夹数量。
    """
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹不存在或不是一个有效的文件夹路径: {folder_path}")
        return None

    try:
        # 获取文件夹中所有文件和子文件夹的列表
        entries = os.listdir(folder_path)
        # 计算列表的长度，即文件和子文件夹的数量
        count = len(entries)
        return count
    except Exception as e:
        print(f"错误：无法访问文件夹 {folder_path} 的内容：{e}")
        return None

if __name__ == "__main__":
    # 检查是否有命令行参数指定文件夹路径
    if len(sys.argv) > 1:
        folder_to_check = sys.argv[1]
    else:
        folder_to_check = DEFAULT_FOLDER_PATH
        print(f"未指定文件夹路径，使用默认路径: {folder_to_check}")

    file_count = count_files_in_folder(folder_to_check)

    if file_count is not None:
        print(f"文件夹 '{folder_to_check}' 中共有 {file_count} 个条目 (包括文件和子文件夹)。")

# 删除已经下载的文件夹里面的损坏的文件 
import os
from PIL import Image
import pandas as pd

def check_and_remove_corrupted_images(folder_path):
    corrupted_images = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img.verify()  # 验证图片是否损坏
            except Exception as e:
                print(f"损坏图片: {file_path}，错误: {e}")
                corrupted_images.append(file_path)
                try:
                    os.remove(file_path)
                    print(f"已删除损坏图片: {file_path}")
                except Exception as del_e:
                    print(f"删除图片失败: {file_path}，错误: {del_e}")

    # 保存损坏图片路径到csv
    if corrupted_images:
        df = pd.DataFrame(corrupted_images, columns=['corrupted_image_path'])
        df.to_csv('corrupted_images.csv', index=False, encoding='utf-8-sig')
        print(f"共发现 {len(corrupted_images)} 张损坏图片，已保存到 corrupted_images.csv")
    else:
        print("未发现损坏图片")

if __name__ == "__main__":
    folder = "/root/autodl-tmp/train_images"  # 修改为你的图片文件夹路径
    check_and_remove_corrupted_images(folder)

##基于下载文件夹呃呃脚本以及查看并删除损坏的图片以后制作数据集脚本

下面的是更有效的删除破损图片的代码 
import os
from PIL import Image, ImageOps # 导入 Pillow 库
# from io import BytesIO # BytesIO 在这个脚本中没有直接用到，但保留了用户原有的导入

# —— 配置区 ——
# 请将这里的路径替换为你实际存放图片的文件夹路径
image_directory_path = r'D:\project\myfirstgo\downloaded_images_to_clean'
# —— 配置结束 ——

def main():
    """
    扫描指定目录，检查图片文件有效性，并删除无效文件。
    """
    print(f"--- 开始检查和清理图片目录: {image_directory_path} ---")

    # 检查目录是否存在且是一个目录
    if not os.path.isdir(image_directory_path):
        print(f"错误：指定的图片目录不存在或不是一个目录：{image_directory_path}")
        return

    try:
        # 获取目录中的所有文件和文件夹列表
        items_in_directory = os.listdir(image_directory_path)
    except Exception as e:
        print(f"扫描目录时发生错误：{e}")
        return

    total_items = len(items_in_directory)
    removed_count = 0
    processed_files_count = 0

    print(f"在目录 '{image_directory_path}' 中找到 {total_items} 个条目 (文件或文件夹)。")

    # 遍历目录中的每个条目
    for i, item_name in enumerate(items_in_directory):
        full_path = os.path.join(image_directory_path, item_name) # 构建完整路径

        # 跳过不是文件的条目（例如，子文件夹）
        if not os.path.isfile(full_path):
            print(f"Skipping (not a file): {item_name}")
            continue

        processed_files_count += 1 # 只对文件进行计数和处理

        # 打印当前处理进度（文件计数），不换行
        print(f"Processing file {processed_files_count}/{total_items} ({i+1}/{total_items} total items): {item_name}... ", end='')

        try:
            # 尝试使用 Pillow 打开图片文件
            # 使用 'with' 语句确保文件资源被正确管理和关闭
            with Image.open(full_path) as img:
                # 尝试加载图片数据。这通常会检测文件是否损坏或格式是否无效。
                # 如果文件是无效的，img.load() 会抛出异常。
                img.load()
                # 如果你特别需要检查并处理 EXIF 方向信息，可以保留下面这行：
                # ImageOps.exif_transpose(img)

            # 如果上面代码没有抛出异常，说明图片是有效的
            print("OK")

        except Exception as e:
            # 如果在打开或加载图片时发生任何异常，说明文件有问题
            print(f"Error: {type(e).__name__} - {e}") # 打印异常类型和信息
            print(f"Removing invalid file: {item_name}") # 提示将要删除文件

            try:
                # 删除无效的文件
                os.remove(full_path)
                removed_count += 1
                print("File removed successfully.")
            except Exception as remove_e:
                # 如果在删除文件时发生错误（例如权限问题）
                print(f"Error removing file {item_name}: {remove_e}")

    print(f"\n--- 检查结束 ---")
    print(f"总共检查文件数： {processed_files_count}")
    print(f"移除无效文件数： {removed_count}")
    # 注意：这里无法准确计算剩余文件，因为 os.listdir() 是在开始时获取的列表，
    # 且可能包含其他类型的文件或删除失败的文件。processed_files_count 是实际检查过的文件数。
    print(f"请重新查看目录 '{image_directory_path}' 确认剩余文件。")


if __name__ == "__main__":
    # 运行主函数
    main()

现在需要根据图片生成一个csv文件 到了这个步骤




# images2csv.py 文件 把images文件转为 csv

import pandas as pd
import os

# 读取原CSV
df = pd.read_csv('total_all.csv')

# 生成caption列
df['caption'] = (
    '该图片为汽车的:' + df['task_type_name'] + 
    '图片 点位类型:' + df['point_type_name'] + 
    ' 点位名称:' + df['point_name']
)

# 提取图片文件名
df['image_name'] = df['url'].apply(lambda x: os.path.basename(x))

# 拼接图片完整路径
df['image_path'] = '/root/autodl-tmp/train_images/' + df['image_name']

# 选择需要的列输出
output_df = df[['caption', 'image_path']]

# 保存为新的CSV
output_df.to_csv('output.csv', index=False, encoding='utf-8-sig')

print("生成output.csv完成")


csv2json.py文件 
import pandas as pd
import json
# 载入CSV文件
df = pd.read_csv('./output.csv')
conversations = []

# 添加对话数据
for i in range(len(df)):
    conversations.append({
        "id": f"identity_{i+1}",
        "conversations": [
            {
                "from": "user",
                "value": f"请你分析一下此图片为汽车的内饰图片还是外饰图片,是什么点位类型、是什么点位名称: <|vision_start|>{df.iloc[i]['image_path']}<|vision_end|>"
            },
            {
                "from": "assistant", 
                "value": df.iloc[i]['caption']
            }
        ]
    })

# 保存为Json
with open('data_vl.json', 'w', encoding='utf-8') as f:
    json.dump(conversations, f, ensure_ascii=False, indent=2)



删掉那些损坏的图片 filter_clean.py
import os
import pandas as pd

# 1. 从 corrupted_images.csv 里读出所有损坏图片的“stem”（不含后缀）
df_corrupt = pd.read_csv('corrupted_images.csv')
corrupted_stems = {
    os.path.splitext(os.path.basename(p))[0]
    for p in df_corrupt['corrupted_image_path']
}
print(f'共 {len(corrupted_stems)} 张损坏图的 stem 被收集。')

# 2. 读入 downloaded_urls.csv，提取每条 url 对应的 stem，过滤掉损坏的，保存为 total_all.csv
df_all = pd.read_csv('downloaded_urls.csv')

# 新列：url 对应的文件名去掉后缀之后的 stem
df_all['stem'] = df_all['url'].map(
    lambda u: os.path.splitext(os.path.basename(u))[0]
)

# 保留不在 corrupted_stems 里的那些行
df_filtered = df_all[~df_all['stem'].isin(corrupted_stems)].copy()
df_filtered.drop(columns=['stem'], inplace=True)

# 输出
df_filtered.to_csv('total_all.csv', index=False, encoding='utf-8-sig')
print(f'过滤后 {len(df_filtered)} 条记录，已保存到 total_all.csv.')

# 3. 遍历 train_images 目录，只保留出现在 total_all.csv 里的图片（同样比对 stem）
valid_stems = {
    os.path.splitext(os.path.basename(u))[0]
    for u in df_filtered['url']
}

train_dir = '/root/autodl-tmp/train_images'  # 请根据实际修改
deleted = 0
for fn in os.listdir(train_dir):
    full = os.path.join(train_dir, fn)
    if not os.path.isfile(full):
        continue

    stem = os.path.splitext(fn)[0]
    # 如果这个文件的 stem 不在我们保留下来的列表里，就删掉
    if stem not in valid_stems:
        os.remove(full)
        deleted += 1

print(f'在 "{train_dir}" 中共删除了 {deleted} 张不在 total_all.csv 列表里的图片。')


# new_csv2json.py 制作LLaMA-Factory数据集
import pandas as pd
import json
import os

# 载入CSV文件
csv_file_path = './output.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"错误：未找到 {csv_file_path} 文件，请确保文件存在。")
    exit()

# 用于存储最终的 JSON 数据列表
json_data_list = []

# 定义固定的人类指令文本
# 根据你的任务调整这里的文本。如果 CSV 中有专门的指令列，应从 CSV 读取。
# 这里的示例使用了你之前提到过的汽车分析指令
FIXED_HUMAN_INSTRUCTION = "请你分析一下此图片为汽车的内饰图片还是外饰图片,是什么点位类型、是什么点位名称:"

# 可选：定义固定的 System 消息文本
# 如果你的数据集需要 System 消息，可以在这里定义。如果不需要，可以注释掉或设为 None。
FIXED_SYSTEM_MESSAGE = None # 你的样例中有，但如果你的任务不需要或 CSV 中没有，可以设为 None
FIXED_SYSTEM_MESSAGE ="你是一个擅长识别汽车图片的分析师。" 

# 遍历 DataFrame 的每一行
for index, row in df.iterrows():
    # 获取图片路径和 caption
    image_path = row.get('image_path') # 使用 .get() 防止列不存在报错
    caption = row.get('caption')     # 使用 .get() 防止列不存在报错

    # 检查关键数据是否存在
    if not image_path:
        print(f"Warning: Skipping row {index} due to missing image_path.")
        continue
    # caption 可以是空的，但如果 caption 是 AI 回复的核心，需要检查
    # if pd.isna(caption):
    #     print(f"Warning: Skipping row {index} due to missing caption.")
    #     continue


    # 构建 messages 列表
    messages_entry = []

    # 添加 System 消息 (如果定义了)
    if FIXED_SYSTEM_MESSAGE is not None:
        messages_entry.append({
            "content": FIXED_SYSTEM_MESSAGE,
            "role": "system"
        })

    # 添加 User 消息，包含 <image> 标记和指令
    # 注意：<image> 标记是特殊的，模型处理时会将其与 images 列表中的图片关联
    user_content = f"<image>{FIXED_HUMAN_INSTRUCTION}"
    # 如果 CSV 中有专门的指令列，例如 'instruction_text'
    # instruction_text = row.get('instruction_text')
    # if instruction_text:
    #     user_content = f"<image>{instruction_text}"
    # else:
    #      user_content = f"<image>{FIXED_HUMAN_INSTRUCTION}" # 使用固定指令作为回退

    messages_entry.append({
        "content": user_content,
        "role": "user"
    })

    # 添加 Assistant 消息
    # 注意：样例中的 assistant content 是一个 JSON 字符串，你的 caption 列需要是这样的格式
    assistant_content = str(caption) if pd.notna(caption) else "" # 确保是字符串

    messages_entry.append({
        "content": assistant_content,
        "role": "assistant"
    })

    # 构建单个数据样本的字典
    data_sample = {
        "messages": messages_entry, # 使用 messages 字段
        "images": [image_path]     # 使用 images 字段，值是包含图片路径的列表
        # 根据目标格式，没有顶层的 "id" 字段
    }

    # 将构建好的样本字典添加到列表中
    json_data_list.append(data_sample)

# 保存为Json文件
output_json_path = 'LLama_Factory_data.json'
try:
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data_list, f, ensure_ascii=False, indent=2) # 使用 ensure_ascii=False 保留中文
except IOError as e:
    print(f"错误：写入文件 {output_json_path} 失败：{e}")
    exit()


print(f"成功将 {len(json_data_list)} 条数据转换为 {output_json_path}")



