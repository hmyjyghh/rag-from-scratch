#!/usr/bin/env python
import os
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
  ('system', system_template),
  ('user', '{text}')
])

# 2. Create model
# model = ChatOpenAI()
model = ChatOpenAI(
  base_url=os.getenv("OPENAI_API_BASE_URL"),  # deepseek的 API 地址
  api_key=os.getenv("OPENAI_API_KEY"),
  model="deepseek-reasoner",                          # 使用的模型名称
  temperature=0.7
)

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

  uvicorn.run(app, host="localhost", port=8000)