#贪心算法，每次选最大
def find_min_coins(amount, denominations):
    # 按面值从大到小排序
    denominations.sort(reverse=True)
    # 用来存储每种面值的纸币数量
    coin_count = {denomination: 0 for denomination in denominations}
    
    # 遍历每种面值
    for denomination in denominations:
        # 计算当前面值可以使用的最大数量
        if amount >= denomination:
            coin_count[denomination] = amount // denomination
            # 更新剩余金额
            amount %= denomination
    
    # 如果amount不为0，说明无法用给定的面值找完零钱
    if amount != 0:
        print("无法用给定的面值找完零钱")
    else:
        print(f"找零金额：{amount}")
        for denomination, count in coin_count.items():
            if count > 0:
                print(f"{denomination}元纸币：{count}张")

# 用户输入需要找零的金额
amount = int(input("请输入需要找零的金额："))

# 用户输入面值数据
denominations_input = input("请输入面值数据（用逗号分隔，例如：50,20,1）：")
denominations = list(map(int, denominations_input.split(',')))

# 查找最少纸币的数量并输出结果
find_min_coins(amount, denominations)
