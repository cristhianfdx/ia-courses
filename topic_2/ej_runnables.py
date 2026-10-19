from langchain_core.runnables import RunnableLambda

step_1 = RunnableLambda(lambda x: f"Número {x}")

def text_duplicate(txt: str) -> list[str]:
    return [txt] * 2

step_2 = RunnableLambda(text_duplicate)

chain = step_1 | step_2

result = chain.invoke(43)
print(result)