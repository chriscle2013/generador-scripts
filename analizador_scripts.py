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

    # --- PROMPT MEJORADO PARA MAYOR ROBUSTEZ EN EL FORMATO ---
    # Se insiste en el formato, pero el parsing será más indulgente.
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

        # --- Depuración TEMPORAL: Mostrar el texto crudo de la IA ---
        # Si las gráficas no aparecen, DESCOMENTA esta línea para ver el texto exacto que Gemini devuelve.
        # st.expander("Ver respuesta RAW de Gemini (para depuración)").code(full_analysis_text)
        
        # --- PARSING MÁS ROBUSTO Y PRESENTACIÓN ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")
        
        # Patrón para identificar cada sección principal (títulos en negritas)
        # Hacemos el patrón más flexible para capturar el título incluso sin los dos puntos
        section_pattern = re.compile(
            r"^\s*\*\*(1\.\s*Tono y Estilo|2\.\s*Gancho \(Hook\)|3\.\s*Desarrollo del Contenido|"
            r"4\.\s*Llamada a la Acción \(CTA\)|5\.\s*Originalidad y Creatividad|"
            r"6\.\s*Claridad y Concisión|7\.\s*Longitud y Ritmo|8\.\s*Resumen General y Conclusión Final)\*\*[:.\s]*", 
            re.MULTILINE
        )
        
        # Dividir el texto por los títulos de las secciones. Usamos un patrón que captura el delimitador.
        parts = section_pattern.split(full_analysis_text)
        
        # El primer elemento de 'parts' será el texto antes del primer título.
        # Luego, los elementos alternarán entre el título capturado y el contenido de la sección.
        
        sections_data = {}
        current_title = None

        # Iterar sobre las partes y reconstruir las secciones
        # La primera parte (parts[0]) es el preámbulo o vacía, la ignoramos para las secciones
        for i in range(1, len(parts)):
            if i % 2 == 1: # Es un título
                current_title = parts[i].strip()
                sections_data[current_title] = ""
            else: # Es el contenido de la sección
                if current_title:
                    sections_data[current_title] = parts[i].strip()

        ordered_keys_raw = [
            "1. Tono y Estilo",
            "2. Gancho (Hook)",
            "3. Desarrollo del Contenido",
            "4. Llamada a la Acción (CTA)",
            "5. Originalidad y Creatividad",
            "6. Claridad y Concisión",
            "7. Longitud y Ritmo",
            "8. Resumen General y Conclusión Final"
        ]

        for key_prefix_raw in ordered_keys_raw:
            # Encontrar la clave exacta que está en sections_data (puede incluir o no los dos puntos al final si Gemini los pone)
            # Normalizamos para la búsqueda
            normalized_key_prefix = key_prefix_raw.replace('**', '').strip()

            found_key = None
            for stored_key in sections_data.keys():
                # Comparamos la parte inicial de la clave almacenada con la clave esperada
                if stored_key.strip().startswith(normalized_key_prefix):
                    found_key = stored_key
                    break
            
            if found_key and sections_data[found_key]:
                content_raw = sections_data[found_key]
                
                # Limpiar el título para la presentación (quitar número y estrellas)
                display_title = normalized_key_prefix.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('7. ', '').replace('8. ', '').strip()
                
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
                suggestion_match = re.search(r'Sugerencia:\s*(.*)', content_raw, re.DOTALL | re.IGNORECASE)
                if suggestion_match:
                    suggestion_text = suggestion_match.group(1).strip()
                    # Si la sugerencia fue encontrada, la quitamos de la descripción
                    description_text = description_text.split('Sugerencia:')[0].strip()

                # --- PRESENTACIÓN EN STREAMLIT ---
                if display_title in ["Tono y Estilo", "Gancho (Hook)", "Desarrollo del Contenido",
                                     "Llamada a la Acción (CTA)", "Originalidad y Creatividad",
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
                
                # Secciones sin puntuación específica pero con posible sugerencia
                elif display_title == "Longitud y Ritmo":
                    st.markdown(f"**{display_title}:** {description_text}")
                    if suggestion_text:
                        st.info(f"💡 Sugerencia: {suggestion_text}")
                
                # Resumen General (normalmente sin puntuación ni sugerencia en formato separado)
                elif display_title == "Resumen General y Conclusión Final":
                    st.markdown(f"### {display_title}")
                    st.markdown(description_text) # La descripción aquí es el resumen completo

                st.markdown("---") # Separador entre cada sección de análisis

            else:
                # Fallback si una sección esperada no se encuentra o está vacía después del parsing
                st.markdown(f"**⚠️ No se pudo extraer la sección '{display_title}'.**")
                # Opcional: st.code(sections_data.get(found_key, "Contenido no encontrado"))
                st.markdown("---")

        return "" # No devolvemos el texto plano, lo mostramos directamente

    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script: {e}. Por favor, revisa tu clave API y los logs de Streamlit Cloud.")
        # Muestra el texto completo de Gemini como fallback en caso de error de parsing grave
        st.markdown("**Análisis de Gemini (Texto Crudo - Fallback por error de parsing):**")
        st.code(full_analysis_text)
        return f"Error al analizar script: {e}"
