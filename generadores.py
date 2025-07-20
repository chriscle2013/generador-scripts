import openai # Librería de OpenAI para compatibilidad con DeepSeek
import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno (útil para desarrollo local)
load_dotenv()

# --- Configuración de la API de DeepSeek ---
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# URL base para la API de DeepSeek (¡IMPORTANTE!)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Inicializar el cliente de OpenAI apuntando a DeepSeek
client = None # Inicializar a None por defecto
if not DEEPSEEK_API_KEY:
    st.error("Error: DEEPSEEK_API_KEY no encontrada. No se puede generar el script.")
else:
    try:
        # Crea un cliente de OpenAI, pero apuntando a la URL de DeepSeek
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
    except Exception as e:
        st.error(f"Error al inicializar el cliente de DeepSeek en generadores.py: {e}")
        client = None

def generar_script(tema, objetivo, estilo, duracion):
    """
    Genera un script para un reel de redes sociales usando la API de DeepSeek AI (DeepSeek-V2).
    """
    if client is None:
        return "Cliente de DeepSeek API no inicializado. Revisa tu clave API y logs."

    # --- Prompt para DeepSeek-V2 ---
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
        # --- Llamada a la API de DeepSeek ---
        response = client.chat.completions.create(
            model="deepseek-chat", # Usamos el modelo generalista de DeepSeek
            messages=[
                {"role": "system", "content": "Eres un experto creador de contenido para redes sociales."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=500, # Ajusta según la longitud deseada del script
            temperature=0.7, # Creatividad (0.0-1.0)
            stream=False, # <--- ¡CAMBIO IMPORTANTE AQUÍ! Asegurarse de no usar streaming
        )

        # Acceder al contenido de la respuesta
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except openai.APIConnectionError as e:
        st.error(f"Error de conexión con la API de DeepSeek: {e}")
        return f"Error de conexión: {e}"
    except openai.RateLimitError as e:
        st.error(f"Error de límite de cuota de DeepSeek: {e}. Has excedido tu cuota gratuita o tu límite de solicitudes. Por favor, espera o revisa tu plan.")
        return f"Error de cuota: {e}"
    except openai.APIStatusError as e:
        st.error(f"Error de la API de DeepSeek (código {e.status_code}): {e.response.text}") # Usar .text para ver el detalle del error
        return f"Error de API: {e.response.text}"
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script: {e}")
        return f"Error inesperado: {e}"
