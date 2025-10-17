import streamlit as st
import openai
from datetime import datetime
import os
import requests

@st.cache_data
def fetch_schedule()->dict:
    """Fetch schedule data from PyConES API"""
    try:
        response = requests.get(
            "https://pretalx.com/pycones-2025/schedule/v/0.3/widgets/schedule.json"
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error al cargar el horario: {e}")
        return None


# Page configuration
st.set_page_config(
    page_title="Chat con IA - PyConES 2025",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Chat con IA - PyConES 2025")
st.markdown("Asistente de IA powered by OpenAI para PyConES 2025")

# Sidebar for OpenAI configuration
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # OpenAI API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Introduce tu clave de API de OpenAI",
    )

    api_key = api_key.strip() if api_key.strip() else os.environ.get("OPENAI_API_KEY", "").strip()
    
    # Model selection
    model = st.selectbox(
        "Modelo",
        ["gpt-4.1", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0
    )
    
    # Temperature setting
    temperature = st.slider(
        "Creatividad (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    st.markdown("---")
    
    # Chat statistics
    if "messages" in st.session_state:
        st.markdown("### 📊 Estadísticas")
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Total mensajes", total_messages)
        st.metric("Mis mensajes", user_messages)
    
    # Clear chat button
    if st.button("🗑️ Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

def get_openai_response(messages, api_key, model, temperature):
    """Get response from OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key)

        # st.write(fetch_schedule())
        
        # Add system message for context
        system_message = {
            "role": "system",
            "content": f"""Eres un asistente útil y amigable para PyConES 2025, la conferencia de Python en España. 
            Puedes ayudar con preguntas sobre:
            - Python y programación
            - Streamlit y desarrollo web
            - PyConES 2025 y la comunidad Python
            - Tecnología en general
            
            Responde en español de manera clara y concisa.
            Usa la siguiente información para ayudar con los schedules y charlas de PyConES 2025:
            {fetch_schedule()["talks"][:50] if fetch_schedule() else "No se pudo cargar la información del horario."}
            """
        }
        
        # Prepare messages for API
        api_messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=temperature,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except openai.AuthenticationError:
        return "❌ Error de autenticación. Verifica tu API key de OpenAI."
    except openai.RateLimitError:
        return "⏱️ Has alcanzado el límite de uso. Intenta de nuevo más tarde."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy tu asistente de IA para PyConES 2025. ¿En qué puedo ayudarte?",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(message["content"])
        with col2:
            st.caption(message.get("timestamp", ""))

# Chat input
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Check if API key is provided
    if not api_key:
        st.error("Por favor, introduce tu API key de OpenAI en la barra lateral.")
        st.stop()
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(prompt)
        with col2:
            st.caption(timestamp)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            # Prepare messages for OpenAI API (exclude timestamps)
            api_messages = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.messages 
                if msg["role"] in ["user", "assistant"]
            ]
            
            response = get_openai_response(api_messages, api_key, model, temperature)
            
        st.markdown(response)
        
        # Add AI response to history
        ai_timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": ai_timestamp
        })
