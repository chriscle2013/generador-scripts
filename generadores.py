# generadores.py

def generar_script_reel(nicho):
    """Genera un script simple para un reel basado en el nicho."""
    scripts_ejemplo = {
        "Inteligencia Artificial": [
            "Escena 1: Introducción a la IA.",
            "Escena 2: Ejemplos prácticos de IA.",
            "Escena 3: Futuro de la IA y llamada a la acción."
        ],
        "Formula 1": [
            "Escena 1: Momentos icónicos de F1.",
            "Escena 2: Explicación de la tecnología de un coche.",
            "Escena 3: ¿Quién ganará la próxima carrera? Predicciones."
        ],
        "Marketing Digital": [
            "Escena 1: Trucos para el SEO.",
            "Escena 2: Importancia del contenido de valor.",
            "Escena 3: Tu negocio en línea, ¡al siguiente nivel!"
        ],
        "Mindset": [
            "Escena 1: El poder del pensamiento positivo.",
            "Escena 2: Hábitos para una mentalidad de crecimiento.",
            "Escena 3: Supera tus límites, ¡cree en ti!"
        ],
        "Mascotas": [
            "Escena 1: Momentos divertidos con mascotas.",
            "Escena 2: Consejos para el cuidado de tu mascota.",
            "Escena 3: ¡Tu mascota te espera para jugar!"
        ]
    }
    return scripts_ejemplo.get(nicho, ["Script genérico para " + nicho])

def generar_copy_hooks(nicho):
    """Genera un copy y hooks simples para un reel basado en el nicho."""
    copys_hooks_ejemplo = {
        "Inteligencia Artificial": {
            "copy": "¡Descubre cómo la IA está cambiando el mundo! 🚀🤖 #InteligenciaArtificial #IA #FuturoTech",
            "hooks": ["¿Qué es la IA realmente?", "¿Lista para el futuro?", "¿IA es el nuevo petróleo?"]
        },
        "Formula 1": {
            "copy": "¡La velocidad que te hace vibrar! 🏎️💨 Vive la emoción de la Fórmula 1. #Formula1 #F1 #Velocidad",
            "hooks": ["¿Eres fan de la F1?", "¿Quién es tu piloto favorito?", "¿Qué coche es el más rápido?"]
        },
        "Marketing Digital": {
            "copy": "¡Potencia tu negocio con estos tips de Marketing Digital! 📈💡 #MarketingDigital #SEO #Emprendedores",
            "hooks": ["¿Quieres más clientes?", "¿Tu negocio está online?", "¿Marketing fácil?"]
        },
        "Mindset": {
            "copy": "Cambia tu mentalidad, cambia tu vida. ✨💪 Impulsa tu crecimiento personal. #Mindset #CrecimientoPersonal #Motivacion",
            "hooks": ["¿Tu mente te limita?", "¿Crees en ti?", "¿Mentalidad imparable?"]
        },
        "Mascotas": {
            "copy": "¡Momentos adorables con tus peludos! 🐶🐱 Consejos para una vida feliz con tu mascota. #Mascotas #AmorAnimal #PerrosYGatos",
            "hooks": ["¿Amas a los animales?", "¿Tienes mascota?", "¿La vida es mejor con ellos?"]
        }
    }
    return copys_hooks_ejemplo.get(nicho, {"copy": f"Copy genérico para {nicho}", "hooks": [f"Hook genérico para {nicho}"]})
