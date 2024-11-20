#!/usr/bin/env python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from langserve import add_routes
from fastapi import FastAPI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 1. Create prompt template
# system_template_text ensures the question is related to Agile/Scrum
system_template_text = (
    "请注意，本系统仅回答与敏捷开发（Scrum）相关的问题。"
    "如果您有其他问题，请重新输入。"
)

# User template will filter non-Agile/Scrum related questions
user_template_text = (
    "问题：{question}\n"
    "如果问题与敏捷开发（Scrum）无关，请回答：“本系统仅回答与敏捷开发（Scrum）相关的问题。”"
)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template_text), ("user", user_template_text)]
)

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

# 4. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8900)

# Root: http://localhost:8900/
# Swagger UI: http://localhost:8900/docs
# Playground UI: http://localhost:8900/chain/playground
# ReDoc UI: http://localhost:8900/redoc
# OpenAPI JSON: http://localhost:8900/openapi.json
# Chain Endpoint: http://localhost:8900/chain
