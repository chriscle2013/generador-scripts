# generadores.py

import google.generativeai as genai
import os
import streamlit as st # Importa streamlit aquí para usar st.error/st.info

# Configura la clave API de Google Gemini
# La clave se lee de os.environ, que Streamlit Secrets.toml expone
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        st.info("API de Gemini configurada correctamente (visible en logs de despliegue).") # Esto solo se verá en el log si la app se carga
    except Exception as e:
        st.error(f"Error al configurar la API de Gemini: {e}")
        genai = None # Asegúrate de que genai no se use si falla la configuración
else:
    st.error("Error: GOOGLE_API_KEY no encontrada en los secretos de Streamlit. Por favor, configúrala.")
    genai = None

# Inicializa el modelo Gemini 1.5 Flash (texto)
model = None
if genai:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # <-- ASÍ DEBE QUEDAR
        st.info("Modelo Gemini 'gemini-1.5-flash' cargado exitosamente.") # Actualiza el mensaje
    except Exception as e:
        st.error(f"Error al inicializar el modelo Gemini 'gemini-1.5-flash': {e}") # Actualiza el mensaje
        model = None

def generar_script_reel(nicho):
    """Genera un script para un reel usando Google Gemini."""
    if model is None:
        st.error("No se puede generar script: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return ["Error: Modelo de IA no inicializado."]

    prompt = f"""
Eres un experto creador de contenido para reels de redes sociales (TikTok, Instagram, YouTube Shorts).
Genera un script corto para un reel de 30-60 segundos sobre el nicho de "{nicho}".
El script debe tener 3 escenas (máximo 2-3 líneas por escena), incluir un hook (gancho) al inicio y una llamada a la acción clara al final.
Utiliza un lenguaje atractivo y específico para el nicho.

Formato de salida:
Hook: [Aquí va el hook]
Escena 1: [Descripción de la escena 1]
Escena 2: [Descripción de la escena 2]
Escena 3: [Descripción de la escena 3 con llamada a la acción]
"""
    st.info(f"Enviando prompt a la IA para generar tu script (nicho: {nicho}):\n{prompt[:100]}...") # Mostrar inicio del prompt
    try:
        response = model.generate_content(prompt)
        
        # Depuración: Verificar si la respuesta contiene contenido
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            st.success("¡Script generado por la IA con éxito!")
            return [part.text for part in response.candidates[0].content.parts]
        else:
            st.warning("Gemini no devolvió un script válido. Posiblemente un error interno de la API o contenido bloqueado.")
            # Puedes imprimir el objeto response completo en los logs para más detalles si no funciona
            # print(response)
            return ["No se pudo generar un script válido. Intenta de nuevo o ajusta el prompt."]
    except Exception as e:
        st.error(f"Error al conectar con la IA para script: {e}. Revisa tu clave API y límites de uso.")
        # Aquí también puedes imprimir 'e' en los logs para ver el error completo
        # import traceback
        # print(traceback.format_exc())
        return [f"Error al generar script: {e}"]

def generar_copy_hooks(nicho):
    """Genera un copy y hooks usando Google Gemini."""
    if model is None:
        st.error("No se puede generar copy/hooks: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return {"copy": "Error: Modelo de IA no inicializado.", "hooks": []}

    prompt = f"""
Eres un experto en marketing digital y creación de copys para redes sociales.
Genera un copy persuasivo y 3 hooks (ganchos) para una publicación de reel de TikTok/Instagram/YouTube sobre el nicho de "{nicho}".
El copy debe ser conciso, incluir emojis y hashtags relevantes. Los hooks deben ser preguntas o frases cortas que inciten a ver el reel.

Formato de salida:
Copy: [Aquí va el copy]
Hooks:
- [Hook 1]
- [Hook 2]
- [Hook 3]
"""
    st.info(f"Enviando prompt a Gemini para copy/hooks (nicho: {nicho}):\n{prompt[:100]}...")
    try:
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            st.success("¡Copy y hooks generados por Gemini con éxito!")
            full_text = "".join([part.text for part in response.candidates[0].content.parts])
            
            lines = full_text.split('\n')
            copy_text = ""
            hooks_list = []
            
            for line in lines:
                if line.lower().startswith("copy:"): # Hazlo case-insensitive
                    copy_text = line[len("Copy:"):].strip()
                elif line.strip().startswith("-"): # Asegúrate de que el guion esté al inicio de la línea limpia
                    hooks_list.append(line[1:].strip()) # Quita el guion y el espacio
            
            if not copy_text and not hooks_list and full_text: # Fallback si el parsing falla
                return {"copy": full_text, "hooks": ["No se pudo parsear, aquí está el texto completo."]}

            return {"copy": copy_text, "hooks": hooks_list}
        else:
            st.warning("Gemini no devolvió copy/hooks válidos. Posiblemente un error interno de la API o contenido bloqueado.")
            return {"copy": "No se pudo generar copy/hooks.", "hooks": []}
    except Exception as e:
        st.error(f"Error al generar copy/hooks: {e}. Revisa tu clave API y límites de uso.")
        return {"copy": f"Error al generar copy/hooks: {e}", "hooks": []}
