"""
app.py

@date: 2025-07-05
@author: Alberto López Navarro
@version: 1.0
@description: Este script es la interfaz principal de la aplicación Meteo Risk, que permite interactuar con la base de datos y realizar diversas operaciones relacionadas con la meteorología.

"""
import config
import pandas as pd
from crud import *
from etl_aemet import *
import os


# Ejemplo de uso
if __name__ == "__main__":
   
    resetear_log('bd.log')  # Reiniciar el log
    con = crear_conexion(config.DB_CONFIG) # Crear la conexión a la base de datos
    
    # Las tablas maestras de municipio y estaciones ya están creadas en sendos ficheros CSV.
    df_municipios = pd.read_csv("municipios.csv")
    df_estaciones = pd.read_csv("estaciones.csv")

    def limpiar_pantalla():
        os.system('cls')

    # Crear un pequeño menú de opciones en linea de comandos 
    def mostrar_menu():
        print('*******************************************************')
        print('*** METEO RISK - Información y notificaciones meteo ***')
        print('*******************************************************')
        print('Tareas iniciales:')
        print('1.- Cargar tablas maestras: OK')
        '''if comprobar_api_key(configuracion.API_KEY):
            print('2.- Comprobar conexión AEMET: Conexión API AEMET correcta.') 
        else:
            print('2.- Comprobar conexión AEMET: Problemas de conexión a la API de la AEMET')
            exit (1)'''
        print('*******************************************************')
        print('MENU DE OPCIONES:')
        print('[1] Listar ZONAS de interés de la aplicación')
        print('[2] Listar VARIABLES disponibles')
        print('[3] Actualizar DATOS de fuente AEMET')
        print('[4] Consultar EVENTOS recientes (últimas 24 horas)')
        print('[5] BORRAR tabla Datos y Eventos')
        print('---------------------------------------------------------')
        print('[0] SALIR DEL PROGRAMA')
        print('*******************************************************')

    # Bucle para mostrar el menú y procesar la opción seleccionada

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Selecciona una opción: ')
       
        if opcion == '1':
            print('ZONAS de interes de la aplicacion:')
            print ('CODIGO, NOMBRE, PROVINCIA')
            consulta = "SELECT codigo, nombre, provincia FROM zona"
            registros = consultar_registros(con, consulta)
            for registro in registros:
                print(registro)
       
        elif opcion == '2':
            print('VARIABLES_METEO disponibles:')
            print ('ID, NOMBRE, UNIDAD, CODIGO ZONA, ZONA, PROVINCIA')
            consulta = "SELECT v.var_id, v.nombre, v.unidad, z.codigo, z.nombre, z.provincia " \
                "FROM zona z, variable v " \
                "WHERE z.zon_id = v.zon_id"
            registros = consultar_registros(con, consulta)
            for registro in registros:
                print(registro)

        elif opcion == '3':
            print('Actualizando datos de una variable:')
            var_id = input('Introduce el ID de la variable a actualizar: ')
            if not var_id.isdigit():
                print('ID de variable no válido. Debe ser un número entero.')
                continue
            var_id = int(var_id)
            print(f'Actualizando variable con ID {var_id}...')  
            actualizar_variable(var_id, con, municipios='municipios', estaciones='estaciones',imprimir=True)
       
        elif opcion == '4':
            print('Eventos ocurridos en las últimas 24 horas:')
            consulta = "SELECT e.var_id, v.nombre, z.nombre, e.fecha, e.descripcion " \
                       "FROM evento e, variable v, zona z " \
                       "WHERE e.var_id = v.var_id AND v.zon_id = z.zon_id AND e.fecha >= NOW() - INTERVAL 1 DAY " \
                       "ORDER BY e.fecha DESC"
            registros = consultar_registros(con, consulta)
            for registro in registros:
                fecha = registro[3]
                if isinstance(fecha, str):
                    fecha = datetime.fromisoformat(fecha)  # Convierte si es string ISO
                fecha_formateada = fecha.strftime('%Y-%m-%d %H:%M')
                print(f"Var: {registro[1]} - Zona: {registro[2]} - Fecha: {fecha_formateada} - Evento: {registro[4]}")

        elif opcion == '5':
            #Pido confirmación para borrar las tablas
            confirmacion = input('¿Estás seguro de que quieres borrar los datos de las tablas Datos y Eventos? (S/N): ').lower()
            if confirmacion == 's':
                print('Borrando datos de las tablas Datos y Eventos...')
                eliminar_registro(con, 'datos')
                eliminar_registro(con, 'evento')
                print('Datos borrados correctamente.')
            else:
                print('Operación cancelada. No se han borrado los datos.')  
                      
        elif opcion == '0':
            print('Saliendo...')
            exit(0)
        else:
            # Opción no válida, muestra mensaje de opcion no válida y pregnta de nuevo por una opción
            print('Opción no válida. Por favor, selecciona una opción del menú.')
            opcion = input('Selecciona una opción: ')

        # Pregunta si se desea volver al menú principal 
        volver = input('\n¿Deseas volver al menú principal? (S/N): ').lower()
        if volver != 's':
            print('Hasta pronto.')
            break