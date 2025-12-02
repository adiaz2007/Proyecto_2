import re
from utils import registrar_accion

def generador_lineas(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            for linea in f:
                yield linea
    except FileNotFoundError:
        print("El archivo no existe.")
        yield 

@registrar_accion
def analizar_contenido(ruta_archivo, buscar_emails=True):
    
    patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    resultados = []
    numero_linea = 0
    
    print(f"\n--- Analizando {ruta_archivo} ---")
    
    for linea in generador_lineas(ruta_archivo):
        numero_linea += 1
        
        if buscar_emails:
            coincidencias = re.findall(patron_email, linea)
            for email in coincidencias:
                resultados.append(f"Línea {numero_linea}: {email}")

    if resultados:
        print(f"Se encontraron {len(resultados)} emails:")
        for res in resultados[:10]: 
            print(res)
        if len(resultados) > 10:
            print("... y más.")
    else:
        print("No se encontraron coincidencias.")
        
    return resultados