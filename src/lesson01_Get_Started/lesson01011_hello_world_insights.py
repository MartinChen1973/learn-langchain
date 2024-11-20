# 1. 演示.env文件中的API密钥使用
# 2. 演示model创建的参数差异
# 3. 查看response的详细内容

# Load the API key from the .env file (#010) 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
# 从当前文件夹或父文件夹中加载.env文件的配置（成为全局可访问的静态变量）。
load_dotenv(find_dotenv())

# Create the OpenAI chatbot 创建聊天机器人
# model或llm是大语言模型Large Language Model的缩写。ChatOpenAI是一个用于与OpenAI或与之兼容的其他模型交互的类。
# model = ChatOpenAI() # 默认是gpt-3.5
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model ="gpt-4o-mini") # Better and cheaper.
# model = ChatOpenAI(model = "gpt-4o") # Better but expensive.
# model = ChatOpenAI(model="gemma-7b-it") # 默认是gpt-3.5
# print(model)

# Start the chatbot and get the response 启动聊天机器人并获得回复
response = model.invoke("say 'hello  worlld !'")
# print(response)

# Print the response 打印回复
# print(response.content)
print(response)
