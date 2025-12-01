import sys
import os
import time

try:
    import utils
    import organizer
    import analyzer
    import auditor
except ImportError as e:
    print("Error Crítico: Faltan archivos del proyecto.")
    print(f"No se pudo cargar: {e.name}.py")
    print("Asegúrate de que utils.py, organizer.py, analyzer.py y auditor.py estén en la misma carpeta.")
    sys.exit()

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    if os.name == 'nt': # Windows
        os.system('cls')
    else: # Mac / Linux
        os.system('clear')

def mostrar_menu():
    print("\n" + "="*40)
    print("       SISTEMA GESTOR DE ARCHIVOS")
    print("="*40)
    print("1. [Organizador] Mover archivos por tipo/tamaño")
    print("2. [Analizador]  Buscar emails en un archivo")
    print("3. [Auditor]     Detectar cambios en una carpeta")
    print("4. Salir")
    print("-" * 40)

def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input(">> Seleccione una opción (1-4): ").strip()

        # --- OPCIÓN 1: ORGANIZAR ---
        if opcion == "1":
            limpiar_pantalla() 
            print("="*30)
            print("   MODULO DE ORGANIZACIÓN")
            print("="*30)
            ruta = input("Ingrese la ruta de la carpeta a organizar: ").strip()
            
            # Usamos la función de utils para validar
            if utils.validar_ruta(ruta):
                print("\nSeleccione criterio de organización:")
                print("   1. Por Extensión (PDF, JPG, etc.)")
                print("   2. Por Tamaño (Pequeños, Grandes)")
                criterio = input("   >> Opción (1 o 2): ").strip()
                
                # Preguntar por simulación
                sim_input = input("   >> ¿Modo Simulación (solo ver)? (S/N): ").strip().lower()
                es_simulacion = (sim_input == 's')
                
                # Llamada al módulo organizer
                organizer.organizar_archivos(ruta, criterio, es_simulacion)
            else:
                print(f"[!] La ruta '{ruta}' no existe o no es una carpeta.")

        # --- OPCIÓN 2: ANALIZAR ---
        elif opcion == "2":
            limpiar_pantalla() 
            print("="*30)
            print("   MODULO DE ORGANIZACIÓN")
            print("="*30)

            ruta_archivo = input("Ingrese la ruta del archivo (.txt, .log): ").strip()
            
            if os.path.isfile(ruta_archivo):
                # Llamada al módulo analyzer
                analyzer.analizar_contenido(ruta_archivo)
            else:
                print(f"[!] El archivo '{ruta_archivo}' no existe.")

        # --- OPCIÓN 3: AUDITAR ---
        elif opcion == "3":
            limpiar_pantalla() 
            print("="*30)
            print("   MODULO DE ORGANIZACIÓN")
            print("="*30)

            ruta = input("Ingrese la ruta de la carpeta a auditar: ").strip()
            
            if utils.validar_ruta(ruta):
                # Llamada al módulo auditor
                auditor.auditar_cambios(ruta)
            else:
                print(f"[!] La ruta '{ruta}' no existe.")

        # --- OPCIÓN 4: SALIR ---
        elif opcion == "4":
            print("Cerrando sistema... ¡Hasta luego!")
            break
        
        else:
            print("\n[!] Opción no válida.")
            time.sleep(1) 
            continue

        print("\n" + "-"*40)
        input("Presione [ENTER] para volver al menú principal...")

if __name__ == "__main__":
    main()