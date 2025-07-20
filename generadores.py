import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Configuración de la API de OpenAI ---
# Asegúrate de que OPENAI_API_KEY esté configurada en los secretos de Streamlit Cloud
# o en tu archivo .env local.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("Error: OPENAI_API_KEY no encontrada. Por favor, configúrala en los secretos de Streamlit o en tu archivo .env.")
    openai.api_key = None # Asegurarse de que la API key no se settee si no existe
else:
    openai.api_key = OPENAI_API_KEY

def generar_script(tema, objetivo, estilo, duracion):
    """
    Genera un script para un reel de redes sociales usando la API de OpenAI (GPT-3.5 Turbo).
    """
    if not openai.api_key:
        return "API Key de OpenAI no configurada. No se puede generar el script."

    # --- Prompt para GPT-3.5 Turbo ---
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
        # --- Llamada a la API de OpenAI ---
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Puedes probar con "gpt-4o" si tienes acceso y más cuota
            messages=[
                {"role": "system", "content": "Eres un experto creador de contenido para redes sociales."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=500, # Ajusta según la longitud deseada del script
            temperature=0.7, # Creatividad (0.0-1.0)
        )
        
        # Acceder al contenido de la respuesta
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except openai.APIConnectionError as e:
        st.error(f"Error de conexión con la API de OpenAI: {e}")
        return f"Error de conexión: {e}"
    except openai.RateLimitError as e:
        st.error(f"Error de límite de cuota de OpenAI: {e}. Has excedido tu cuota gratuita o tu límite de solicitudes. Por favor, espera o revisa tu plan.")
        return f"Error de cuota: {e}"
    except openai.APIStatusError as e:
        st.error(f"Error de la API de OpenAI (código {e.status_code}): {e.response}")
        return f"Error de API: {e.response}"
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script: {e}")
        return f"Error inesperado: {e}"
