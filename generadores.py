# generadores.py (Versión con Google Gemini)

import google.generativeai as genai
import os # Necesario para acceder a las variables de entorno/secrets

# Configura la clave API de Google Gemini
# La clave se lee de os.environ, que Streamlit Secrets.toml expone
if os.environ.get("GOOGLE_API_KEY"):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
else:
    # Esto es útil para el desarrollo local si no quieres configurar secrets.toml
    # en tu máquina, pero preferirás usar variables de entorno locales.
    # Para el despliegue en Streamlit Cloud, el secrets.toml es el método.
    print("Advertencia: GOOGLE_API_KEY no encontrada en las variables de entorno.")

# Inicializa el modelo Gemini Pro (texto)
# Puedes elegir otros modelos si los necesitas
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error al inicializar el modelo Gemini: {e}")
    model = None # Asegúrate de que model sea None si falla la inicialización

def generar_script_reel(nicho):
    """Genera un script para un reel usando Google Gemini."""
    if model is None:
        return ["Error: Modelo de IA no inicializado. Revisa tu clave API."]

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
    try:
        response = model.generate_content(prompt)
        # Acceder al texto generado. Si hay multiples candidatos, toma el primero.
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return [part.text for part in response.candidates[0].content.parts]
        else:
            return ["No se pudo generar un script. Intenta de nuevo o ajusta el prompt."]
    except Exception as e:
        return [f"Error al conectar con la IA para script: {e}. Intenta de nuevo."]

def generar_copy_hooks(nicho):
    """Genera un copy y hooks usando Google Gemini."""
    if model is None:
        return {"copy": "Error: Modelo de IA no inicializado.", "hooks": ["Error al generar hooks."]}

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
    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            # Asumimos que la respuesta será un solo bloque de texto que parsaremos
            full_text = "".join([part.text for part in response.candidates[0].content.parts])
            
            # Simple parsing para extraer copy y hooks
            lines = full_text.split('\n')
            copy_text = ""
            hooks_list = []
            
            for line in lines:
                if line.startswith("Copy:"):
                    copy_text = line.replace("Copy:", "").strip()
                elif line.startswith("-"):
                    hooks_list.append(line.replace("-", "").strip())
                    
            if not copy_text and not hooks_list: # Fallback si el parsing falla
                return {"copy": full_text, "hooks": ["No se pudo parsear, aquí está el texto completo."]}

            return {"copy": copy_text, "hooks": hooks_list}
        else:
            return {"copy": "No se pudo generar copy/hooks. Intenta de nuevo.", "hooks": []}
    except Exception as e:
        return {"copy": f"Error al conectar con la IA para copy/hooks: {e}. Intenta de nuevo.", "hooks": []}
