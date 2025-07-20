import dashscope # ¡Nueva librería!
from http import HTTPStatus # Para manejar los estados de respuesta HTTP
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Qwen ---
# Asegúrate de que DASHSCOPE_API_KEY esté configurada en los secretos de Streamlit Cloud
# o en tu archivo .env local.
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")

# Asignar la API Key a la configuración de dashscope
if DASHSCOPE_API_KEY:
    dashscope.api_key = DASHSCOPE_API_KEY
else:
    st.error("Error: DASHSCOPE_API_KEY no encontrada. No se puede generar el script.")

# Nombre del modelo Qwen a usar (ej. Qwen-Turbo es un buen punto de partida por su eficiencia)
# Debes verificar el nombre exacto del modelo en la documentación de Qwen/Alibaba Cloud.
QWEN_MODEL_NAME = "qwen-turbo" # O "qwen-plus", "qwen-max", etc.

def generar_script(tema, objetivo, estilo, duracion):
    """
    Genera un script para un reel de redes sociales usando la API de Qwen (Dashscope).
    """
    if not DASHSCOPE_API_KEY:
        return "API Key de Qwen no configurada. Revisa los secretos de Streamlit o tu archivo .env."

    # --- Construir el mensaje para la API de Qwen ---
    # Qwen espera un formato de mensajes similar a OpenAI/Anthropic
    messages_payload = [
        {"role": "system", "content": "Eres un experto creador de contenido para redes sociales."},
        {"role": "user", "content": f"""
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
        """}
    ]

    try:
        # --- Llamada a la API de Qwen usando dashscope ---
        # dashscope.Generation.call es el método para completaciones de chat
        response = dashscope.Generation.call(
            model=QWEN_MODEL_NAME,
            messages=messages_payload,
            # top_p=0.8, # Puedes ajustar parámetros como top_p, etc.
            # result_format='message', # Asegura que la respuesta sea en formato de mensaje
        )

        # Verificar si la llamada fue exitosa
        if response.status_code == HTTPStatus.OK:
            # Acceder al contenido de la respuesta de Qwen
            # La estructura es response.output.choices[0].message.content
            if response.output and response.output.choices and response.output.choices[0].message and response.output.choices[0].message.content:
                return response.output.choices[0].message.content
            else:
                return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."
        else:
            # Manejo de errores de la API de Qwen
            return (f"Error de la API de Qwen (código {response.status_code}): "
                    f"Código de error: {response.code}, Mensaje: {response.message}")

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script con Qwen: {e}")
        return f"Error inesperado al generar script: {e}"
