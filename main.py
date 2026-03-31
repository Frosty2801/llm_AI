from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv
import os

load_dotenv()

record = []

while True:
    user_input = input("You: ")

    record.append(HumanMessage(content=user_input))

    response = llm.invoke(record)

    record.append(AIMessage(content=response.content))
    print("AI: ", response.content)


llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model=os.getenv("DEEPSEEK_MODEL")
)

prompt = ChatPromptTemplate.from_template(
    """
    Actua como un asistente financiero experto en inversiones
        
    """
)

chain = prompt | llm

response = chain.invoke({"tema": "tensorflow y pytorch y que diferencias hay entre ellos junto con langchain"})

print(response.content)

