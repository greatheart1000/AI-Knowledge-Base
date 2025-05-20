评估测试集的准确率 
1） 一共用了多少个图训练？    # 6155  （含 76点位？）
2） 测试用了 多少图 ？   # 824张图片 （含 76点位？）
3）每个位置　，对得多少，　错得多少？　要有个比率

训练集或者测试集里面每个类别的个数
import pandas as pd
# 1. 读入 CSV（根据需要加上 encoding、sep 等参数）
df = pd.read_csv(r"C:\Users\great\Downloads\filtered_data.csv")
# 2. 按四列分组，统计每一类的样本数量
grouped = (
    df
    .groupby(
        ["task_type_name", "material_type_name", "point_type_name", "point_name"],
        dropna=False  # 如果要把 NaN 也算一种类，可以保留这一行
    )
    .size()       # 统计每个组合的行数
    .reset_index(name="count")
)
# 3. 总共多少类
total_classes = grouped.shape[0]

# 4. 输出结果
print(f"总共 {total_classes} 类")
print(grouped)
grouped['type'] =grouped['task_type_name']+grouped['material_type_name']+':'+grouped['point_type_name']+'/'+grouped['point_name']
grouped.to_csv("grouped_counts.csv", index=False)




总的准确率 
import os
import pandas as pd
# 2. 读取 CSV 文件到 DataFrame
csv_file_path= r'C:\Users\great\Downloads\predictions.csv'
df = pd.read_csv(csv_file_path)
test_df = pd.read_csv('test.csv')
print(test_df['url'].head())
test_df['filename'] = test_df['url'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else None)
print("测试集数据总数:",len(test_df['filename'].tolist()))
# print(test_df['filename'].tolist())

print(f"成功读取 CSV 文件: {csv_file_path}，共 {len(df)} 行数据。")
# 创建一个列表来存储所有要保存到新 CSV 的数据
results_to_save = []

for item,data in zip(df['item'].tolist(),df['prediction'].tolist()):
    #print(item)
    alist = data.split(" ")
    part_1,part_2,part_3 = alist[0] ,alist[1],alist[2]
    pred =part_1.split(":")[-1]+"/"+part_2+" "+part_3
    print('pred:',pred)
    if item in test_df['filename'].tolist():
        #得到与item一样的 test_df的那一行数据
        matching_row = test_df[test_df['filename'] == item]
        if not matching_row.empty:
            # 获取匹配到的第一行作为 Series 对象
            single_row_data = matching_row.iloc[0]
            # 现在你可以直接通过列名访问这些值了：
            task_type = single_row_data['task_type_name']
            material_type = single_row_data['material_type_name']
            point_type = single_row_data['point_type_name']
            point_name = single_row_data['point_name']
            text =task_type+material_type+'/'+f"点位类型:{point_type} 点位名称:{point_name}"
            print('true:',text)
            if pred ==text:
                results_to_save.append([item, text,pred, '√'])
            else:
                results_to_save.append([item, text, pred, '×'])
output_csv_path = 'prediction_vs_true.csv'
output_df = pd.DataFrame(results_to_save, columns=['image', 'true', 'pred','count'])
# 保存到 CSV 文件，使用 utf-8 编码以确保中文显示正常
output_df.to_csv(output_csv_path, index=False, encoding='utf-8')

print(f"\n所有文件处理完毕。结果已保存到 '{output_csv_path}'。")
