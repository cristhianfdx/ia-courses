

from dotenv import load_dotenv

from common.ollama_connection import get_chat_ollama

load_dotenv()

llm = get_chat_ollama(model="deepseek-v4.1-flash", temperature=0.7)

response = llm.invoke("Hola, responde en español.")
print(response.content)