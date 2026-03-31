import argparse
import os

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def _make_empty_tile(size):
    # 浅色渐变 + 轻微噪点：作为“设计元素”的空位填充
    c1 = (246, 246, 246)
    c2 = (232, 232, 232)

    grad = Image.linear_gradient("L").resize((size, size), Image.BILINEAR).rotate(45)
    tile = ImageOps.colorize(grad, black=c1, white=c2)

    noise = Image.effect_noise((size, size), 18).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    tile = Image.blend(tile, noise_rgb, 0.06)

    return tile


def create_collage(folder, target_ratio, rows, cols):
    # 获取所有图片文件
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"文件夹不存在: {folder}")

    images = []
    for f in os.listdir(folder):
        if not f.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        images.append(Image.open(os.path.join(folder, f)))
    n = len(images)

    if n == 0:
        raise ValueError(f"文件夹中未找到图片: {folder}")

    if rows <= 0 or cols <= 0:
        raise ValueError("rows/cols 必须为正整数")

    capacity = rows * cols
    if n > capacity:
        raise ValueError(
            f"图片数量({n})超过网格容量({rows}x{cols}={capacity})，请增大 rows/cols 或减少图片"
        )

    # 计算最小图片尺寸作为 cell_size
    cell_size = min(min(img.size) for img in images)

    # 目标比例仍用于最终画布留白/补边，行列由运行参数决定
    w, h = target_ratio

    # 缩放图片大小
    grid_w, grid_h = cols * cell_size, rows * cell_size
    # 网格底色固定为白色（空白格也保持干净）
    collage = Image.new("RGB", (grid_w, grid_h), 255)

    # 位置分配：默认按顺序从左到右、从上到下放图。
    # 但当需要填充 2 个空位时，优先把空位放到左上角与右下角。
    missing = capacity - n
    all_slots = list(range(capacity))

    if missing == 2:
        empty_slots = [0, capacity - 1]
        image_slots = [s for s in all_slots if s not in empty_slots]
    else:
        image_slots = all_slots[:n]
        empty_slots = all_slots[n:]

    # 拼接图片（不做圆角处理，保持封面方形）
    for img_idx, img in enumerate(images):
        slot = image_slots[img_idx]
        img = ImageOps.fit(img, (cell_size, cell_size), method=Image.Resampling.LANCZOS)
        x, y = (slot % cols) * cell_size, (slot // cols) * cell_size
        collage.paste(img, (x, y))

    # 缺格处理：用纹理块填满剩余单元格，让“缺一块”变成设计
    if empty_slots:
        tile = _make_empty_tile(cell_size)
        for slot in empty_slots:
            x, y = (slot % cols) * cell_size, (slot // cols) * cell_size
            collage.paste(tile, (x, y))

    # 调整到目标比例
    target_w = grid_w
    target_h = int(grid_w * h / w)
    if target_h < grid_h:
        target_h = grid_h
        target_w = int(grid_h * w / h)

    # 创建背景：默认使用“拼贴图拉伸 + 模糊 + 轻微加白”更适合作为封面
    blur_radius = max(8, min(target_w, target_h) // 30)
    final = collage.resize((target_w, target_h), Image.LANCZOS).filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )
    final = ImageEnhance.Brightness(final).enhance(1.08)
    final = Image.blend(final, Image.new("RGB", (target_w, target_h), 255), 0.18)

    final.paste(collage, ((target_w - grid_w) // 2, (target_h - grid_h) // 2))

    # 保存图片
    output_name = f"{os.path.basename(folder)}_{w}x{h}_{rows}x{cols}.jpg"
    final.save(output_name)
    print(f"拼接完成，已保存到 {output_name}")


# 添加命令行参数解析
def parse_args():
    parser = argparse.ArgumentParser(description="拼接图片为目标比例")
    parser.add_argument("folder", type=str, help="图片所在文件夹路径")
    parser.add_argument("width", type=int, help="目标比例的宽度部分")
    parser.add_argument("height", type=int, help="目标比例的高度部分")
    parser.add_argument("rows", type=int, help="网格行数")
    parser.add_argument("cols", type=int, help="网格列数")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    target_ratio = (args.width, args.height)
    create_collage(args.folder, target_ratio, args.rows, args.cols)
