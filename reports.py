import os
import datetime

def generar_reporte_organizacion(ruta_directorio, archivos_movidos):
    """
    Genera un reporte sobre la organización de archivos.
    """
    nombre_reporte = os.path.join(ruta_directorio, "reporte_organizacion.txt")
    
    with open(nombre_reporte, "w", encoding="utf-8") as f:
        f.write(f"Reporte de Organización - {datetime.datetime.now()}\n")
        f.write(f"Archivos movidos: {archivos_movidos}\n")
        f.write("\n--- Fin del reporte ---\n")
    
    print(f"[INFO] Reporte generado: {nombre_reporte}")

def generar_reporte_analisis(ruta_archivo, resultados):
    """
    Genera un reporte sobre el análisis de contenido.
    """
    nombre_reporte = f"reporte_analisis_{os.path.basename(ruta_archivo)}.txt"
    
    with open(nombre_reporte, "w", encoding="utf-8") as f:
        f.write(f"Reporte de Análisis - {datetime.datetime.now()}\n")
        f.write(f"Archivo analizado: {ruta_archivo}\n")
        f.write(f"Total de coincidencias: {len(resultados)}\n\n")
        f.write("Detalles:\n")
        for linea in resultados:
            f.write(f"{linea}\n")
        f.write("\n--- Fin del reporte ---\n")
    
    print(f"[INFO] Reporte generado: {nombre_reporte}")