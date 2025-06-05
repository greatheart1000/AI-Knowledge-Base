import json
import pandas as pd
records = []
num =0
with open('output_cot.jsonl' , 'r',encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        image_url = data['image_url']
        task_type = data['gt_task_type']
        point_type = data['gt_point_type']
        point_name = data['gt_point_name']
        cot = data['cot']
        model_pred_json =data['model_pred_json']
        if len(cot)>10:
            pass
            #print(cot)
            # print()
            # #print(cot.split('\n\n')[0])
            # part1= cot.split('\n\n')[0]
            # print()
            # adata = {
            #     "task_type": task_type,
            #     "point_type": point_type,
            #     "point_name": point_name
            # }
            # part2 = "\n最终 JSON:\n" + json.dumps(adata, ensure_ascii=False)
            # part = part1 + part2
            # #print(part)
            # print('=============')
            # records.append({
            #     'image_url': image_url,
            #     'part': part
            # })
        else:
            adata = {
                "task_type": task_type,
                "point_type": point_type,
                "point_name": point_name
            }
            part2 = "\n最终 JSON:\n" + json.dumps(adata, ensure_ascii=False)
            part1= model_pred_json['COT']
            part = part1 + part2
            records.append({
                'image_url': image_url,
                'part': part
            })
            num+=1
print(num)

# 把所有记录一次性转换成 DataFrame
df = pd.DataFrame(records, columns=['image_url', 'part'])

# 保存为 CSV，utf-8-sig 保证 Excel 下能正确识别中文
df.to_csv('part3_cot.csv', index=False, encoding='utf-8-sig')

print("保存完毕，共写入 %d 条记录" % len(df))

import pandas as pd

encodings = ['utf-8-sig', 'utf-8', 'gb18030', 'gbk', 'latin1']
for enc in encodings:
    try:
        df1 = pd.read_csv('part1_cot.csv', encoding=enc)
        print(f"成功用编码: {enc}")
        break
    except Exception as e:
        print(f"编码 {enc} 失败：{e}")


# 假设 df1 已经正确读入，并且有列 'part1'
df1 = pd.read_csv('part1_cot.csv', encoding='gb18030')

# 读入 df2
df2 = pd.read_csv('part2_cot.csv', encoding='utf-8-sig')

# （注意：先读 df2，再读 df1，保证 part1 的行在后面）
# 2. 垂直拼接
combined = pd.concat([df2, df1], axis=0, ignore_index=True)
# 3. 保存成一个新文件
combined.to_csv('combined_part12.csv',
                index=False,
                encoding='utf-8-sig')

print(f"写入完毕，共 {len(combined)} 行")

df1 = pd.read_csv('combined_part12.csv', encoding='utf-8-sig')

# 读入 df2
df2 = pd.read_csv('part3_cot.csv', encoding='utf-8-sig')

# （注意：先读 df2，再读 df1，保证 part1 的行在后面）
# 2. 垂直拼接
combined = pd.concat([df2, df1], axis=0, ignore_index=True)
# 3. 保存成一个新文件
combined.to_csv('combined_part123.csv',
                index=False,
                encoding='utf-8-sig')

print(f"写入完毕，共 {len(combined)} 行")

df = pd.read_csv('combined_part123.csv', encoding='utf-8-sig')
df['image_url'].tolist()

import pandas as pd
import json
# 载入CSV文件
df = pd.read_csv('combined_part123.csv', encoding='gb18030')
conversations = []
with open("point_mapping.json", 'r', encoding='utf-8') as f:
    mapping = json.load(f)

mapping_str = json.dumps(mapping, ensure_ascii=False, indent=2)

SYSTEM_PROMPT = f"""
你是汽车图像分类专家。
下面给出了所有合法的二级点位类型(point_type_name) (辅助图,整体外观,其他细节)及其对应的三级点位名称(point_name)列表：
{mapping_str}
请你按照严格的三步推理流程，结合给定的图片，生成符合逻辑的推理过程：
1. 第一步：确认这是一张“外观”图片，并简要说明依据。
2. 第二步：从上述 point_type_name 列表中，选择最符合的那一项，并说明理由。
3. 第三步：在选中的 point_type_name 对应的点位名称列表里，选择最符合的 point_name，并说明理由。

在推理过程中，请确保你的解释和理由能够合理支持给定的答案。

最后，请仅输出一个有效 JSON：
{{"task_type": "外观", "point_type": "…", "point_name": "…"}}
请开始你的推理过程：
"""

# 添加对话数据
for i in range(len(df)):
    print(df.iloc[i]['image_url'])
    url_path ="/root/autodl-tmp/train_images/"+df.iloc[i]['image_url'].split('/')[-1]
    conversations.append({
        "id": f"identity_{i+1}",
        "conversations": [
            {
                "from": "user",
                "value": f"{SYSTEM_PROMPT} <|vision_start|>{url_path}<|vision_end|>"
            },
            {
                "from": "assistant",
                "value": df.iloc[i]['part']
            }
        ]
    })

# 保存为Json
with open('train_data_vl.json', 'w', encoding='utf-8') as f:
    json.dump(conversations, f, ensure_ascii=False, indent=2)
