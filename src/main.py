from langchain_core.messages import HumanMessage, AIMessage

from src.config import *
from src.models import llm
from src.prompts import prompt

# ----------------- static prompt -----------------
chain = prompt | llm

print("--- STATIC PROMPT ---")

for chunk in chain.stream({"tema": "tensorflow y pytorch y que diferencias hay entre ellos junto con langchain"}):
    print(chunk.content, end="", flush=True)

print("\n----------------------------------\n")


# -----------------interactive continuous chat ---------------------
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

    print("AI: ", end="", flush=True)
    full_response = ""
    
    # Interactive chat with streaming
    for chunk in llm.stream(record):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
        
    print("\n")

    record.append(AIMessage(content=full_response))
