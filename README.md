<h1 align="center">
    <br>
    MeteoRisk
    <br>
</h1>

<p align="center">
Aplicación Web con Fuentes de Datos Abiertos para Notificacones sobre Fenómenos Meteorológicos Adversos
</p>

## Descripción
MeteoRisk es un sistema de información que utiliza fuentes de datos abiertos para para tratar de enviar notificaciones a la población sobre fenómenos meteorolígicos adversos. En este repositorio de código encontrarás la prueba de concepto del proyecto. La aplicación ha sido creada con el lenguaje de programación **Python** versión 3.12.7 y como base de datos **MySQL** versión 9.1.0.
## Aspectos clave
* Extrae información de determinadas fuentes abiertas de datos, como pueden ser AEMET OpenData, los SAIH de las confederaciones hidrográficas y el portal de datos abiertos del Gobierno de España.
* Transforma los datos descargados y los convierte en información útil y manejable por el usuario.
* Analiza si se han rebasado determinados umbrales y en caso positivo, genera eventos que se convertirán en notificaciones dirigidas a los usuarios registrados.
## Base de datos
* Debes disponer de un servidor de bases de datos MySQL compatible con la version 9.1.0 o superior.
* Descarga el archivo **meteo_db.sql** e impórtalo en tu servidor.
* Descarga el archvio **insert_datos.sql*** e impórtalo en el servidor. El fichero contine los datos necesarios para realizar la prueba de concepto.
## Instalación 
* Edita el fichero **config.py** con los datos de conexión de tu servidor y con tu APY_KEY de la AEMET. 
* En el fichero **requirements.txt** encontrarás los paquetes necesarios del proyecto. Recomiendo crear un entorno virtual.
Ejecuta la siguiente instrucción en la línea de comandos:
```python
pip install -r requirements.txt
```
## Instrucciones de uso
Descarga los archivos del proyecto, incluidos los ficheros **CSV***, despliega la base de datos, configura los parámetros de tu servidor, copia tu APY_KEY y lanza la aplicación:
```python
py app.py
```
La aplicación está desarrollada en línea de comandos. Verás la siguiente información. A partir de ahora eres libre para ejecutar y probar la aplicación.
## Capturas de pantalla
### Interfaz de usuario en línea de comandos
![Screenshot 1](/img/imagen1.png)
### Evento por termperaturas máximas generado en un zona geográfica.
![Screenshot 2](/img/imagen2.png)
### Lista de los eventos de las últimas 24 horas.
![Screenshot 3](/img/imagen3.png)
<p align="center">
 Creado con mucho ❤️ por Alberto López Navarro en Valdepeñas
</p>
