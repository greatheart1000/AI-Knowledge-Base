import os
from PIL import Image, UnidentifiedImageError

def is_image_valid(image_path: str) -> bool:
    """
    使用 PIL verify() 来检查文件完整性。
    成功打开并验证通过则返回 True，否则 False。
    """
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except (IOError, OSError, SyntaxError, UnidentifiedImageError):
        return False

def clean_broken_images(base_dir: str):
    """
    递归遍历 base_dir 下所有文件，尝试按图像打开并验证：
    - 验证失败（抛异常）的文件即认为“损坏”并删除。
    - 不再依赖文件后缀。
    """
    total_checked = 0
    total_deleted = 0

    for root, dirs, files in os.walk(base_dir):
        for fname in files:
            path = os.path.join(root, fname)
            total_checked += 1

            if not is_image_valid(path):
                try:
                    os.remove(path)
                    total_deleted += 1
                    print(f"[删除] 损坏或非图像文件: {path}")
                except Exception as e:
                    print(f"[错误] 删除失败: {path}，{e}")

    print("\n=== 清理完成 ===")
    print(f"扫描文件总数:           {total_checked}")
    print(f"检测并删除损坏/非图像文件: {total_deleted}")

if __name__ == "__main__":
    # 改成你的 con_train 根目录
    train_base_dir = "/data/con_train/train"
    clean_broken_images(train_base_dir)
