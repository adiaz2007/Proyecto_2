import os
import json
import datetime

# Intentamos importar el decorador. Si falla, definimos uno "falso" para que no se rompa.
try:
    from utils import registrar_accion
except ImportError:
    # Si por alguna razón utils falla, usamos un decorador simple que no hace nada
    def registrar_accion(funcion):
        return funcion

SNAPSHOT_FILE = "estado_carpeta.json"

def obtener_estado_actual(ruta):
    """Auxiliar: Crea un diccionario {archivo: fecha_modificacion}"""
    estado = {}
    if not os.path.exists(ruta):
        return estado
        
    try:
        # Escanear archivos en la ruta
        for archivo in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, archivo)
            if os.path.isfile(ruta_completa):
                estado[archivo] = os.path.getmtime(ruta_completa)
    except Exception as e:
        print(f"Error leyendo carpeta: {e}")
        
    return estado

# --- AQUÍ ESTÁ LA FUNCIÓN QUE FALTABA ---
@registrar_accion
def auditar_cambios(ruta_objetivo):
    """
    Compara el estado actual de la carpeta con el guardado en el JSON.
    Esta es la función que llama el main.py
    """
    print(f"\n--- Auditoría de Cambios en: {ruta_objetivo} ---")
    
    # 1. Cargar estado anterior (Snapshot)
    estado_anterior = {}
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, 'r') as f:
                estado_anterior = json.load(f)
        except:
            print("[Info] No se pudo leer el snapshot anterior o está vacío.")

    # 2. Obtener estado actual
    estado_actual = obtener_estado_actual(ruta_objetivo)
    
    # 3. Comparar conjuntos (Sets)
    set_anterior = set(estado_anterior.keys())
    set_actual = set(estado_actual.keys())
    
    nuevos = list(set_actual - set_anterior)
    eliminados = list(set_anterior - set_actual)
    modificados = []
    
    # Detectar modificados (están en ambos, pero con fecha distinta)
    for archivo in set_actual.intersection(set_anterior):
        if estado_actual[archivo] != estado_anterior[archivo]:
            modificados.append(archivo)
            
    # 4. Reportar resultados en pantalla
    if not nuevos and not eliminados and not modificados:
        print(">> No se detectaron cambios recientes.")
    else:
        if nuevos: print(f"[+] Nuevos archivos detectados: {nuevos}")
        if eliminados: print(f"[-] Archivos eliminados: {eliminados}")
        if modificados: print(f"[*] Archivos modificados: {modificados}")
    
    # 5. Guardar nuevo estado para la próxima vez
    try:
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(estado_actual, f)
        print(">> Snapshot actualizado correctamente.")
    except Exception as e:
        print(f"Error guardando snapshot: {e}")
