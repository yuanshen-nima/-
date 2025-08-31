from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import streamlit as st
import time
import re
from ollama import chat, ChatResponse
from openai import OpenAI
from io import BytesIO

# 考试大纲生成函数
def generate_outline(exam_content, subject, iterations=2):
    outline = ""
    progress_bar = st.progress(0)
    
    for i in range(iterations):
        progress_bar.progress((i + 1) / iterations)
        time.sleep(0.5)  # 模拟处理延迟
        
        # 提取题目信息
        questions = re.findall(r'### 题目\d+\n\*\*题型\*\*:(.+?)\n\*\*题目内容\*\*:(.+?)\n\*\*答题要求\*\*:(.+?)\n\*\*分值\*\*:(.+?)\n', exam_content, re.DOTALL)
        
        # 构建大纲内容
        outline = f"{subject}考试大纲 (迭代{i+1}/{iterations})\n\n"
        outline += "📌 一、考试概况\n"
        outline += f"🔹 科目: {subject}\n"
        outline += f"🔹 题目总数: {len(questions)}\n"
        outline += f"🔹 总分: 100分\n\n"
        
        outline += "📊 二、题型分布\n"
        type_counts = {}
        for q in questions:
            q_type = q[0].strip()
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
        for t, count in type_counts.items():
            outline += f"✅ {t}: {count}题\n"
        outline += "\n"
        
        outline += "🧠 三、知识点分布\n"
        topics = get_subject_topics(subject)
        outline += " | ".join([f"📌{t}" for t in topics]) + "\n\n"
        
        outline += "📝 四、题目要求\n"
        for i, q in enumerate(questions, 1):
            outline += f"{i}. {q[1].strip()} ⭐分值: {q[3].strip()}\n"
        
        outline += "\n🎯 五、评分标准\n"
        outline += "1. 📐 按步骤给分\n"
        outline += "2. ✔️ 答案准确完整\n"
        outline += "3. 📚 符合学科规范\n"
    
    progress_bar.empty()
    return outline
# PDF生成函数（放在最前面）
def generate_pdf(content, subject):
    try:
        # 注册中文字体（使用系统自带或指定路径）
        try:
            pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
        except:
            st.warning("未找到SimSun字体，使用默认字体")
        
        # 创建PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # 设置字体（简化处理，不使用Bold变体）
        try:
            font_name = "SimSun"
            pdfmetrics.registerFont(TTFont(font_name, "simsun.ttc"))
            c.setFont(font_name, 12)
        except:
            font_name = "Helvetica"
            c.setFont(font_name, 12)
        
        # 添加标题（使用常规字体加粗效果）
        c.setFont(font_name, 14)
        c.drawCentredString(width/2, height-50, f"{subject}试卷")
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
                text = c.beginText(50, y_position)
                text.textLine(line)
                c.drawText(text)
                y_position -= 15
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
        
    except Exception as e:
        st.error(f"生成PDF失败: {str(e)}")
        return b''



# 科目主题映射
def get_subject_topics(subject):
    topics_map = {
        "语文": ["古诗文", "现代文阅读", "作文", "文言文", "修辞手法", "现代汉语", "古代汉语"],
        "数学": ["代数", "几何", "函数", "概率统计", "方程", "不等式", "三角函数"],
        "英语": ["reading", "writing", "grammar", "vocabulary", "listening", "speaking"],
        "物理": ["力学", "电学", "光学", "热学", "原子物理", "电磁学", "动力学"],
        "化学": ["无机化学", "有机化学", "化学反应", "化学方程式", "实验", "分子结构", "化学键"]
    }
    return topics_map.get(subject, [])

def get_other_subject_keywords(subject):
    other_subjects = {
        "语文": ["equation", "chemical", "physics", "math", "calculate"],
        "数学": ["文言文", "作文", "化学式", "物理公式", "英语单词"],
        "英语": ["古诗", "方程式", "化学反应", "物理实验", "数学公式"],
        "物理": ["古诗文", "作文", "化学式", "英语单词", "代数"],
        "化学": ["古诗文", "作文", "物理公式", "英语单词", "几何"]
    }
    return other_subjects.get(subject, [])

# 页面设置
st.set_page_config(page_title="AI模型调用工具", layout="wide")
st.title("AI模型调用工具")

# 模型选择
model_option = st.selectbox(
    "选择模型",
    ("ollama (deepseek-r1:8b)", "deepseek (deepseek-reasoner)","ollama (deepseek-r1:1.5b)"),
    index=0
)

