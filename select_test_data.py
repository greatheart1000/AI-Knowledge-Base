import pandas as pd
import os
import random
import shutil # 导入 shutil 模块用于文件复制
import requests    # 新增
# --- 配置路径 ---
input_csv_path = 'Downloaded_images.csv' # 您的输入 CSV 文件路径
combined_csv_path = 'combined_part123.csv' # 您不希望重复的图片来源 CSV 文件路径
output_csv_path = 'Random_Unique_PointName_Images.csv' # 筛选后保存的新 CSV 文件路径
num_images_to_select = 20 # 您希望每个 point_name 种类选择的图片数量

# --- 新增：测试图片文件夹路径 ---
downloaded_images_folder = '/root/autodl-tmp/downloaded_images' # 您的下载图片文件夹路径
test_images_folder = '/root/autodl-tmp/test_images_for_training' # 新的测试图片文件夹路径

# 确保测试图片文件夹存在
os.makedirs(test_images_folder, exist_ok=True)
print(f"确保测试图片文件夹 '{test_images_folder}' 存在。")

# --- 步骤 0: 从 combined_part123.csv 获取不希望重复的图片文件名列表 ---
combined_image_names_to_exclude = set()
try:
    df_combined = pd.read_csv(combined_csv_path, encoding='gb18030') # 假设 combined_part123.csv 可能是 gb18030 编码
    print(f"成功读取 '{combined_csv_path}'，总行数: {len(df_combined)}")

    # 从 combined_part123.csv 的 'url' 列提取文件名
    # 假设 'url' 是包含图片URL的列名
    if 'url' in df_combined.columns:
        for url in df_combined['url'].tolist():
            # 提取文件名，处理可能的查询参数和锚点
            image_name = url.split('/')[-1].split('?')[0].split('#')[0]
            combined_image_names_to_exclude.add(image_name)
        print(f"从 '{combined_csv_path}' 中提取了 {len(combined_image_names_to_exclude)} 个不希望重复的图片文件名。")
    else:
        print(f"警告: '{combined_csv_path}' 中未找到 'url' 列。将无法排除重复图片。")

except FileNotFoundError:
    print(f"警告: '{combined_csv_path}' 文件不存在。将不对图片进行排除。")
except Exception as e:
    print(f"读取 '{combined_csv_path}' 或提取文件名时发生错误: {e}。将不对图片进行排除。")

# --- 步骤 1: 读取 CSV 文件 ---
try:
    df = pd.read_csv(input_csv_path, encoding='utf-8')
    print(f"成功读取 CSV 文件: '{input_csv_path}'，总行数: {len(df)}")
except FileNotFoundError:
    print(f"错误: 输入 CSV 文件 '{input_csv_path}' 不存在。请检查路径。")
    exit()
except Exception as e:
    print(f"读取 CSV 文件时发生错误: {e}")
    exit()

# --- 步骤 2: 筛选 task_type_name == '外观' 的行 ---
column_task_type = 'task_type_name' # 任务类型列的名称
column_point_name = 'point_name'   # 点位名称列的名称
column_image_url = 'url' # 假设图片URL列名为 'url'

if column_task_type not in df.columns:
    print(f"错误: CSV 文件中不存在列 '{column_task_type}'。请检查列名。")
    print(f"可用列: {df.columns.tolist()}")
    exit()

if column_point_name not in df.columns:
    print(f"错误: CSV 文件中不存在列 '{column_point_name}'。请检查列名。")
    print(f"可用列: {df.columns.tolist()}")
    exit()

if column_image_url not in df.columns:
    print(f"错误: CSV 文件中不存在列 '{column_image_url}'。请检查列名。")
    print(f"可用列: {df.columns.tolist()}")
    exit()

df_exterior = df[df[column_task_type] == '外观']
print(f"筛选 '{column_task_type}' 为 '外观' 后，共 {len(df_exterior)} 行。")

if df_exterior.empty:
    print("没有找到 task_type_name 为 '外观' 的行，无法进行选择。")
    exit()

# --- 步骤 3: 获取所有唯一的 point_name ---
unique_point_names = df_exterior[column_point_name].unique().tolist()
print(f"在 '外观' 类型中，共有 {len(unique_point_names)} 种不同的 '{column_point_name}'。")

