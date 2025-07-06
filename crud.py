# crud.py
# FICHERO CON LAS FUNCIONES CRUD (Create, Read, Update, Delete) PARA MANIPULAR LA BASE DE DATOS

"""
@date: 2025-06-01
@author: Alberto López Navarro
@version: 1.0
@description: Este módulo contiene funciones CRUD (Create, Read, Update, Delete) para interactuar con una base de datos MySQL.
"""
"""
Lista de funciones:
- crear_conexion: Establece una conexión a la base de datos.
- cerrar_conexion: Cierra una conexión activa a la base de datos.
- insertar_registro: Inserta un nuevo registro en una tabla.
- leer_registros: Recupera todos los registros de una tabla.
- consultar_registros: Ejecuta una consulta SQL y devuelve los resultados.
- actualizar_registro: Actualiza uno o varios registros de una tabla.
- eliminar_registro: Elimina uno o varios registros de una tabla.
- consulta_a_dataframe: Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de pandas.
"""

import mysql.connector
from config import *
import pandas as pd

# CREAR una conexión a la base de datos
def crear_conexion(config):
    """
    Establece una conexión con la base de datos utilizando los parámetros especificados.

    Parámetros:
        config (dict): Diccionario con los parámetros de conexión. Debe incluir las claves:
                       'host', 'user', 'password' y 'database'.

    Retorna:
        conexion (obj): Objeto de conexión si es exitosa; None en caso de error.

    El resultado de la operación se registra en el archivo de log 'bd.log'.
    """
    try:
        # Intento de conexión con los parámetros proporcionados
        conexion = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        # Log de éxito
        logging.info("Conexión exitosa a la base de datos.")
        return conexion

    except mysql.connector.Error as err:
        # Log del error con detalle del mensaje proporcionado por el conector
        logging.error(f"Error al conectar con la base de datos: {err}")
        return None
    
# CERRAR la conexión a la base de datos
def cerrar_conexion(conexion):
    """
    Cierra una conexión activa con la base de datos, si está abierta.

    Parámetros:
        conexion (obj): Objeto de conexión a la base de datos, compatible con el método is_connected().

    Este procedimiento verifica si la conexión está activa antes de intentar cerrarla.
    Registra el resultado en un archivo de log, incluyendo errores si ocurren durante el proceso.
    """
    try:
        if conexion and conexion.is_connected():
            conexion.close()  # Cierra la conexión si está activa
            logging.info("Conexión a la base de datos cerrada correctamente.")
        else:
            logging.info("La conexión a la base de datos ya estaba cerrada o es nula.")
    except Exception as error:
        logging.error(f"Error al intentar cerrar la conexión: {error}")

# INSERTAR un nuevo registro
def insertar_registro(conexion, tabla, datos):
    """
    Inserta un nuevo registro en la tabla especificada de la base de datos.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        tabla (str): Nombre de la tabla en la que se desea insertar el registro.
        datos (dict): Diccionario con los datos a insertar, donde las claves son los nombres
                      de las columnas y los valores los correspondientes datos.

    Retorna:
        int: ID del nuevo registro insertado si la operación fue exitosa.
        None: Si ocurrió un error durante la inserción.

    Observaciones:
        - La operación se registra en el archivo de log 'bd.log'.
        - Usa parámetros preparados para evitar inyecciones SQL.
    """
    try:
        cursor = conexion.cursor()

        # Construcción dinámica de columnas y placeholders (%s)
        columnas = ', '.join(datos.keys())
        placeholders = ', '.join(['%s'] * len(datos))
        consulta_sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"

        # Ejecutar la inserción con los valores
        cursor.execute(consulta_sql, tuple(datos.values()))
        conexion.commit()

        nuevo_id = cursor.lastrowid
        logging.info(f"Registro insertado correctamente en '{tabla}' con ID {nuevo_id}.")
        return nuevo_id

    except Exception as error:
        logging.error(f"Error al insertar en la tabla '{tabla}': {error}")
        return None

# READ: Leer registros
def leer_registros(conexion, tabla):
    """
    Recupera todos los registros almacenados en una tabla específica de la base de datos.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        tabla (str): Nombre de la tabla de la cual se desean obtener los registros.

    Retorna:
        list: Lista de tuplas que representan los registros encontrados.
              Si ocurre un error, se devuelve una lista vacía.

    Detalles:
        - El resultado se registra en el log 'bd.log'.
        - En caso de error, se captura la excepción y se registra el motivo.
    """
    try:
        cursor = conexion.cursor()
        consulta = f"SELECT * FROM {tabla}"
        cursor.execute(consulta)

        registros = cursor.fetchall()
        logging.info(f"Consulta realizada correctamente en la tabla '{tabla}' ({len(registros)} registros recuperados).")
        return registros

    except Exception as error:
        logging.error(f"Error al leer registros de la tabla '{tabla}': {error}")
        return []

# CONSULTAR: Ejecutar una consulta SQL
def consultar_registros(conexion, consulta):
    """
    Ejecuta una consulta SQL arbitraria y devuelve todos los resultados obtenidos.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        consulta (str): Consulta SQL en formato texto que se desea ejecutar.

    Retorna:
        list: Lista de tuplas con los registros recuperados.
              Devuelve una lista vacía si la consulta falla.

    Observaciones:
        - Esta función permite realizar consultas complejas sin estar limitadas a una sola tabla.
        - Los resultados y errores se registran en el archivo de log 'bd.log'.
    """
    try:
        cursor = conexion.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        logging.info(f"Consulta ejecutada correctamente: '{consulta}' ({len(resultados)} registros recuperados).")
        return resultados

    except Exception as error:
        logging.error(f"Error al ejecutar la consulta '{consulta}': {error}")
        return []
   
