import streamlit as st
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar funciones desde tus módulos
from generador_scripts import generar_script
from analizador_scripts import analizar_script

st.set_page_config(layout="wide", page_title="Generador de Scripts para Reels 🎬")

# --- Configuración de la API (Se mueve la carga de la clave al nivel de cada módulo) ---
# Asegúrate de que OPENAI_API_KEY esté configurada en los secretos de Streamlit Cloud
# o en tu archivo .env local.

st.title("Generador y Analizador de Scripts para Reels 🎬")
st.markdown("Crea y optimiza scripts virales para TikTok, Instagram y YouTube Shorts.")

# --- Entrada del Usuario ---
st.header("1. Creador de Scripts ✍️")
tema = st.text_input("💡 Tema de tu Reel:", help="Ej: Receta de arepas, trucos para estudiar, noticias de última hora de F1.")
objetivo = st.selectbox("🎯 Objetivo del Reel:", 
                        ["Captar la atención y educar", "Entretener y generar interacción", "Vender un producto/servicio", "Generar leads/suscripciones", "Viralizar un concepto"],
                        help="¿Qué quieres lograr con este Reel?")
estilo = st.selectbox("🎭 Estilo/Tono deseado:", 
                      ["Informativo y directo", "Humorístico y sarcástico", "Inspirador y motivacional", "Dramático y sensacionalista", "Curioso y misterioso"],
                      help="¿Cómo quieres que suene tu Reel?")
duracion = st.slider("⏱️ Duración aproximada (segundos):", 15, 90, 30, step=5, help="La duración ideal para un Reel.")

if st.button("✨ Generar Script"):
    if tema:
        with st.spinner("Generando tu script con IA... ¡Esto puede tomar unos segundos! 🤖"):
            script_generado = generar_script(tema, objetivo, estilo, duracion)
            if script_generado:
                st.subheader("📝 Script Generado:")
                st.write(script_generado)
                st.session_state['last_generated_script'] = script_generado
            else:
                st.error("No se pudo generar el script. Intenta de nuevo.")
    else:
        st.warning("Por favor, ingresa el tema del Reel para generar el script.")

# --- Analizador de Scripts ---
st.header("2. Analizador de Scripts 📊")
script_para_analizar = ""
if 'last_generated_script' in st.session_state and st.session_state['last_generated_script']:
    st.info("Script generado automáticamente cargado para análisis.")
    script_para_analizar = st.session_state['last_generated_script']
else:
    st.info("Pega tu script para analizarlo (o genera uno primero).")

script_completo_para_analizar = st.text_area("✍️ Pega el script completo aquí para analizar:", 
                                            value=script_para_analizar, height=300)

if st.button("🔬 Analizar Script"):
    if script_completo_para_analizar:
        with st.spinner("Analizando tu script con IA... ¡Casi listo! 🧠"):
            # La función analizar_script ahora renderiza directamente en Streamlit
            analisis_resultado = analizar_script(script_completo_para_analizar)
            if analisis_resultado: # Si hay un string de error, lo mostramos
                st.error(analisis_resultado)
            # Si la función retorna vacío, significa que ya renderizó el contenido
    else:
        st.warning("Por favor, pega un script o genera uno para analizar.")

st.markdown("---")
st.markdown("Desarrollado con ❤️ por tu asistente de Python.")
