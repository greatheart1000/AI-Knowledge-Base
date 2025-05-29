#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/29 16:12
# @Author  : caijian
# @File    : test2.py
# @Software: PyCharm
import pandas as pd

# --- 配置 ---
csv_file_path = 'unique_sampled.csv' # 请确保路径正确

true_task_col = 'task_type_name'
true_point_type_col = 'point_type_name'
true_point_name_col = 'point_name'
prediction_col = 'prediction'

# --- 1. 读取 CSV 文件 ---
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"错误：文件 '{csv_file_path}' 未找到。请检查文件名和路径。")
    exit()
except Exception as e:
    print(f"读取CSV文件时发生错误: {e}")
    exit()

# 检查必要的列
required_true_cols = [true_task_col, true_point_type_col, true_point_name_col]
if not all(col in df.columns for col in required_true_cols):
    print(f"错误：CSV文件中缺少真实标签列: {', '.join(required_true_cols)}")
    exit()
if prediction_col not in df.columns:
    print(f"错误：CSV文件中缺少预测列: {prediction_col}")
    exit()

# --- 2. 定义解析预测字符串的函数 (与之前相同) ---
def parse_prediction_string(prediction_str):
    if not isinstance(prediction_str, str):
        return None, None, None
    parts = prediction_str.split(" ")
    if len(parts) == 3:
        try:
            pred_task = parts[0].split(':')[-1][:2]
            pred_point_type = parts[1].split(':')[-1]
            pred_point_name = parts[2].split(':')[-1]
            return pred_task, pred_point_type, pred_point_name
        except Exception: # 更通用的异常捕获
            return None, None, None
    else:
        return None, None, None

# --- 3. 应用解析函数，为DataFrame添加预测结果列 (与之前相同) ---
try:
    df[['pred_task', 'pred_point_type', 'pred_point_name']] = df[prediction_col].apply(
        lambda x: pd.Series(parse_prediction_string(x))
    )
except Exception as e:
    print(f"解析预测列时发生错误: {e}")
    exit()

# --- 4. 判断各个组件及组合预测的正确性 (与之前相同) ---
df['is_task_correct'] = (df['pred_task'] == df[true_task_col])
df['is_ptype_correct'] = (df['pred_point_type'] == df[true_point_type_col])
df['is_pname_correct'] = (df['pred_point_name'] == df[true_point_name_col])

df['is_task_ptype_correct'] = df['is_task_correct'] & df['is_ptype_correct']
df['is_task_pname_correct'] = df['is_task_correct'] & df['is_pname_correct']
df['is_ptype_pname_correct'] = df['is_ptype_correct'] & df['is_pname_correct']
df['is_all_three_correct'] = df['is_task_correct'] & df['is_ptype_correct'] & df['is_pname_correct']

# --- 5. 按类别分组并计算各类别的详细准确率指标 ---
class_group_cols = [true_task_col, true_point_type_col, true_point_name_col]

class_detailed_accuracies = df.groupby(class_group_cols, dropna=False).agg(
    total_instances=('pred_task', 'size'),
    sum_correct_task=('is_task_correct', 'sum'),
    sum_correct_ptype=('is_ptype_correct', 'sum'),
    sum_correct_pname=('is_pname_correct', 'sum'),
    sum_correct_task_ptype=('is_task_ptype_correct', 'sum'),
    sum_correct_task_pname=('is_task_pname_correct', 'sum'),
    sum_correct_ptype_pname=('is_ptype_pname_correct', 'sum'),
    sum_correct_all_three=('is_all_three_correct', 'sum')
).reset_index()

# 定义准确率指标列名和对应的计数器列名
metrics_to_calculate = {
    'acc_task_only': 'sum_correct_task',
    'acc_ptype_only': 'sum_correct_ptype',
    'acc_pname_only': 'sum_correct_pname',
    'acc_task_ptype': 'sum_correct_task_ptype',
    'acc_task_pname': 'sum_correct_task_pname',
    'acc_ptype_pname': 'sum_correct_ptype_pname',
    'acc_all_three': 'sum_correct_all_three'
}

# 计算各项准确率并保留两位小数
for acc_col_name, sum_col_name in metrics_to_calculate.items():
    # 先计算原始准确率值
    accuracy_values = class_detailed_accuracies[sum_col_name] / class_detailed_accuracies['total_instances']
    # 将可能出现的 NaN (因除以0产生，尽管这里 total_instances 通常不为0) 替换为 0
    accuracy_values = accuracy_values.fillna(0)
    # 对准确率值四舍五入到两位小数
    class_detailed_accuracies[acc_col_name] = accuracy_values.round(2)

# --- 6. 输出结果 ---
print(f"\n总共处理了 {len(df)} 行数据。")
print(f"识别出 {len(class_detailed_accuracies)} 个不同的类别。")
print("\n每个类别内部的详细准确率指标 (准确率已保留两位小数)：")

# 如果希望打印时也严格控制小数位数（例如0.5显示为0.50），可以使用float_format
# 不过 .round(2) 已经改变了DataFrame中的值，通常直接打印即可
# 如果有特别的显示需求，可以这样：
# formatters = {col: '{:.2f}'.format for col in metrics_to_calculate.keys()}
# print(class_detailed_accuracies.to_string(formatters=formatters))
print(class_detailed_accuracies.to_string()) # 打印DataFrame，现在准确率列已经是两位小数了
# (可选) 将结果保存到新的CSV文件
output_detailed_accuracy_file = 'class_detailed_accuracy_report.csv' # 文件名
class_detailed_accuracies.to_csv(output_detailed_accuracy_file, index=False, encoding='utf-8-sig')
# 当保存到CSV时，由于我们已经对DataFrame中的值进行了round(2)，所以CSV中也会是两位小数。
# 如果想确保CSV中特定格式如 "0.50"，可以使用 float_format='%.2f' 参数：
# class_detailed_accuracies.to_csv(output_detailed_accuracy_file, index=False, encoding='utf-8-sig', float_format='%.2f')
print(f"\n详细准确率报告已保存至: {output_detailed_accuracy_file}")
