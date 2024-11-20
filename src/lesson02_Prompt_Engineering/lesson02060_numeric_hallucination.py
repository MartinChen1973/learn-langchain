# Load the API key from the .env file (#010) 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

# 从当前文件夹或父文件夹中加载.env文件的配置（成为全局可访问的静态变量）。
load_dotenv(find_dotenv())

# Create the OpenAI chatbot 创建聊天机器人
# model = ChatOpenAI() # 3.5。 Clever, but not enough
model = ChatOpenAI(model="gpt-4o-mini") # Very Clever, but still not enough
# model = ChatOpenAI(model="gpt-4o") # Super Clever

# Start the chatbot and get the response 启动聊天机器人并获得回复
# **注意**：早期的gpt-4o 模型曾经无法正确回答这个问题，现在已经可以了（2024-11-8）
query  = """
    -12.11和-12.89是否都介于-27到-7之间？
"""
# query  = """
#     有两个数字分别是-12.11和-12.89。这两个数字的绝对值都大于7，且小于27。
#     如果上述描述正确或条件满足，请直接回答“通过”（只包含两个汉字，不要任何标点符合、解释）。
#     否则，请回答“失败|原因：……”。失败的原因请采用三段论的表述方式，即：“要求的条件是……，而实际情况是……，所以判定为失败。”
#     如果无法确定，按失败处理。
# """
response = model.invoke(query)

print(response)
