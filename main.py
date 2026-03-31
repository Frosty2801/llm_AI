from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model=os.getenv("DEEPSEEK_MODEL")
)

prompt = ChatPromptTemplate.from_template(
    "Explicame {tema} de forma sencilla"
)

chain = prompt | llm

response = chain.invoke({"tema": "modelos llm"})

print(response.content)

