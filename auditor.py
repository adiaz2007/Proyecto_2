import os
import json
import time

# Intentamos importar utils
try:
    from utils import registrar_accion
except ImportError:
    def registrar_accion(f): return f

SNAPSHOT_FILE = "estado_carpeta.json"

def obtener_estado_actual(ruta):
    estado = {}
    if not os.path.exists(ruta):
        return estado
    for archivo in os.listdir(ruta):
        ruta_c = os.path.join(ruta, archivo)
        if os.path.isfile(ruta_c):
            # Guardamos fecha de modificación
            estado[archivo] = os.path.getmtime(ruta_c)
    return estado

@registrar_accion
def auditar_cambios(ruta_objetivo):
    
    # 1. Cargar estado anterior
    estado_anterior = {}
    if os.path.exists(SNAPSHOT_FILE):
            
            with open(SNAPSHOT_FILE, 'r') as f:
                estado_anterior = json.load(f)

    # 2. Obtener estado actual
    estado_actual = obtener_estado_actual(ruta_objetivo)
    

    # 3. Comparar
    set_anterior = set(estado_anterior.keys())
    set_actual = set(estado_actual.keys())
    
    nuevos = list(set_actual - set_anterior)
    eliminados = list(set_anterior - set_actual)
    modificados = []
    
    for archivo in set_actual.intersection(set_anterior):
        # Comparamos fechas (float)
        if estado_actual[archivo] != estado_anterior[archivo]:
            modificados.append(archivo)
            print(f"    Antes: {estado_anterior[archivo]} | Ahora: {estado_actual[archivo]}")

    # 4. Mostrar Resultados (FORCE PRINT)
    print("\n--- RESULTADOS ---")
    if nuevos: 
        print(f"[+] NUEVOS: {nuevos}")
    else:
        print("[ ] No hay nuevos.")

    if eliminados: 
        print(f"[-] ELIMINADOS: {eliminados}")
    else:
        print("[ ] No hay eliminados.")

    if modificados: 
        print(f"[*] MODIFICADOS: {modificados}")
    else:
        print("[ ] No hay modificados.")

    # 5. Guardar
    with open(SNAPSHOT_FILE, 'w') as f:
        json.dump(estado_actual, f)