import streamlit as st
from generadores import generar_script, generar_copy_hooks
from analizador_scripts import analizar_script
from historial_manager import guardar_en_historial, cargar_historial, limpiar_historial

# --- Configuración de la Página y Estado de la Sesión ---
st.set_page_config(
    page_title="Generador de Contenido para Reels",
    page_icon="🎬",
    layout="centered"
)

# Inicializar el estado de la sesión si aún no existe
if 'script_generado' not in st.session_state:
    st.session_state['script_generado'] = None
if 'copy_hooks_generado' not in st.session_state:
    st.session_state['copy_hooks_generado'] = None
if 'tema_input' not in st.session_state:
    st.session_state['tema_input'] = ""

# --- Título Principal ---
st.title("🎬 Generador de Contenido para Reels y Redes Sociales")
st.markdown("Crea scripts, copys y hooks para TikTok, Instagram y YouTube.")

# --- Campo de Texto para el Tema ---
st.session_state['tema_input'] = st.text_input(
    "Ingresa el tema para tu Contenido",
    placeholder="Ej: Marketing de afiliados para principiantes, Receta de arepas con queso, Últimas noticias de la Fórmula 1",
    help="Escribe sobre qué quieres generar contenido.",
    value=st.session_state['tema_input']
)

st.sidebar.title("Navegación")
opcion_seleccionada = st.sidebar.radio(
    "Ir a:",
    ("Generador de Contenido Completo", "Analizador de Scripts", "Historial de Contenido")
)

# --- Contenido Principal Basado en la Opción Seleccionada ---

if opcion_seleccionada == "Generador de Contenido Completo":
    st.header(f"✍️ Generador de Contenido Completo")
    st.write("Genera ideas y estructuras para tus videos de reels, junto con copy y hooks.")

    if st.button("Generar Contenido"):
        if st.session_state['tema_input']:
            with st.spinner(f'Generando contenido para "{st.session_state["tema_input"]}"...'):
                # Generar y guardar en el estado de la sesión
                st.session_state['script_generado'] = generar_script(
                    st.session_state['tema_input'], "persuasivo", "enérgico", 30
                )
                st.session_state['copy_hooks_generado'] = generar_copy_hooks(
                    st.session_state['tema_input'], [st.session_state['script_generado']]
                )
        else:
            st.warning("¡Por favor, ingresa un tema antes de generar contenido!")

    # Mostrar el contenido si ya fue generado (usando el estado de la sesión)
    if st.session_state['script_generado']:
        st.subheader("Script Generado:")
        st.markdown(st.session_state['script_generado']) 

        st.markdown("---")

        st.subheader("Copy y Hooks Sugeridos para este Script:")
        st.success(f"**Copy:** {st.session_state['copy_hooks_generado']['copy']}")
        
        st.markdown("**Hooks:**")
        if st.session_state['copy_hooks_generado']['hooks']:
            for hook in st.session_state['copy_hooks_generado']['hooks']:
                st.info(f"- {hook}")

        st.markdown("---")

        st.subheader("Análisis Rápido del Script:")
        analizar_script(st.session_state['script_generado'])

        # Botón para guardar el contenido, ahora con un mensaje de éxito
        if st.button("💾 Guardar en Historial"):
            guardar_en_historial(
                st.session_state['tema_input'], 
                st.session_state['script_generado'], 
                st.session_state['copy_hooks_generado']
            )
            st.success("¡Contenido guardado en el historial con éxito!")

elif opcion_seleccionada == "Analizador de Scripts":
    st.header("🔍 Analizador de Scripts")
    st.write("Pega aquí tu script para obtener un análisis y sugerencias.")
    
    script_input_analizador = st.text_area(
        "Pega tu script aquí:",
        height=200,
        placeholder="Ej: Escena 1: Presenta el problema. Escena 2: Muestra la solución con un producto de IA..."
    )

    if st.button("Analizar Script"):
        if script_input_analizador:
            with st.spinner('Analizando script...'):
                analizar_script(script_input_analizador)
        else:
            st.warning("Por favor, pega un script para analizar.")

elif opcion_seleccionada == "Historial de Contenido":
    st.header("📚 Historial de Contenido Generado")
    st.write("Aquí puedes revisar y reutilizar el contenido que has guardado.")

    historial = cargar_historial()

    if not historial:
        st.info("El historial está vacío. Genera y guarda algo de contenido primero.")
    else:
        # Botón para limpiar el historial
        if st.button("🗑️ Limpiar Historial"):
            limpiar_historial()
            st.session_state['script_generado'] = None
            st.session_state['copy_hooks_generado'] = None
            st.rerun()

        for registro in reversed(historial):
            with st.expander(f"**Tema:** {registro['tema']} (Generado: {registro['fecha']})"):
                st.subheader("Script Generado:")
                st.markdown(registro['script'])
                
                st.subheader("Copy y Hooks Sugeridos:")
                st.success(f"**Copy:** {registro['copy_hooks']['copy']}")
                st.markdown("**Hooks:**")
                for hook in registro['copy_hooks']['hooks']:
                    st.info(f"- {hook}")

st.markdown("---")
st.markdown("Desarrollado con ❤️ por tu asistente de Python.")
