N, M, K = map(int, input().split())  
list1 = []  
for i in range(N):  
    # 统计当前行的1的数量  
    list1.append(input().count('1'))  

list2 = []  
for i in range(N - M + 1):  
    # 计算该段中的1的数量  
    count = sum(list1[i:i + M])  
    list2.append(count)  

if list2:  
    list2.sort(reverse=True)  
    print(list2[0])  
else:  
    print("No valid subarray found")  # 如果找不到有效的子数组，提供反馈