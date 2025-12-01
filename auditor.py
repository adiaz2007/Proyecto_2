import os
import json
import datetime
import time

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
    
    print("--- Primera Ejecución (Debería detectar archivo1 como nuevo) ---")
    nuevos, borrados, modificados = auditor.auditar(dir_prueba)
    print(f"Nuevos: {nuevos}")
    print(f"Borrados: {borrados}")
    print(f"Modificados: {modificados}")

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