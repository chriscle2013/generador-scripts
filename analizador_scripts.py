import google.generativeai as genai
import os
import streamlit as st

# La configuración de la API y la inicialización del modelo son cruciales aquí también.
# Asegúrate de que GOOGLE_API_KEY esté disponible en Streamlit Cloud Secrets.

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"Error al configurar la API de Gemini en analizador_scripts: {e}")
        genai = None
else:
    st.error("Error: GOOGLE_API_KEY no encontrada en los secretos de Streamlit para el analizador. Por favor, configúrala.")
    genai = None

model = None
if genai:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al inicializar el modelo Gemini 'gemini-1.5-flash' en analizador_scripts: {e}")
        model = None

def analizar_script(script_texto):
    """
    Realiza un análisis avanzado de un script usando Google Gemini, evaluando tono, hook, CTA, etc.
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar con la IA."

    if model is None:
        st.error("No se puede analizar el script: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return "Error: Modelo de IA para análisis no inicializado."

    prompt = f"""
    Eres un experto analista de contenido para reels de redes sociales (TikTok, Instagram, YouTube Shorts).
    Tu tarea es analizar el siguiente script para un reel y proporcionar un feedback detallado.
    Evalúa los siguientes puntos y sé constructivo en tus sugerencias:

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir:
    1.  **Tono y Estilo:** ¿Es el tono adecuado para un reel? ¿Es atractivo y mantiene la atención?
    2.  **Gancho (Hook):** ¿Es efectivo el inicio del script para captar la atención en los primeros segundos? Sugiere mejoras si es necesario.
    3.  **Desarrollo del Contenido:** ¿Fluye bien el mensaje? ¿Es claro y conciso? ¿Hay una progresión lógica?
    4.  **Llamada a la Acción (CTA - Call To Action):** ¿Es clara y persuasiva la CTA final? ¿Es fácil de entender para el espectador qué debe hacer?
    5.  **Longitud y Ritmo:** ¿Es apropiado para un reel corto (30-60 segundos)? ¿Sugiere algún ajuste de ritmo?
    6.  **Sugerencias Generales:** Cualquier otra recomendación para mejorar el script.

    Por favor, presenta tu análisis de manera estructurada con encabezados para cada punto.
    """
    st.info("Enviando script a Gemini para análisis...")
    try:
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            st.success("¡Análisis de script generado por Gemini!")
            return "\n".join([part.text for part in response.candidates[0].content.parts])
        else:
            st.warning("Gemini no devolvió un análisis válido. Posiblemente un error interno de la API o contenido bloqueado.")
            return "No se pudo generar el análisis del script. Intenta de nuevo."
    except Exception as e:
        st.error(f"Error al conectar con la IA para análisis de script: {e}. Revisa tu clave API y límites de uso.")
        return f"Error al analizar script: {e}"
