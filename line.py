import cv2
import numpy as np

# 1. 读取图像
image = cv2.imread('/Volumes/g/Downloads/line/8.jpg')

# 2. 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. 二值化图像，突出白色分隔线
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# 4. 形态学操作：膨胀突出纵向线条
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))  # 长条核，突出垂直线
vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

# 5. 霍夫变换检测直线
lines = cv2.HoughLinesP(vertical_lines, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# 6. 绘制检测到的线
line_image = np.zeros_like(image)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 绘制线段
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 7. 结果叠加显示
output = cv2.addWeighted(image, 0.8, line_image, 1, 0)

# 9. 保存结果
cv2.imwrite("/Volumes/g/Downloads/line/8_line.jpg", output)
