import os
import random
import requests
import pandas as pd
from urllib.parse import urlparse

def sample_and_download(
    data_file: str,
    point_name_col: str,
    point_code_col: str,
    point_type_col: str,
    url_col: str,
    output_root: str,
    output_csv: str,
    samples_per_class: int = 20,
    timeout: float = 10.0
):
    """
    从 data_file 中读取数据，按 point_name 分组，每组随机选 samples_per_class 条，
    下载图片到 output_root/point_name/ 下，并把 metadata 保存到 output_csv。
    """
    # 1. 读取表格
    ext = os.path.splitext(data_file)[1].lower()
    if ext in (".xls", ".xlsx"):
        df = pd.read_excel(data_file)
    elif ext == ".csv":
        df = pd.read_csv(data_file)
    else:
        raise ValueError("只支持 .xls/.xlsx/.csv 文件")

    # 2. 检查必要列
    for col in (point_name_col, point_code_col, point_type_col, url_col):
        if col not in df.columns:
            raise KeyError(f"在输入表格中找不到列：{col}")

    # 丢掉缺 URL 或 point_name 的行
    df = df.dropna(subset=[point_name_col, url_col])

    # 3. 创建输出根目录
    os.makedirs(output_root, exist_ok=True)

    records = []  # 用来汇总输出 CSV 的行

    # 4. 按 point_name 分组
    grouped = df.groupby(point_name_col)
    for pn, group in grouped:
        # 随机选取
        n = min(samples_per_class, len(group))
        sampled = group.sample(n, random_state=42)  # 固定种子可复现

        # 为这个 point_name 创建子目录
        safe_pn = str(pn).replace("/", "_")  # 避免非法字符
        dest_dir = os.path.join(output_root, safe_pn)
        os.makedirs(dest_dir, exist_ok=True)

        print(f"[{pn}] 总 {len(group)} 张，抽 {n} 张，下载到：{dest_dir}")

        # 5. 下载每张图片
        for _, row in sampled.iterrows():
            url = row[url_col]
            # 从 URL path 中提取文件名
            fname = os.path.basename(urlparse(url).path)
            if not fname:
                print(f"  ⚠️  无法从 URL 解析文件名，跳过：{url}")
                continue

            dst_path = os.path.join(dest_dir, fname)
            # 已下载过则跳过
            if os.path.exists(dst_path):
                print(f"  已存在，跳过：{dst_path}")
            else:
                try:
                    resp = requests.get(url, stream=True, timeout=timeout)
                    resp.raise_for_status()
                    with open(dst_path, "wb") as f:
                        for chunk in resp.iter_content(1024):
                            if chunk:
                                f.write(chunk)
                    print(f"  ✔ 下载成功：{fname}")
                except Exception as e:
                    print(f"  ✖ 下载失败：{url} -> {e}")
                    continue

            # 6. 收集 metadata
            records.append({
                "task_type_name":row["task_type_name"],
                point_name_col:   pn,
                point_code_col:   row[point_code_col],
                point_type_col:   row[point_type_col],
                url_col:          url,
                "local_path":     dst_path
            })

    # 7. 保存结果到 CSV
    df_out = pd.DataFrame(records)
    df_out.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\n全部下载完毕，已保存 metadata 到：{output_csv}")


if __name__ == "__main__":
    # --- 用户配置区域 ---
    data_file         = "all_images.xlsx"       # 输入表格
    point_name_col    = "point_name"           # 分类列
    point_code_col    = "point_code"
    point_type_col    = "point_type_name"
    url_col           = "url"
    output_root       = "./test_images_0624"  # 下载图片存放根目录
    output_csv        = "./test_metadata_0624.csv"
    samples_per_class = 20

    sample_and_download(
        data_file,
        point_name_col,
        point_code_col,
        point_type_col,
        url_col,
        output_root,
        output_csv,
        samples_per_class
    )
