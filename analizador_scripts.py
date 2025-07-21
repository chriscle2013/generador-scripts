# analizador_scripts.py
from huggingface_hub import InferenceClient
import os
import streamlit as st
import re
from dotenv import load_dotenv

load_dotenv()

# --- Configuración de la API de Hugging Face ---
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

# Mismo nombre de modelo que en generadores.py
HF_MODEL_NAME = "microsoft/Phi-4-mini-flash-reasoning"

client = None
if not HF_API_TOKEN:
    st.error("Error: HF_API_TOKEN no encontrada. No se puede analizar el script.")
else:
    try:
        client = InferenceClient(model=HF_MODEL_NAME, token=HF_API_TOKEN)
    except Exception as e:
        st.error(f"Error al inicializar el cliente de Hugging Face en analizador_scripts.py: {e}")
        client = None

def analizar_script(script_texto):
    """
    Realiza un análisis avanzado de un script usando la API de Hugging Face (Phi-4-mini-flash-reasoning).
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar con la IA."

    if client is None:
        return "Cliente de Hugging Face API no inicializado. Revisa tu token API y logs."

    full_analysis_text = ""

    # --- Prompt para Phi-4-mini-flash-reasoning ---
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

    st.info(f"✨ Enviando script a {HF_MODEL_NAME} (Hugging Face) para un análisis *supercargado*...")
    try:
        # --- Llamada a la API de Hugging Face para text-generation ---
        response = client.text_generation(
            prompt=prompt_text,
            max_new_tokens=800,
            temperature=0.7, # Puedes ajustar para más o menos creatividad
        )

        if response:
            full_analysis_text = response
        else:
            st.warning(f"😕 {HF_MODEL_NAME} no devolvió un análisis válido. La respuesta estaba vacía o incompleta.")
            return "No se pudo generar el análisis del script."

        st.success("✅ ¡Análisis completo generado!")

        # --- Depuración (Mantener activo por si falla de nuevo) ---
        st.expander(f"Ver respuesta RAW de {HF_MODEL_NAME} (para depuración)").code(full_analysis_text)

        # --- PARSING Y PRESENTACIÓN (No cambia, el formato de salida se lo pedimos a la IA) ---
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

                score_match = re.search(r'Puntuación:\s*(\d+)%', content_raw, re.IGNORECASE)
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

        return ""

    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script con {HF_MODEL_NAME}: {e}. Por favor, revisa tu código.")
        st.markdown(f"**Análisis de {HF_MODEL_NAME} (Texto Crudo - Fallback por error en la app):**")
        st.code(full_analysis_text if full_analysis_text else f"No se pudo obtener el análisis de {HF_MODEL_NAME} debido a un error interno.")
        return f"Error al analizar script: {e}"
