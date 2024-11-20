# 1. 演示使用参数化模板，限制用户输入的问题，以便更好地引导用户输入。

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load the API key from the .env file 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Prompt: create a prompt 创建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个热心的AI助手。"),
    ("user", "请用{language}给我讲一个关于{subject}的{type}。") # 使用参数化模板，限制用户输入的问题，以便更好地引导用户输入。
])

# Model: Create the OpenAI chatbot 创建聊天机器人
llm = ChatOpenAI()

# OutputParser: Create an output parser 创建输出解析器
output_parser = StrOutputParser()

# Chain: Create and invoke a chain 创建并调用链
chain = prompt | llm | output_parser

# Invoke the chain 调用链
print(chain.invoke({"type" : "joke", "subject": "cats", "language":"English"}))
print(chain.invoke({"type" : "short poem", "subject": "dogs", "language":"Chinese"}))