import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv
import re

load_dotenv()

# --- Configuración de la API de Google Gemini ---
# Usamos GEMINI_API_KEY para ser consistentes con la documentación
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
# El nombre del modelo que estamos usando.
GEMINI_MODEL_NAME = "gemini-1.5-flash"

client = None
if not GEMINI_API_KEY:
    st.error("Error: GEMINI_API_KEY no encontrada. Revisa los secretos de Streamlit Cloud o tu archivo .env")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        client = genai.GenerativeModel(GEMINI_MODEL_NAME)
    except Exception as e:
        st.error(f"Error al configurar la API de Gemini o inicializar el modelo: {e}")
        client = None

def generar_script(tema, objetivo, estilo, duracion):
    """
    Genera un script completo para un reel (con título, hook, desarrollo y CTA).
    """
    if client is None:
        return "No se puede generar script: Modelo de IA no inicializado."

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
        response = client.generate_content(prompt_text,
                                           generation_config={"max_output_tokens": 500, "temperature": 0.7})
        
        if response.text:
            return response.text
        else:
            return "No se pudo generar el script. La respuesta de la IA estaba vacía o incompleta."

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al generar el script con Gemini: {e}")
        return f"Error inesperado al generar script: {e}"

def generar_copy_hooks(tema, script_generado):
    """Genera un copy y hooks usando Google Gemini, basado en un script dado y un tema."""
    if client is None:
        st.error("No se puede generar copy/hooks: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return {"copy": "Error: Modelo de IA no inicializado.", "hooks": []}

    script_texto = "\n".join(script_generado)

    prompt = f"""
    Eres un experto en marketing digital y creación de copys para redes sociales.
    Genera un copy persuasivo y 3 hooks (ganchos) para una publicación de reel de TikTok/Instagram/YouTube.
    El contenido debe ser sobre el tema de "{tema}" y **basado en el siguiente script**:

    --- SCRIPT ---
    {script_texto}
    --- FIN SCRIPT ---

    El copy debe ser conciso, incluir emojis y hashtags relevantes. Los hooks deben ser preguntas o frases cortas que inciten a ver el reel.

    Formato de salida:
    Copy: [Aquí va el copy]

    Hooks:
    - [Hook 1]
    - [Hook 2]
    - [Hook 3]
    """
    try:
        response = client.generate_content(prompt)
        
        if response.text:
            st.success("¡Copy y hooks generados por Gemini con éxito!")
            full_text = response.text
            
            copy_text = ""
            hooks_list = []
            
            # --- Lógica de parsing MEJORADA ---
            copy_match = re.search(r'Copy:(.*?)(?=Hooks:)', full_text, re.DOTALL | re.IGNORECASE)
            if copy_match:
                copy_text = copy_match.group(1).strip()

            hooks_match = re.search(r'Hooks:(.*)', full_text, re.DOTALL | re.IGNORECASE)
            if hooks_match:
                hooks_section = hooks_match.group(1)
                hooks_list = re.findall(r'^\s*[-*]\s*(.*)', hooks_section, re.MULTILINE)
            
            if not copy_text and not hooks_list and full_text:
                return {"copy": full_text, "hooks": ["No se pudo parsear, aquí está el texto completo."]}

            return {"copy": copy_text, "hooks": hooks_list}
        else:
            st.warning("Gemini no devolvió copy/hooks válidos. Posiblemente un error interno de la API o contenido bloqueado.")
            return {"copy": "No se pudo generar copy/hooks.", "hooks": []}

    except Exception as e:
        st.error(f"Error al generar copy/hooks: {e}. Revisa tu clave API y límites de uso.")
        return {"copy": f"Error al generar copy/hooks: {e}", "hooks": []}
