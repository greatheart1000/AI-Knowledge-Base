import os
import math
import json
import torch
import pandas as pd
from PIL import Image
from torchvision import transforms
from model import resnet34

def batch_infer(
    metadata_csv: str,
    class_indices_json: str,
    weights_path: str,
    batch_size: int = 10,
    output_csv: str = "test_metadata_with_pred.csv",
    log_interval: int = 100,       # 每多少张图片打印一次
):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"[START] using device: {device}")

    # 1. 读入 metadata
    df = pd.read_csv(metadata_csv)
    assert "local_path" in df.columns and "point_name" in df.columns, \
        "CSV 必须包含 local_path 和 point_name 两列"
    n = len(df)

    # 2. 图像预处理
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    # 3. class_indict
    with open(class_indices_json, "r") as f:
        class_indict = json.load(f)  # {"0":"baking_cakes", ...}

    # 4. 模型加载
    model = resnet34(num_classes=len(class_indict)).to(device)
    assert os.path.exists(weights_path), f"找不到模型权重 {weights_path}"
    sd = torch.load(weights_path, map_location=device, weights_only=True)
    model.load_state_dict(sd)
    model.eval()

    # 准备输出列
    df["predicted"] = ""
    df["correct"]   = False

    processed = 0  # 全局已处理图片数

    with torch.no_grad():
        steps = math.ceil(n / batch_size)
        for step in range(steps):
            batch_df = df.iloc[step*batch_size : (step+1)*batch_size]
            imgs, idxs = [], []
            for idx, row in batch_df.iterrows():
                try:
                    img = Image.open(row["local_path"]).convert("RGB")
                    imgs.append(data_transform(img))
                    idxs.append(idx)
                except Exception as e:
                    print(f"[WARN] 无法打开 {row['local_path']}，跳过：{e}")

            if not imgs:
                continue

            batch_tensor = torch.stack(imgs, dim=0).to(device)
            out = model(batch_tensor).cpu()
            probs = torch.softmax(out, dim=1)
            preds = torch.argmax(probs, dim=1).numpy()

            # 填回 df 并打印（每 log_interval 张）
            for local_idx, cls_idx in zip(idxs, preds):
                pred_label = class_indict[str(int(cls_idx))]
                df.at[local_idx, "predicted"] = pred_label
                df.at[local_idx, "correct"]   = (pred_label == df.at[local_idx, "point_name"])
                processed += 1

                # 如果达到打印间隔，就把最近这一张也打印出来
                if processed % log_interval == 0 or processed == n:
                    print(f"[PROGRESS] {processed}/{n} images processed, "
                          f"last prediction: {df.at[local_idx, 'local_path']} => {pred_label}, "
                          f"correct: {df.at[local_idx, 'correct']}")

    # 5. 保存结果
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"[DONE] all done, saved to {output_csv}")

if __name__ == "__main__":
    batch_infer(
        metadata_csv       = "test_metadata.csv",
        class_indices_json = "./class_indices.json",
        weights_path       = "./resNet34_100.pth",
        batch_size         = 10,
        output_csv         = "test_metadata_with_pred.csv",
        log_interval       = 100
    )
