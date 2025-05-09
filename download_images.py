import pandas as pd
import requests
import os
from urllib.parse import urlparse
import re  # 导入正则表达式模块

def extract_filename_from_url(url):
    """从 URL 中提取日期后的文件名部分。"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    match = re.search(r'/\d{4}-\d{2}-\d{2}-(.*?)$', path)
    if match:
        return match.group(1)
    else:
        # 如果没有找到日期格式，则尝试获取最后的文件名
        return os.path.basename(path)

def download_images(url, save_path):
    """下载指定 URL 的图片并保存到指定路径。"""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"成功下载: {os.path.basename(save_path)}", flush=True)
        return True
    except requests.exceptions.RequestException as e:
        print(f"下载失败 URL: {url}, 错误: {e}", flush=True)
        return False
    except Exception as e:
        print(f"处理 URL: {url} 时发生错误: {e}", flush=True)
        return False

def download_images_by_label(df, download_dir="downloaded_images", images_per_label=40,exclude_labels=None):
    """
    根据 DataFrame 中的 'point_name' 标签下载指定数量的图片到对应的文件夹，并使用日期后的部分作为文件名。

    Args:
        df (pd.DataFrame): 包含 'point_name' 和 'url' 列的 Pandas DataFrame。
        download_dir (str, optional): 下载图片保存的根目录。默认为 "downloaded_images"。
        images_per_label (int, optional): 每个标签要下载的图片数量。默认为 30。
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    labels = set(df['point_name'].tolist())
    for label in labels:
        if label in exclude_labels:
            print(f"跳过标签: {label}", flush=True)
            continue
        print(f"开始处理标签: {label}")
        label_df = df[df['point_name'] == label]
        urls_to_download = label_df['url'].tolist()[:images_per_label]

        label_dir = os.path.join(download_dir, label)
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)

        downloaded_count = 0
        for url in urls_to_download:
            filename = extract_filename_from_url(url)
            save_path = os.path.join(label_dir, filename)
            if download_images(url, save_path):
                downloaded_count += 1
                if downloaded_count >= images_per_label:
                    print(f"标签 '{label}' 已下载 {images_per_label} 张图片。", flush=True)
                    break
        print(f"标签 '{label}' 处理完成，共下载 {downloaded_count} 张图片。", flush=True)

# 假设你的 Excel 文件路径是 'C:\Users\great\Downloads\点位图片对应url.xlsx'
excel_file_path = '点位图片对应url.xlsx'
excluded_categories = [
    "HUD抬头显示",
    "车头局部",
    "第二排座椅前后调节",
    "第二排座椅躺平整体",
    "第三排",
    "方向盘左侧功能按键",
    "副驾驶座椅整体",
    "后备箱",
    "后排玻璃特写",
    "后排电源",
    "前排杯架",
    "前阅读灯"
]

try:
    df = pd.read_excel(excel_file_path)
    download_images_by_label(df,exclude_labels=excluded_categories)
    print("所有标签的图片下载完成。", flush=True)
except FileNotFoundError:
    print(f"错误: 文件 '{excel_file_path}' 未找到。", flush=True)
except Exception as e:
    print(f"发生错误: {e}", flush=True)
