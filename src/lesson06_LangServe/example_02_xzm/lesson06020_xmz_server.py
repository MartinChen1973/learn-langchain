# 1. 演示如何使用LangServe的add_routes方法，将chain添加到FastAPI的app中
# 具体用法见代码末尾

#!/usr/bin/env python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_tools.retriever.LangChainRetriever import LangChainRetriever
from dotenv import load_dotenv, find_dotenv
from fastapi.responses import RedirectResponse
from langserve import add_routes

# Load the API key from the .env file
load_dotenv(find_dotenv())

# Define Pydantic model for request body
class QuestionRequest(BaseModel):
    question: str

# Langchain_tools retriever
retriever = LangChainRetriever.create_question_and_context_from_path(
    "src/lesson06_LangServe/example_02_xzm/xmz.md"
)

# Create a prompt
template_text = """仅依赖下面的context回答用户的问题:
Context：{context}

Question: {question}

注意：
1. 如果问题的某些条件（如年龄、性别、症状等）不能在上下文中完全匹配，请在给出答案的同时加以说明。
2. 请把“上下文”称为“我的知识库”。
"""

prompt_template = ChatPromptTemplate.from_template(template_text)

# Create model
model = ChatOpenAI()

# Create parser
parser = StrOutputParser()

# Create RunnableParallel for question and context
question_and_context = RunnableParallel(
    {
        "question": RunnablePassthrough(),
        "context": retriever,
    }
)

# Create the chain
chain = question_and_context | prompt_template | model | parser

# Define the FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# Add the chain route
add_routes(
    app,
    chain,
    path="/chain",
)

@app.post("/ask")
async def get_chain_response(request: QuestionRequest):
    try:
        # Extract only the question text
        result = chain.invoke(request.question)
        return {"question": request.question, "answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8930)

# Run the server with the following command:

# 1. Terminal / New Terminal打开一个终端窗口（此时应该位于项目根目录），运行下面的指令
# python .\src\lesson06_LangServe\example_02_xzm\lesson06020_xmz_server.py

# 2. 测试性访问如下地址应可以看到相关内容（而非404页面不存在）
# Root: http://localhost:8930/
# Swagger UI: http://localhost:8930/docs
# Playground UI: http://localhost:8930/chain/playground
# ReDoc UI: http://localhost:8930/redoc
# OpenAPI JSON: http://localhost:8930/openapi.json
# Chain Endpoint: http://localhost:8930/chain

# 3. 如果要运行Client端的代码，请参考Client代码中的使用说明。