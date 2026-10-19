from langchain_core.prompts import ChatPromptTemplate

from common.ollama_connection import get_chat_ollama

llm = get_chat_ollama()

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un traductor del español al inglés my preciso."),
        ("human", "{text}")
    ]
)

messages = chat_prompt.format_messages(text= "Hola mundo, como estas?")
for m in messages:
    print(f"{type(m)}: {m.content}")


