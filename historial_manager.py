import json
import os
from datetime import datetime

HISTORY_FILE = "historial_contenido.json"

def guardar_en_historial(tema, script, copy_hooks):
    """
    Guarda un nuevo registro de contenido generado en un archivo JSON.
    """
    historial = cargar_historial()
    
    # Asignar un ID único al nuevo registro
    nuevo_id = max([r['id'] for r in historial]) + 1 if historial else 1
    
    nuevo_registro = {
        "id": nuevo_id,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tema": tema,
        "script": script,
        "copy_hooks": copy_hooks
    }
    
    historial.append(nuevo_registro)
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def cargar_historial():
    """
    Carga el historial de contenido desde el archivo JSON.
    Si el archivo no existe, devuelve una lista vacía.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def borrar_registros_seleccionados(ids_a_borrar):
    """
    Elimina registros específicos del historial basados en sus IDs.
    """
    if not ids_a_borrar:
        return
        
    historial = cargar_historial()
    
    # Creamos un nuevo historial que no contenga los IDs a borrar
    nuevo_historial = [registro for registro in historial if registro['id'] not in ids_a_borrar]
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(nuevo_historial, f, ensure_ascii=False, indent=4)

def limpiar_historial():
    """
    Borra todos los registros del historial.
    """
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
