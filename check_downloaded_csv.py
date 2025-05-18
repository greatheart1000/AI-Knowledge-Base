"""我现在不想重新下载图片，只是单纯想根据下载得到的图片的文件夹和test.csv得到下载图片的csv，代码怎么写呢
好的，如果你只是想根据已有的 test.csv 文件和已经下载到某个文件夹（比如 downloaded_images_last_part）中的图片，来生成一个只包含对应图片已存在行的新的 CSV 文件，而不需要进行任何下载操作，那代码就简单得多了。
你需要做的是：
读取 test.csv 文件。
获取已下载图片文件夹中所有文件的列表。
遍历 CSV 文件中的每一行。
对于每一行，根据 URL 确定图片的文件名。
检查这个文件名是否存在于已下载文件夹的文件列表中。
如果存在，就保留这一行数据。
最后将所有保留的行数据写入一个新的 CSV 文件。
以下是实现这个功能的 Python 脚本："""
import pandas as pd
import os
from urllib.parse import urlparse

# --- 配置部分 ---
csv_file = "test.csv"  # 你的原始 CSV 文件名
downloaded_images_folder = "downloaded_images_last_part"  # 存放已下载图片的文件夹路径
url_column = "url"  # CSV 文件中包含图片 URL 的列名
output_csv_file = "existing_downloaded_urls.csv"  # 保存对应图片已存在的行的新 CSV 文件名
# ----------------

def get_filename_from_url(url):
    """从 URL 中提取文件名"""
    if not url:
        return None
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        # 增加对文件名的基本检查
        if not filename or filename == '/' or '.' not in filename.split('/')[-1]:
            return None
        return filename
    except Exception as e:
        print(f"Warning: Could not parse filename from URL '{url}': {e}")
        return None

# 用于存储对应图片已存在的原始行数据（以字典形式存储）
existing_rows_data = []

try:
    # 1. 读取原始 CSV 文件
    df = pd.read_csv(csv_file)

    if url_column not in df.columns:
        print(f"错误：CSV 文件 '{csv_file}' 中找不到名为 '{url_column}' 的列。")
        exit()

    # 2. 获取已下载图片文件夹中所有文件的列表
    if not os.path.isdir(downloaded_images_folder):
        print(f"错误：已下载图片文件夹不存在: {downloaded_images_folder}")
        print("请确保文件夹路径正确，并且文件夹中包含你想要检查的图片文件。")
        exit()

    # 获取文件夹中所有条目（文件和子文件夹）的名称列表
    existing_files_in_folder = set(os.listdir(downloaded_images_folder)) # 使用 set 加快查找速度
    print(f"在文件夹 '{downloaded_images_folder}' 中找到 {len(existing_files_in_folder)} 个条目。")


    # 3. 遍历 CSV 文件中的每一行
    print(f"正在检查 {len(df)} 行 CSV 数据...")
    for index, row in df.iterrows():
        url = row.get(url_column) # 安全获取 URL

        if not url:
            # print(f"Warning: Skipping row {index} due to empty URL.") # 可选：打印空 URL 警告
            continue

        # 4. 根据 URL 确定预期的文件名
        expected_filename = get_filename_from_url(url)

        if expected_filename is None:
             # print(f"Warning: Skipping row {index} due to invalid URL format: {url}") # 可选：打印无效 URL 警告
             continue


        # 5. 检查预期的文件名是否存在于已下载文件夹的文件列表中
        if expected_filename in existing_files_in_folder:
            # 6. 如果文件存在，保留这一行数据
            existing_rows_data.append(row.to_dict()) # 将整行数据转为字典并添加到列表中
            # print(f"找到匹配文件: {expected_filename}") # 可选：打印找到匹配的提示

    print(f"\n检查完成。找到 {len(existing_rows_data)} 行对应的图片已存在。")

    # 7. 将所有保留的行数据写入一个新的 CSV 文件
    if existing_rows_data:
        # 从收集到的字典列表创建新的 DataFrame
        output_df = pd.DataFrame(existing_rows_data)

        # 为了保持与原 CSV 文件相同的列顺序，重新排序列
        original_columns = df.columns.tolist()
        # 确保 output_df 包含所有原始列，并按原始顺序排列
        # 这里假设 existing_rows_data 中的字典包含了原始行的所有键
        output_df = output_df[original_columns]


        # 将新的 DataFrame 保存为 CSV 文件
        # index=False 不写入 DataFrame 的索引
        # encoding='utf-8' 用于正确处理可能的中文或其他非 ASCII 字符
        output_df.to_csv(output_csv_file, index=False, encoding='utf-8')

        print(f"成功将 {len(existing_rows_data)} 条记录保存到文件: '{output_csv_file}'")
    else:
        print("没有找到对应的图片文件，未创建输出 CSV 文件。")

except FileNotFoundError:
    print(f"错误：找不到文件 '{csv_file}'。")
except Exception as e:
    print(f"发生意外错误: {e}")
