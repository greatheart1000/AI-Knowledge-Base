import pandas as pd
import json

def generate_point_code_to_name_json(csv_file_path: str, output_json_path: str = "point_code_to_name.json"):
    """
    从CSV文件中提取point_code到point_name的映射，并保存为JSON。
    生成的JSON格式为: {"point_code": "point_name", ...}

    Args:
        csv_file_path (str): 包含 point_code 和 point_name 列的 CSV 文件路径。
        output_json_path (str): 生成的 JSON 文件的保存路径。
    """
    try:
        df = pd.read_excel(csv_file_path)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {csv_file_path}")
        return
    except Exception as e:
        print(f"读取CSV文件时发生错误: {e}")
        return

    # 确保这两列存在
    if "point_code" not in df.columns or "point_name" not in df.columns:
        print("错误: CSV 文件中缺少 'point_code' 或 'point_name' 列。")
        return

    # 提取唯一的 point_code 和 point_name 映射
    # 注意：这里假设一个 point_code 只对应一个 point_name
    # 如果一个 point_code 可能对应多个 point_name，你需要处理这种多对一关系
    # 例如：df[['point_code', 'point_name']].drop_duplicates()
    point_code_to_name_map = {}
    for index, row in df.iterrows():
        code = str(row["point_code"]) # 确保键是字符串
        name = str(row["point_name"]) # 确保值是字符串
        point_code_to_name_map[code] = name

    print(f"生成的 point_code 到 point_name 映射: {point_code_to_name_map}")

    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(point_code_to_name_map, f, ensure_ascii=False, indent=4)
        print(f"成功生成 {output_json_path}")
    except Exception as e:
        print(f"保存JSON文件时发生错误: {e}")

# 如何使用这个函数：
if __name__ == "__main__":
    # 假设你的 test_metadata.csv 文件就在当前目录下
    generate_point_code_to_name_json(
        csv_file_path='all_images.xlsx',
        output_json_path="./code2name.json"
    )
