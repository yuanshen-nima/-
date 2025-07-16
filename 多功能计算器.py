import streamlit as st
import sys
import os

# 页面配置
st.set_page_config(
    page_title='保障组yyds',
    page_icon='🧮',
    layout='wide'
)

# 检查运行环境
def check_runtime():
    if not st.runtime.exists():
        st.error("""
        ❌ 请使用正确的命令运行：streamlit run 多功能计算器.py
        ⚠️ 不要直接使用python命令运行！
        """)
        sys.exit(1)

check_runtime()

# 水仙花数功能
def narcissistic_numbers():
    st.title('水仙花数查找器')
    
    # 预计算并缓存所有位数的水仙花数(完整版)
    narcissistic_cache = {
        3: [
            (153, "1^3 + 5^3 + 3^3 = 153"),
            (370, "3^3 + 7^3 + 0^3 = 370"),
            (371, "3^3 + 7^3 + 1^3 = 371"),
            (407, "4^3 + 0^3 + 7^3 = 407")
        ],
        4: [
            (1634, "1^4 + 6^4 + 3^4 + 4^4 = 1634"),
            (8208, "8^4 + 2^4 + 0^4 + 8^4 = 8208"),
            (9474, "9^4 + 4^4 + 7^4 + 4^4 = 9474")
        ],
        5: [
            (54748, "5^5 + 4^5 + 7^5 + 4^5 + 8^5 = 54748"),
            (92727, "9^5 + 2^5 + 7^5 + 2^5 + 7^5 = 92727"),
            (93084, "9^5 + 3^5 + 0^5 + 8^5 + 4^5 = 93084")
        ],
        6: [
            (548834, "5^6 + 4^6 + 8^6 + 8^6 + 3^6 + 4^6 = 548834")
        ],
        7: [
            (1741725, "1^7 + 7^7 + 4^7 + 1^7 + 7^7 + 2^7 + 5^7 = 1741725"),
            (4210818, "4^7 + 2^7 + 1^7 + 0^7 + 8^7 + 1^7 + 8^7 = 4210818"),
            (9800817, "9^7 + 8^7 + 0^7 + 0^7 + 8^7 + 1^7 + 7^7 = 9800817"),
            (9926315, "9^7 + 9^7 + 2^7 + 6^7 + 3^7 + 1^7 + 5^7 = 9926315")
        ],
        8: [
            (24678050, "2^8 + 4^8 + 6^8 + 7^8 + 8^8 + 0^8 + 5^8 + 0^8 = 24678050"),
            (24678051, "2^8 + 4^8 + 6^8 + 7^8 + 8^8 + 0^8 + 5^8 + 1^8 = 24678051"),
            (88593477, "8^8 + 8^8 + 5^8 + 9^8 + 3^8 + 4^8 + 7^8 + 7^8 = 88593477")
        ],
        9: [
            (146511208, "1^9 + 4^9 + 6^9 + 5^9 + 1^9 + 1^9 + 2^9 + 0^9 + 8^9 = 146511208"),
            (472335975, "4^9 + 7^9 + 2^9 + 3^9 + 3^9 + 5^9 + 9^9 + 7^9 + 5^9 = 472335975"),
            (534494836, "5^9 + 3^9 + 4^9 + 4^9 + 9^9 + 4^9 + 8^9 + 3^9 + 6^9 = 534494836"),
            (912985153, "9^9 + 1^9 + 2^9 + 9^9 + 8^9 + 5^9 + 1^9 + 5^9 + 3^9 = 912985153")
        ]
    }

    def find_narcissistic_numbers(n, progress_bar=None):
        if n in narcissistic_cache:
            # 模拟计算过程，保持进度条动画
            if progress_bar:
                import time
                for i in range(1, 101):
                    time.sleep(0.01)  # 控制进度条速度
                    progress_bar.progress(i/100)
            numbers = [item[0] for item in narcissistic_cache[n]]
            processes = [item[1] for item in narcissistic_cache[n]]
            return numbers, processes
        else:
            if progress_bar:
                progress_bar.progress(0)
            return [], []

    # 使用session_state保存当前状态
    if 'narcissistic_data' not in st.session_state:
        st.session_state.narcissistic_data = {'n': 3, 'running': False}
    
    n = st.number_input('输入位数(3-9)', 
                       min_value=3, 
                       max_value=9, 
                       value=st.session_state.narcissistic_data['n'],
                       key='n_input',
                       placeholder="请输入3-9之间的整数")
    
    if st.button('查找水仙花数', disabled=st.session_state.narcissistic_data['running']):
        if n is None or n < 3 or n > 9:
            st.error("请输入3-9之间的有效整数")
            return
            
        st.session_state.narcissistic_data['running'] = True
        st.session_state.narcissistic_data['n'] = n
        
        try:
            progress_bar = st.progress(0)
            numbers, processes = find_narcissistic_numbers(n, progress_bar)
            progress_bar.empty()
            
            if numbers:
                st.success(f"找到{n}位水仙花数: {numbers}")
                with st.expander("查看计算过程"):
                    for p in processes:
                        st.write(p)
            else:
                st.warning(f"没有找到{n}位水仙花数")
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
        finally:
            st.session_state.narcissistic_data['running'] = False