# UPDATE: Actualizar registros
def actualizar_registro(conexion, nombre_tabla, nuevos_datos, condicion=None):
    """
    Modifica uno o varios registros de una tabla en función de una condición SQL opcional.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        nombre_tabla (str): Nombre de la tabla en la que se desea realizar la actualización.
        nuevos_datos (dict): Diccionario con los campos como claves y los nuevos valores como valores.
        condicion (str, opcional): Expresión SQL que define la cláusula WHERE (sin incluir la palabra clave 'WHERE').
                                   Si no se proporciona, se actualizarán todos los registros de la tabla.

    Retorna:
        int: Número de registros modificados si la operación es exitosa.
             En caso de error, se devuelve 0 y se registra el fallo en el log.

    Nota:
        - Se registra un aviso en el log si la actualización se hace sin condición.
    """
    try:
        cursor = conexion.cursor()

        # Genera la parte de asignación: campo1 = %s, campo2 = %s, ...
        asignaciones = ', '.join([f"{columna} = %s" for columna in nuevos_datos])

        # Arma la sentencia SQL con o sin condición
        if condicion:
            consulta_sql = f"UPDATE {nombre_tabla} SET {asignaciones} WHERE {condicion}"
        else:
            consulta_sql = f"UPDATE {nombre_tabla} SET {asignaciones}"
            logging.warning(f"Actualización sin condición en la tabla '{nombre_tabla}'. Se modificarán todos los registros.")

        # Ejecutar la consulta
        valores = tuple(nuevos_datos.values())
        cursor.execute(consulta_sql, valores)
        conexion.commit()

        registros_afectados = cursor.rowcount
        logging.info(f"{registros_afectados} registro(s) actualizado(s) en la tabla '{nombre_tabla}'" +
                     (f" con condición: {condicion}." if condicion else " sin condición."))

        return registros_afectados

    except Exception as error:
        logging.error(f"Error al actualizar registros en la tabla '{nombre_tabla}': {error}")
        return 0

# DELETE: Borrar registros
def eliminar_registro(conexion, nombre_tabla, condicion=None):
    """
    Elimina uno o varios registros de una tabla en función de una condición opcional.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        nombre_tabla (str): Nombre de la tabla de la que se desean eliminar registros.
        condicion (str, opcional): Condición SQL que define la cláusula WHERE (sin incluir la palabra clave 'WHERE').
                                   Si no se proporciona, se eliminarán todos los registros de la tabla.

    Retorna:
        int: Número de registros eliminados. En caso de error, se devuelve 0.

    La operación se registra en el archivo de log 'bd.log'.
    """
    try:
        cursor = conexion.cursor()

        # Construye la consulta SQL según haya condición o no
        if condicion:
            consulta_sql = f"DELETE FROM {nombre_tabla} WHERE {condicion}"
        else:
            consulta_sql = f"DELETE FROM {nombre_tabla}"

        # Ejecuta la consulta
        cursor.execute(consulta_sql)
        conexion.commit()

        registros_eliminados = cursor.rowcount

        # Log informativo según se use o no condición
        if condicion:
            logging.info(f"{registros_eliminados} registro(s) eliminado(s) de la tabla '{nombre_tabla}' con condición: {condicion}.")
        else:
            logging.warning(f"Eliminación sin condición: {registros_eliminados} registro(s) eliminado(s) de la tabla '{nombre_tabla}'.")

        return registros_eliminados

    except Exception as error:
        logging.error(f"Error al eliminar registros de la tabla '{nombre_tabla}': {error}")
        return 0

# PANDAS: A patir de SELECT SQL devuelve un dataframe de pandas
def consulta_a_dataframe(conexion, consulta_sql):
    """
    Ejecuta una consulta SELECT sobre la base de datos y devuelve los resultados en un DataFrame de pandas.

    Parámetros:
        conexion (obj): Objeto de conexión activo a la base de datos.
        consulta_sql (str): Cadena de texto con la consulta SELECT a ejecutar.

    Retorna:
        pd.DataFrame: Objeto DataFrame con los resultados de la consulta.
                      Si ocurre un error, se devuelve un DataFrame vacío.

    Observaciones:
        - Esta función está orientada a facilitar el análisis exploratorio de datos (AED).
        - Se registran tanto las consultas exitosas como los errores en el archivo de log 'bd.log'.
    """
    try:
        cursor = conexion.cursor()
        cursor.execute(consulta_sql)

        # Obtener nombres de columnas desde la descripción del cursor
        columnas = [col[0] for col in cursor.description]

        # Recuperar todos los registros
        datos = cursor.fetchall()

        # Crear el DataFrame con los datos y columnas obtenidas
        df = pd.DataFrame(datos, columns=columnas)

        logging.info(f"Consulta convertida a DataFrame correctamente. Filas: {len(df)}. Consulta: {consulta_sql}")
        return df

    except Exception as error:
        logging.error(f"Error al ejecutar la consulta para DataFrame: {error} | Consulta: {consulta_sql}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío si hay error