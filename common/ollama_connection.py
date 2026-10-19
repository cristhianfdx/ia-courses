import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def get_chat_ollama(model: str = "deepseek-v4.1-flash", temperature: float | None = None) -> ChatOllama:
    return ChatOllama(
        model=model,
        temperature=temperature,
        base_url=os.getenv("OLLAMA_BASE_URL"),
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
            }
        },
    )