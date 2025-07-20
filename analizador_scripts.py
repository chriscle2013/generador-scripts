# analizador_scripts.py

import streamlit as st # Asegúrate de que streamlit esté importado si lo usas aquí

def analizar_script(script_texto):
    """
    Realiza un análisis básico de un script.
    En una versión más avanzada, esto podría usar IA para dar feedback.
    """
    if not script_texto.strip():
        return "El script está vacío. No hay nada que analizar."

    lineas = [linea.strip() for linea in script_texto.split('\n') if linea.strip()]
    num_lineas = len(lineas)
    
    analisis = []

    analisis.append(f"✅ **Análisis Rápido del Script**:")
    analisis.append(f"- El script tiene **{num_lineas}** líneas de contenido.")

    # Detectar presencia de palabras clave básicas
    palabras_clave_hook = ["hook", "gancho", "¿cómo", "¿sabías", "descubre", "aprende", "secreto"]
    palabras_clave_cta = ["llama ahora", "clic aquí", "visita", "sigue para más", "compra ahora", "regístrate"]

    tiene_hook = any(any(pk in linea.lower() for pk in palabras_clave_hook) for linea in lineas[:2]) # Busca hook en las primeras 2 líneas
    tiene_cta = any(any(pk in linea.lower() for pk in palabras_clave_cta) for linea in lineas[-2:]) # Busca CTA en las últimas 2 líneas

    if tiene_hook:
        analisis.append("- Parece que tiene un **buen gancho (hook)** al principio. ¡Bien hecho!")
    else:
        analisis.append("- ⚠️ **Sugerencia:** Considera añadir un **gancho (hook) fuerte** al inicio para captar la atención.")

    if tiene_cta:
        analisis.append("- Incluye una **llamada a la acción (CTA)** clara. ¡Excelente para la conversión!")
    else:
        analisis.append("- ⚠️ **Sugerencia:** Añade una **llamada a la acción (CTA)** al final para guiar a tu audiencia.")

    if num_lineas < 3:
        analisis.append("- 💡 **Sugerencia:** El script es muy corto. Considera añadir más detalles o una escena adicional.")
    elif num_lineas > 7:
        analisis.append("- 💡 **Sugerencia:** El script es algo largo. Para un reel corto, podrías buscar ser más conciso.")
    else:
        analisis.append("- El script tiene una longitud **adecuada** para un reel.")

    analisis.append("\nEsperamos que este análisis te sea útil para mejorar tu contenido.")
    
    return "\n".join(analisis)
