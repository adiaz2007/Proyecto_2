import os
import json
import datetime
import time

def decorador_auditoria(funcion_original):
    """
    Decorador que registra el inicio y fin de la ejecución de una función
    en un archivo de log llamado 'audit.log'.
    """
    def envoltura(*argumentos, **kwargs):
        nombre_func = funcion_original.__name__
        hora_actual_inicio = datetime.datetime.now()
        
        with open("audit.log", "a", encoding='utf-8') as f:
            f.write(f"Iniciando [{nombre_func}] a las [{hora_actual_inicio}]\n")
        
        # EJECUTAR funcion_original
        resultado = funcion_original(*argumentos, **kwargs)
        
        hora_actual_fin = datetime.datetime.now()
        
        # ABRIR "audit.log" (modo append) para el cierre
        with open("audit.log", "a", encoding='utf-8') as f:
            f.write(f"Finalizado [{nombre_func}] a las [{hora_actual_fin}]\n")
        
        return resultado
    
    return envoltura

class Auditor:
    def tomar_snapshot_actual(self, ruta_directorio):
        """
        Recorre el directorio y crea un diccionario {archivo: fecha_modificacion}.
        """
        estado_actual = {}
        
        # Verificamos que la ruta exista para evitar errores
        if not os.path.exists(ruta_directorio):
            print(f"Error: El directorio {ruta_directorio} no existe.")
            return estado_actual

        # PARA archivo EN ruta_directorio
        for nombre_archivo in os.listdir(ruta_directorio):
            ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
            
            # Solo nos interesan archivos, no subcarpetas
            if os.path.isfile(ruta_completa):
                fecha_modificacion = os.path.getmtime(ruta_completa)
                estado_actual[nombre_archivo] = fecha_modificacion
                
        return estado_actual

    @decorador_auditoria
    def auditar(self, ruta_directorio):
        # 1. Cargar estado anterior
        # SI existe "snapshot.json"
        if os.path.exists("snapshot.json"):
            with open("snapshot.json", "r", encoding='utf-8') as f:
                try:
                    estado_anterior = json.load(f)
                except json.JSONDecodeError:
                    estado_anterior = {} # Si el archivo está corrupto o vacío
        else:
            estado_anterior = {}

        # 2. Obtener estado actual
        estado_actual = self.tomar_snapshot_actual(ruta_directorio)

        # 3. Comparar (Lógica de Conjuntos)
        claves_actuales = set(estado_actual.keys())
        claves_anteriores = set(estado_anterior.keys())

        # Archivos nuevos: están en actual PERO NO en anterior
        archivos_nuevos = list(claves_actuales - claves_anteriores)
        
        # Archivos borrados: están en anterior PERO NO en actual
        archivos_borrados = list(claves_anteriores - claves_actuales)
        
        # Archivos modificados
        archivos_modificados = []

        # PARA archivo EN estado_actual (Intersección para evitar key errors)
        archivos_comunes = claves_actuales.intersection(claves_anteriores)
        
        for archivo in archivos_comunes:
            # SI fechas son diferentes
            if estado_actual[archivo] != estado_anterior[archivo]:
                archivos_modificados.append(archivo)

        # 4. Guardar nuevo estado
        with open("snapshot.json", "w", encoding='utf-8') as f:
            json.dump(estado_actual, f, indent=4)

        return (archivos_nuevos, archivos_borrados, archivos_modificados)

# --- BLOQUE DE PRUEBA (Para ejecutar el código) ---
if __name__ == "__main__":
    # Crear un directorio de prueba si no existe
    dir_prueba = "carpeta_prueba"
    if not os.path.exists(dir_prueba):
        os.makedirs(dir_prueba)
        # Crear un archivo inicial
        with open(os.path.join(dir_prueba, "archivo1.txt"), "w") as f:
            f.write("Hola mundo")

    auditor = Auditor()
    
    print("--- Primera Ejecución (Debería detectar archivo1 como nuevo) ---")
    nuevos, borrados, modificados = auditor.auditar(dir_prueba)
    print(f"Nuevos: {nuevos}")
    print(f"Borrados: {borrados}")
    print(f"Modificados: {modificados}")

    # Simular cambios
    time.sleep(1.1) # Pausa para asegurar cambio de timestamp
    
    # 1. Modificar archivo existente
    with open(os.path.join(dir_prueba, "archivo1.txt"), "w") as f:
        f.write("Hola mundo modificado")
    
    # 2. Crear archivo nuevo
    with open(os.path.join(dir_prueba, "archivo2.txt"), "w") as f:
        f.write("Soy nuevo")
        
    print("\n--- Segunda Ejecución (Detectar cambios y nuevos) ---")
    nuevos, borrados, modificados = auditor.auditar(dir_prueba)
    print(f"Nuevos: {nuevos}")
    print(f"Borrados: {borrados}")
    print(f"Modificados: {modificados}")