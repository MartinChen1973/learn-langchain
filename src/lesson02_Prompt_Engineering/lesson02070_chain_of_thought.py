# 1. 演示复杂过程的提示词工程
# 2. 思维链的特点：分步骤、阶段性成果、可迭代（重复之前的步骤）

# Load the API key from the .env file (#010) 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv())

# Create the OpenAI chatbot 创建聊天机器人
model = ChatOpenAI(model="gpt-4o-mini") # Very Clever, but still not enough

# Read code from a file 从文件中读取代码
with open("src/lesson02_Prompt_Engineering/data/code.py", "r", encoding="utf-8") as file:
    code = file.read()

# 普通提示词
print("普通提示词的结果***********************************")
query  = """
利用代码中的 add_node() 和 add_edge() 和 add_conditional_edges() 
创建一个 mermaid td digram 脚本。
完整代码如下：
"""

input = query + code

response = model.invoke(input)

print(response.content)

# 思维链提示词
print("思维链提示词的结果***********************************")
query  = """
第一步：提取代码中包含 add_node() 和 add_edge() 和 add_conditional_edges() 的代码行，并列出上述代码行
第二步：单独列出包含 add_node(), add_edge 和 add_conditional_edges 的代码行
第三步：创建一个 mermaid td digram 脚本。请严格按照第三步中的代码行的数量绘制：为 add_edge 绘制实线，为 add_conditional_edges 绘制虚线。
第四步：输出mermaid脚本（不要额外的解释，只要脚本）。

完整代码如下：
"""

input = query + code

response = model.invoke(input)

print(response.content)
