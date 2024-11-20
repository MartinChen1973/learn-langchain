# 1. 演示如何通过封装来简化代码（单个文件）

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_tools.retriever.LangChainRetriever import LangChainRetriever

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

# Langchain_tools question and context  -----------------------------------
question_and_context = LangChainRetriever.create_question_and_context_from_path(
    "src/lesson03_RAG/md/leave_policy.md"
)

# Create a prompt 创建提示词
template = """仅依赖下面的context回答用户的问题:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
parser = StrOutputParser()

chain = question_and_context | prompt | model | parser

# Questions
questions = [
    "请问找谁请病假？",
    # "需要什么证明文件吗？",
    # "最多可以请几天呢？"
]

for question in questions:
    result = chain.invoke(question)
    print(f"Q: {question}\nA: {result}")
