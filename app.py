# app.py

# Importa las funciones de los módulos
from generadores import generar_script_reel, generar_copy_hooks
from analizador_scripts import analizar_script

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
            script_generado = generar_script_reel(nicho_seleccionado)
            print(f"\n--- Script para {nicho_seleccionado} ---")
            for linea in script_generado:
                print(f"- {linea}")
            # Puedes ofrecer la opción de analizarlo de inmediato
            analizar_ahora = input("¿Quieres analizar este script ahora? (s/n): ").lower()
            if analizar_ahora == 's':
                # Unimos el script para pasarlo como un solo string
                script_completo = " ".join(script_generado)
                resultado_analisis = analizar_script(script_completo)
                print(f"Resultado del análisis: {resultado_analisis}")

        elif opcion == '2':
            nicho_seleccionado = seleccionar_nicho()
            contenido_generado = generar_copy_hooks(nicho_seleccionado)
            print(f"\n--- Copy y Hooks para {nicho_seleccionado} ---")
            print(f"**Copy:** {contenido_generado['copy']}")
            print("**Hooks:**")
            for hook in contenido_generado['hooks']:
                print(f"- {hook}")

        elif opcion == '3':
            # Para analizar un script en esta opción, podríamos pedir al usuario que lo pegue
            # o que indique un archivo. Por ahora, lo haremos simple:
            print("\nIntroduce el script que deseas analizar (o 'salir' para cancelar):")
            script_para_analizar = input("Script: ")
            if script_para_analizar.lower() != 'salir':
                resultado_analisis = analizar_script(script_para_analizar)
                print(f"Resultado del análisis: {resultado_analisis}")
            else:
                print("Análisis cancelado.")

        elif opcion == '4':
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
