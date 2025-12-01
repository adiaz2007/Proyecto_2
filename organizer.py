import os
import shutil
# Intentamos importar utils, si falla no pasa nada
try:
    from utils import registrar_accion
except ImportError:
    def registrar_accion(func): return func

@registrar_accion
def organizar_archivos(ruta_origen, criterio, simulacion=False):

    if not os.path.exists(ruta_origen):
        print("La ruta no existe en el sistema.")
        return 0

    # Listar archivos
    todos_archivos = os.listdir(ruta_origen)
    archivos = [f for f in todos_archivos if os.path.isfile(os.path.join(ruta_origen, f))]
   
    if len(archivos) == 0:
        print("No encontré archivos (solo carpetas o nada).")

    contador = 0

    for archivo in archivos:
        ruta_completa = os.path.join(ruta_origen, archivo)
        nombre_carpeta = "Varios"

        # Lógica de clasificación
        if criterio == "1": # Por Extensión
            ext = archivo.split('.')[-1].upper()
            if len(ext) > 0 and len(ext) < 6:
                nombre_carpeta = ext
            else:
                nombre_carpeta = "OTROS"
            
        elif criterio == "2": # Por Tamaño
            tamano_mb = os.path.getsize(ruta_completa) / (1024 * 1024)
            if tamano_mb < 1:
                nombre_carpeta = "Pequeños"
            elif tamano_mb < 50:
                nombre_carpeta = "Medianos"
            else:
                nombre_carpeta = "Grandes"

        
        if simulacion:

            print(f"[SIMULACIÓN] Movería '{archivo}' a carpeta '{nombre_carpeta}'")
        else:
            carpeta_destino = os.path.join(ruta_origen, nombre_carpeta)
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            try:
                shutil.move(ruta_completa, os.path.join(carpeta_destino, archivo))
                print(f"[OK] Movido: {archivo} -> {nombre_carpeta}")
                contador += 1
            except Exception as e:
                print(f"[ERROR] {e}")

    return contador