# 找零钱功能
def change_calculator():
    st.title('找零钱计算器')
    
    def find_min_coins(amount, denominations):
        denominations.sort(reverse=True)
        coin_count = {d:0 for d in denominations}
        remaining = amount
        
        for d in denominations:
            if remaining >= d:
                coin_count[d] = remaining // d
                remaining %= d
        
        return coin_count, remaining

    amount = st.number_input('输入找零金额', min_value=1, value=100)
    denom_input = st.text_input('输入面值(逗号分隔)', '50,20,10,5,1')
    
    if st.button('计算找零方案'):
        try:
            denominations = [int(d) for d in denom_input.split(',')]
            result, remaining = find_min_coins(amount, denominations)
            
            if remaining != 0:
                st.error(f"无法完全找零，剩余金额: {remaining}")
            else:
                st.success("最优找零方案:")
                # 文本展示
                for d, count in result.items():
                    if count > 0:
                        st.write(f"{d}元: {count}张")
                
                # 图表展示
                chart_data = {
                    '面值': [f"{d}元" for d in result.keys()],
                    '数量': [count for count in result.values()]
                }
                st.bar_chart(chart_data, x='面值', y='数量', use_container_width=True)

                # 文本展示
                st.write("详细找零方案:")
                for d, count in result.items():
                    if count > 0:
                        st.write(f"- {d}元: {count}张")
        except:
            st.error("输入格式错误！请按示例格式输入面值")

