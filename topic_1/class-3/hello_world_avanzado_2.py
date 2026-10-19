from langchain.prompts import PromptTemplate

from common.ollama_connection import get_chat_ollama

llm = get_chat_ollama()

template = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre. \nNombre del usuario {nombre}\n Asistente:"
)

chain = template | llm

resultado = chain.invoke({"nombre":"Cristhian"})
print(resultado.content)