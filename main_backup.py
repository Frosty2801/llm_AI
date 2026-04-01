from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv
import os

load_dotenv()

# model install
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model=os.getenv("DEEPSEEK_MODEL")
)

# static prompt
prompt = ChatPromptTemplate.from_template(
    """
    Actua como un asistente financiero experto en inversiones.
    Tengo 1000 dolares para invertir, ¿en que me recomiendas invertir?, 
    ademas aplica la regla 50/30/20 y explicame como distribuir el dinero.
    """
)

chain = prompt | llm
response_estatico = chain.invoke({""})
print("--- RESPUESTA INICIAL ESTÁTICA ---")
print(response_estatico.content)
print("----------------------------------\n")


# record of conversation and bucle for continuous chat
record = []
print("Puedes comenzar el chat. Escribe 'salir' para detener la ejecución.")

while True:
    user_input = input("You: ")
    
    # finish talk
    if user_input.lower() in ['salir', 'exit', 'quit']:
        print("Saliendo del chat...")
        break

    record.append(HumanMessage(content=user_input))

    response = llm.invoke(record)

    record.append(AIMessage(content=response.content))
    print("AI: ", response.content)
