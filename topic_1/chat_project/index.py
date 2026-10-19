import streamlit as st
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

from common.ollama_connection import get_chat_ollama

# Config website App

st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + StreamLit. ¡Escribe tu mensaje abajo para iniciar!")

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["deepseek-v4.1-flash", "glm-5.3-flash"])

    chat_model = get_chat_ollama(model=model_name, temperature=temperature)

# Messages history initialize

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""
        Eres un asistente útil y amigable llamado ChatBot Pro.
        
        Historial de conversación:
        {historial}
        
        Responde de manera clara y concisa a la siguiente:
        {mensaje}
    """
)

# LCEL - LangChain Expression Language
cadena = prompt_template | chat_model

# Show preview messages
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # Don't show message
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    
    with st.chat_message(role):
        st.markdown(msg.content)


# 1. Defines el cuadro de diálogo (la alerta) usando el decorador
@st.dialog("⚠️ Confirmar acción")
def confirmar_borrado():
    st.write("¿Estás seguro de que deseas eliminar toda la conversación? Esta acción no se puede deshacer.")
    
    # Usamos columnas para poner los botones de Sí y No uno al lado del otro
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sí, eliminar", type="primary"):
            st.session_state.mensajes = []
            st.rerun() # Refresca la app (el modal se cerrará automáticamente)
            
    with col2:
        if st.button("Cancelar"):
            st.rerun() # Refresca la app cerrando el modal sin borrar nada

# 2. Llamas a la función del modal cuando se presiona el botón principal
if st.button("🗑️ Nueva conversación"):
    confirmar_borrado()

# Input text
pregunta = st.chat_input(placeholder="Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
        
        try:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                stream = cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes})
                
                for chunk in stream:
                    full_response += chunk.content
                    response_placeholder.markdown(full_response + "▌")
                    
                response_placeholder.markdown(full_response)
        
            # Save message in memory
            st.session_state.mensajes.append(HumanMessage(content=pregunta))
            st.session_state.mensajes.append(AIMessage(content=full_response))
            
        except Exception as e:
            st.error(f"Error al generar respuesta: {str(e)}")
            st.info("verifica que tu API Key es el correcto.")

            

    

