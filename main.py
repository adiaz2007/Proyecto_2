import os
from organizer import organizar_archivos

def main():
    print("Bienvenido al organizador de archivos")

    ruta_directorio = input("Por favor, ingresa la ruta del directorio a organizar: ")
    
    print("\nCriterios disponibles:")
    print("1. extension (Organizar por extensión de archivo)")
    print("2. tamano (Organizar por tamaño de archivo)")
    print("3. fecha (Organizar por fecha de modificación)")
    
    criterio = input("\nSelecciona un criterio (escribe 'extension', 'tamano' o 'fecha'): ")

    if criterio not in ['extension', 'tamano', 'fecha']:
        print("Criterio no válido. Por favor, intenta de nuevo.")
        return

    simulacion = input("\n¿Quieres hacer una simulación? (s/n): ").lower()
    es_simulacion = simulacion == 's'

    archivos_movidos = organizar_archivos(ruta_directorio, criterio, es_simulacion)

    if archivos_movidos is not None:
        print(f"\n¡Organización completada! Total de archivos procesados: {archivos_movidos}")

if __name__ == "__main__":
    main()