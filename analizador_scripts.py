import google.generativeai as genai
import os
import streamlit as st
import re

# Configuración de la API y el modelo (se mantiene igual)
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

    prompt = f"""
    Eres un **analista de contenido de primer nivel para reels de redes sociales** (TikTok, Instagram, YouTube Shorts).
    Tu misión es realizar un análisis **profundo, dinámico y accionable** del siguiente script para un reel.
    Evalúa cada punto de forma crítica pero constructiva, y **siempre proporciona una sugerencia concreta o un ejemplo de cómo mejorar** si detectas una debilidad.

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir y presentar los siguientes puntos. Para los puntos con puntuación, genera un valor del 0 al 100%.

    1.  **Tono y Estilo (0-100%):**
        * Describe el tono general del script (ej. inspirador, humorístico, informativo, dramático).
        * Evalúa lo bien que este tono se adapta al objetivo de un reel (ser atractivo, dinámico, memorable).
        * **Puntuación:** [X%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    2.  **Gancho (Hook) (0-100%):**
        * Evalúa la efectividad del inicio del script para captar la atención en los primeros 3-5 segundos.
        * ¿Genera curiosidad, emoción, o resuelve un problema inicial?
        * **Puntuación:** [Y%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    3.  **Desarrollo del Contenido (0-100%):**
        * ¿Fluye bien el mensaje principal? ¿Es claro, conciso y hay una progresión lógica de la idea?
        * ¿Se mantiene el interés a lo largo del script?
        * **Puntuación:** [Z%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    4.  **Llamada a la Acción (CTA - Call To Action) (0-100%):**
        * ¿Es la CTA final clara, persuasiva y fácil de entender para el espectador qué debe hacer a continuación?
        * ¿Es única o inspiradora?
        * **Puntuación:** [W%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    5.  **Originalidad y Creatividad (0-100%):**
        * ¿El script ofrece una perspectiva única o un enfoque creativo?
        * ¿Se destaca de lo común?
        * **Puntuación:** [A%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    6.  **Claridad y Concisión (0-100%):**
        * ¿El mensaje es directo y fácil de comprender?
        * ¿Se eliminaron las palabras innecesarias y el script es breve para la duración del reel?
        * **Puntuación:** [B%]
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    7.  **Longitud y Ritmo (Evaluación General):**
        * ¿Es apropiado para un reel corto (30-60 segundos)?
        * ¿Sugiere algún ajuste de ritmo (ej. más rápido, pausas)?
        * **Sugerencia:** [Sugerencia específica de mejora o un ejemplo].

    8.  **Resumen General y Conclusión Final:**
        * Ofrece una conclusión general sobre la fortaleza del script y su potencial.
        * Termina con un mensaje motivador.

    Presenta tu análisis de manera atractiva usando Markdown para encabezados, negritas y listas.
    """

    st.info("✨ Enviando script a Gemini para un análisis *supercargado*...")
    try:
        response = model.generate_content(prompt)
        
        if not (response.candidates and response.candidates[0].content and response.candidates[0].content.parts):
            st.warning("😕 Gemini no devolvió un análisis válido. Parece que no hubo contenido o fue bloqueado. Intenta de nuevo.")
            return "No se pudo generar el análisis del script."

        full_analysis_text = "".join([part.text for part in response.candidates[0].content.parts])
        
        st.success("✅ ¡Análisis completo generado!")

        # --- Parsear la respuesta para una presentación estructurada ---
        # Este parsing se vuelve más complejo porque la IA puede variar el formato levemente.
        # Intentaremos extraer cada sección con sus subtítulos de forma robusta.
        
        # Diccionario para almacenar los resultados parseados
        # Guardaremos el texto completo de cada sección para luego formatearlo en Streamlit
        parsed_sections = {}
        current_section_title = None
        
        # Usamos expresiones regulares para identificar los títulos de sección y las puntuaciones
        section_titles_regex = re.compile(
            r"^(1\.\s*\*Tono y Estilo\*\*|2\.\s*\*Gancho \(Hook\)\*\*|3\.\s*\*Desarrollo del Contenido\*\*|"
            r"4\.\s*\*Llamada a la Acción \(CTA\)\*\*|5\.\s*\*Originalidad y Creatividad\*\*|"
            r"6\.\s*\*Claridad y Concisión\*\*|7\.\s*\*Longitud y Ritmo\*\*|"
            r"8\.\s*\*Resumen General y Conclusión Final\*\*:?)"
        )

        lines = full_analysis_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line: # Ignorar líneas vacías
                continue

            match_title = section_titles_regex.match(line)
            if match_title:
                current_section_title = match_title.group(0).replace('*', '') # Quitar negritas para la clave
                parsed_sections[current_section_title] = []
            
            if current_section_title:
                parsed_sections[current_section_title].append(line)

        # --- Presentación Gráfica en Streamlit ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")
        
        # Iterar a través de las secciones y mostrarlas
        ordered_keys = [
            "1. Tono y Estilo",
            "2. Gancho (Hook)",
            "3. Desarrollo del Contenido",
            "4. Llamada a la Acción (CTA)",
            "5. Originalidad y Creatividad",
            "6. Claridad y Concisión",
            "7. Longitud y Ritmo",
            "8. Resumen General y Conclusión Final"
        ]

        for key_prefix in ordered_keys:
            # Encontrar la clave exacta que usó la IA (puede incluir un ':')
            full_key = next((k for k in parsed_sections if k.startswith(key_prefix)), None)
            
            if full_key and parsed_sections[full_key]:
                section_content_lines = parsed_sections[full_key]
                
                # Intentar extraer puntuación y descripción para métricas
                score = None
                description = []
                suggestion = []

                # Secciones con puntuación
                if key_prefix in ["1. Tono y Estilo", "2. Gancho (Hook)", "3. Desarrollo del Contenido",
                                  "4. Llamada a la Acción (CTA)", "5. Originalidad y Creatividad",
                                  "6. Claridad y Concisión"]:
                    
                    # El primer elemento de la lista debe contener la puntuación y la descripción principal
                    main_line = section_content_lines[0]
                    score_match = re.search(r'Puntuación: (\d+%)', main_line)
                    if score_match:
                        score_str = score_match.group(1).replace('%', '')
                        score = int(score_str)
                        description_part = main_line.replace(f"{score_match.group(0)}", "").replace(f"{key_prefix}:", "").strip()
                        if description_part:
                            description.append(description_part)
                    else:
                        # Si no hay puntuación en la primera línea, es la descripción
                        description.append(main_line.replace(f"{key_prefix}:", "").strip())
                    
                    # El resto de las líneas pueden ser la sugerencia
                    for line_idx in range(1, len(section_content_lines)):
                        line_content = section_content_lines[line_idx].replace('**Sugerencia:**', '').strip()
                        if line_content:
                            suggestion.append(line_content)
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.metric(key_prefix.replace('. ', '. ')[3:], f"{score}%" if score is not None else "N/A")
                    with col2:
                        st.markdown(f"**{key_prefix.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '')}:** {' '.join(description)}")
                        if score is not None:
                            st.progress(score)
                        if suggestion:
                            st.info(f"💡 Sugerencia: {' '.join(suggestion)}")
                
                # Secciones sin puntuación (como Longitud y Ritmo, Resumen General)
                else:
                    st.markdown(f"### {key_prefix}")
                    # Unimos todas las líneas de la sección y las mostramos
                    section_text = "\n".join(section_content_lines).replace(f"{key_prefix}:", "").strip()
                    st.markdown(section_text)
                
                st.markdown("---") # Separador entre cada sección de análisis

        return "" # No devolvemos el texto plano, lo mostramos directamente en Streamlit

    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script: {e}. Por favor, revisa tu clave API y los logs de Streamlit Cloud.")
        return f"Error al analizar script: {e}"
