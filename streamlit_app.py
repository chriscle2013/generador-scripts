# app.py

def mostrar_menu_principal():
    print("\n--- Generador de Contenido para Reels ---")
    print("1. Generar Script para Reel")
    print("2. Generar Copy y Hooks")
    print("3. Analizar Script (Módulo Externo)")
    print("4. Salir")
    opcion = input("Selecciona una opción: ")
    return opcion

def seleccionar_nicho():
    nichos = ["Inteligencia Artificial", "Formula 1", "Marketing Digital", "Mindset", "Mascotas"]
    print("\n--- Selecciona un Nicho ---")
    for i, nicho in enumerate(nichos):
        print(f"{i + 1}. {nicho}")
    while True:
        try:
            opcion = int(input("Ingresa el número del nicho: "))
            if 1 <= opcion <= len(nichos):
                return nichos[opcion - 1]
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def main():
    while True:
        opcion = mostrar_menu_principal()

        if opcion == '1':
            nicho_seleccionado = seleccionar_nicho()
            print(f"\nGenerando script para: {nicho_seleccionado}")
            # Aquí llamaremos a la función del generador de scripts
            # Por ahora, un mensaje de prueba
            print(f"Script de ejemplo para {nicho_seleccionado}: '¡Descubre los secretos de la IA en menos de 60 segundos!'")
        elif opcion == '2':
            nicho_seleccionado = seleccionar_nicho()
            print(f"\nGenerando copy y hooks para: {nicho_seleccionado}")
            # Aquí llamaremos a la función del generador de copys y hooks
            # Por ahora, mensajes de prueba
            print(f"Copy: '¡No te pierdas este reel lleno de tips de {nicho_seleccionado}! #reelviral #{nicho_seleccionado.lower().replace(' ', '')}'")
            print(f"Hook: '¿Quieres dominar {nicho_seleccionado}?'")
        elif opcion == '3':
            print("\nActivando el módulo de análisis de scripts...")
            # Aquí llamaremos a tu módulo de análisis
            # Por ahora, un mensaje de prueba
            print("Análisis de script completado (simulado).")
        elif opcion == '4':
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
