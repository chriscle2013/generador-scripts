import google.generativeai as genai
import os
import streamlit as st

# Configura la clave API de Google Gemini
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # st.info("API de Gemini configurada correctamente.") # Comentado para evitar el info constante en la UI
    except Exception as e:
        st.error(f"Error al configurar la API de Gemini: {e}")
        genai = None
else:
    st.error("Error: GOOGLE_API_KEY no encontrada en los secretos de Streamlit. Por favor, configúrala.")
    genai = None

# Inicializa 'model' a None al principio del script para asegurar que siempre esté definida
model = None
if genai:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Usando 'gemini-1.5-flash'
        # st.info("Modelo Gemini 'gemini-1.5-flash' cargado exitosamente.") # Comentado para evitar el info constante en la UI
    except Exception as e:
        st.error(f"Error al inicializar el modelo Gemini 'gemini-1.5-flash': {e}")
        model = None

def generar_script_reel(tema):
    """Genera un script para un reel basado en el tema proporcionado usando Google Gemini."""
    if model is None:
        st.error("No se puede generar script: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return ["Error: Modelo de IA no inicializado."]

    prompt = f"""
Eres un experto creador de contenido para reels de redes sociales (TikTok, Instagram, YouTube Shorts).
Genera un script corto para un reel de 30-60 segundos sobre el tema de "{tema}".
El script debe tener 3 escenas (máximo 2-3 líneas por escena), incluir un hook (gancho) al inicio y una llamada a la acción clara al final.
Utiliza un lenguaje atractivo y específico para el tema.

Formato de salida:
Hook: [Aquí va el hook]
Escena 1: [Descripción de la escena 1]
Escena 2: [Descripción de la escena 2]
Escena 3: [Descripción de la escena 3 con llamada a la acción]
"""
    # st.info(f"Enviando prompt a Gemini para script (tema: {tema}):\n{prompt[:100]}...") # Comentado para evitar el info constante en la UI
    try:
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            st.success("¡Script generado por Gemini con éxito!")
            return [part.text for part in response.candidates[0].content.parts]
        else:
            st.warning("Gemini no devolvió un script válido. Posiblemente un error interno de la API o contenido bloqueado.")
            return ["No se pudo generar un script válido. Intenta de nuevo o ajusta el prompt."]
    except Exception as e:
        st.error(f"Error al conectar con la IA para script: {e}. Revisa tu clave API y límites de uso.")
        return [f"Error al generar script: {e}"]

def generar_copy_hooks(tema, script_generado):
    """Genera un copy y hooks usando Google Gemini, basado en un script dado y un tema."""
    if model is None:
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
    # st.info(f"Enviando prompt a Gemini para copy/hooks (tema: {tema}, basado en script):\n{prompt[:100]}...") # Comentado para evitar el info constante en la UI
    try:
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            st.success("¡Copy y hooks generados por Gemini con éxito!")
            full_text = "".join([part.text for part in response.candidates[0].content.parts])
            
            lines = full_text.split('\n')
            copy_text = ""
            hooks_list = []
            
            for line in lines:
                if line.lower().startswith("copy:"):
                    copy_text = line[len("Copy:"):].strip()
                elif line.strip().startswith("-"):
                    hooks_list.append(line[1:].strip())
                    
            if not copy_text and not hooks_list and full_text:
                return {"copy": full_text, "hooks": ["No se pudo parsear, aquí está el texto completo."]}

            return {"copy": copy_text, "hooks": hooks_list}
        else:
            st.warning("Gemini no devolvió copy/hooks válidos. Posiblemente un error interno de la API o contenido bloqueado.")
            return {"copy": "No se pudo generar copy/hooks.", "hooks": []}
    except Exception as e:
        st.error(f"Error al generar copy/hooks: {e}. Revisa tu clave API y límites de uso.")
        return {"copy": f"Error al generar copy/hooks: {e}", "hooks": []}
