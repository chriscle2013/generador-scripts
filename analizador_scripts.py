import google.generativeai as genai
import os
import streamlit as st
import re

# Configuración de la API y el modelo (mantener igual)
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
    Presenta los resultados de manera más gráfica y con sugerencias específicas.
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar con la IA."

    if model is None:
        st.error("⚠️ No se puede analizar el script: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return "Error: Modelo de IA para análisis no inicializado."

    # --- PROMPT (Mantenemos el prompt, ya que el contenido es bueno) ---
    prompt = f"""
    Eres un **analista de contenido de primer nivel para reels de redes sociales** (TikTok, Instagram, YouTube Shorts).
    Tu misión es realizar un análisis **profundo, dinámico y accionable** del siguiente script para un reel.
    Evalúa cada punto de forma crítica pero constructiva, y **siempre proporciona una sugerencia concreta o un ejemplo de cómo mejorar** si detectas una debilidad.

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir y presentar los siguientes puntos. Para los puntos con puntuación, genera un valor del 0 al 100%.

    **Formato de Salida ABSOLUTAMENTE OBLIGATORIO para el parsing:**
    Cada punto debe iniciar con su título numerado y en negritas.
    Si hay una puntuación, DEBE incluir la frase exacta "Puntuación: [X%]".
    Si hay una sugerencia, DEBE incluir la frase exacta "Sugerencia: [Sugerencia concreta o ejemplo]".

    **1. Tono y Estilo:**
    [Descripción del tono]. Puntuación: [X%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **2. Gancho (Hook):**
    [Efectividad del gancho]. Puntuación: [Y%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **3. Desarrollo del Contenido:**
    [Claridad y progresión del mensaje]. Puntuación: [Z%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **4. Llamada a la Acción (CTA - Call To Action):**
    [Claridad y persuasión de la CTA]. Puntuación: [W%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **5. Originalidad y Creatividad:**
    [Nivel de originalidad y frescura]. Puntuación: [A%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **6. Claridad y Concisión:**
    [Facilidad de comprensión y brevedad]. Puntuación: [B%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **7. Longitud y Ritmo:**
    [Adecuación para reel (30-60s) y flujo general].
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **8. Resumen General y Conclusión Final:**
    [Conclusión general y potencial. Mensaje motivador final].
    """

    st.info("✨ Enviando script a Gemini para un análisis *supercargado*...")
    try:
        response = model.generate_content(prompt)
        
        if not (response.candidates and response.candidates[0].content and response.candidates[0].content.parts):
            st.warning("😕 Gemini no devolvió un análisis válido. Parece que no hubo contenido o fue bloqueado. Intenta de nuevo.")
            return "No se pudo generar el análisis del script."

        full_analysis_text = "".join([part.text for part in response.candidates[0].content.parts])
        
        st.success("✅ ¡Análisis completo generado!")

        # --- Depuración TEMPORAL (Mantener activo por si falla de nuevo) ---
        st.expander("Ver respuesta RAW de Gemini (para depuración)").code(full_analysis_text)
        
        # --- PARSING MÁS ROBUSTO CON re.finditer ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")
        
        # Patrón para identificar los títulos de sección.
        # Captura el título completo (ej. "1. Tono y Estilo") y también el texto hasta la siguiente sección.
        # re.DOTALL permite que '.' coincida con saltos de línea
        section_regex = re.compile(
            r"^\s*\*\*(?P<title>\d+\.\s*[^:]+)\*\*[:\s]*(?P<content>.*?)(?=\s*\*\*(\d+\.\s*)|$)",
            re.MULTILINE | re.DOTALL
        )
        
        parsed_data = {}
        for match in section_regex.finditer(full_analysis_text):
            title = match.group('title').strip()
            content = match.group('content').strip()
            parsed_data[title] = content

        # Definir el orden deseado para las secciones
        ordered_section_titles = [
            "1. Tono y Estilo",
            "2. Gancho (Hook)",
            "3. Desarrollo del Contenido",
            "4. Llamada a la Acción (CTA)",
            "5. Originalidad y Creatividad",
            "6. Claridad y Concisión",
            "7. Longitud y Ritmo",
            "8. Resumen General y Conclusión Final"
        ]

        # Iterar a través de los títulos en el orden deseado para la presentación
        for full_title_in_order in ordered_section_titles:
            content_raw = parsed_data.get(full_title_in_order)
            
            if content_raw:
                # Limpiar el título para la presentación
                display_title = full_title_in_order.split('.', 1)[1].strip() # Quita el número y el primer punto

                score = None
                description_text = content_raw
                suggestion_text = ""

                # --- Extracción de Puntuación ---
                score_match = re.search(r'Puntuación:\s*(\d+)%', content_raw, re.IGNORECASE)
                if score_match:
                    score = int(score_match.group(1))
                    # La descripción es lo que está antes de "Puntuación:"
                    description_text = content_raw.split(score_match.group(0))[0].strip()
                
                # --- Extracción de Sugerencia ---
                # Usar re.DOTALL para que '.' coincida con saltos de línea si la sugerencia es multi-línea
                suggestion_match = re.search(r'Sugerencia:\s*(.*)', content_raw, re.DOTALL | re.IGNORECASE)
                if suggestion_match:
                    suggestion_text = suggestion_match.group(1).strip()
                    # Si la sugerencia fue encontrada, la quitamos de la descripción
                    description_text = description_text.split('Sugerencia:')[0].strip()

                # --- PRESENTACIÓN EN STREAMLIT ---
                if "Puntuación" in full_title_in_order: # Para secciones que deben tener métrica y progreso
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.metric(display_title, f"{score}%" if score is not None else "N/A")
                    with col2:
                        st.markdown(f"**{display_title}:** {description_text}")
                        if score is not None:
                            st.progress(score)
                        if suggestion_text:
                            st.info(f"💡 Sugerencia: {suggestion_text}")
                
                elif display_title == "Longitud y Ritmo": # Sección especial sin % pero con sugerencia
                    st.markdown(f"**{display_title}:** {description_text}")
                    if suggestion_text:
                        st.info(f"💡 Sugerencia: {suggestion_text}")
                
                elif display_title == "Resumen General y Conclusión Final": # Sección final
                    st.markdown(f"### {display_title}")
                    st.markdown(description_text) 

                st.markdown("---") # Separador entre cada sección de análisis
            else:
                # Esto es si una sección esperada no se encuentra en el texto de Gemini
                # Puede ocurrir si Gemini omite una sección o cambia mucho el formato.
                # Lo mostramos como una advertencia silenciosa o para depuración.
                # st.warning(f"No se encontró la sección: {full_title_in_order}")
                pass # No hacer nada si no se encuentra, para evitar un output "ruidoso"

        return "" # Ya mostramos todo directamente en Streamlit

    except Exception as e:
        # Aquí capturamos cualquier error durante el parsing o la presentación
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script: {e}. Por favor, revisa tu código.")
        st.markdown("**Análisis de Gemini (Texto Crudo - Fallback por error en la app):**")
        st.code(full_analysis_text)
        return f"Error al analizar script: {e}"
