from PIL import Image
import os


def add_watermark(input_folder, watermark_path, output_folder, scale_factor=0.3):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 打开水印图像并获取其初始尺寸
    watermark = Image.open(watermark_path).convert("RGBA")

    # 遍历输入文件夹中的所有图片
    for filename in os.listdir(input_folder):
        # 检查文件是否为图片格式（如jpg, png等）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path).convert("RGBA")

            # 获取图片尺寸
            img_width, img_height = img.size

            # 计算水印的新尺寸，基于原图尺寸和缩放比例
            new_watermark_width = int(img_width * scale_factor)
            new_watermark_height = int(watermark.size[1] * (new_watermark_width / watermark.size[0]))
            watermark_resized = watermark.resize((new_watermark_width, new_watermark_height), Image.LANCZOS)

            # 计算水印位置，使其居中
            position = (
                (img_width - new_watermark_width) // 2,
                (img_height - new_watermark_height) // 4
            )

            # 将水印叠加到图片上
            watermarked_img = img.copy()
            watermarked_img.paste(watermark_resized, position, watermark_resized)

            # 保存带有水印的图片到输出文件夹
            output_path = os.path.join(output_folder, filename)
            watermarked_img = watermarked_img.convert("RGB")  # 转换为RGB模式，去除alpha通道
            watermarked_img.save(output_path)
            print(f"Processed and saved: {output_path}")


# 设置输入目录，水印图片路径，和输出目录
input_folder = '20241108'  # 替换为图片所在的文件夹路径
watermark_path = 'shuiyin.png'  # 水印图片的文件路径
output_folder = 'output_20241108'  # 替换为输出文件夹的路径

# 运行函数
add_watermark(input_folder, watermark_path, output_folder)
