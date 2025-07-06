"""
etl_aemet.py

@date: 2025-06-01
@author: Alberto López Navarro
@version: 1.0
@description: ETL para interactuar con la API de AEMET y obtener datos meteorológicos.
"""
"""
Lista de funciones:
- comprobar_api_key: Comprueba si una API key de AEMET es válida.
- create_master_municipios: Crea un CSV con el maestro de municipios de AEMET.
- create_master_estaciones: Crea un CSV con el maestro de estaciones de AEMET.
- get_municipios_zona: Obtiene los municipios de una zona específica.
- get_estaciones_provincia: Obtiene las estaciones meteorológicas de una provincia.
- get_estaciones: Obtiene las estaciones meteorológicas de una zona y provincia.    
- get_observacion_zona: Obtiene las observaciones meteorológicas de una zona específica.
- actualizar_variable: Actualiza los datos de una variable meteorológica en la base de datos.
- analizar_dato: Analiza el valor de una variable meteorológica y registra un evento si se supera un umbral.
- imprimir_observacion: Imprime la temperatura máxima más reciente de una observación.
"""
import requests
import pandas as pd
import time
from crud import *
import datetime

from config import *

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIgYWxiZXJ0by5sb3BlejA1MUBjb211bmlkYWR1bmlyLm5ldCIsImp0aSI6IjNkYzcwZWU0LTk5MzYtNGRkOS04ZGJiLTE4MzBhZTQ0MTQ5ZCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQ5MjI4MTk3LCJ1c2VySWQiOiIzZGM3MGVlNC05OTM2LTRkZDktOGRiYi0xODMwYWU0NDE0OWQiLCJyb2xlIjoiIn0.-yh8FwjmlIx6kHULWln5qiR1ipvPOTj85OnTUNSnbu4"

