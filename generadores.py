from huggingface_hub import InferenceClient, HfHub
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Hugging Face ---
# Asegúrate de que HF_API_TOKEN esté configurada en los secretos de Streamlit Cloud
# o en tu archivo .env local.
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

# Nombre del modelo Hugging Face a usar.
# Hemos elegido deepseek-ai/DeepSeek-R1-0528
HF_MODEL_NAME = "deepseek-ai/DeepSeek-R1-0528"

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
    Genera un script para un reel de redes sociales usando la API de Hugging Face (DeepSeek-R1-0528).
    """
    if client is None:
        return "Cliente de Hugging Face API no inicializado. Revisa tu token API y logs."

    # --- Prompt para DeepSeek-R1-0528 ---
    # Este modelo es un modelo de chat, por lo que el formato del prompt es importante.
    # Aunque InferenceClient.text_generation no tiene parámetros 'system', 'user', 'assistant' explícitos,
    # el modelo puede inferir roles si el prompt está bien estructurado.
    # Aquí un formato de chat que el modelo DeepSeek puede entender.
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
        # --- Llamada a la API de Hugging Face para text2text-generation ---
        # Usa el método `text_generation` para modelos de texto-a-texto
        response = client.text_generation(
            prompt=prompt_text,
            max_new_tokens=500, # Cantidad máxima de tokens a generar
            temperature=0.6, # Temperatura recomendada para DeepSeek-R1 para un balance entre creatividad y coherencia
            # top_p=0.9, # Puedes ajustar parámetros como top_p
        )

        if response:
            return response
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script con DeepSeek-R1-0528: {e}")
        return f"Error inesperado al generar script: {e}"
