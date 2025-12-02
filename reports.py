import os
import csv
import datetime

# Intentamos importar el decorador
try:
    from utils import registrar_accion
except ImportError:
    def registrar_accion(f): return f

@registrar_accion
def generar_reporte_csv(ruta_carpeta):
    """
    Genera un archivo 'inventario.csv' con los datos de la carpeta.
    """
    print(f"\n--- GENERANDO REPORTE DE: {ruta_carpeta} ---")
    
    if not os.path.exists(ruta_carpeta):
        print(f"[ERROR] La ruta '{ruta_carpeta}' no existe.")
        return

    nombre_reporte = "inventario_archivos.csv"
    archivos_encontrados = []

    # 1. Recopilar datos
    try:
        contenido = os.listdir(ruta_carpeta)
        for nombre in contenido:
            ruta_completa = os.path.join(ruta_carpeta, nombre)
            
            if os.path.isfile(ruta_completa):
                # Obtener datos reales del sistema
                tamano_bytes = os.path.getsize(ruta_completa)
                tamano_kb = round(tamano_bytes / 1024, 2)
                timestamp = os.path.getmtime(ruta_completa)
                fecha = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                extension = nombre.split('.')[-1] if '.' in nombre else "SIN EXT"

                archivos_encontrados.append([nombre, extension, f"{tamano_kb} KB", fecha])
                
    except Exception as e:
        print(f"[ERROR] Al leer archivos: {e}")
        return

    # 2. Escribir CSV
    if archivos_encontrados:
        try:
            # encoding='utf-8-sig' es para que Excel abra bien las tildes/ñ
            with open(nombre_reporte, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=';') # Usamos ; para que Excel lo separe bien
                
                # Encabezados
                writer.writerow(["NOMBRE DEL ARCHIVO", "EXTENSIÓN", "TAMAÑO", "FECHA MODIFICACIÓN"])
                
                # Datos
                writer.writerows(archivos_encontrados)
                
            print(f"[ÉXITO] Reporte guardado como: '{nombre_reporte}'")
            print(f">> Se listaron {len(archivos_encontrados)} archivos.")
            
        except Exception as e:
            print(f"[ERROR] No se pudo crear el archivo CSV: {e}")
    else:
        print("[AVISO] La carpeta está vacía, no se generó reporte.")