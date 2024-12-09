import cv2
import numpy as np
from paddleocr import PaddleOCR
from enum import Enum
import json

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

class TableExtractionMode(Enum):
    ROWS = 1
    COLS = 2

def extract_table(image_path, mode, slice_obj):
    # 读取图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("无法加载图片，请检查路径！")

    # 二值化处理
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    isRow = mode == TableExtractionMode.ROWS

    # 检测水平和垂直线条
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))  # 水平核
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))   # 垂直核
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, vertical_kernel, iterations=4)

    lines = horizontal_lines if isRow else vertical_lines
    
    # 寻找轮廓
    contours, _ = cv2.findContours(lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    
    print('bounding_boxes', bounding_boxes)

    # 排序轮廓（按行或列顺序）
    bounding_boxes = sorted(bounding_boxes, key=lambda x: x[1 if isRow else 0])
    
    # 提取对应行或列的图像
    extracted_images = []
    start, stop = slice_obj.start, slice_obj.stop
    box_len = len(bounding_boxes)
    start_row = start or 0
    stop_row = stop
    if stop != None:
        if stop > box_len:
            stop_row = box_len
        elif stop < 0:
            stop_row = box_len - stop
        else:
            stop_row = stop
    else:
        stop_row = box_len
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        if start_row <= i < stop_row:
            extracted_images.append(image[y:y + h, x:x + w])
    return [ocrProcessor(x) for x in extracted_images]

# 测试代码
in_dir = '/Volumes/g/Downloads/line/'  # 替换为你的表格图片路径
output_dir = '/Volumes/g/Downloads/line/'
slice_obj = slice(1, -1)  # 示例：设置为 None

# read all file in image_path
import os
for file in os.listdir(in_dir):
    if file.endswith('.jpg') or file.endswith('.png'):
        in_path = os.path.join(in_dir, file)
        output_path = os.path.join(output_dir, file)
        # 提取结果
        extracted = extract_table(in_path, TableExtractionMode.COLS, slice_obj)
        # print('extracted', extracted)
        # write extracted to json file
        with open(f"{output_path}.json", "w") as f:
            json.dump(extracted, f, ensure_ascii=False)
        break

# 保存提取的图像
# for idx, img in enumerate(extracted):
    # cv2.imwrite(f"{output_path}extracted_{idx}.png", img)

print("提取完成！")