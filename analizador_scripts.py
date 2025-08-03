import google.generativeai as genai
import os
import streamlit as st
import re
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Google Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
GEMINI_MODEL_NAME = "gemini-2.5-flash" 

client = None
if not GEMINI_API_KEY:
    st.error("Error: GEMINI_API_KEY no encontrada en los secretos de Streamlit. Por favor, configúrala.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        client = genai.GenerativeModel(GEMINI_MODEL_NAME)
    except Exception as e:
        st.error(f"Error al configurar la API de Gemini o inicializar el modelo: {e}")
        client = None

def analizar_script(script_texto):
    """
    Realiza un análisis avanzado de un script usando la API de Google Gemini.
    """
    if not script_texto.strip():
        st.warning("El script está vacío. No hay nada que analizar.")
        return

    if client is None:
        st.error("Cliente de Gemini API no inicializado. Revisa tu clave API y logs.")
        return

    full_analysis_text = ""
    prompt_text = f"""
    Eres un **analista de contenido de primer nivel para reels de redes sociales** (TikTok, Instagram, YouTube Shorts).
    Tu misión es realizar un análisis **profundo, dinámico y accionable** del siguiente script para un reel.
    Evalúa cada punto de forma crítica pero constructiva, y **siempre proporciona una sugerencia concreta o un ejemplo de cómo mejorar** si detectas una debilidad.

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir y presentar los siguientes puntos. Para los puntos con puntuación, genera un valor del 0 al 100%.

    **Formato de Salida ABSOLUTAMENTE OBLIGATORIO para el parsing:**
    Cada punto debe iniciar con su título numerado SIN negritas (ej. "1. Tono y Estilo:").
    Si hay una puntuación, DEBE incluir la frase exacta "Puntuación: [X%]".
    Si hay una sugerencia, DEBE incluir la frase exacta "Sugerencia: [Sugerencia concreta o ejemplo]".

    1. Tono y Estilo:
    [Descripción del tono]. Puntuación: [X%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    2. Gancho (Hook):
    [Efectividad del gancho]. Puntuación: [Y%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    3. Desarrollo del Contenido:
    [Claridad y progresión del mensaje]. Puntuación: [Z%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    4. Llamada a la Acción (CTA - Call To Action):
    [Claridad y persuasión de la CTA]. Puntuación: [W%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    5. Originalidad y Creatividad:
    [Nivel de originalidad y frescura]. Puntuación: [A%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    6. Claridad y Concisión:
    [Facilidad de comprensión y brevedad]. Puntuación: [B%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    7. Longitud y Ritmo:
    [Adecuación para reel (30-60s) y flujo general].
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    8. Resumen General y Conclusión Final:
    [Conclusión general y potencial. Mensaje motivador final].
    """

    st.info(f"✨ Enviando script a Gemini para un análisis *supercargado*...")
    try:
        response = client.generate_content(prompt_text,
                                           generation_config={"max_output_tokens": 800, "temperature": 0.7})
        if response and response.text:
            full_analysis_text = response.text
        else:
            st.warning("😕 Gemini no devolvió un análisis válido. La respuesta estaba vacía o incompleta.")
            return

        st.success("✅ ¡Análisis completo generado!")

        st.expander("Ver respuesta RAW de Gemini (para depuración)").code(full_analysis_text)

        # --- PARSING Y PRESENTACIÓN ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")

        section_regex = re.compile(
            r"^\s*(?P<title>\d+\.\s*[^:]+):\s*(?P<content>.*?)(?=\s*\d+\.\s*[^:]+:|$)",
            re.MULTILINE | re.DOTALL
        )

        parsed_data = {}
        for match in section_regex.finditer(full_analysis_text):
            title = match.group('title').strip()
            content = match.group('content').strip()
            parsed_data[title] = content

        ordered_section_titles = [
            "1. Tono y Estilo",
            "2. Gancho (Hook)",
            "3. Desarrollo del Contenido",
            "4. Llamada a la Acción (CTA - Call To Action)",
            "5. Originalidad y Creatividad",
            "6. Claridad y Concisión",
            "7. Longitud y Ritmo",
            "8. Resumen General y Conclusión Final"
        ]

        for full_title_in_order in ordered_section_titles:
            content_raw = parsed_data.get(full_title_in_order, "")

            if content_raw:
                display_title = re.sub(r'^\d+\.\s*', '', full_title_in_order).strip()

                score = None
                description_text = content_raw
                suggestion_text = ""
                
                score_match = re.search(r'Puntuación:[\s\n]*(\d+)%', content_raw, re.IGNORECASE)
                if score_match:
                    score = int(score_match.group(1))
                    description_text = content_raw.split(score_match.group(0))[0].strip()

                suggestion_match = re.search(r'Sugerencia:\s*(.*)', content_raw, re.DOTALL | re.IGNORECASE)
                if suggestion_match:
                    suggestion_text = suggestion_match.group(1).strip()
                    description_text = description_text.split('Sugerencia:')[0].strip()

                if display_title in ["Tono y Estilo", "Gancho (Hook)", "Desarrollo del Contenido",
                                     "Llamada a la Acción (CTA - Call To Action)", "Originalidad y Creatividad",
                                     "Claridad y Concisión"]:
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.metric(display_title, f"{score}%" if score is not None else "N/A")
                    with col2:
                        st.markdown(f"**{display_title}:** {description_text}")
                        if score is not None:
                            st.progress(score)
                        if suggestion_text:
                            st.info(f"💡 Sugerencia: {suggestion_text}")

                elif display_title == "Longitud y Ritmo":
                    st.markdown(f"**{display_title}:** {description_text}")
                    if suggestion_text:
                        st.info(f"💡 Sugerencia: {suggestion_text}")

                elif display_title == "Resumen General y Conclusión Final":
                    st.markdown(f"### {display_title}")
                    st.markdown(description_text)

                st.markdown("---")
            else:
                pass
    
    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script con Gemini: {e}. Por favor, revisa tu código.")
        st.markdown(f"**Análisis de Gemini (Texto Crudo - Fallback por error en la app):**")
        st.code(full_analysis_text if full_analysis_text else "No se pudo obtener el análisis de Gemini debido a un error interno.")
