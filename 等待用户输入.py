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
    neighbors = []  # 存储每个元素的邻居
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

# 打印结果  
print("原二维数组:")  
print(sum_array)  
print("\n对比度为:")  
print(result)