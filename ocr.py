import cv2
import numpy as np
from paddleocr import PaddleOCR

def ocrProcessor(image):
    # 初始化PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    # 进行OCR识别
    result = ocr.ocr(image, cls=True)

    # 提取OCR结果
    ocr_data = []
    for line in result:
        for res in line:
            text = res[1][0]
            ocr_data.append(text)
    return ocr_data

# 测试代码
in_dir = '/Volumes/g/Downloads/uni_wechat/'  # 替换为你的表格图片路径
output_dir = '/Volumes/g/Downloads/uni_wechat/'
slice_obj = slice(0, 1)

# read all file in image_path
import os
for file in os.listdir(in_dir):
    if file.endswith(('.jpg', '.jpeg', '.png')):
        in_path = os.path.join(in_dir, file)
        output_path = os.path.join(output_dir, file)
        extracted = ocrProcessor(in_path)
        # write extracted to json file
        with open(f"{output_path}.json", "w") as f:
            json.dump(extracted, f, ensure_ascii=False)
        break

print("提取完成！")