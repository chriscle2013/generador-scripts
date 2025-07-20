# app.py (No necesita muchos cambios si ya está adaptado a Streamlit)

import streamlit as st
# Asegúrate de que las importaciones estén aquí
from generadores import generar_script_reel, generar_copy_hooks
from analizador_scripts import analizar_script

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Generador de Contenido para Reels",
    page_icon="🎬",
    layout="centered"
)

# --- Título Principal ---
st.title("🎬 Generador de Contenido para Reels y Redes Sociales")
st.markdown("Crea scripts, copys y hooks para TikTok, Instagram y YouTube.")

# --- Selección de Nicho Global ---
nichos = ["Inteligencia Artificial", "Formula 1", "Marketing Digital", "Mindset", "Mascotas"]
if 'nicho_seleccionado' not in st.session_state:
    st.session_state.nicho_seleccionado = nichos[0]

st.session_state.nicho_seleccionado = st.selectbox(
    "Selecciona el Nicho para tu Contenido",
    options=nichos,
    index=nichos.index(st.session_state.nicho_seleccionado),
    help="Elige el tema principal para tu contenido."
)

st.sidebar.title("Navegación")
opcion_seleccionada = st.sidebar.radio(
    "Ir a:",
    ("Generador de Scripts", "Generador de Copys y Hooks", "Analizador de Scripts")
)

# --- Contenido Principal Basado en la Opción Seleccionada ---

if opcion_seleccionada == "Generador de Scripts":
    st.header(f"✍️ Generador de Scripts para Reels - **{st.session_state.nicho_seleccionado}**")
    st.write("Genera ideas y estructuras para tus videos de reels.")

    if st.button("Generar Script"):
        with st.spinner('Generando script...'):
            script = generar_script_reel(st.session_state.nicho_seleccionado) # Corrección ya aplicada
            st.subheader("Script Generado:")
            # Usar st.markdown para mostrar el script generado por la IA
            # Ya que la respuesta puede venir en un formato más libre
            for linea in script: # Iterar sobre las líneas de la respuesta de la IA
                st.markdown(linea) # Mostrar cada línea como markdown

            st.markdown("---")

            st.subheader("Análisis Rápido del Script:")
            script_completo_para_analizar = "\n".join(script) # Unir para el analizador
            analisis_resultado = analizar_script(script_completo_para_analizar)
            st.info(analisis_resultado)

elif opcion_seleccionada == "Generador de Copys y Hooks":
    st.header(f"📝 Generador de Copys y Hooks - **{st.session_state.nicho_seleccionado}**")
    st.write("Crea textos atractivos para tus publicaciones y ganchos que capten la atención.")

    if st.button("Generar Copy y Hooks"):
        with st.spinner('Generando copy y hooks...'):
            contenido = generar_copy_hooks(st.session_state.nicho_seleccionado)
            
            st.subheader("Copy Sugerido:")
            st.success(f"**{contenido['copy']}**")
            
            st.subheader("Hooks Sugeridos:")
            if contenido['hooks']:
                for hook in contenido['hooks']:
                    st.info(f"- {hook}")
            else:
                st.warning("No se pudieron generar hooks específicos.")

elif opcion_seleccionada == "Analizador de Scripts":
    st.header("🔍 Analizador de Scripts")
    st.write("Pega aquí tu script para obtener un análisis y sugerencias.")

    script_input = st.text_area(
        "Pega tu script aquí:",
        height=200,
        placeholder="Ej: Escena 1: Presenta el problema. Escena 2: Muestra la solución con un producto de IA..."
    )

    if st.button("Analizar Script"):
        if script_input:
            with st.spinner('Analizando script...'):
                resultado_analisis = analizar_script(script_input)
                st.subheader("Resultados del Análisis:")
                st.info(resultado_analisis)
        else:
            st.warning("Por favor, pega un script para analizar.")

st.markdown("---")
st.markdown("Desarrollado con ❤️ por tu asistente de Python.")
