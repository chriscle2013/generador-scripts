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

    # --- PROMPT MEJORADO PARA MAYOR ROBUSTEZ EN EL FORMATO ---
    prompt = f"""
    Eres un **analista de contenido de primer nivel para reels de redes sociales** (TikTok, Instagram, YouTube Shorts).
    Tu misión es realizar un análisis **profundo, dinámico y accionable** del siguiente script para un reel.
    Evalúa cada punto de forma crítica pero constructiva, y **siempre proporciona una sugerencia concreta o un ejemplo de cómo mejorar** si detectas una debilidad.

    --- SCRIPT A ANALIZAR ---
    {script_texto}
    --- FIN SCRIPT ---

    El análisis debe cubrir y presentar los siguientes puntos. Para los puntos con puntuación, genera un valor del 0 al 100%.

    **Formato de Salida Obligatorio:**
    Cada punto debe iniciar con su título en negritas y terminar con la puntuación (si aplica) de esta forma: `Puntuación: [X%]`. Las sugerencias deben ser claras.

    **1. Tono y Estilo (0-100%):**
    Descripción del tono. Puntuación: [X%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **2. Gancho (Hook) (0-100%):**
    Efectividad del gancho. Puntuación: [Y%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **3. Desarrollo del Contenido (0-100%):**
    Claridad y progresión del mensaje. Puntuación: [Z%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **4. Llamada a la Acción (CTA - Call To Action) (0-100%):**
    Claridad y persuasión de la CTA. Puntuación: [W%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **5. Originalidad y Creatividad (0-100%):**
    Nivel de originalidad y frescura. Puntuación: [A%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **6. Claridad y Concisión (0-100%):**
    Facilidad de comprensión y brevedad. Puntuación: [B%]
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **7. Longitud y Ritmo (Evaluación General):**
    Adecuación para reel (30-60s) y flujo general.
    Sugerencia: [Sugerencia específica de mejora o un ejemplo].

    **8. Resumen General y Conclusión Final:**
    Conclusión general y potencial. Termina con un mensaje motivador.
    """

    st.info("✨ Enviando script a Gemini para un análisis *supercargado*...")
    try:
        response = model.generate_content(prompt)
        
        if not (response.candidates and response.candidates[0].content and response.candidates[0].content.parts):
            st.warning("😕 Gemini no devolvió un análisis válido. Parece que no hubo contenido o fue bloqueado. Intenta de nuevo.")
            return "No se pudo generar el análisis del script."

        full_analysis_text = "".join([part.text for part in response.candidates[0].content.parts])
        
        st.success("✅ ¡Análisis completo generado!")

        # --- Depuración: Mostrar el texto crudo de la IA para entender el formato ---
        # Si la interfaz sigue sin mostrar nada, descomenta la siguiente línea para ver qué devuelve Gemini
        # st.code(full_analysis_text) 
        
        # --- PARSING MÁS ROBUSTO Y PRESENTACIÓN ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")
        
        # Usaremos expresiones regulares para dividir el texto por los títulos principales
        # y para extraer la puntuación y la sugerencia de cada bloque.
        
        # Patrón para identificar cada sección principal (títulos en negritas)
        # Adaptado para que coincida con el formato exacto del prompt
        section_pattern = re.compile(
            r"^\*\*(1\.\sTono y Estilo|2\.\sGancho \(Hook\)|3\.\sDesarrollo del Contenido|"
            r"4\.\sLlamada a la Acción \(CTA\)|5\.\sOriginalidad y Creatividad|"
            r"6\.\sClaridad y Concisión|7\.\sLongitud y Ritmo|8\.\sResumen General y Conclusión Final)\*\*[:\s]*"
        )
        
        # Dividir el texto por los títulos de las secciones
        sections = section_pattern.split(full_analysis_text)
        
        # El primer elemento de 'sections' será vacío o un preámbulo,
        # luego los pares (título, contenido)
        
        # Si hay un preámbulo antes del primer título, lo ignoramos
        # o lo mostramos como un mensaje general si es relevante.
        # Por simplicidad, asumiremos que los títulos de sección están al inicio.
        
        # Iterar sobre las secciones procesadas
        # Saltar el primer elemento vacío (si existe) y procesar en pares (título, contenido)
        i = 1 # Empezamos desde el primer título
        while i < len(sections):
            title_raw = sections[i]
            content_raw = sections[i+1].strip() if i+1 < len(sections) else ""
            i += 2

            # Limpiar el título para la presentación (quitar número y estrellas)
            display_title = title_raw.replace('**', '').replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('7. ', '').replace('8. ', '').strip()
            
            # --- Extraer puntuación y sugerencia para las secciones métricas ---
            score = None
            description = content_raw
            suggestion = ""

            score_match = re.search(r'Puntuación:\s*(\d+)%', content_raw)
            if score_match:
                score = int(score_match.group(1))
                # La descripción es lo que está antes de "Puntuación:"
                description = content_raw.split(score_match.group(0))[0].strip()
            
            suggestion_match = re.search(r'Sugerencia:\s*(.*)', content_raw, re.DOTALL)
            if suggestion_match:
                suggestion = suggestion_match.group(1).strip()
                # Quitar la sugerencia de la descripción si fue parte de ella
                description = description.split('Sugerencia:')[0].strip()
            
            # --- Presentación en Streamlit ---
            if display_title in ["Tono y Estilo", "Gancho (Hook)", "Desarrollo del Contenido",
                                 "Llamada a la Acción (CTA)", "Originalidad y Creatividad",
                                 "Claridad y Concisión"]:
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.metric(display_title, f"{score}%" if score is not None else "N/A")
                with col2:
                    st.markdown(f"**{display_title}:** {description}")
                    if score is not None:
                        st.progress(score)
                    if suggestion:
                        st.info(f"💡 Sugerencia: {suggestion}")
            
            elif display_title == "Longitud y Ritmo":
                st.markdown(f"**{display_title}:** {description}")
                if suggestion:
                    st.info(f"💡 Sugerencia: {suggestion}")
            
            elif display_title == "Resumen General y Conclusión Final":
                st.markdown(f"### {display_title}")
                st.markdown(description) # La descripción aquí es el resumen completo

            st.markdown("---") # Separador entre cada sección de análisis

        return "" # No devolvemos el texto plano, lo mostramos directamente

    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script: {e}. Por favor, revisa tu clave API y los logs de Streamlit Cloud.")
        # También puedes imprimir el texto crudo del análisis aquí para depuración
        # st.code(full_analysis_text)
        return f"Error al analizar script: {e}"
