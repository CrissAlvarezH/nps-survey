


# NPS survey
Aplicación que consiste en un api rest para gestionar las encuestas de NPS 

**Stack:**
- [Python](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/) 
- [Poetry](https://python-poetry.org/)
- [Docker](https://docs.docker.com/engine/) y [Docker compose](https://docs.docker.com/compose/)
- [Postgres](https://www.postgresql.org/)
- [AWS CLI](https://aws.amazon.com/es/cli/)
- AWS Services ([CloudFormation](https://aws.amazon.com/es/cloudformation/), [ECR](https://aws.amazon.com/es/ecr/), [Fargate](https://aws.amazon.com/es/fargate/), [ECS](https://aws.amazon.com/es/ecs/), [RDS](https://aws.amazon.com/es/rds/))

## Documentación

- [Infraestructura](#infraestructura)
- [Base de datos](#base-de-datos)
- [Despliegue](#despliegue)
	- [Despligue local](#despliegue-local)
	- [Despligue en aws](#despliegue-en-aws)
- [API](#api)
	- [Colección de Postman](#colección-de-postman)
- [Tests](#tests)


# Infraestructura 
<img src='https://github.com/CrissAlvarezH/nps-survey/blob/main/docs/imgs/infra-aws.png'/>


# Base de datos

<img src='https://github.com/CrissAlvarezH/nps-survey/blob/main/docs/imgs/db-diagram.png'/>

# Despliegue

## Despliegue local
Para realizar el despliegue en local necesitaremos tener instalado [Docker](https://docs.docker.com/engine/) y [Docker compose](https://docs.docker.com/compose/), los cuales serán usados para empaquetar la app y correrla como un contenedor en nuestra maquina, ademas se usarán para descargar y encender un [contenedor postgres](https://hub.docker.com/_/postgres) que nos servirá como base de datos de nuestra app.

### Variables de entorno
Las variables de entorno necesarias para el funcionamiento del proyecto estan en `.env.example`, el cual tiene valores de prueba en cada variable, por tanto el primer paso es copiar y pegar este archivo y despues renombrarlo a `.env`, si lo deseamos podemos cambiar los valores predeterminados, sin embargo, los valores por defecto son funcionales.
Para hacer esto usando la consola el comando es el siguiente:
```
cp .env.example .env
```

### Ejecutar app con docker

Preferiblemente usaremos `make` (el cual podemos instalar usando el comando `sudo apt install make`) para correr el proyecto con el siguiente comando

```
make up
```
En caso de no quere usar `make` los comandos serán los siguiente

```
docker compose up database -d
docker compose up app
```

Despues de correr los comandos deberemos tener en la consola lo siguiente:

```
...
npssurvey-app-1  |   Applying nps.0002_initial... OK
npssurvey-app-1  |   Applying nps.0003_alter_company_description... OK
npssurvey-app-1  |   Applying nps.0004_remove_company_persons_alter_nps_user_and_more... OK
npssurvey-app-1  |   Applying nps.0005_remove_nps_user_nps_person... OK
npssurvey-app-1  |   Applying nps.0006_nps_metadata... OK
npssurvey-app-1  |   Applying sessions.0001_initial... OK
npssurvey-app-1  | nps data inserted successfully
npssurvey-app-1  | Watching for file changes with StatReloader
```

Con esto ya podemos hacer uso de la api en local apuntando a `localhost:8000`
