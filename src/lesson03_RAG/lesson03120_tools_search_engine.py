# 1. 演示如何通过封装来简化代码（URL）

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_tools.retriever.LangChainRetriever import LangChainRetriever

# Load the API key from the .env file   从.env文件中加载API密钥
load_dotenv(find_dotenv())

# Create the retriever from url 从url创建检索器
question_and_context = LangChainRetriever.create_question_and_context_from_url(
    "https://docs.smith.langchain.com/overview"
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
