from langchain_core.prompts import ChatPromptTemplate

# static prompt
prompt = ChatPromptTemplate.from_template(
    """
    Actua como alguien experto en desarrollo de software, enfocado en IA.
    Explicame porque se utiliza langchain y como funciona. 
    """
)
