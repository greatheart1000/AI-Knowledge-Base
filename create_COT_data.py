import json
import pandas as pd
records = []

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
            #print(cot)
            print()
            #print(cot.split('\n\n')[0])
            part1= cot.split('\n\n')[0]
            print()
            adata = {
                "task_type": task_type,
                "point_type": point_type,
                "point_name": point_name
            }
            part2 = "\n最终 JSON:\n" + json.dumps(adata, ensure_ascii=False)
            part = part1 + part2
            #print(part)
            print('=============')
            records.append({
                'image_url': image_url,
                'part': part
            })
# 把所有记录一次性转换成 DataFrame
df = pd.DataFrame(records, columns=['image_url', 'part'])

# 保存为 CSV，utf-8-sig 保证 Excel 下能正确识别中文
df.to_csv('part2_cot.csv', index=False, encoding='utf-8-sig')

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
