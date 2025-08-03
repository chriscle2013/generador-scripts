import json
import os
from datetime import datetime

HISTORY_FILE = "historial_contenido.json"

def guardar_en_historial(tema, script, copy_hooks):
    """
    Guarda un nuevo registro de contenido generado en un archivo JSON.
    """
    historial = cargar_historial()
    
    nuevo_registro = {
        "id": len(historial) + 1,
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
            return json.load(f)
    return []

def limpiar_historial():
    """
    Borra todos los registros del historial.
    """
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