# 试卷参数设置
st.subheader("试卷参数设置")
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("科目", ["语文", "数学", "英语", "物理", "化学"], index=0)
    difficulty = st.select_slider("难度", ["简单", "中等", "困难"], value="中等")
    
with col2:
    question_count = st.slider("总题数", 5, 30, 10)
    outline_iterations = st.slider("大纲迭代次数", 1, 5, 2, 
                                 help="增加迭代次数可以优化大纲质量")
    st.write("各题型数量分配:")
    
    # 题型数量分配
    type_counts = {}
    available_types = ["选择题", "填空题", "计算题", "解答题", "作文题"]
    cols = st.columns(len(available_types))
    for i, q_type in enumerate(available_types):
        with cols[i]:
            type_counts[q_type] = st.number_input(
                f"{q_type}",
                min_value=0,
                max_value=question_count,
                value=0 if q_type == "作文题" else min(3, question_count),
                step=1,
                key=f"type_{q_type}"
            )
    
    # 验证总数
    total = sum(type_counts.values())
    if total != question_count:
        st.warning(f"⚠️ 题型数量总和应为{question_count}，当前为{total}")

# 生成提示
system_prompt = f"你是一名资深中学{subject}教师，拥有10年以上出题经验"
user_prompt = f"""请严格按以下要求生成{subject}试卷：

一、【科目强制要求】
1. 本题库为{subject}专用，禁止出现其他学科内容
2. 所有题目必须使用{subject}专业术语和规范表达
3. 题目内容必须属于以下{subject}核心范畴：
   - {', '.join(get_subject_topics(subject))}
4. 禁止出现以下跨学科内容：
   - {', '.join(get_other_subject_keywords(subject))}

二、【试卷规格】
• 题目总数：{question_count}道（必须精确）
• 难度级别：{difficulty}
• 题型分布（必须严格执行）：
   {", ".join([f"◇ {k}: {v}道" for k, v in type_counts.items() if v > 0])}
• 总分分值：100分（必须精确）

三、【题目生成规则】
1. 题目唯一性：确保所有题目内容不重复
2. 难度一致性：所有题目保持相同难度水平
3. 编号连续性：题目编号从1开始连续递增
4. 分值设置：根据难度设置合理分值（{difficulty}题：5-20分），
5. 生成策略：每次生成5道题

四、【题目格式规范（必须严格遵守）】
### 题目X（X为1-{question_count}的编号）
**题型**：[具体题型]
**题目内容**：[清晰表述的具体问题]
**选项**：(仅选择题需要)
A) [选项内容]
B) [选项内容] 
C) [选项内容]
D) [选项内容]
**答题要求**：[具体要求，如计算步骤、字数限制等]
**分值**：[整数分值]
**答案**：[简洁准确的参考答案，选择题需标注正确选项如"A"]

五、【生成示例】
### 题目1（{subject}示例）
**题型**：{next(iter(type_counts.keys()), "选择题")}
**题目内容**：[符合{subject}学科的具体问题]
**答题要求**：[具体要求，如计算步骤、字数限制等]
**分值**：[整数分值]
**答案**：[简洁准确的参考答案]

六、【特别指令】
1. 生成完成后，严格检查题目数量和题型分布
2. 确保所有题目完全符合{subject}学科规范
3. 现在开始生成前{min(5, question_count)}道题
"""

# 添加科目示例函数
def get_subject_example(subject):
    examples = {
        "语文": "分析《岳阳楼记》中'先天下之忧而忧，后天下之乐而乐'的修辞手法及思想内涵",
        "数学": "已知二次函数f(x)=x²-4x+3，求其在区间[0,4]的最小值和最大值",
        "英语": "阅读下面短文，选择最佳答案: 'The Eiffel Tower, __ is located in Paris, attracts millions of visitors each year.' A) which B) where C) when D) that",
        "物理": "质量为2kg的物体在水平面上受10N水平拉力作用，摩擦系数为0.2，求加速度",
        "化学": "写出乙烯与溴水反应的化学方程式，并说明反应类型"
    }
    return examples.get(subject, "")

def get_subject_answer_example(subject):
    answers = {
        "语文": "运用对偶修辞，体现了作者忧国忧民的崇高思想境界",
        "数学": "最小值：f(2)= -1，最大值：f(4)=3",
        "英语": "A) which",
        "物理": "加速度a=3m/s²",
        "化学": "CH₂=CH₂ + Br₂ → CH₂BrCH₂Br；加成反应"
    }
    return answers.get(subject, "")
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
        client = OpenAI(api_key="sk-4e843df1f877485f8c76bfcee461d3f7", 
                      base_url="https://api.deepseek.com")
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

