def find_narcissistic_numbers(n):
    # 计算n位数的最小值和最大值
    min_number = 10**(n-1)
    max_number = 10**n - 1
    
    water_number_list = []
    for number in range(min_number, max_number + 1):
        # 将数字转换为字符串，以便逐位处理
        num_str = str(number)
        sum_of_powers = sum(int(digit)**n for digit in num_str)
        
        # 如果该和等于原始数字，则为水仙花数
        if sum_of_powers == number:
            # 显示计算过程
            print(f"找到水仙花数：{number}")
            process = " + ".join(f"{digit}^{n}" for digit in num_str)
            print(f"计算过程：{process} = {sum_of_powers}")
            # 将水仙花数添加到列表中
            water_number_list.append(number)
    
    # 输出所有找到的水仙花数及其总数
    print(f"\n{n}位数的水仙花数有：{water_number_list}")
    print(f"{n}位数的水仙花数总数为：{len(water_number_list)}")

# 用户输入位数
n = int(input("请输入你所要查找水仙花数位数："))
find_narcissistic_numbers(n)
