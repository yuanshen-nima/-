import streamlit as st
from ollama import chat, ChatResponse
from openai import OpenAI
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import base64
import os

# 页面设置
st.set_page_config(page_title="AI教学大纲生成工具", layout="wide")
st.title("AI教学大纲生成工具")

# 模型选择
model_option = st.selectbox(
    "选择模型",
    ("ollama (deepseek-r1:1.5b)", "deepseek (deepseek-reasoner)"),
    index=0
)

# 教学大纲参数设置
st.subheader("教学大纲参数设置")
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("科目", ["语文", "数学", "英语", "物理", "化学"], index=1)
    grade = st.selectbox("年级", ["初一", "初二", "初三", "高一", "高二", "高三"], index=0)
with col2:
    topics = st.multiselect(
        "主要话题",
        ["基础概念", "应用题", "实验", "理论", "写作"],
        default=["基础概念", "应用题", "理论"]
    )
    chapters = st.slider("章节数量", 5, 20, 10)

# 生成提示
system_prompt = f"你是一名资深中学{subject}教师"
user_prompt = f"""请为{grade}年级的{subject}学科生成一份教学大纲，要求涵盖以下主要话题：{", ".join(topics)}。 
共{chapters}章，按照真实教学标准编写，包括每章的教学目标、内容概述、重点难点以及教学建议。"""

# 处理函数
def process_request(model, system, user):
    if model.startswith("ollama"):
        model_name = model.split("(")[1].split(")")[0]  # 从"ollama (deepseek-r1:8b)"提取"deepseek-r1:8b"
        response: ChatResponse = chat(model=model_name, messages=[
            {'role': 'user', 'content': f'{system}。{user}'}
        ])
        content = response.message.content
        if "</think>" in content:
            parts = content.split("</think>")
            result = parts[1] if len(parts) > 1 else content
        else:
            result = content
        if "```" in result:
            result = result.split("```")[1] if len(result.split("```")) > 1 else result
    else:
        client = OpenAI(api_key="sk-1f40294152b2491a9dd5ee6b8e28c023", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            stream=False
        )
        result = response.choices[0].message.content
    return result

# 生成PDF的函数
def generate_pdf(content, subject, grade):
    try:
        # 设置字体路径
        font_path = os.path.join(os.path.dirname(__file__), 'simsun.ttc')
        
        # 注册中文字体（使用系统自带或指定路径）
        try:
            pdfmetrics.registerFont(TTFont('SimSun', font_path))
        except:
            st.warning("未找到SimSun字体，使用默认字体")
            font_name = "Helvetica"
        else:
            font_name = "SimSun"
        
        # 创建PDF对象
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # 设置字体大小
        c.setFont(font_name, 12)
        
        # 添加标题（使用常规字体加粗效果）
        c.setFont(font_name, 16)
        c.drawCentredString(width/2, height-50, f"{grade}年级{subject}教学大纲")
        c.setFont(font_name, 12)
        
        # 添加内容
        y_position = height - 80
        for line in content.split("\n"):
            if y_position < 50:  # 换页判断
                c.showPage()
                y_position = height - 50
            
            if line.startswith("###"):
                # 使用字号加粗效果替代Bold字体
                c.setFont(font_name, 14)
                c.drawString(50, y_position, line.replace("###", "").strip())
                y_position -= 20
                c.setFont(font_name, 12)
            else:
                c.drawString(50, y_position, line.strip())
                y_position -= 15
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
    except Exception as e:
        st.error(f"生成PDF失败: {str(e)}")
        return b''

# 生成PDF下载链接的函数
def create_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">点击下载PDF文件</a>'
    return href

# 提交按钮
if st.button("提交"):
    with st.spinner("模型处理中..."):
        try:
            output = process_request(model_option, system_prompt, user_prompt)
            if output:
                st.success("处理完成！")
                
                # 显示生成的大纲
                st.subheader("生成的教学大纲")
                st.markdown(output, unsafe_allow_html=True)
                
                # 将生成的内容保存到session state中
                st.session_state['outline_content'] = output
                
                # 生成PDF并提供下载
                try:
                    pdf_bytes = generate_pdf(output, subject, grade)
                    st.markdown(create_download_link(pdf_bytes, f"{grade}_{subject}_教学大纲.pdf"), 
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"PDF生成失败: {str(e)}")
            else:
                st.warning("收到空响应，请重试")
        except ImportError:
            st.error("模块未安装，请先执行: pip install ollama")
        except IndexError:
            st.error("响应解析错误，请检查输入格式")
        except Exception as e:
            st.error(f"处理失败: {str(e)}")

# 如果之前已经生成了大纲，显示下载按钮
if 'outline_content' in st.session_state:
    st.subheader("PDF下载")
    try:
        pdf_bytes = generate_pdf(st.session_state['outline_content'], subject, grade)
        st.markdown(create_download_link(pdf_bytes, f"{grade}_{subject}_教学大纲.pdf"), 
                    unsafe_allow_html=True)
    except Exception as e:
        st.error(f"PDF生成失败: {str(e)}")

# 显示生成提示
with st.expander("查看生成提示"):
    st.code(f"系统提示: {system_prompt}")
    st.code(f"用户输入: {user_prompt}")

# 安全提示
st.warning("注意：当前使用硬编码API密钥，请勿在生产环境中使用此配置")
