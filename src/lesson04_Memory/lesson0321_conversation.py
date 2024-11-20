# 1. 演示如何记住对话历史，并在后续的对话中使用它们。

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

# Load the API key from the .env file 从.env文件中加载API密钥
load_dotenv(find_dotenv())

# Create the OpenAI chatbot 创建聊天机器人
model = ChatOpenAI()

# create a document retrieval chain 创建文档检索链
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "根据下面的对话历史回答用户的问题:\n\n",
        ),  # context from search engine. 来自搜索引擎的上下文。
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # 在这里将会出现 user, ai, user, ai... 对话历史
        ("user", "{input}"),
    ]
)
history_chain = prompt | model

chat_history = []

# Start the chatbot and get the response   启动聊天机器人并获得回复
questions = ["金庸先生是谁？", 
             "他写的最后一篇武侠小说是？", 
             "这本小说是哪一年出版的？"]
for question in questions:
    print("User>>" + question)
    response = history_chain.invoke({"input": question, "chat_history": chat_history})
    answer = response.content
    print("AI  >>" + answer)

    # Append the conversation history 添加对话历史
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))