def comprobar_api_key(api_key: str) -> bool:
    """
    Comprueba si una API key de AEMET es válida realizando una petición de prueba.

    Parametros:
        api_key (str): Clave de acceso a la API de AEMET.
    Devuelve:
        bool: True si la API key es válida, False en caso contrario.
    """
    url = "https://opendata.aemet.es/opendata/api/maestro/municipios"
    headers = {"accept": "application/json", "api_key": api_key}
    
    try:
        logging.info("Comprobando validez de la API Key...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("API Key válida.")
        return True
    except requests.exceptions.HTTPError as http_err:
        logging.error("Error HTTP al comprobar la API Key: %s", http_err)
    except requests.exceptions.RequestException as req_err:
        logging.error("Error de conexión al comprobar la API Key: %s", req_err)
    except Exception as e:
        logging.exception("Error inesperado al comprobar la API Key.")
    
    return False
    
def create_master_municipios(api_key):
    """
    Crea un CSV con el maestro de municipios de AEMET.

    Parámetros:
        api_key (str): Clave de acceso a la API de AEMET.
    Devuelve:    
        None: La función no devuelve nada, pero crea un archivo CSV llamado 'municipios.csv'.
    Excepciones:
       requests.exceptions.HTTPError: Si hay un error al realizar la solicitud a la API.
    """
    logging.info("Creando maestro de municipios...")
    url = "https://opendata.aemet.es/opendata/api/maestro/municipios"
    headers = {"accept": "application/json", "api_key": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    datos_url = response.json()["datos"]

    # Descargar los datos reales
    municipios_response = requests.get(datos_url)
    municipios_response.raise_for_status()
    municipios = municipios_response.json()

    # Convertir a DataFrame
    df = pd.DataFrame(municipios)
    
    df.to_csv("municipios.csv", index=False, encoding="utf-8-sig")

def create_master_estaciones(api_key):
    """
    Crea un CSV con el maestro de estaciones de AEMET.
    Parámetros:
        api_key (str): Clave de acceso a la API de AEMET.
    Devuelve:
        None: La función no devuelve nada, pero crea un archivo CSV llamado 'estaciones.csv'.
    Excepciones:
        requests.exceptions.HTTPError: Si hay un error al realizar la solicitud a la API.
    """
    logging.info("Creando maestro de estaciones...")
    # Obtener el listado de todas las estaciones
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

    headers = {"accept": "application/json", "api_key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    datos_url = response.json()["datos"]

    # Descargar los datos reales
    estaciones_response = requests.get(datos_url)
    estaciones_response.raise_for_status()
    estaciones = estaciones_response.json()

    # Convertir a DataFrame y exportar a csv
    df = pd.DataFrame(estaciones)

    df.to_csv("estaciones.csv", index=False, encoding="utf-8-sig")

def get_municipios_zona(zona_id, api_key, file=None):
    """
    Obtiene los municipios de una zona específica a partir de un DataFrame de municipios o desde la API de AEMET.
    
    Parámetros:
        zona_id (str): ID de la zona geográfica.
        api_key (str): Clave de acceso a la API de AEMET.
        file (str, opcional): Nombre del archivo CSV con el maestro de municipios. Si es None, se usa la API.
    Devuelve:
        df (DataFrame): DataFrame con los municipios de la zona.
        coste (float): Tiempo en segundos que ha tardado la operación.
    Excepciones:
        requests.exceptions.HTTPError: Si hay un error al realizar la solicitud a la API.
    """
    inicio = time.time()
    
    if file != None:
        # Cargar el maestro de municipios desde un archivo CSV
        df = pd.read_csv(file + ".csv", encoding="utf-8-sig")
        df["zona_comarcal"] = df["zona_comarcal"].astype(str)
    else:
        # Obtener el listado de municipios desde la API de AEMET  
        url = "https://opendata.aemet.es/opendata/api/maestro/municipios"
    
        headers = {"accept": "application/json", "api_key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        datos_url = response.json()["datos"]

        # Descargar los datos reales
        municipios_response = requests.get(datos_url)
        municipios_response.raise_for_status()
        municipios = municipios_response.json()

        # Convertir a DataFrame
        df = pd.DataFrame(municipios)
        print(df)
    
    # Filtrar municipios por zona_comarcal=zona_id
    df = df[df['zona_comarcal'] == zona_id]

    # Eliminar columnas innecesarias
    df = df.drop(['latitud','id_old','url','latitud_dec','capital','longitud_dec','longitud'], axis=1)

    fin = time.time()

    coste =round((fin - inicio), 2)  # Tiempo en segundos

    return df, coste

def get_estaciones_provincia(provincia, api_key, file = None):
    """
    Obtiene las estaciones meteorológicas de una provincia específica a partir de un DataFrame de estaciones o desde la API de AEMET.

    Parámetros:
        provincia (str): Nombre de la provincia para filtrar las estaciones.
        api_key (str): Clave de acceso a la API de AEMET.
        file (str, opcional): Nombre del archivo CSV con el maestro de estaciones. Si es None, se usa la API.
    Devuelve:
        df (DataFrame): DataFrame con las estaciones de la provincia.
        coste (float): Tiempo en segundos que ha tardado la operación.
    Excepciones:
        requests.exceptions.HTTPError: Si hay un error al realizar la solicitud a la API.
    """
    logging.info(f"Obteniendo estaciones de la provincia: {provincia}")
    inicio = time.time()
    
    if file != None:
        # Cargar el maestro de estaciones desde un archivo CSV
        df = pd.read_csv(file + ".csv", encoding="utf-8-sig")
        #df["zona_comarcal"] = df["zona_comarcal"].astype(str)
    else:
        # Obtener el listado de todas las estaciones
        url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

        headers = {"accept": "application/json", "api_key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        datos_url = response.json()["datos"]

        # Descargar los datos reales
        estaciones_response = requests.get(datos_url)
        estaciones_response.raise_for_status()
        estaciones = estaciones_response.json()

        # Convertir a DataFrame
        df = pd.DataFrame(estaciones)

    # Filtrar estaciones por provincia
    df = df[df['provincia'] == provincia]

    # Eliminar columnas innecesarias
    df = df.drop(['latitud','indsinop','longitud'], axis=1)
    fin = time.time()
    coste =round((fin - inicio), 2)  # Tiempo en segundos
    return df, coste

def get_estaciones(zona_id :str, provincia : str, api_key : str, municipios = None, estaciones = None):
    """
    Cruza los municipios de una zona con las estaciones de una provincia según el campo 'nombre'.
    
    Parámetros:
        zona_id (str): ID de la zona geográfica.
        provincia (str): Nombre de la provincia para filtrar las estaciones.
        api_key (str): Clave de acceso a la API de AEMET.
        municipios (list[str], opcional): Lista de nombres de municipios a filtrar. Si es None, se obtienen todos los municipios de la zona.        
        estaciones (list[str], opcional): Lista de nombres de estaciones a filtrar. Si es None, se obtienen todas las estaciones de la provincia.
    Devuvelve:
        df (DataFrame): DataFrame resultante del cruce de datos.
        coste (float): Tiempo en segundos que ha tardado la operación.
    Excepciones:
        ValueError: si no se encuentra ninguna coincidencia entre municipios y estaciones.
        Exception: si ocurre cualquier otro error durante la ejecución.
    """
    inicio = time.time()
    try:
        df_municipios, _ = get_municipios_zona(zona_id, api_key, municipios)
        df_municipios['nombre'] = df_municipios['nombre'].str.upper()
        logging.info(f"Obtenidos {len(df_municipios)} municipios para zona {zona_id}.")

        df_estaciones, _ = get_estaciones_provincia(provincia, api_key, estaciones)
        logging.info(f"Obtenidas {len(df_estaciones)} estaciones para provincia {provincia}.")

        df_resultado = pd.merge(df_municipios, df_estaciones, on='nombre', how='inner')

        if df_resultado.empty:
            logging.warning("No se encontraron coincidencias entre municipios y estaciones.")
            raise ValueError("No hay coincidencias entre los municipios de la zona y las estaciones de la provincia.")

        coste = round(time.time() - inicio, 2)
        logging.info(f"Proceso completado en {coste} segundos. Coincidencias: {len(df_resultado)}.")
        return df_resultado, coste

    except ValueError as ve:
        logging.error(f"Error de cruce de datos: {ve}")
        raise

    except Exception as e:
        logging.exception("Error inesperado al obtener las estaciones.")
        raise RuntimeError("Error inesperado durante la obtención de estaciones.") from e

def get_observacion_zona(zonas, api_key : str):
    """
    Obtiene las observaciones meteorológicas de una zona específica a partir de un DataFrame de zonas.

    Parámetros:
        zonas (DataFrame): DataFrame que contiene las zonas con sus respectivos 'indicativo'.
        api_key (str): Clave de acceso a la API de AEMET.
    Devuelve:
        df (DataFrame): DataFrame con las observaciones meteorológicas de las estaciones de la zona.
    Excepciones:
        requests.exceptions.HTTPError: Si hay un error al realizar la solicitud a la API.
    """
    start_time = time.time()
    observaciones_total = []

    for _, row in zonas.iterrows():
        indicativo = row.get("indicativo")
        if not indicativo:
            logging.warning("Fila sin 'indicativo', se omite.")
            continue

        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{indicativo}"
        headers = {"accept": "application/json", "api_key": api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            datos_url = response.json().get("datos")

            if not datos_url:
                logging.warning(f"No se encontró la URL de datos para la estación {indicativo}")
                continue

            datos = requests.get(datos_url)
            datos.raise_for_status()
            df_estacion = pd.DataFrame(datos.json())

            if df_estacion.empty:
                logging.info(f"La estación {indicativo} no devolvió observaciones.")
            else:
                observaciones_total.append(df_estacion)
                logging.info(f"Estación {indicativo} procesada con éxito.")

        except requests.exceptions.HTTPError as http_err:
            logging.warning(f"HTTP error con estación {indicativo}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.warning(f"Error de conexión con estación {indicativo}: {req_err}")
        except Exception as err:
            logging.error(f"Error inesperado con estación {indicativo}: {err}")

    if observaciones_total:
        df_resultado = pd.concat(observaciones_total, ignore_index=True)
    else:
        df_resultado = pd.DataFrame()
        logging.warning("No se obtuvo ninguna observación válida.")

    duration = round(time.time() - start_time, 2)
    logging.info(f"Finalizado. Tiempo total: {duration} segundos.")
    return df_resultado

def imprimir_observacion(df):
    """
    Imprime la temperatura máxima más reciente de una observación y su ubicación.
    Parámetros:
        df (DataFrame): DataFrame que contiene las observaciones meteorológicas.
    Devuelve:
        None: La función no devuelve nada, pero imprime la información en la consola.
    Excepciones:
        ValueError: Si el DataFrame está vacío o no contiene las columnas necesarias.
    """
    
    #Me quedos solo con las columnas idema, ubi ta tamax y fecha_local
    df = df[['idema', 'ubi','ta', 'tamax', 'fecha_local']]

    # Escribir por pantalla la termperatura maxima mas reciente, y decir de donde es.
    print("****************************")
    print("Temperatura MAXIMA:", df.iloc[0]['tamax'], "ºC en la estación de", df.iloc[0]['ubi'], "a las", df.iloc[0]['fecha_local'].strftime('%Y-%m-%d %H:%M'))
    print("Temperatura actual:", df.iloc[0]['ta'], "ºC (puede ser inferior a la máxima)")
    print("****************************")

def analizar_dato(var_id : str, dato : float, bd, fecha : datetime):    
    """
    Analiza el valor de una variable meteorológica y registra un evento si se supera un umbral.
    
    Parámetros:
        var_id (str): ID de la variable meteorológica.
        dato (float): Valor de la variable a analizar.
        fecha (date): Fecha del dato.
    Devuelve:
        None: La función no devuelve nada, pero registra eventos si es necesario.
    """
    consulta = "SELECT * FROM variable WHERE var_id = " + str(var_id)
    resultado = consultar_registros(bd, consulta) 
    if not resultado:
        raise ValueError(f"No se encontró la variable con ID {var_id}") 
    if resultado[0][2] == 'tamax':
        umbral_superior = resultado[0][6]
        
    if dato >= umbral_superior:
        evento = {
            "var_id": var_id,
            "fecha": fecha,
            "descripcion": f"Riesgo por temp. MAXIMAS: {dato} ºC",
            "validado": 0
        }
        insertar_registro(bd, 'evento', evento)
        print(f"¡¡ Evento registrado !! {evento['descripcion']}", "(Umbral "  + str(umbral_superior) + " ºC superado.)")
    else:
        print(f"No se ha registrado evento. Valor {dato} por debajo del umbral {umbral_superior} ºC.")

def actualizar_variable(var_id: str, bd, municipios: str = None, estaciones: str = None, imprimir: bool = False) -> None:
    """
    Actualiza los datos de una variable meteorológica en la base de datos.
    
    Parámetros:
        var_id (str): ID de la variable meteorológica a actualizar.
        bd: Conexión a la base de datos.
        municipios (str, opcional): Nombre del archivo CSV con el maestro de municipios. Si es None, se usa el maestro por defecto.
        estaciones (str, opcional): Nombre del archivo CSV con el maestro de estaciones. Si es None, se usa el maestro por defecto.
        imprimir (bool, opcional): Si es True, imprime la observación más reciente. Por defecto es False.
    Devuelve:
        None: La función no devuelve nada, pero imprime información sobre la actualización.
    Excepciones:
        ValueError: Si no se encuentra la variable con el ID proporcionado.
        Exception: Si ocurre cualquier otro error durante la actualización.
    """

    consulta = "SELECT z.codigo,z.provincia,z.nombre FROM variable v, zona z WHERE v.zon_id = z.zon_id AND v.var_id = " + str(var_id)
    resultado = consultar_registros(bd, consulta) 
    
    zona = resultado[0] if resultado else None
    print(f"Zona de la variable {var_id}: {zona[0]}")
    print(f"Nombre de la zona {var_id}: {zona[2]}")
    print(f"Provincia de la variable {var_id}: {zona[1]}")

    zona_id = zona[0]
    provincia = zona[1].upper()

    try:
        df1, coste = get_estaciones(zona_id, provincia, API_KEY, municipios, estaciones)
    except ValueError as e:
        logging.warning(f"No existen estaciones en la zona {zona_id}: {e}")
        print("****************************")
        print("NO EXISTEN ESTACIONES DE OBSERVACIÓN EN LA ZONA: ", zona_id)
        print("****************************")
        return

    df = get_observacion_zona(df1, API_KEY)
    if df.empty:
        logging.warning(f"No se obtuvieron observaciones para la zona {zona_id}")
        print("****************************")
        print("NO se obtuvieron datos en ala ZONA: ", zona_id)
        print("****************************")
        return

    # Convertir la columna 'fint' a datetime con zona horaria
    try:
        df['fint'] = pd.to_datetime(df['fint'], format="%Y-%m-%dT%H:%M:%S%z", errors='coerce')
        df = df.dropna(subset=['fint'])
        df['fecha_local'] = df['fint'].dt.tz_convert('Europe/Madrid')
    except Exception as e:
        logging.error(f"Error procesando fechas: {e}")
        return 

    # Ordenar por fecha local, me quedo solo con las 5 últimas observaciones y la temperatura máxima
    df = df.sort_values(by='fecha_local', ascending=False, ignore_index=True)
    df = df.head(5) 
    # Me quedo solo con la temperatura máxima
    df = df[df['tamax'] == df['tamax'].max()]

    if df.empty:
        logging.warning("No hay datos válidos para insertar.")
        return

     # Preparo el dato para insertar en la tabla 'datos'
    d1 = {
        "var_id": var_id,
        "fue_id": 1,
        "fecha": df.iloc[0]['fecha_local'],
        "valor": float(df.iloc[0]['tamax'])
    }

    # Inserto el dato en la base de datos
    insertar_registro(bd, 'datos', d1)
    
    if imprimir:
        imprimir_observacion(df)

    # Analizo el dato, por si se genera un evento
    analizar_dato(var_id, d1['valor'], bd, d1['fecha'])