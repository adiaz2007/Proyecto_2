import os
import shutil
import time
from datetime import datetime


def organizar_archivos(ruta_directorio, criterio, es_simulacion):

    if not os.path.exists(ruta_directorio):
        print(f"Oye, la ruta '{ruta_directorio}' no existe. Revisa bien.")
        return

    try:
        lista_archivos = os.listdir(ruta_directorio)
    except Exception as error:
        print(f"No pude leer la carpeta. Error: {error}")
        return

    archivos_movidos = 0

    print(f"\n--- Arrancando organización por: {criterio} ---")

    for archivo in lista_archivos:

        ruta_completa = os.path.join(ruta_directorio, archivo)

        if os.path.isdir(ruta_completa):
            continue

        if archivo == "main.py" or archivo.startswith("."):
            continue

        nombre_carpeta = "Otros"

        try:
            if criterio == "extension":
                parte_nombre, parte_extension = os.path.splitext(archivo)

                if parte_extension:
                    nombre_carpeta = parte_extension[1:].upper()
                else:
                    nombre_carpeta = "Sin_Extension"

            elif criterio == "tamano":
                tamano_bytes = os.path.getsize(ruta_completa)
                if tamano_bytes < 1_048_576:
                    nombre_carpeta = "Pequeños"
                elif tamano_bytes < 104_857_600:
                    nombre_carpeta = "Medianos"
                else:
                    nombre_carpeta = "Grandes"

            elif criterio == "fecha":
                tiempo_raro = os.path.getmtime(ruta_completa)
                fecha_real = datetime.fromtimestamp(tiempo_raro)
                nombre_carpeta = fecha_real.strftime("%Y-%m")

            ruta_carpeta_destino = os.path.join(ruta_directorio, nombre_carpeta)
            ruta_final = os.path.join(ruta_carpeta_destino, archivo)

            if es_simulacion == True:
                print(
                    f"[SIMULACIÓN] Movería '{archivo}' a la carpeta '{nombre_carpeta}'"
                )
                archivos_movidos += 1

            else:
                os.makedirs(ruta_carpeta_destino, exist_ok=True)

                if not os.path.exists(ruta_final):
                    shutil.move(ruta_completa, ruta_final)
                    print(f"[LISTO] Moví '{archivo}' a '{nombre_carpeta}'")
                    archivos_movidos += 1
                else:
                    print(
                        f"[CUIDADO] El archivo '{archivo}' ya existe en destino. Lo salté."
                    )

        except Exception as e:
            print(f"Ups, error con '{archivo}': {e}")

    print(f"\nProceso terminado. Archivos procesados: {archivos_movidos}")
    return archivos_movidos
