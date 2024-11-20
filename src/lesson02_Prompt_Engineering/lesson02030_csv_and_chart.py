# 1. 演示如何使用csv文件和图表回答开放性问题。

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data', 'sales2023_first_quarter.csv')

# Read csv file as a whole text
with open(file_path, 'r', encoding='utf-8') as file:
    csv_text = file.read()

# Create a prompt 创建提示词
template = """仅依赖下面的前后文回答用户的问题:
Context: {context}

Question: {question}

Note: {note}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model = "gpt-4o-mini")
# model = ChatOpenAI(model="gpt-4") # 如果由于问题复杂，导致实验效果不佳，请使用gpt-4o模型
output_parser = StrOutputParser()

# Create a note for the prompt 创建提示词的注释
note = """
1. 请使用中文回答问题。
2. 请只根据Context回答问题。
3. 在给出规律、做出总结时，请提供具体的数字。
4. **重要！**当收到“绘制图表”或“使用图表”等指令时，必须回答时包含绘图所需的python代码。
5. 请选择恰当的图表形式（如比较时应选择柱状图、展示趋势时应使用折线图等）。
6. python代码必须直接可运行，也不要有需要替换的文字。
7. 如果代码中需要数据，请在请在context中获取，不要尝试在文件中读取。
8. 注意图表中使用utf-8编码和设置中文字体为Microsoft YaHei。比如：
# Set the font globally
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Or another font that supports Chinese
matplotlib.rcParams['axes.unicode_minus'] = False  # Solve the problem that the negative sign '-' is displayed as a square
9. 如果同时有文字分析内容，又有图表，请想办法把文字分析内容与图表放在同一界面中，方便同时查看。
"""

# chain = setup_and_retrieval | prompt | model | output_parser
chain = prompt | model | output_parser

# Questions
questions = [
    # "2024年一月份一共卖出多少辆车？",
    # "2024-01-01~2024-01-31期间一共有卖出多少辆车？",
    # "2024-01-01~2024-01-31期间一共有多少订单?",
    # "2024年一季度按销售人员从多到少排列分别是谁？各有多少辆车？",
    """请从月份、销售人员、车型三个方面分析订单中的规律，并绘制图表进行展示。。"""
]

# Invoke the chain 调用链
for question in questions:
    result = chain.invoke({"question": question, "context": csv_text, "note": note})
    print(f"Q: {question}\nA: {result}")

    # 从result中提取代码并执行
    if "```python" in result:
        code = result.split("```python")[1].split("```")[0]
        if (code.strip() != ""):
            print("执行代码：" + code)
            exec(code)
