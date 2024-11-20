# 1. 演示如何生成并执行代码。

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load the API key from the .env file 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Prompt: create a prompt 创建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional AI coder."),
    ("user", "{input}")
])

# Model: Create the OpenAI chatbot 创建聊天机器人
model = ChatOpenAI(name="gpt-4o-mini") 
# model = ChatOpenAI(name="gpt-4o") 

# OutputParser: Create an output parser 创建输出解析器
output_parser = StrOutputParser()

# Chain: Create and invoke a chain 创建并调用链
chain = prompt | model | output_parser

# 生成代码
shape = "圆"
color1 = "红色"
color2 = "蓝色"
_prompt = f"请编写一段python代码，能在屏幕上绘制两个互相不连接的{shape}，其中一个是{color1}，另外一个是{color2}。（只要代码）"
# _prompt = f"请编写一段代码，能在屏幕上绘制两个互相不连接的{shape}，其中一个是{color1}，另外一个也是{color1}。（只要代码）"

result = chain.invoke({"input": _prompt})

# Print the response 打印回复
print(result)

# 读取并执行代码（代码在result中，以```python开头，```结束）
code = result.split("```python")[1].split("```")[0]
exec(code)

# 用regex可以实现更复杂内容的读取。
# import re
# match = re.search(r"```python(.*?)```", result, re.DOTALL)
# code = match.group(1) if match else None
# exec(code)
