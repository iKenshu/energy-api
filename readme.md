# Energy API

## Cómo ejecutar el código

Requisito:

1. Tener docker instalado

Primero debes clonar este repositorio, puedes hacerlo con el siguiente comando:

`git@github.com:iKenshu/energy-api.git`

Usar docker compose para hacer build de la aplicación y ejecutarla

`docker-compose up -d --build`

A continuación necesitarás ejecutar la migración para la base de datos:

`docker-compose exec web python manage.py migrate`

Ahora ejecutaremos un comando para cargar la base de datos con la información proporcionada en el excel:

`docker-compose exec web python manage.py loaddata data.json`

Después de esto, podrás entrar a la siguiente URL http://127.0.0.1:8000/api

Para correr los test se debe ejecutar la siguiente línea:

`docker-compose exec web python manage.py test`

### cURL

La url recibe *date* en un formato de 'YYYY-MM-DD' y *period* entre 'daily, weekly y monthly'

`curl -v -X GET -H application/json http://127.0.0.1:8000/api/?date=2022-10-12&period=daily`
