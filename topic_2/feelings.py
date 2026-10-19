import json
from typing import Any

from langchain_core.runnables import RunnableLambda, RunnableParallel

from common.ollama_connection import get_chat_ollama

llm = get_chat_ollama(temperature=0)

def preprocess_text(text: str) -> str:
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text: str) -> str | list[str | dict]:
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text: str)  -> Any | dict[str, str]:
    """Analiza el sentimiento y devuelve resultado estructurado"""
    
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

sentiment_branch = RunnableLambda(analyze_sentiment)


def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merge_results_branch = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel(
    {
        "resumen": summary_branch,
        "sentimiento_data": sentiment_branch
    }
)

def process_one(t):
    resumen = generate_summary(t)           # LLamada al LLM 1
    sentimiento_data = analyze_sentiment(t) # LLamada al LLM 2
    return merge_results({
        "resumen": resumen,
        "sentimiento_data": sentimiento_data
    })

process = RunnableLambda(process_one)

chain = preprocessor | parallel_analysis | merge_results_branch

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

result_batch = chain.batch(textos_prueba)
print(result_batch)

""" 
for texto in textos_prueba:
    resultado = chain.invoke(texto)
    print(f"Texto: {texto}")
    print(f"Resultado: {resultado}")
    print("-" * 50)
"""