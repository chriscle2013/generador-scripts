import openai
import os
import streamlit as st
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Configuración de la API de OpenAI ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("Error: OPENAI_API_KEY no encontrada. Por favor, configúrala en los secretos de Streamlit o en tu archivo .env.")
    openai.api_key = None
else:
    openai.api_key = OPENAI_API_KEY

def analizar_script(script_texto):
    """
    Realiza un análisis avanzado de un script usando la API de OpenAI (GPT-3.5 Turbo).
    Presenta los resultados de manera más gráfica y con sugerencias específicas.
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar con la IA."

    if not openai.api_key:
        return "API Key de OpenAI no configurada. No se puede analizar el script."

    # Inicializar full_analysis_text antes del try, para que siempre esté definida
    full_analysis_text = "" 
    
    # --- PROMPT para GPT-3.5 Turbo ---
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

    st.info("✨ Enviando script a OpenAI para un análisis *supercargado*...")
    try:
        # --- Llamada a la API de OpenAI ---
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Puedes probar con "gpt-4o" si tienes acceso y más cuota
            messages=[
                {"role": "system", "content": "Eres un analista de contenido de primer nivel para reels de redes sociales."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=800, # Ajusta para que el análisis sea lo suficientemente largo
            temperature=0.7,
        )
        
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            full_analysis_text = response.choices[0].message.content
        else:
            st.warning("😕 OpenAI no devolvió un análisis válido. La respuesta estaba vacía o incompleta.")
            return "No se pudo generar el análisis del script."

        st.success("✅ ¡Análisis completo generado!")

        # --- Depuración TEMPORAL (Mantener activo por si falla de nuevo) ---
        st.expander("Ver respuesta RAW de OpenAI (para depuración)").code(full_analysis_text)
        
        # --- PARSING MÁS ROBUSTO Y PRESENTACIÓN ---
        st.subheader("🚀 Análisis Detallado y Accionable de tu Script")
        st.markdown("---")
        
        # Patrón para identificar los títulos de sección (sin negritas, como lo pide el prompt)
        section_regex = re.compile(
            r"^\s*(?P<title>\d+\.\s*[^:]+):\s*(?P<content>.*?)(?=\s*\d+\.\s*[^:]+:|$)",
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
            "4. Llamada a la Acción (CTA - Call To Action)",
            "5. Originalidad y Creatividad",
            "6. Claridad y Concisión",
            "7. Longitud y Ritmo",
            "8. Resumen General y Conclusión Final"
        ]

        # Iterar a través de los títulos en el orden deseado para la presentación
        for full_title_in_order in ordered_section_titles:
            content_raw = parsed_data.get(full_title_in_order, "")
            
            if content_raw: 
                display_title = re.sub(r'^\d+\.\s*', '', full_title_in_order).strip()

                score = None
                description_text = content_raw
                suggestion_text = ""

                # --- Extracción de Puntuación ---
                score_match = re.search(r'Puntuación:\s*(\d+)%', content_raw, re.IGNORECASE)
                if score_match:
                    score = int(score_match.group(1))
                    description_text = content_raw.split(score_match.group(0))[0].strip()
                
                # --- Extracción de Sugerencia ---
                suggestion_match = re.search(r'Sugerencia:\s*(.*)', content_raw, re.DOTALL | re.IGNORECASE)
                if suggestion_match:
                    suggestion_text = suggestion_match.group(1).strip()
                    description_text = description_text.split('Sugerencia:')[0].strip()

                # --- PRESENTACIÓN EN STREAMLIT ---
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

    except openai.APIConnectionError as e:
        st.error(f"Error de conexión con la API de OpenAI: {e}")
        st.markdown("**Análisis de OpenAI (Texto Crudo - Fallback por error de conexión):**")
        st.code("No se pudo conectar con la API de OpenAI. Revisa tu conexión a internet o el estado del servicio.")
        return f"Error de conexión: {e}"
    except openai.RateLimitError as e:
        st.error(f"Error de límite de cuota de OpenAI: {e}. Has excedido tu cuota gratuita o tu límite de solicitudes. Por favor, espera o revisa tu plan.")
        st.markdown("**Análisis de OpenAI (Texto Crudo - Fallback por error de cuota):**")
        st.code("Cuota de API excedida. Por favor, espera o contacta al administrador.")
        return f"Error de cuota: {e}"
    except openai.APIStatusError as e:
        st.error(f"Error de la API de OpenAI (código {e.status_code}): {e.response}")
        st.markdown("**Análisis de OpenAI (Texto Crudo - Fallback por error de estado de API):**")
        st.code(f"Error de API: {e.response}")
        return f"Error de API: {e.response}"
    except Exception as e:
        st.error(f"❌ ¡Ups! Ha ocurrido un error inesperado al analizar el script: {e}. Por favor, revisa tu código.")
        st.markdown("**Análisis de OpenAI (Texto Crudo - Fallback por error en la app):**")
        st.code(full_analysis_text if full_analysis_text else "No se pudo obtener el análisis de OpenAI debido a un error interno.")
        return f"Error al analizar script: {e}"
