import re  

# 使用绝对路径打开文件  
file_path = "/home/dependent_files/data3.txt"  

# 初始化一个列表来存储结果  
weather_data = []  

# 读取文件内容  
with open(file_path, 'r', encoding='utf-8') as file:  
    content = file.read()  

    # 使用正则表达式匹配日期、天气情况、最低温度、最高温度和风向  
    # 假定每行的格式为 "日期 天气情况 最低温度 最高温度 风向"  
    # 日期格式为 "2021年01月01日"  
    pattern = re.compile(r'(\d{4}年\d{2}月\d{2}日)\s+(\S+)\s+(-?\d+)℃\s+(-?\d+)℃\s+(\S+)')  
    matches = pattern.findall(content)  
    
    # 处理匹配到的数据  
    for match in matches:  
        date, weather, low_temp, high_temp, wind_dir = match  
        weather_data.append({  
            'date': date,  
            'weather': weather,  
            'low_temp': low_temp,  
            'high_temp': high_temp,  
            'wind_dir': wind_dir  
        })  

# 输出结果  
for data in weather_data:  
    print(f"日期: {data['date']}, 天气情况: {data['weather']}, "  
          f"最低温度: {data['low_temp']}℃, 最高温度: {data['high_temp']}℃, "  
          f"风向: {data['wind_dir']}")