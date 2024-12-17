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