# --- 步骤 4: 确定需要处理的所有唯一的 point_name (这里是全部) ---
# 既然您希望每个种类都选择，那么 selected_point_names 就是所有唯一的 point_name
selected_point_names = unique_point_names
print(f"将为每种 '{column_point_name}' (共 {len(selected_point_names)} 种) 尝试选择 {num_images_to_select} 张图片。")

# --- 步骤 5: 对于每个选中的 point_name，随机选择指定数量的图片，并排除已存在图片 ---
list_of_df_to_concat = [] # 用来存储每个point_name筛选出的DataFrame

for pn in selected_point_names:
    # 筛选出当前 point_name 的所有行
    df_current_point_name = df_exterior[df_exterior[column_point_name] == pn].copy() # 使用 .copy() 避免 SettingWithCopyWarning

    # 为当前 point_name 的数据创建临时文件名列
    df_current_point_name['_temp_image_name'] = df_current_point_name[column_image_url].apply(
        lambda url: url.split('/')[-1].split('?')[0].split('#')[0]
    )
    # 筛选掉在 combined_image_names_to_exclude 集合中的图片
    df_filtered_for_exclusion = df_current_point_name[
        ~df_current_point_name['_temp_image_name'].isin(combined_image_names_to_exclude)
    ].drop(columns=['_temp_image_name']) # 移除临时列

    if not df_filtered_for_exclusion.empty:
        # 从排除后的行中随机选择指定数量的图片
        # 确保选择的数量不超过当前可用的行数
        current_selection_count = min(num_images_to_select, len(df_filtered_for_exclusion))
        random_rows_for_pn = df_filtered_for_exclusion.sample(n=current_selection_count)
        list_of_df_to_concat.append(random_rows_for_pn)
        print(f"  '{pn}' 类别已选择 {current_selection_count} 张图片。")
    else:
        print(f"警告: '{pn}' 类型中没有可供选择的图片（可能因排除或数量不足而为空）。")

# 将所有选中的 DataFrame 拼接起来
if list_of_df_to_concat:
    df_final_selection = pd.concat(list_of_df_to_concat, ignore_index=True)
else:
    df_final_selection = pd.DataFrame(columns=df.columns) # 如果没有选中任何行，创建空DataFrame

print(f"\n最终选择了 {len(df_final_selection)} 张图片，它们包含多个 '{column_point_name}' 种类，每个种类最多 {num_images_to_select} 张。")

# --- 步骤 6: 保存结果到新的 CSV 文件 ---
try:
    df_final_selection.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"筛选结果已保存到 '{output_csv_path}'。")
except Exception as e:
    print(f"保存筛选结果时发生错误: {e}")

# --- 新增步骤 7: 将选中的图片复制到测试文件夹 ---
copied_count = 0
for index, row in df_final_selection.iterrows():
    image_url  = row[column_image_url]
    image_name = image_url.split('/')[-1].split('?')[0].split('#')[0]

    source_image_path      = os.path.join(downloaded_images_folder, image_name)
    destination_image_path = os.path.join(test_images_folder,    image_name)

    # 如果测试目录已存在，认为“已处理”
    if os.path.exists(destination_image_path):
        print(f"跳过：测试目录已存在 {image_name}")
        copied_count += 1
        continue

    # 1. 优先从本地已下载目录复制
    if os.path.exists(source_image_path):
        try:
            shutil.copy(source_image_path, destination_image_path)
            print(f"复制本地图片 {image_name}")
            copied_count += 1
        except Exception as e:
            print(f"复制失败 {image_name}：{e}")
        continue

    # 2. 本地不存在，则从网络下载
    try:
        print(f"本地无 {image_name}，尝试从 URL 下载…")
        resp = requests.get(image_url, stream=True, timeout=10)
        resp.raise_for_status()
        # 将下载的图片直接写入测试目录
        with open(destination_image_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"下载并保存 {image_name}")
        copied_count += 1
    except Exception as e:
        print(f"下载失败 {image_name}：{e}")

print(f"\n共处理 {copied_count} 张图片，保存在 {test_images_folder}")