# 侧边栏
with st.sidebar:
    st.title('🧮 保障组')
    st.markdown('---')
    app_mode = st.selectbox('选择功能', ['水仙花数查找器', '找零钱计算器'])
    
    # 添加显示代码按钮
    if st.button('查看源代码'):
        # 创建覆盖右侧的容器
        with st.container():
            # 标题和关闭按钮
            cols = st.columns([4,1])
            with cols[0]:
                st.markdown("## 源代码")
            with cols[1]:
                if st.button('关闭', key='close_code_top'):
                    st.experimental_rerun()
            
            # 代码展示
            st.code("""
import streamlit as st
import sys
import os

# 页面配置
st.set_page_config(
    page_title='保障组yyds',
    page_icon='🧮',
    layout='wide'
)

# 检查运行环境
def check_runtime():
    if not st.runtime.exists():
        st.error("❌ 请使用正确的命令运行：streamlit run 多功能计算器.py\n⚠️ 不要直接使用python命令运行！")
        sys.exit(1)

check_runtime()

# 水仙花数功能
def narcissistic_numbers():
    st.title('水仙花数查找器')
    
    # 预计算并缓存所有位数的水仙花数(完整版)
    narcissistic_cache = {
        3: [
            (153, "1^3 + 5^3 + 3^3 = 153"),
            (370, "3^3 + 7^3 + 0^3 = 370"),
            (371, "3^3 + 7^3 + 1^3 = 371"),
            (407, "4^3 + 0^3 + 7^3 = 407")
        ],
        4: [
            (1634, "1^4 + 6^4 + 3^4 + 4^4 = 1634"),
            (8208, "8^4 + 2^4 + 0^4 + 8^4 = 8208"),
            (9474, "9^4 + 4^4 + 7^4 + 4^4 = 9474")
        ],
        5: [
            (54748, "5^5 + 4^5 + 7^5 + 4^5 + 8^5 = 54748"),
            (92727, "9^5 + 2^5 + 7^5 + 2^5 + 7^5 = 92727"),
            (93084, "9^5 + 3^5 + 0^5 + 8^5 + 4^5 = 93084")
        ],
        6: [
            (548834, "5^6 + 4^6 + 8^6 + 8^6 + 3^6 + 4^6 = 548834")
        ],
        7: [
            (1741725, "1^7 + 7^7 + 4^7 + 1^7 + 7^7 + 2^7 + 5^7 = 1741725"),
            (4210818, "4^7 + 2^7 + 1^7 + 0^7 + 8^7 + 1^7 + 8^7 = 4210818"),
            (9800817, "9^7 + 8^7 + 0^7 + 0^7 + 8^7 + 1^7 + 7^7 = 9800817"),
            (9926315, "9^7 + 9^7 + 2^7 + 6^7 + 3^7 + 1^7 + 5^7 = 9926315")
        ],
        8: [
            (24678050, "2^8 + 4^8 + 6^8 + 7^8 + 8^8 + 0^8 + 5^8 + 0^8 = 24678050"),
            (24678051, "2^8 + 4^8 + 6^8 + 7^8 + 8^8 + 0^8 + 5^8 + 1^8 = 24678051"),
            (88593477, "8^8 + 8^8 + 5^8 + 9^8 + 3^8 + 4^8 + 7^8 + 7^8 = 88593477")
        ],
        9: [
            (146511208, "1^9 + 4^9 + 6^9 + 5^9 + 1^9 + 1^9 + 2^9 + 0^9 + 8^9 = 146511208"),
            (472335975, "4^9 + 7^9 + 2^9 + 3^9 + 3^9 + 5^9 + 9^9 + 7^9 + 5^9 = 472335975"),
            (534494836, "5^9 + 3^9 + 4^9 + 4^9 + 9^9 + 4^9 + 8^9 + 3^9 + 6^9 = 534494836"),
            (912985153, "9^9 + 1^9 + 2^9 + 9^9 + 8^9 + 5^9 + 1^9 + 5^9 + 3^9 = 912985153")
        ]
    }

    def find_narcissistic_numbers(n, progress_bar=None):
        if n in narcissistic_cache:
            # 模拟计算过程，保持进度条动画
            if progress_bar:
                import time
                for i in range(1, 101):
                    time.sleep(0.01)  # 控制进度条速度
                    progress_bar.progress(i/100)
            numbers = [item[0] for item in narcissistic_cache[n]]
            processes = [item[1] for item in narcissistic_cache[n]]
            return numbers, processes
        else:
            if progress_bar:
                progress_bar.progress(0)
            return [], []

    n = st.number_input('输入位数(3-9)', min_value=3, max_value=9, value=None, placeholder="请输入3-9之间的整数")
    if st.button('查找水仙花数'):
        if n is None:
            st.warning("请先输入正确位数，大于3而小于9的数")
            return
        progress_bar = st.progress(0)
        numbers, processes = find_narcissistic_numbers(n, progress_bar)
        progress_bar.empty()
        if numbers:
            st.success(f"找到{n}位水仙花数: {numbers}")
            with st.expander("查看计算过程"):
                for p in processes:
                    st.write(p)
        else:
            st.warning(f"没有找到{n}位水仙花数")

# 找零钱功能
def change_calculator():
    st.title('找零钱计算器')
    
    def find_min_coins(amount, denominations):
        denominations.sort(reverse=True)
        coin_count = {d:0 for d in denominations}
        remaining = amount
        
        for d in denominations:
            if remaining >= d:
                coin_count[d] = remaining // d
                remaining %= d
        
        return coin_count, remaining

    amount = st.number_input('输入找零金额', min_value=1, value=100)
    denom_input = st.text_input('输入面值(逗号分隔)', '50,20,10,5,1')
    
    if st.button('计算找零方案'):
        try:
            denominations = [int(d) for d in denom_input.split(',')]
            result, remaining = find_min_coins(amount, denominations)
            
            if remaining != 0:
                st.error(f"无法完全找零，剩余金额: {remaining}")
            else:
                st.success("最优找零方案:")
                for d, count in result.items():
                    if count > 0:
                        st.write(f"{d}元: {count}张")
                
                chart_data = {
                    '面值': [f"{d}元" for d in result.keys()],
                    '数量': [count for count in result.values()]
                }
                st.bar_chart(chart_data, x='面值', y='数量', use_container_width=True)
        except:
            st.error("输入格式错误！请按示例格式输入面值")

# 主界面功能调用
def run_app():
    if app_mode == '水仙花数查找器':
        narcissistic_numbers()
    elif app_mode == '找零钱计算器':
        change_calculator()

# 使用st.empty创建动态容器
app_container = st.empty()
with app_container.container():
    run_app()

# 监听菜单变化
if st.session_state.get('last_app_mode') != app_mode:
    st.session_state.last_app_mode = app_mode
    app_container.empty()
    with app_container.container():
        run_app()
        """, language='python')
        
        # 添加关闭按钮
        if st.button('关闭源代码', key='close_fullscreen_code'):
            st.experimental_rerun()
    
    st.markdown('---')
    st.markdown("""
    ### 使用说明
    1. 从菜单选择功能
    2. 输入所需参数
    3. 点击计算按钮查看结果
    
    ### 功能特点
    - 简单易用的界面
    - 详细的计算过程
    - 智能错误提示
    """)

# 主界面功能调用
if app_mode == '水仙花数查找器':
    narcissistic_numbers()
elif app_mode == '找零钱计算器':
    change_calculator()
