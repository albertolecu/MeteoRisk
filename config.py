"""
configuracion.py
@date: 2025-07-05
@author: Alberto López Navarro
@version: 1.0
@description: Este script contiene la configuración necesaria para la aplicación Meteo Risk, incluyendo la conexión a la base de datos, \
      la API Key de AEMET y un par de funciones para controlar el log de acciones del sistema..
"""
import logging

# Parámetros de conexión con la base de datos MySQL
DB_CONFIG = {
    'host':     'la_ip_de_tu_host',
    'user':     'tu_user',
    'password': 'tu_pass',
    'database': 'meteo_db'
}

# API Key de AEMET
API_KEY = "el_texto_de_tu_API_KEY_de_la_AEMET"

# Configuración básica del sistema de logging
logging.basicConfig(
    filename='bd.log',               # Archivo donde se guardan los logs
    level=logging.INFO,              # Nivel mínimo que se registra
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del mensaje
    datefmt='%Y-%m-%d %H:%M:%S'      # Formato de la fecha/hora
)

def mostrar_log(ruta_log='bd.log'):
    """
    Muestra por consola el contenido del archivo de log.

    Parámetros:
        ruta_log (str): Ruta del archivo de log. Por defecto, 'bd.log'.
    """
    try:
        with open(ruta_log, 'r', encoding='latin-1') as archivo:
            print("\n=== CONTENIDO DEL LOG ===\n")
            print(archivo.read())
    except FileNotFoundError:
        print(f"El archivo de log '{ruta_log}' no existe todavía.")
    
def resetear_log(ruta_log='bd.log'):
    """
    Vacía el contenido del archivo de log.

    Parámetros:
        ruta_log (str): Ruta del archivo de log. Por defecto, 'bd.log'.
    """
    with open(ruta_log, 'w', encoding='utf-8') as archivo:
        archivo.write("")  # Borra el contenido
    print(f"Log reiniciado: {ruta_log}")