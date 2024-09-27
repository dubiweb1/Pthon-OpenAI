import streamlit as st
from langchain_openai import ChatOpenAI  # Import actualizado
import openai

# Inicializamos el modelo con GPT-4 y DALL·E API
llm = ChatOpenAI(model="gpt-4", temperature=0, api_key="xxxxxxxxxxxxxx")
openai.api_key = "sk-tu-api-key-correcta"  # Aquí usa la API key correcta de OpenAI para generación de imágenes

# Custom CSS para mejorar la interfaz
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .stTextInput {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título y descripción principal
st.title("💻 DubiWeb, tu tutor virtual")
st.subheader("🤖 DubiWeb está aquí para ayudarte en cualquier momento del día. ¡No dudes en preguntarme!")

# Inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div class='message'>{message['content']}</div>", unsafe_allow_html=True)

# Input del usuario y manejo del estado del input
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

def handle_input():
    # Actualiza el valor del prompt en session_state
    prompt = st.session_state.prompt
    if prompt:
        st.chat_message("user").markdown(f"**Tú:** {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})

        if "imagen" in prompt.lower() or "dibuja" in prompt.lower():
            # Llamar a la API de DALL·E para generar la imagen
            try:
                response = openai.Image.create(prompt=prompt, n=1, size="512x512")
                image_url = response['data'][0]['url']
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"[Imagen generada]({image_url})"})
            except Exception as e:
                st.error(f"Error al generar la imagen: {e}")
        else:
            # Generar respuesta de texto usando GPT-4
            try:
                response = llm.invoke([{"role": "user", "content": prompt}]).content
                st.chat_message("assistant").markdown(f"**DubiWeb:** {response}")
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error al generar la respuesta: {e}")
        
        # Limpiar el campo de texto después de enviar el mensaje
        st.session_state.prompt = ""

# Renderizar el campo de entrada y procesar el input
st.text_input("💬 Escribe tu mensaje o describe la imagen que quieres generar...",
              key="prompt", on_change=handle_input)

# Scroll automático hacia el último mensaje
st.markdown("""
    <script>
    document.getElementById('MainContainer').scrollTop = document.getElementById('MainContainer').scrollHeight;
    </script>
    """, unsafe_allow_html=True)

# Footer con estilo
st.markdown("""
    <div style='text-align: center; padding-top: 20px;'>
    <p style="font-size: 12px;">🔗 Desarrollado por <a href="https://educacionactiva.net" style="color: #4CAF50;">Educación Activa</a></p>
    </div>
    """, unsafe_allow_html=True)