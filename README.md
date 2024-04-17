# testApiBloomAlert
API Test realizado para BloomAlert:

Esta API se encuentra desarrollada bajo FastApi, considera la lectura de datos desde un archivo .CSV y desde una BD MySQL, como tambien la lectura de un archivo JSON (GeoJSON) que marca un area sobre un mapa.

Dentro del repositorio se encuentran 2 archivos .CSV y 1 archivo JSON (GeoJSON) facilitados por BloomAlert.

En el caso de utilizar BD, dentro del repositorio se incluye un archivo .SQL para crear dicha BD bajo MySQL, tambien debera modificar los parametros de conexion dentro de la API, dependiendo como se monte la BD

Detalles del funcionamiento de la API, se encuntran como comentarios dentro del codigo.

Considere tener la libreria "pymysql" para una correcta ejecucion.

Ejecute el proyecto utilizando: 

-uvicorn main:app --reload
