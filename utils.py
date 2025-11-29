import os
import datetime


def registrar_accion(funcion):

    def envoltura(*args, **kwargs):
        # Escribir inicio en el log
        with open("audit.log", "a", encoding="utf-8") as f:
            f.write(f"[INFO] Iniciando {funcion.__name__} - {datetime.datetime.now()}\n")
        
        # Ejecutar la función original
        resultado = funcion(*args, **kwargs)
        
        # Escribir fin en el log
        with open("audit.log", "a", encoding="utf-8") as f:
            f.write(f"[INFO] Finalizado {funcion.__name__} - {datetime.datetime.now()}\n")
        
        return resultado
    return envoltura

def validar_ruta(ruta):
    return os.path.exists(ruta) and os.path.isdir(ruta)