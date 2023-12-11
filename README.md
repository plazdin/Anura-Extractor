# Anura extractor

Utilidad para extraer datos de la API de Anura y cargarlos en BigQuery ya formateados, con el objetivo de reducir la carga de trabajo al sector de powerBi.
Para ello, utiliza la biblioteca requests para conectarse a la API, la biblioteca pandas para formatear los datos y la pandas-gbq para cargar los datos en BigQuery.

(Este repositorio solo contiene material informativo y de demostración, por lo que no contiene datos que comprometan al cliente.)

## Configuración:

Para configurar el proyecto, primero debes tener las credenciales de google, renombrarlo a google_secrets.json y agregarlas a la carpeta config. Para más información, por favor diríjase al siguiente link:
https://developers.google.com/workspace/guides/create-credentials?hl=es-419.

Se requieren las tablas y datasets dentro del archivo bigquery-credentials.env
También se requieren las credenciales de la api en cuestión

## Instalación:

``docker compose up -d``

## Ejecución:

Para ejecutar el script, es necesario conocer el id o nombre del contenedor, ya que esta tarea está cronada por el host del contenedor.
Se ejecuta de la siguiente manera:

``docker exec nombre_contenedor python3 main.py``

Además, este archivo recibe parámetros custom para fecha y horas, por lo que es posible obtener ciertos rangos de horas y fechas, de acuerdo a la necesidad.
Por ejemplo, para obtener solo lo extraido desde las 12 hasta las 15 del día que se ejecuta, el código debería ser el siguiente:

``docker exec nombre_contenedor python3 main.py -t 12 15``

Si usted quiere una fecha específica, esta es pasada con la bandera -d, de la siguiente manera:

``docker exec nombre_contenedor python3 main.py -t 12 -d YYYY-MM-DD``

También es posible pasar un rango de fechas de la misma forma, separando por espacios, al igual que el ejemplo anterior de la hora.

Adicionalmente, si usted lo desea, puede configurar el archivo de correo para agregar distintos destinatarios que recibiran un correo informando el estado de todas las solicitudes de este día.
se ejecuta de la siguiente manera:

``docker exec nombre_contenedor python3 email_module.py``

## Cronización:

Por default, este script debe ejecutarse cada 1 horas, ya que por defecto solo extrae el completo de la hora anterior a la que se ejecuta, por ej, si corre a las 17hs, este extrae todo entre las 16:00:00 y las 16:59:59.000.
Este comportamiento está diseñado en base a la necesidad del cliente, pero puede ser facilmente alterado.

Para cronizar la tarea, puedes utilizar el siguiente comando:

``crontab -e``

Agrega la siguiente línea al archivo crontab:

``0 * * * * docker exec nombre_contenedor python3 main.py``

Este comando ejecutará el proyecto main.py cada hora.
