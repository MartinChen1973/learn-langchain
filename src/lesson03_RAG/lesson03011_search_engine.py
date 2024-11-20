# 1. 演示如何借助搜索引擎来回答用户的问题
#    搜索引擎可提供实时信息，尤其是在模型生成之后才出现的信息。

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv, find_dotenv

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

# Create the retriever from url 从url创建检索器
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector_store = FAISS.from_documents(documents, embeddings)
retriever = vector_store.as_retriever()

# Create a prompt 创建提示词
template = """仅依赖下面的context回答用户的问题:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
# model = ChatOpenAI(model = "gpt-4") # 如果由于问题复杂，导致实验效果不佳，请使用gpt-4模型
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(  # RunnableParallel是一个并行运行多个Runnable的工具。它可以将多个Runnable组合成一个并行的处理流程，以实现更复杂的任务或功能。
    {
        "context": retriever,  # 用retriever处理输入问题，输出放入context字段
        "question": RunnablePassthrough(),
    }  # 把输入问题，不加处理传送到question字段
)
chain = setup_and_retrieval | prompt | model | output_parser

# Questions
question = "How can langsmith help with testing？"
# question = """
# How can langchain help with soft prompts and prompt tuning? 
# To answer the question, give me a short sentence. And,
# 1. it's in md format, with the topic, in this case "soft prompts and prompt tuning", maked as bold.
# 2. the sentence is in English. 
# 3. keep the sentence simple and straight forward. But it must cover the awnswer's content.
# 4. totally about 200 words would be good.
# 5. Important! Key words in it are followed by (it's Chinese). 4~6 key words should be enough.

# Exmaple: 
# **Prompt Composition (提示构成)** involves the process of creating (创建) and structuring (结构化) prompts to effectively communicate (有效沟通) with AI systems, requiring careful consideration of language (语言考量) and context (上下文) to elicit (引出) desired responses (期望的响应). Prompt Templates (提示模板) serve as predefined structures (预定义的结构) or formats (格式), aiding in the consistent (一致性) and efficient (效率) generation of these prompts, ensuring relevance (相关性) and clarity (清晰度) in interaction (互动).
# """

result = chain.invoke(question)
print(f"Q: {question}\nA: {result}")
