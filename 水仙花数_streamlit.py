import streamlit as st
import sys
import os

# 增强的运行环境检查
def check_runtime():
    # 检查是否通过streamlit run运行
    if not st.runtime.exists():
        # 中文错误提示
        error_msg = """
        ❌ 错误：运行方式不正确！
        
        您必须使用以下命令运行本程序：
        
        streamlit run 水仙花数_streamlit.py
        
        ⚠️ 不要直接使用python命令运行！
        
        正确运行步骤：
        1. 打开命令提示符(CMD)
        2. 输入: cd d:\\python3学习
        3. 输入: streamlit run 水仙花数_streamlit.py
        4. 等待浏览器自动打开
        
        如果看到"streamlit不是内部命令"：
        请先安装streamlit: pip install streamlit
        """
        print(error_msg)
        sys.exit(1)

# 检查运行环境
check_runtime()

def find_narcissistic_numbers(n):
    min_number = 10**(n-1)
    max_number = 10**n - 1
    
    water_number_list = []
    process_info = []
    
    for number in range(min_number, max_number + 1):
        num_str = str(number)
        sum_of_powers = sum(int(digit)**n for digit in num_str)
        
        if sum_of_powers == number:
            process = " + ".join(f"{digit}^{n}" for digit in num_str)
            process_info.append(f"{number}: {process} = {sum_of_powers}")
            water_number_list.append(number)
    
    return water_number_list, process_info

st.title('水仙花数查找器')
st.write('这是一个查找n位数水仙花数的工具')

n = st.number_input('请输入要查找的水仙花数位数', 
                   min_value=1, 
                   max_value=6, 
                   value=3,
                   step=1,
                   help='输入1-6之间的整数')

if st.button('开始查找'):
    st.write(f'正在查找{n}位数的水仙花数...')
    numbers, processes = find_narcissistic_numbers(n)
    
    st.subheader('查找结果')
    if numbers:
        st.success(f'找到{n}位数的水仙花数: {numbers}')
        st.write(f'共找到{len(numbers)}个水仙花数')
        
        with st.expander("查看计算过程"):
            for process in processes:
                st.write(process)
    else:
        st.warning(f'没有找到{n}位数的水仙花数')

st.info('使用方法: 输入位数后点击"开始查找"按钮')
