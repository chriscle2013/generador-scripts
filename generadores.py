# generadores.py
from huggingface_hub import InferenceClient # Removed HfHub
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Hugging Face ---
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
HF_MODEL_NAME = "deepseek-ai/DeepSeek-R1-0528"

client = None
if not HF_API_TOKEN:
    st.error("Error: HF_API_TOKEN no encontrada. No se puede generar el script.")
else:
    try:
        client = InferenceClient(model=HF_MODEL_NAME, token=HF_API_TOKEN)
    except Exception as e:
        st.error(f"Error al inicializar el cliente de Hugging Face en generadores.py: {e}")
        client = None

def generar_script(tema, objetivo, estilo, duracion):
    if client is None:
        return "Cliente de Hugging Face API no inicializado. Revisa tu token API y logs."

    prompt_text = f"""
    Eres un experto creador de contenido para redes sociales (TikTok, Instagram Reels, YouTube Shorts).
    Tu tarea es generar un script detallado y creativo para un reel, basado en la siguiente información:

    Tema: {tema}
    Objetivo: {objetivo}
    Estilo/Tono: {estilo}
    Duración aproximada: {duracion} segundos

    El script debe incluir:
    1.  **Título sugerido para el Reel.**
    2.  **Gancho (Hook):** Las primeras 3-5 segundos que captarán la atención.
    3.  **Desarrollo del Contenido:** La narrativa principal, con escenas o puntos clave.
    4.  **Llamada a la Acción (CTA - Call To Action):** Qué quieres que el espectador haga al final (ej. seguirte, comentar, comprar).
    5.  **Ideas de Elementos Visuales/Sonido:** Sugerencias para imágenes, texto en pantalla, transiciones, música, etc.

    La respuesta debe ser clara, concisa y fácil de seguir para alguien que va a grabar el reel.
    Formato de Salida:
    ---
    **Título:** [Tu título aquí]

    **Gancho:**
    [Descripción del gancho]

    **Desarrollo del Contenido:**
    [Escena 1: Descripción]
    [Escena 2: Descripción]
    ...
    [Escena N: Descripción]

    **Llamada a la Acción:**
    [Tu CTA aquí]

    **Elementos Visuales/Sonido:**
    [Lista de ideas visuales/sonido]
    ---
    """

    try:
        response = client.text_generation(
            prompt=prompt_text,
            max_new_tokens=500,
            temperature=0.6,
        )

        if response:
            return response
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script con DeepSeek-R1-0528: {e}")
        return f"Error inesperado al generar script: {e}"
