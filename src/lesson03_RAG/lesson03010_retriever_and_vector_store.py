# 1. 演示如何使用向量存储和检索器
# 2. 演示如何使用RunnableParallel并行运行多个Runnable

from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

# 用向量存储vector store创建一个索引Retriever. Create an index retriever with a vector store.
vectorstore = DocArrayInMemorySearch.from_texts(  # "Vector Store"是一个存储向量表示的数据库或系统，用于管理和检索向量化的数据。这些向量可以是文本、图像或其他类型的数据，它们被存储在向量空间中，使得相似的项目在空间中更接近。Vector Store通常用于支持各种自然语言处理任务，如信息检索、文本分类和相似度匹配。
    [
        "我们公司的前台叫小丽。",
        "公司附近国贸三期楼下的烤鱼很好吃。",
        "你的直属领导是张经理。",
        "请事假需要提前一天向直属领导提交申请。病假无需提前请假，可以于事后向直属领导补办，但需要有医院的就诊记录。",
    ],
    embedding=OpenAIEmbeddings(),  # "embedding"指的是将数据转换为向量表示的过程，在自然语言处理中特别常见。通过嵌入，文本、图像或其他数据可以被表示为高维空间中的向量，其中相似的项目在空间中更接近。这种表示形式有助于机器学习模型理解和处理数据。
)
retriever = (
    vectorstore.as_retriever()
)  # "Retriever"是指一种在自然语言处理中用于检索信息的模型或系统。它通常被用来从大型文本语料库中根据查询或需求检索相关信息。Retriever可以基于关键词匹配、相似度计算或其他检索技术来工作，帮助用户找到他们感兴趣的信息。

# Create a prompt 创建提示词
template = """仅依赖下面的context回答用户的问题:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(  # RunnableParallel是一个并行运行多个Runnable的工具。它可以将多个Runnable组合成一个并行的处理流程，以实现更复杂的任务或功能。
    {
        "context": retriever,  # 可以理解为：context = retriever("question")
        "question": RunnablePassthrough(),
    }  # 把输入问题，不加处理传送到question字段
)
chain = setup_and_retrieval | prompt | model | parser

# Questions
# question = "我们公司前台叫什么名字？"
# question = "附近有好吃的吗？"
question = "我第一次在公司吃饭，想请个人一起。有什么推荐的人选和地方不？"
# question = "我想请假去看病，需要什么手续？向谁请假？"
# question = "我是新来的，公司有没有顺风车到天通苑？"

result = chain.invoke(question)
print(f"Q: {question}\nA: {result}")
