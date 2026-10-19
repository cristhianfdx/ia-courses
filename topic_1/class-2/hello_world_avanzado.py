from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from common.ollama_connection import get_chat_ollama

llm = get_chat_ollama()

template = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre. \nNombre del usuario {nombre}\n Asistente:"
)

chain = LLMChain(llm=llm, prompt=template)

resultado = chain.run(nombre="Cristhian")
print(resultado)