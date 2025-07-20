import google.generativeai as genai
import os
import streamlit as st
import re # Importar para usar expresiones regulares

# Configuración de la API y el modelo (se mantiene igual, es crucial que funcione)
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
    Presenta los resultados de manera más gráfica.
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar con la IA."

    if model is None:
        st.error("No se puede analizar el script: Modelo de IA no inicializado. Revisa tu clave API y logs.")
        return "Error: Modelo de IA para análisis no inicializado."

    prompt = f"""
    Eres un experto analista de contenido para reels de redes sociales (TikTok, Instagram, YouTube Shorts).
    Tu tarea es analizar el siguiente script para un reel y proporcionar un feedback detallado.
    Evalúa los siguientes puntos y sé constructivo en tus sugerencias.

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir:
    1.  **Tono y Estilo:** Evalúa el tono general del script (ej. inspirador, humorístico, informativo, etc.). Asigna una puntuación del 0 al 100% sobre lo bien que el tono general se adapta al objetivo probable de un reel (ser atractivo y dinámico).
    2.  **Gancho (Hook):** Evalúa la efectividad del inicio del script para captar la atención en los primeros segundos. Asigna una puntuación del 0 al 100% sobre la fortaleza del hook.
    3.  **Desarrollo del Contenido:** Evalúa cómo fluye el mensaje. ¿Es claro, conciso y hay una progresión lógica? Asigna una puntuación del 0 al 100% a la claridad y fluidez.
    4.  **Llamada a la Acción (CTA - Call To Action):** Evalúa si la CTA final es clara y persuasiva. Asigna una puntuación del 0 al 100% a la efectividad de la CTA.
    5.  **Longitud y Ritmo:** ¿Es apropiado para un reel corto (30-60 segundos)? Evalúa del 0 al 100% su adecuación.

    Presenta tu análisis en el siguiente formato estructurado. Cada punto principal debe estar en una nueva línea y seguido de la descripción y la puntuación si aplica. Utiliza 'Puntuación:' para los porcentajes.
    
    Tono y Estilo: [Descripción del tono]. Puntuación: [X%]
    Gancho (Hook): [Descripción del hook]. Puntuación: [Y%]
    Desarrollo del Contenido: [Descripción del desarrollo]. Puntuación: [Z%]
    Llamada a la Acción (CTA): [Descripción de la CTA]. Puntuación: [W%]
    Longitud y Ritmo: [Descripción de longitud]. Puntuación: [V%]
    Sugerencias Generales: [Aquí van recomendaciones adicionales].
    """

    st.info("Enviando script a Gemini para un análisis detallado...")
    try:
        response = model.generate_content(prompt)
        
        if not (response.candidates and response.candidates[0].content and response.candidates[0].content.parts):
            st.warning("Gemini no devolvió un análisis válido. Intenta de nuevo.")
            return "No se pudo generar el análisis del script."

        full_analysis_text = "".join([part.text for part in response.candidates[0].content.parts])
        
        st.success("¡Análisis generado!")

        # Extraer puntos y puntuaciones usando regex o splitting
        lines = full_analysis_text.split('\n')
        
        # Diccionario para almacenar los resultados parseados
        parsed_results = {
            "Tono y Estilo": {"desc": "", "score": None},
            "Gancho (Hook)": {"desc": "", "score": None},
            "Desarrollo del Contenido": {"desc": "", "score": None},
            "Llamada a la Acción (CTA)": {"desc": "", "score": None},
            "Longitud y Ritmo": {"desc": "", "score": None},
            "Sugerencias Generales": ""
        }

        current_key = None
        for line in lines:
            if line.startswith("Tono y Estilo:"):
                current_key = "Tono y Estilo"
            elif line.startswith("Gancho (Hook):"):
                current_key = "Gancho (Hook)"
            elif line.startswith("Desarrollo del Contenido:"):
                current_key = "Desarrollo del Contenido"
            elif line.startswith("Llamada a la Acción (CTA):"):
                current_key = "Llamada a la Acción (CTA)"
            elif line.startswith("Longitud y Ritmo:"):
                current_key = "Longitud y Ritmo"
            elif line.startswith("Sugerencias Generales:"):
                current_key = "Sugerencias Generales"
            
            if current_key:
                # Extraer descripción y puntuación
                match = re.search(r'Puntuación: (\d+%)', line)
                if match:
                    score_str = match.group(1).replace('%', '')
                    parsed_results[current_key]["score"] = int(score_str)
                    # La descripción es todo lo demás antes de "Puntuación:"
                    parsed_results[current_key]["desc"] = line.split("Puntuación:")[0].replace(f"{current_key}:", "").strip()
                else:
                    # Si no hay puntuación (para Sugerencias Generales o si IA falla el formato)
                    if current_key == "Sugerencias Generales":
                        parsed_results[current_key] += line.replace(f"{current_key}:", "").strip() + "\n"
                    else:
                        parsed_results[current_key]["desc"] = line.replace(f"{current_key}:", "").strip()

        # --- Presentación Gráfica en Streamlit ---
        st.subheader("📊 Análisis Detallado del Script")
        
        # Tono y Estilo
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Tono", f"{parsed_results['Tono y Estilo']['score']}%" if parsed_results['Tono y Estilo']['score'] is not None else "N/A")
        with col2:
            st.markdown(f"**Tono y Estilo:** {parsed_results['Tono y Estilo']['desc']}")
            if parsed_results['Tono y Estilo']['score'] is not None:
                st.progress(parsed_results['Tono y Estilo']['score'])

        st.markdown("---")

        # Gancho (Hook)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Hook", f"{parsed_results['Gancho (Hook)']['score']}%" if parsed_results['Gancho (Hook)']['score'] is not None else "N/A")
        with col2:
            st.markdown(f"**Gancho (Hook):** {parsed_results['Gancho (Hook)']['desc']}")
            if parsed_results['Gancho (Hook)']['score'] is not None:
                st.progress(parsed_results['Gancho (Hook)']['score'])
        
        st.markdown("---")

        # Desarrollo del Contenido
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Desarrollo", f"{parsed_results['Desarrollo del Contenido']['score']}%" if parsed_results['Desarrollo del Contenido']['score'] is not None else "N/A")
        with col2:
            st.markdown(f"**Desarrollo del Contenido:** {parsed_results['Desarrollo del Contenido']['desc']}")
            if parsed_results['Desarrollo del Contenido']['score'] is not None:
                st.progress(parsed_results['Desarrollo del Contenido']['score'])

        st.markdown("---")
        
        # Llamada a la Acción (CTA)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("CTA", f"{parsed_results['Llamada a la Acción (CTA)']['score']}%" if parsed_results['Llamada a la Acción (CTA)']['score'] is not None else "N/A")
        with col2:
            st.markdown(f"**Llamada a la Acción (CTA):** {parsed_results['Llamada a la Acción (CTA)']['desc']}")
            if parsed_results['Llamada a la Acción (CTA)']['score'] is not None:
                st.progress(parsed_results['Llamada a la Acción (CTA)']['score'])

        st.markdown("---")

        # Longitud y Ritmo
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Longitud", f"{parsed_results['Longitud y Ritmo']['score']}%" if parsed_results['Longitud y Ritmo']['score'] is not None else "N/A")
        with col2:
            st.markdown(f"**Longitud y Ritmo:** {parsed_results['Longitud y Ritmo']['desc']}")
            if parsed_results['Longitud y Ritmo']['score'] is not None:
                st.progress(parsed_results['Longitud y Ritmo']['score'])

        st.markdown("---")

        # Sugerencias Generales en un expander
        with st.expander("💡 Sugerencias Generales para Mejorar"):
            st.markdown(parsed_results["Sugerencias Generales"])

        return "" # No devolvemos el texto plano, lo mostramos directamente

    except Exception as e:
        st.error(f"Error al conectar con la IA para análisis de script: {e}. Revisa tu clave API y límites de uso.")
        return f"Error al analizar script: {e}"
