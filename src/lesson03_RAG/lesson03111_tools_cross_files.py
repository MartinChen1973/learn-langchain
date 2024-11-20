# 1. 演示如何通过封装来简化代码（多个文件）
# 2. 演示如何在多个文件中搜索，且答案涉及到多个信息的推理
 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_tools.retriever.LangChainRetriever import LangChainRetriever

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

# Langchain_tools question and context | FOLDER -----------------------------------
question_and_context = LangChainRetriever.create_question_and_context_from_path(
    "src/lesson03_RAG/md",  # 从文件夹中获取文本数据，包含《组织结构图》和《请假政策》。
    # k=1, # 从每个文件中提取的段落数，缺省为7。如果只提取1段，则无法完成跨文档的问题回答。
)

# Create a prompt 创建提示词
template = """仅依赖下面的context回答用户的问题:
Context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
parser = StrOutputParser()

chain = question_and_context | prompt | model | parser

# Questions
questions = [
    # "请问找谁请病假？",
    # "于禁的直属领导是谁？",
    # "根据于禁相关的组织结构回答：于禁的直接主管是谁？",
    # "根据组织结构回答：张飞的直接主管是谁？",
    "张飞要请假，请问要找哪位？",
    # "根据组织结构与请假政策思考并回答：张飞要请假，请问要找哪位？张飞的直接主管叫什么名字？",
    # "需要什么证明文件吗？",
    # "最多可以请几天呢？"
]

for question in questions:
    result = chain.invoke(question)
    print(f"Q: {question}\nA: {result}")