# 状态控制
if 'running' not in st.session_state:
    st.session_state.running = False

# 停止按钮回调
def stop_execution():
    st.session_state.running = False

# 按钮布局
col1, col2 = st.columns(2)
with col1:
    submit_clicked = st.button("提交")
with col2:
    st.button("停止", on_click=stop_execution)

# 初始化生成状态
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'exam_content' not in st.session_state:
    st.session_state.exam_content = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# 仅在点击提交按钮后开始生成
if submit_clicked:
    st.session_state.running = True
    st.session_state.submitted = True
    st.session_state.generated = False

if st.session_state.running and st.session_state.submitted and not st.session_state.generated:
    try:
        output = ""
        generated_questions = set()
        
        # 优化批量生成策略
        chunk_size = min(10, question_count)  # 减小批量大小提高成功率
        chunks = [(i, min(i + chunk_size, question_count)) 
                 for i in range(0, question_count, chunk_size)]

        # 严格按用户输入的题型数量分配
        question_types = []
        if total == question_count:  # 数量匹配时才使用用户输入
            for q_type, count in type_counts.items():
                question_types.extend([q_type] * count)
        else:  # 数量不匹配时自动平均分配
            st.warning("⚠️ 题型数量总和不匹配，已自动调整分配")
            base_count = question_count // len(type_counts)
            remainder = question_count % len(type_counts)
            question_types = []
            for i, q_type in enumerate(type_counts):
                count = base_count + (1 if i < remainder else 0)
                question_types.extend([q_type] * count)
        
        status_area = st.empty()
        current_question_num = 1
        max_retries = 5  # 增加重试次数
        
        for start, end in chunks:
            if not st.session_state.running:
                st.warning("生成已中止")
                break
                
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    status_area.text(f"正在生成题目 {current_question_num}-{min(current_question_num + chunk_size -1, question_count)}/{question_count} (尝试 {retry_count+1}/{max_retries})...")
                    
                    # 动态生成当前批次的题目编号
                    current_batch_size = min(chunk_size, question_count - current_question_num + 1)
                    batch_end = current_question_num + current_batch_size - 1
                    chunk_prompt = f"{user_prompt}\n请生成题目{current_question_num}-{batch_end}"
                    
                    partial_output = process_request(model_option, system_prompt, chunk_prompt)
                    
                    # 增强题目完整性验证
                    try:
                        # 分割题目
                        raw_questions = re.split(r'### 题目\d+', partial_output)[1:]
                        if not raw_questions:
                            raise ValueError("未生成任何题目")
                        
                        questions = []
                        for question in raw_questions:
                            try:
                                # 严格检查必填字段
                                required_fields = {
                                    "题型": r'(?:\*\*题型\*\*|题型)[：:].+',
                                    "题目内容": r'(?:\*\*题目内容\*\*|题目内容)[：:].+',
                                    "答题要求": r'(?:\*\*答题要求\*\*|答题要求)[：:].+',
                                    "分值": r'(?:\*\*分值\*\*|分值)[：:].+\d+分?',
                                    "答案": r'(?:\*\*答案\*\*|答案)[：:].+'
                                }
                                
                                # 题型特定检查
                                if q_type == "选择题":
                                    if not re.search(r'[A-D]\)\s*.+', question):
                                        raise ValueError("选择题必须包含A-D选项")
                                    if not re.search(r'\*\*答案\*\*:\s*[A-D]', question):
                                        raise ValueError("选择题答案必须为A-D选项")
                                        
                                elif q_type == "填空题":
                                    if not re.search(r'_{3,}', question):
                                        raise ValueError("填空题必须包含填空标记___")
                                    if not re.search(r'\*\*答案\*\*:\s*.+', question):
                                        raise ValueError("填空题必须提供答案")
                                        
                                elif q_type == "解答题":
                                    if not re.search(r'\*\*答题要求\*\*:.+步骤', question):
                                        raise ValueError("解答题必须说明答题步骤要求")
                                    if not re.search(r'\*\*答案\*\*:.+过程', question):
                                        raise ValueError("解答题答案必须包含解题过程")
                                
                                missing_fields = []
                                for field, pattern in required_fields.items():
                                    if not re.search(pattern, question, re.DOTALL):
                                        missing_fields.append(field)
                                
                                if missing_fields:
                                    raise ValueError(f"题目缺少以下字段: {', '.join(missing_fields)}")
                                
                                # 检查题型特定要求
                                q_type = question_types[current_question_num + len(questions) - 1]
                                if q_type == "选择题":
                                    if not re.search(r'[A-D]\)\s*.+', question):
                                        raise ValueError(f"题目应为选择题但缺少选项")
                                    if re.search(r'_{3,}', question):
                                        raise ValueError(f"选择题不应包含填空标记")
                                elif q_type == "填空题":
                                    if re.search(r'[A-D]\)\s*.+', question):
                                        raise ValueError(f"填空题不应包含选项")
                                    if not re.search(r'_{3,}', question):
                                        raise ValueError(f"填空题缺少填空标记")
                                
                                # 检查科目关键词
                                subject_keywords = {
                                    "语文": ["修辞", "文言", "现代文", "作文", "古诗"],
                                    "数学": ["函数", "方程", "几何", "概率", "计算"],
                                    "英语": ["grammar", "reading", "writing", "vocabulary", "英语"],
                                    "物理": ["力学", "电学", "光学", "热学", "物理"],
                                    "化学": ["反应", "化学式", "实验", "分子", "化学"]
                                }
                                
                                found_keywords = [
                                    keyword for keyword in subject_keywords[subject] 
                                    if re.search(keyword, question)
                                ]
                                
                                if not found_keywords:
                                    raise ValueError(f"题目内容不符合{subject}学科要求")
                                
                                questions.append(question)
                                
                            except ValueError as ve:
                                st.warning(f"题目验证失败: {str(ve)}")
                                continue
                                
                    except Exception as e:
                        st.error(f"题目处理失败: {str(e)}")
                        raise
                        
                        questions = []
                        for question in raw_questions:
                            # 检查必填字段
                            required_fields = {
                                "题型": r'(?:\*\*题型\*\*|题型)[：:].+',
                                "题目内容": r'(?:\*\*题目内容\*\*|题目内容)[：:].+',
                                "答题要求": r'(?:\*\*答题要求\*\*|答题要求)[：:].+',
                                "分值": r'(?:\*\*分值\*\*|分值)[：:].+',
                                "答案": r'(?:\*\*答案\*\*|答案)[：:].+'
                            }
                            
                            missing_fields = []
                            for field, pattern in required_fields.items():
                                if not re.search(pattern, question, re.DOTALL):
                                    missing_fields.append(field)
                            
                            if missing_fields:
                                raise ValueError(f"题目缺少以下字段: {', '.join(missing_fields)}")
                            
                            # 检查题型特定要求
                            q_type = question_types[current_question_num + len(questions) - 1]
                            if q_type == "选择题":
                                if not re.search(r'[A-D]\)\s*.+', question):
                                    raise ValueError(f"题目应为选择题但缺少选项")
                                if re.search(r'_{3,}', question):
                                    raise ValueError(f"选择题不应包含填空标记")
                            elif q_type == "填空题":
                                if re.search(r'[A-D]\)\s*.+', question):
                                    raise ValueError(f"填空题不应包含选项")
                                if not re.search(r'_{3,}', question):
                                    raise ValueError(f"填空题缺少填空标记")
                            
                            # 检查科目关键词
                            subject_keywords = {
                                "语文": ["修辞", "文言", "现代文", "作文", "古诗"],
                                "数学": ["函数", "方程", "几何", "概率", "计算"],
                                "英语": ["grammar", "reading", "writing", "vocabulary", "英语"],
                                "物理": ["力学", "电学", "光学", "热学", "物理"],
                                "化学": ["反应", "化学式", "实验", "分子", "化学"]
                            }
                            
                            found_keywords = [
                                keyword for keyword in subject_keywords[subject] 
                                if re.search(keyword, question)
                            ]
                            
                            if not found_keywords:
                                raise ValueError(f"题目内容不符合{subject}学科要求")
                            
                            questions.append(question)
                        
                        # 验证每个题目
                        for i, question in enumerate(questions):
                            # 检查必填字段
                            required_fields = {
                                "题型": r'(?:\*\*题型\*\*|题型)[：:].+',
                                "题目内容": r'(?:\*\*题目内容\*\*|题目内容)[：:].+',
                                "答题要求": r'(?:\*\*答题要求\*\*|答题要求)[：:].+',
                                "分值": r'(?:\*\*分值\*\*|分值)[：:].+',
                                "答案": r'(?:\*\*答案\*\*|答案)[：:].+'
                            }
                            
                            missing_fields = []
                            for field, pattern in required_fields.items():
                                if not re.search(pattern, question, re.DOTALL):
                                    missing_fields.append(field)
                            
                            if missing_fields:
                                raise ValueError(f"题目{current_question_num+i}缺少以下字段: {', '.join(missing_fields)}")
                            
                            # 检查题型特定要求
                            q_type = question_types[current_question_num + i - 1]
                            if q_type == "选择题":
                                if not re.search(r'[A-D]\)\s*.+', question):
                                    raise ValueError(f"题目{current_question_num+i}应为选择题但缺少选项")
                                if re.search(r'_{3,}', question):
                                    raise ValueError(f"题目{current_question_num+i}为选择题不应包含填空标记")
                            elif q_type == "填空题":
                                if re.search(r'[A-D]\)\s*.+', question):
                                    raise ValueError(f"题目{current_question_num+i}为填空题不应包含选项")
                                if not re.search(r'_{3,}', question):
                                    raise ValueError(f"题目{current_question_num+i}缺少填空标记")
                            
                            # 检查科目关键词
                            subject_keywords = {
                                "语文": ["修辞", "文言", "现代文", "作文", "古诗"],
                                "数学": ["函数", "方程", "几何", "概率", "计算"],
                                "英语": ["grammar", "reading", "writing", "vocabulary", "英语"],
                                "物理": ["力学", "电学", "光学", "热学", "物理"],
                                "化学": ["反应", "化学式", "实验", "分子", "化学"]
                            }
                            
                            found_keywords = [
                                keyword for keyword in subject_keywords[subject] 
                                if re.search(keyword, question)
                            ]
                            
                            if not found_keywords:
                                raise ValueError(
                                    f"题目{current_question_num+i}内容不符合{subject}学科要求"
                                )
                        
                    # 完全重写题目编号系统
                    raw_questions = re.split(r'### 题目\d+', partial_output)[1:]
                    valid_questions = []
                    
                    # 预处理：提取有效题目
                    for question in raw_questions:
                        # 根据题型提取内容
                        if question_types[current_question_num + i - 1] == "选择题":
                            pure_content = re.sub(
                                r'(^\s*|\*\*答案\*\*:.*|\b题目\d+\b)', 
                                '', 
                                question, 
                                flags=re.DOTALL
                            ).strip()
                        else:
                            pure_content = re.sub(
                                r'(^\s*|\*\*答案\*\*:.*|\b题目\d+\b|[A-D]\)\s*.+)', 
                                '', 
                                question, 
                                flags=re.DOTALL
                            ).strip()
                        
                        # 验证题目内容完整性
                        required_parts = ["题目内容", "答题要求", "分值", "答案"]
                        if (pure_content and 
                            pure_content not in generated_questions and
                            all(part in question for part in required_parts)):
                            # 提取答案部分
                            answer = re.search(r'\*\*答案\*\*:(.*)', question, flags=re.DOTALL)
                            valid_questions.append({
                                'content': pure_content,
                                'answer': answer.group(1) if answer else ""
                            })
                            generated_questions.add(pure_content)
                    
                    # 动态生成连续编号题目
                    fixed_output = ""
                    for i, q in enumerate(valid_questions):
                        question_num = current_question_num + i
                        fixed_question = f"### 题目{question_num}\n{q['content']}"
                        if q['answer']:
                            fixed_question += f"\n**答案**:{q['answer']}"
                        
                        if fixed_output:
                            fixed_output += "\n\n" + fixed_question
                        else:
                            fixed_output = fixed_question
                    
                    # 更新当前题目编号
                    if valid_questions:
                        current_question_num += len(valid_questions)
                    
                    if fixed_output:
                        output += "\n\n" + fixed_output if output else fixed_output
                        success = True
                    else:
                        raise ValueError("所有题目都重复")
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        st.error(f"生成题目{current_question_num}-{batch_end}失败: {str(e)}")
                    else:
                        status_area.text(f"生成失败: {str(e)}, 正在重试...")
                        time.sleep(1)  # 重试前短暂等待
        
        # 最终验证
        question_count_in_output = output.count('### 题目')
        st.session_state.generated_count = question_count_in_output
        
        if question_count_in_output >= question_count:
            st.success(f"成功生成{question_count_in_output}道试题！")
            st.markdown(output, unsafe_allow_html=True)
            st.session_state.generated = True
            st.session_state.exam_content = output
        else:
            st.warning(f"已生成{question_count_in_output}道题（目标:{question_count}）")
            st.markdown(output, unsafe_allow_html=True)
            st.session_state.exam_content = output
            
            # 添加继续生成按钮
            if st.button("继续生成剩余题目", key="continue_generate"):
                st.session_state.running = True
                st.session_state.generated = False
                st.rerun()
                
    except ImportError:
        st.error("模块未安装，请先执行: pip install ollama")
    except IndexError:
        st.error("响应解析错误，请检查输入格式")
    except Exception as e:
        st.error(f"处理失败: {str(e)}")
        if 'generated_count' in st.session_state:
            st.button("重试生成", on_click=lambda: st.session_state.update({
                "running": True,
                "generated": False
            }))
    finally:
            # 显示已生成的内容（专业试卷格式）
            if st.session_state.generated and st.session_state.exam_content:
                with st.expander("📝 生成的试卷内容", expanded=True):
                    st.markdown(f"""
                    <div style='font-family: "Times New Roman", Times, serif;'>
                        <h2 style='text-align: center;'>{subject}试卷</h2>
                        <hr style='border: 1px solid #000;'>
                        {st.session_state.exam_content}
                        <hr style='border: 1px solid #000;'>
                        <p style='text-align: right;'>总分：100分</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                            # 持久化显示生成的题目内容
                            st.markdown(f"""
                            <div style='font-family: "Times New Roman", Times, serif;'>
                                <h2 style='text-align: center;'>{subject}试卷</h2>
                                <hr style='border: 1px solid #000;'>
                                {st.session_state.exam_content}
                                <hr style='border: 1px solid #000;'>
                                <p style='text-align: right;'>总分：100分</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 生成PDF下载按钮（不改变状态）
                            with st.container():
                                pdf_bytes = generate_pdf(st.session_state.exam_content, subject)
                                if pdf_bytes:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.download_button(
                                            label="⬇️ 下载试卷(PDF)",
                                            data=pdf_bytes,
                                            file_name=f"{subject}_试卷.pdf",
                                            mime="application/pdf",
                                            key="pdf_download"
                                        )
                                    
                                    outline = generate_outline(
                                        st.session_state.exam_content, 
                                        subject,
                                        outline_iterations
                                    )
                                    outline_bytes = generate_pdf(outline, f"{subject}考试大纲")
                                    
                                    with col2:
                                        st.download_button(
                                            label="⬇️ 下载考试大纲(PDF)",
                                            data=outline_bytes,
                                            file_name=f"{subject}_考试大纲.pdf",
                                            mime="application/pdf",
                                            key="outline_download"
                                        )
                                else:
                                    st.error("PDF生成失败，请重试")
                    except Exception as e:
                        st.error(f"生成PDF时出错: {str(e)}")
                        st.button("重试PDF生成", on_click=lambda: st.session_state.update({"already_displayed": False}))

# 考试大纲生成函数
def generate_outline(exam_content, subject):
    # 提取题目信息
    questions = re.findall(r'### 题目\d+\n\*\*题型\*\*:(.+?)\n\*\*题目内容\*\*:(.+?)\n\*\*答题要求\*\*:(.+?)\n\*\*分值\*\*:(.+?)\n', exam_content, re.DOTALL)
    
    # 构建大纲内容
    outline = f"{subject}考试大纲\n\n"
    outline += "一、考试概况\n"
    outline += f"科目: {subject}\n"
    outline += f"题目总数: {len(questions)}\n"
    outline += "总分: 100分\n\n"
    
    outline += "二、题型分布\n"
    type_counts = {}
    for q in questions:
        q_type = q[0].strip()
        type_counts[q_type] = type_counts.get(q_type, 0) + 1
    for t, count in type_counts.items():
        outline += f"{t}: {count}题\n"
    outline += "\n"
    
    outline += "三、知识点分布\n"
    topics = get_subject_topics(subject)
    outline += ", ".join(topics) + "\n\n"
    
    outline += "四、题目要求\n"
    for i, q in enumerate(questions, 1):
        outline += f"{i}. {q[1].strip()} (分值: {q[3].strip()})\n"
    
    outline += "\n五、评分标准\n"
    outline += "1. 按步骤给分\n"
    outline += "2. 答案准确完整\n"
    outline += "3. 符合学科规范\n"
    
    return outline

# 显示生成提示
with st.expander("查看生成提示"):
    st.code(f"系统提示: {system_prompt}")
    st.code(f"用户输入: {user_prompt}")



# 安全提示
st.warning("注意：当前使用硬编码API密钥，请勿在生产环境中使用此配置")
