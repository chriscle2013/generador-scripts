from huggingface_hub import InferenceClient
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Hugging Face ---
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

# Nombre del modelo Hugging Face a usar.
HF_MODEL_NAME = "microsoft/Phi-4-mini-flash-reasoning"

client = None
if not HF_API_TOKEN:
    st.error("Error: HF_API_TOKEN no encontrada. No se puede generar el script.")
else:
    try:
        # Inicializa el cliente de Inferencias de Hugging Face
        client = InferenceClient(model=HF_MODEL_NAME, token=HF_API_TOKEN)
    except Exception as e:
        st.error(f"Error al inicializar el cliente de Hugging Face en generadores.py: {e}")
        client = None

def generar_script(tema, objetivo, estilo, duracion):
    """
    Genera un script para un reel de redes sociales usando la API de Hugging Face (Phi-4-mini-flash-reasoning).
    """
    if client is None:
        return "Cliente de Hugging Face API no inicializado. Revisa tu token API y logs."

    # --- Prompt para Phi-4-mini-flash-reasoning ---
    # Este modelo es de "text-generation" y "razonamiento", por lo que un prompt directo funciona bien.
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
        # --- Llamada a la API de Hugging Face para text-generation ---
        # Usamos client.text_generation() ya que es un modelo de generación de texto.
        response = client.text_generation(
            prompt=prompt_text,
            max_new_tokens=500, # Cantidad máxima de tokens a generar
            temperature=0.7, # Un poco más alto para creatividad, pero puedes ajustar
        )

        if response:
            return response
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script con {HF_MODEL_NAME}: {e}")
        return f"Error inesperado al generar script: {e}"
