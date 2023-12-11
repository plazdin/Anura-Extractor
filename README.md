Anura extractor, para extraer datos de la API de Anura y cargarlos en BigQuery ya formateados, con el objetivo de reducir la carga de trabajo al sector de powerBi.
Para ello, utiliza la biblioteca requests para conectarse a la API, la biblioteca pandas para formatear los datos y la pandas-gbq para cargar los datos en BigQuery.

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
  
  Adicionalmente, si usted lo desea, puede configurar el archivo de correo para agregar distintos destinatarios que recibiran un correo informando el estado de todas las solicitudes de este día.
  se ejecuta de la siguiente manera:
``docker exec nombre_contenedor python3 email_module.py``

## Cronización:

Por default, este script debe ejecutarse cada 1 horas, ya que por defecto solo extrae el completo de la hora anterior a la que se ejecuta, por ej, si corre a las 17hs, este extrae todo entre las 16:00:00 y las 16:59:59.000
Este comportamiento está diseñado en base a la necesidad del cliente, pero puede ser facilmente alterado.

Para cronizar la tarea, puedes utilizar el siguiente comando:

``crontab -e``

Agrega la siguiente línea al archivo crontab:

``0 * * * * docker exec nombre_contenedor python3 main.py``

Este comando ejecutará el proyecto main.py cada hora.
