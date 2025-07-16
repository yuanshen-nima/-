import math
import numpy as np
sum_array = np.array([[1, 5, 255,225,100,200,255,200],
                      [1, 7, 254,255,100,10,10,9],
                      [3,7,10,100,100,2,9,6],
                      [3,6,10,10,9,2,8,2],
                      [2,1,8,8,9,3,4,2],
                      [1,0,7,8,8,3,2,1],
                      [1,1,8,8,7,2,2,1],
                      [2,3,9,8,7,2,2,0]])  # 待处理的二维数组

def calculate_average_difference(arr):
    rows, cols = arr.shape
    average_diff = 0  # 存储每个元素的平均差值
    neighbors = []
    for i in range(rows):
        for j in range(cols):
            # 上邻居
            if i - 1 >= 0:
                
                neighbors.append(abs(arr[i][j] - arr[i - 1][j]))
            # 下邻居
            if i + 1 < rows:
                neighbors.append(abs(arr[i][j] - arr[i + 1][j]))
            # 左邻居
            if j - 1 >= 0:
                neighbors.append(abs(arr[i][j] - arr[i][j - 1]))
            # 右邻居
            if j + 1 < cols:
                neighbors.append(abs(arr[i][j] - arr[i][j + 1]))

            # 计算sum[i][j]的邻居的绝对值之和
    if neighbors:
        sum_neighbors = sum(abs(v) for v in neighbors)
        average_diff = (sum_neighbors) / len(neighbors)
    return average_diff

# 计算平均差值
result = calculate_average_difference(sum_array)


height, width = sum_array.shape
input_image=sum_array
output_image=input_image.copy();
# 线性对比度展宽
# 通过改变以下四个常量参数的值调整图像效果
f_a = 2
f_b = 100
g_a = 1
g_b = 200

ARFA = g_a / f_a
BEITA = (g_b - g_a) / (f_b - f_a)
GARMA = (255 - g_b) / (255 - f_b)

for i in range(0, height):  # 遍历每一个像素点
    for j in range(0, width):
        if 0 <= input_image[i, j] < f_a:
            output_image[i, j] = ARFA * input_image[i, j]
        elif f_a <= input_image[i, j] < f_b:
            output_image[i, j] = BEITA * (input_image[i, j] - f_a) + g_a
        elif f_b <= input_image[i, j] < 255:
            output_image[i, j] = GARMA * (input_image[i, j] - f_b) + g_b

print(input_image)
print(calculate_average_difference(input_image))
print(output_image)
print(calculate_average_difference(output_image))

#非线性动态范围调整
# 增益常数
h, w = sum_array.shape
image =sum_array.copy()
c = 100
# 计算
for i in range(h):
    for j in range(w):
        image[i][j] = c*math.log10((sum_array[i][j]+1))
        if image[i][j] > 255:
            image[i][j] = 255
# 绘图
print(image)
print(calculate_average_difference(image))

#直方图均衡化
# 计算灰度直方图
output_image = np.zeros([height,width])

histogram = np.zeros([256])
gray_prob = np.zeros([256])
gray_cumulprob = np.zeros([256])
IMG_RESOLUTION = height * width  # 计算分辨率
for i in range(0, height):
    for j in range(0, width):
        GRAY_VALUE = input_image[i, j]
        histogram[GRAY_VALUE] += 1  # 计算直方图

for i in range(256):
    gray_prob[i] = histogram[i] / IMG_RESOLUTION  # 计算灰度概率分布


for i in range(0, 256):
    gray_cumulprob[i] = gray_prob[i] + gray_cumulprob[i-1]  # 计算灰度累计概率分布
gray_cumulprob[0] = 0
# 新图旧图像映射
for i in range(0, height):
    for j in range(0, width):
        output_image[i ,j] = 255 * gray_cumulprob[input_image[i, j]]



print()
print(output_image)
print(calculate_average_difference(output_image))
print(output_image[4][6])
print()