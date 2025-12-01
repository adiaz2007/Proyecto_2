import os
import json
import datetime

<<<<<<< HEAD
def decorador_auditoria(funcion_original):
    
    def envoltura(*argumentos, **kwargs):
        nombre_func = funcion_original.__name__
        hora_actual_inicio = datetime.datetime.now()
        
        with open("audit.log", "a", encoding='utf-8') as f:
            f.write(f"Iniciando [{nombre_func}] a las [{hora_actual_inicio}]\n")
        
        
        resultado = funcion_original(*argumentos, **kwargs)
        
        hora_actual_fin = datetime.datetime.now()
        
        
        with open("audit.log", "a", encoding='utf-8') as f:
            f.write(f"Finalizado [{nombre_func}] a las [{hora_actual_fin}]\n")
        
        return resultado
    
    return envoltura

class Auditor:
    def tomar_snapshot_actual(self, ruta_directorio):
        
        estado_actual = {}
        
        
        if not os.path.exists(ruta_directorio):
            print(f"Error: El directorio {ruta_directorio} no existe.")
            return estado_actual

        
        for nombre_archivo in os.listdir(ruta_directorio):
            ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
            
          
            if os.path.isfile(ruta_completa):
                fecha_modificacion = os.path.getmtime(ruta_completa)
                estado_actual[nombre_archivo] = fecha_modificacion
                
        return estado_actual

    @decorador_auditoria
    def auditar(self, ruta_directorio):
       
        if os.path.exists("snapshot.json"):
            with open("snapshot.json", "r", encoding='utf-8') as f:
                try:
                    estado_anterior = json.load(f)
                except json.JSONDecodeError:
                    estado_anterior = {}
        else:
            estado_anterior = {}

      
        estado_actual = self.tomar_snapshot_actual(ruta_directorio)

        
        claves_actuales = set(estado_actual.keys())
        claves_anteriores = set(estado_anterior.keys())

        
        archivos_nuevos = list(claves_actuales - claves_anteriores)
        
        archivos_borrados = list(claves_anteriores - claves_actuales)
        
        archivos_modificados = []

        archivos_comunes = claves_actuales.intersection(claves_anteriores)
        
        for archivo in archivos_comunes:
            if estado_actual[archivo] != estado_anterior[archivo]:
                archivos_modificados.append(archivo)

        
        with open("snapshot.json", "w", encoding='utf-8') as f:
            json.dump(estado_actual, f, indent=4)

        return (archivos_nuevos, archivos_borrados, archivos_modificados)

if __name__ == "__main__":
    dir_prueba = "carpeta_prueba"
    if not os.path.exists(dir_prueba):

        os.makedirs(dir_prueba)
        
        with open(os.path.join(dir_prueba, "archivo1.txt"), "w") as f:
            f.write("Hola mundo")

    auditor = Auditor()
=======
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
>>>>>>> d6acf5e99b542524df80e0777077921ebc5ad20c
    
    # 1. Cargar estado anterior (Snapshot)
    estado_anterior = {}
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, 'r') as f:
                estado_anterior = json.load(f)
        except:
            print("[Info] No se pudo leer el snapshot anterior o está vacío.")

<<<<<<< HEAD
    time.sleep(1.1) 
    
    
    with open(os.path.join(dir_prueba, "archivo1.txt"), "w") as f:
        f.write("Hola mundo modificado")
    
    
    with open(os.path.join(dir_prueba, "archivo2.txt"), "w") as f:
        f.write("Soy nuevo")
        
    print("\n--- Segunda Ejecución (Detectar cambios y nuevos) ---")
    nuevos, borrados, modificados = auditor.auditar(dir_prueba)
    print(f"Nuevos: {nuevos}")
    print(f"Borrados: {borrados}")
    print(f"Modificados: {modificados}")
=======
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
>>>>>>> d6acf5e99b542524df80e0777077921ebc5ad20c
