from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from src.models import llm
from src.prompts import prompt_system
from src.tools import obtener_fecha_actual

herramientas = [obtener_fecha_actual]
llm_con_herramientas = llm.bind_tools(herramientas)

# ----------------- CHAT INTERACTIVO CONTINUO ---------------------
# Inicializamos el "record" agregando a la fuerza tu SystemMessage como la primera instrucción invisible de la charla
record = [prompt_sistema]

print("Eres bienvenido al chat. ¡Soy tu experto en Software y LangChain!")
print("Escribe 'salir' para detener la ejecución.\n")


while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['salir', 'exit', 'quit']:
        print("Saliendo del chat...")
        break

    record.append(HumanMessage(content=user_input))

    response = llm_con_herramientas.invoke(record)

    # ai decision
    if response.tool_calls:
        print(f"\n   [⚙️ La IA decidió pausar y usar la herramienta: '{response.tool_calls[0]['name']}']")
        
        # save in memory
        record.append(response)
        
        for tool_call in response.tool_calls:
            # execute tool
            if tool_call["name"] == "obtener_fecha_actual":
                resultado_herramienta = obtener_fecha_actual.invoke(tool_call["args"])
                print(f"   [✅ Enviándole el papelito de vuelta con el resultado: {resultado_herramienta}]\n")
                
                # return the result to the ai
                mensaje_herramienta = ToolMessage(
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                    content=str(resultado_herramienta)
                )
                record.append(mensaje_herramienta)
                
        # final response
        respuesta_final = llm_con_herramientas.invoke(record)
        print("AI:", respuesta_final.content)
        record.append(respuesta_final)
    else:
        # if ai don't use tools
        print("AI:", response.content)
        record.append(response)

