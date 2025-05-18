下载图片至文件夹，只保留好的图片至问价 请你再将下载后 图片损坏的图片不保存到文件夹里，只保留那些图片好的到文件夹以及新的csv里面 这个代码怎么写呢

import requests
import threading
import os
# import re # 这个脚本中没有用到 re 模块，可以移除
import pandas as pd
from urllib.parse import urlparse
import time
import csv
from PIL import Image # 导入 Pillow 库

# 定义一个线程锁，用于安全访问共享数据（成功下载的列表）
list_lock = threading.Lock()
# 定义一个列表，用于存储成功下载并验证通过的图片对应的行数据
successful_rows_data = []

def verify_image(filepath):
    """
    验证图片文件是否有效（非损坏）。
    使用 Pillow 尝试打开并验证。
    """
    try:
        img = Image.open(filepath)
        img.verify() # 尝试验证图片文件的完整性
        img.close() # 关闭文件句柄，释放资源
        return True
    except (IOError, SyntaxError, FileNotFoundError, Image.UnidentifiedImageError) as e:
        # 捕获常见的图片损坏、文件不存在或格式无法识别错误
        # print(f"图片验证失败 (文件可能已损坏): {filepath} - {e}") # 可选：打印验证失败的详细信息
        return False
    except Exception as e:
        # 捕获验证过程中可能发生的其他意外错误
        print(f"图片验证过程中发生意外错误: {filepath} - {e}")
        return False

def download_image_and_verify(row_data, url, save_dir, max_retries=3, retry_delay=5, timeout=30):
    """
    下载单个图片，文件名取自 URL 的最后一部分。
    下载成功后进行图片验证，只有验证通过的图片才保留并将其行数据加入成功列表。
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    # 检查文件名是否有效
    if not filename or filename == '/' or '.' not in filename: # 增加对文件名的基本检查
        print(f"Warning: Skipping URL with invalid filename in path: {url}")
        return

    filepath = os.path.join(save_dir, filename)

    # 检查文件是否已经存在
    if os.path.exists(filepath):
        # 如果文件已存在，先验证它是否有效
        if verify_image(filepath):
            print(f"已存在文件验证成功，跳过下载: {filepath}")
            # 已存在且有效，标记为成功
            with list_lock:
                successful_rows_data.append(row_data)
            return # 文件已存在且有效，直接返回
        else:
            # 已存在但验证失败，删除损坏文件并尝试重新下载
            print(f"已存在文件验证失败，可能已损坏，删除并尝试重新下载: {filepath}")
            try:
                os.remove(filepath)
                print(f"已删除损坏文件: {filepath}")
            except OSError as e:
                print(f"删除损坏文件失败 {filepath}: {e}")
            # 文件被删除，继续下面的下载流程


    # 开始下载循环
    for i in range(max_retries):
        try:
            # 设置更长的超时时间
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功 (200 OK)

            # 确保保存目录存在 (可以在主线程中一次性完成，但这里再次检查也无妨)
            os.makedirs(save_dir, exist_ok=True)

            # 将图片内容写入文件
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # --- 下载成功后进行图片验证 ---
            if verify_image(filepath):
                print(f"成功下载并验证图片: {url} -> {filepath} (尝试次数: {i+1})")
                # 下载且验证成功！将对应的行数据添加到共享列表中
                with list_lock:
                    successful_rows_data.append(row_data)
                return  # 下载并验证成功，退出重试循环

            else:
                # 图片下载成功，但验证失败，文件可能已损坏
                print(f"图片文件下载成功但验证失败，文件可能已损坏: {filepath} (尝试次数: {i+1})")
                # 删除这个损坏的文件
                try:
                    os.remove(filepath)
                    print(f"已删除损坏文件: {filepath}")
                except OSError as e:
                    print(f"删除损坏文件失败 {filepath}: {e}")
                # 验证失败，不计为本次尝试的成功，如果还有重试次数会继续尝试下载

        except requests.exceptions.RequestException as e:
            print(f"下载失败 (尝试 {i+1}/{max_retries}): {url} - {e}")
            # 检查是否是已存在的网络错误，不应重试的可以跳过
            # if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code in [404, 403]:
            #    print(f"永久性错误（如404/403），不再重试: {url}")
            #    break # 不再重试

            if i < max_retries - 1:
                time.sleep(retry_delay)
        except Exception as e: # 捕获下载或写入过程中可能发生的其他意外异常
             print(f"下载或写入过程中发生意外错误: {url} - {e}")
             break # 发生意外错误，不再重试

    # 如果循环结束仍未成功（下载失败或验证失败次数达到上限）
    print(f"下载多次失败或最终验证失败，跳过: {url}")
    # 这些失败的行不会被添加到 successful_rows_data 中

# 修改主函数，启动多线程，并保存结果
if __name__ == "__main__":
    excel_file = "test.csv"  # 你的 CSV 文件名
    save_directory = "downloaded_images_validated"  # 指定保存图片的文件夹，改个名字区分
    url_column = "url"  # 指定包含图片 URL 的列名
    output_csv_file = "successful_and_valid_downloads.csv" # 指定保存成功下载并验证通过记录的新 CSV 文件名

    num_threads = 10  # 可以调整线程数量
    max_retries = 3    # 下载失败后的最大重试次数
    retry_delay = 5    # 重试之间的等待时间（秒）
    timeout = 30       # 下载超时时间（秒）

    try:
        df = pd.read_csv(excel_file)
        if url_column not in df.columns:
            print(f"错误：CSV 文件中找不到名为 '{url_column}' 的列。")
            exit()

        # 确保保存图片的文件夹存在
        os.makedirs(save_directory, exist_ok=True)

        threads = []
        # 遍历 DataFrame 的每一行，为每一行创建一个下载线程
        for index, row in df.iterrows():
            url = row.get(url_column) # 使用 .get() 安全获取 URL

            if not url: # 如果 URL 为空，跳过这一行
                print(f"Warning: Skipping row {index} due to empty URL.")
                continue

            # 将整行数据转换为字典传递给线程
            row_data = row.to_dict()

            # 创建线程，目标函数是 download_image_and_verify
            # 将行数据、URL、保存目录、共享列表和锁作为参数传递
            thread = threading.Thread(target=download_image_and_verify,
                                      args=(row_data, url, save_directory, max_retries, retry_delay, timeout))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成下载任务
        for thread in threads:
            thread.join()

        print("\n====== 所有图片下载和验证尝试完成！======\n")

        # 所有线程都结束后，successful_rows_data 列表中就包含了所有成功下载并验证通过的图片对应的行数据

        # 将成功下载并验证通过的行数据保存到新的 CSV 文件
        if successful_rows_data:
            # 从收集到的字典列表创建新的 DataFrame
            successful_df = pd.DataFrame(successful_rows_data)

            # 将新的 DataFrame 保存为 CSV 文件
            # encoding='utf-8' 用于处理中文字符
            successful_df.to_csv(output_csv_file, index=False, encoding='utf-8')
            print(f"成功将 {len(successful_rows_data)} 条有效记录保存到文件: '{output_csv_file}'")
        else:
            print("没有图片成功下载并通过验证，未创建输出 CSV 文件。")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{excel_file}'。")
    except Exception as e:
        print(f"发生错误: {e}")
