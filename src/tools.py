import datetime
from langchain_core.tools import tool

@tool
def obtener_fecha_actual() -> str:
    """Devuelve la fecha y hora actual del sistema. Útil si el usuario pregunta qué día o qué hora es."""
    ahora = datetime.datetime.now()
    return f"La fecha y hora actual del sistema es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
