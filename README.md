<h1 align="center">
    <br>
    MeteoRisk
    <br>
</h1>

<p align="center">
<b>Aplicación Web con Fuentes de Datos Abiertos para Notificaciones sobre Fenómenos Meteorológicos Adversos</b><br/>
TFG - Trabajo Fin de Grado Ingeniería Informática <br/>
UNIR – Universidad Internacional de La Rioja  
</p>


## Descripción
**MeteoRisk** es un sistema de información desarrollado como prueba de concepto para notificar posibles riesgos meteorológicos a los usuarios sobre fenómenos meteorológicos adversos. Utiliza fuentes de datos abiertos, como AEMET OpenData, SAIH y el portal de Datos Abiertos del Gobierno de España, para detectar en tiempo real variables meteorológicas que superen umbrales críticos y generar eventos que se transforman en notificaciones.

Este sistema complementa los sistemas oficiales de alerta, sin interferir con sus competencias, y está orientado a la prevención ciudadana.
## Tecnologías utilizadas
| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| Python     | 3.12.7  | Lenguaje principal de programación |
| MySQL      | 9.1.0   | Sistema de gestión de base de datos |
| Requests   | -       | Librería para peticiones HTTP |
| Pandas     | -       | Manipulación y análisis de datos |

## Aspectos clave
* Extrae información de determinadas fuentes abiertas de datos, como pueden ser AEMET OpenData, los SAIH de las confederaciones hidrográficas y el portal de datos abiertos del Gobierno de España.
* Transforma los datos descargados y los convierte en información útil y manejable por el usuario.
* Analiza si se han rebasado determinados umbrales y en caso positivo, genera eventos que se convertirán en notificaciones dirigidas a los usuarios registrados.
## Base de datos
* Debes disponer de un servidor de bases de datos MySQL compatible con la versión 9.1.0 o superior.
* Descarga el archivo **meteo_db.sql** e impórtalo en tu servidor.
* Descarga el archivo **insert_datos.sql** e impórtalo en el servidor. El fichero contiene los datos necesarios para realizar la prueba de concepto.
## Instalación 
1. Clona el repositorio:
```bash
git clone https://github.com/albertolecu/MeteoRisk.git
```
2. Crea un entorno virtual y actívalo:
```python
python -m venv venv
.venv\Scripts\activate     # en Windows
```
3. Instala las dependencias:
```python
pip install -r requirements.txt
```
4. Configura tu archivo **config.py** con los siguientes datos:
* Parámetros de conexión a tu base de datos MySQL
* Tu clave de API (API_KEY) de AEMET 
## Instrucciones de uso
Descarga los archivos del proyecto, incluidos los ficheros **CSV**, despliega la base de datos, configura los parámetros de tu servidor, copia tu APY_KEY y lanza la aplicación:
```python
py app.py
```
La aplicación está desarrollada en línea de comandos. Verás la siguiente información. A partir de ahora eres libre para ejecutar y probar la aplicación.
## Capturas de pantalla
### Interfaz de usuario en línea de comandos
![Screenshot 1](/img/imagen1.png)
### Evento por temperaturas máximas generado en una zona geográfica.
![Screenshot 2](/img/imagen2.png)
### Lista de los eventos de las últimas 24 horas.
![Screenshot 3](/img/imagen3.png)
## Contribuciones

¡Toda contribución es bienvenida! Puedes crear un *fork*, proponer cambios o abrir *issues* para mejoras.

## Contacto
**Autor:** Alberto López Navarro  
**Email:** albertolecu@gmail.com
<p align="center">
 Creado con mucho ❤️ por Alberto López Navarro en Valdepeñas
</p>
