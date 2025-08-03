import streamlit as st
from generadores import generar_script, generar_copy_hooks # ¡CAMBIO AQUÍ!
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

# --- Campo de Texto para el Tema ---
tema_input = st.text_input(
    "Ingresa el tema para tu Contenido",
    placeholder="Ej: Marketing de afiliados para principiantes, Receta de arepas con queso, Últimas noticias de la Fórmula 1",
    help="Escribe sobre qué quieres generar contenido."
)

st.sidebar.title("Navegación")
opcion_seleccionada = st.sidebar.radio(
    "Ir a:",
    ("Generador de Contenido Completo", "Analizador de Scripts")
)

# --- Contenido Principal Basado en la Opción Seleccionada ---

if opcion_seleccionada == "Generador de Contenido Completo":
    st.header(f"✍️ Generador de Contenido Completo")
    st.write("Genera ideas y estructuras para tus videos de reels, junto con copy y hooks.")

    if st.button("Generar Contenido"):
        if tema_input:
            with st.spinner(f'Generando contenido para "{tema_input}"...'):
                # Generar Script
                script = generar_script(tema_input, "persuasivo", "enérgico", 30) # ¡CAMBIO AQUÍ! Añadí los parámetros
                st.subheader("Script Generado:")
                # Ya no necesitas iterar si la respuesta es una sola cadena
                st.markdown(script) 

                st.markdown("---")

                # Generar Copy y Hooks para el script recién generado
                st.subheader("Copy y Hooks Sugeridos para este Script:")
                contenido_copy_hooks = generar_copy_hooks(tema_input, [script]) # Envía el script como lista
                
                st.success(f"**Copy:** {contenido_copy_hooks['copy']}")
                
                st.markdown("**Hooks:**")
                if contenido_copy_hooks['hooks']:
                    for hook in contenido_copy_hooks['hooks']:
                        st.info(f"- {hook}")
                else:
                    st.warning("No se pudieron generar hooks específicos para este script.")

                st.markdown("---")

                st.subheader("Análisis Rápido del Script:")
                # La función analizar_script necesita una cadena, no una lista
                analisis_resultado = analizar_script(script) 
                st.info(analisis_resultado)
        else:
            st.warning("¡Por favor, ingresa un tema antes de generar contenido!")

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
                # El analizador de scripts no usa parámetros adicionales
                analizar_script(script_input) 
        else:
            st.warning("Por favor, pega un script para analizar.")

st.markdown("---")
st.markdown("Desarrollado con ❤️ por tu asistente de Python.")
