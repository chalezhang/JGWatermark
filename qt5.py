import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSlider, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import os


class WatermarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_folder = ''
        self.output_folder = ''
        self.watermark_path = 'shuiyin.png'  # 水印图片路径
        self.scale_factor = 0.4  # 默认水印大小比例
        self.height_position = 0.25  # 默认高度位置为 1/2
        self.width_position = 0.5  # 默认宽度位置为 1/2

    def initUI(self):
        layout = QVBoxLayout()

        # 添加 logo 图片并调整大小
        self.logo_label = QLabel(self)
        pixmap = QPixmap("logo.png")  # 替换为你的 logo 文件路径
        pixmap = pixmap.scaled(200, 200)  # 调整 logo 大小为 200 x 200 像素
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(200, 200)  # 设置 QLabel 固定大小
        layout.addWidget(self.logo_label)

        self.label_input = QLabel("选择输入文件夹")
        layout.addWidget(self.label_input)
        self.btn_input = QPushButton("选择输入文件夹")
        self.btn_input.clicked.connect(self.select_input_folder)
        layout.addWidget(self.btn_input)

        self.label_output = QLabel("选择输出文件夹")
        layout.addWidget(self.label_output)
        self.btn_output = QPushButton("选择输出文件夹")
        self.btn_output.clicked.connect(self.select_output_folder)
        layout.addWidget(self.btn_output)

        # 添加滑块设置水印大小
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(100)
        self.size_slider.setValue(40)  # 默认值 30%
        self.size_slider.setTickInterval(10)
        self.size_slider.setTickPosition(QSlider.TicksBelow)
        self.size_slider.valueChanged.connect(self.update_watermark_size)
        layout.addWidget(QLabel("水印大小 (10-100%)"))
        layout.addWidget(self.size_slider)

        # 添加下拉菜单选择水印宽度位置
        self.width_position_combo = QComboBox()
        self.width_position_combo.addItems(["0", "1/4", "1/2", "3/4"])
        self.width_position_combo.currentTextChanged.connect(self.update_width_position)
        layout.addWidget(QLabel("水印宽度位置"))
        layout.addWidget(self.width_position_combo)

        # 添加下拉菜单选择水印高度位置
        self.height_position_combo = QComboBox()
        self.height_position_combo.addItems(["0", "1/4", "1/2", "3/4"])
        self.height_position_combo.currentTextChanged.connect(self.update_height_position)
        layout.addWidget(QLabel("水印高度位置"))
        layout.addWidget(self.height_position_combo)

        # 添加显示处理进度的 QLabel
        self.progress_label = QLabel("处理进度：尚未开始")
        layout.addWidget(self.progress_label)

        self.btn_process = QPushButton("添加水印并保存")
        self.btn_process.clicked.connect(self.add_watermark)
        layout.addWidget(self.btn_process)

        self.setLayout(layout)
        self.setWindowTitle("极光珠宝水印添加工具")

    def select_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        self.label_input.setText(f"输入文件夹: {self.input_folder}")

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        self.label_output.setText(f"输出文件夹: {self.output_folder}")

    def update_watermark_size(self, value):
        self.scale_factor = value / 100.0  # 将滑块值转换为比例
        self.progress_label.setText(f"水印大小设置为: {value}%")

    def update_width_position(self, position):
        self.width_position = self.get_position_ratio(position)
        self.progress_label.setText(f"水印宽度位置设置为: {position}")

    def update_height_position(self, position):
        self.height_position = self.get_position_ratio(position)
        self.progress_label.setText(f"水印高度位置设置为: {position}")

    def get_position_ratio(self, position):
        if position == "0":
            return 0.0
        elif position == "1/4":
            return 0.25
        elif position == "1/2":
            return 0.5
        elif position == "3/4":
            return 0.75
        return 0.5  # 默认返回 1/2

    def add_watermark(self):
        if not self.input_folder or not self.output_folder:
            self.progress_label.setText("请先选择输入和输出文件夹")
            return

        watermark = Image.open(self.watermark_path).convert("RGBA")

        os.makedirs(self.output_folder, exist_ok=True)

        image_files = [f for f in os.listdir(self.input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        if not image_files:
            self.progress_label.setText("未找到任何图片文件")
            return

        for idx, filename in enumerate(image_files, start=1):
            img_path = os.path.join(self.input_folder, filename)
            img = Image.open(img_path).convert("RGBA")

            img_width, img_height = img.size
            new_watermark_width = int(img_width * self.scale_factor)
            new_watermark_height = int(watermark.size[1] * (new_watermark_width / watermark.size[0]))
            watermark_resized = watermark.resize((new_watermark_width, new_watermark_height), Image.LANCZOS)

            # 计算水印位置
            x_position = int(self.width_position * (img_width - new_watermark_width))
            y_position = int(self.height_position * (img_height - new_watermark_height))
            position = (x_position, y_position)

            watermarked_img = img.copy()
            watermarked_img.paste(watermark_resized, position, watermark_resized)
            output_path = os.path.join(self.output_folder, filename)
            watermarked_img = watermarked_img.convert("RGB")
            watermarked_img.save(output_path)

            self.progress_label.setText(f"正在处理：{filename} ({idx}/{len(image_files)})")
            QApplication.processEvents()

        self.progress_label.setText("所有图片已处理完成！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WatermarkApp()
    ex.show()
    sys.exit(app.exec_())
