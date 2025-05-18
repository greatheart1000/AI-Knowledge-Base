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
