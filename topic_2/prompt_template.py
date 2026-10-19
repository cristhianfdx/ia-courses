from langchain_core.prompts import PromptTemplate

from common.ollama_connection import get_chat_ollama

llm = get_chat_ollama()

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {product}"

prompt = PromptTemplate(
    template=template,
    input_variables=["product"]
)

full_prompt = prompt.format(product="café orgánico")
print(full_prompt)