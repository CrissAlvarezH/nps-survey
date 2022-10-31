


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

## Despliegue en aws
Para desplegar en aws necesitamos tener instalado y configurado el [cli de aws](https://aws.amazon.com/es/cli/), para esto usaremos el comando `aws configure` en introduciremos nuestras credenciales con los permisos necesarios para desplegar la infra anteriormente descrita.

### 1. Crear servicios en AWS via IAC

El despliegue será en parte via IAC usando [CloudFormation](https://aws.amazon.com/es/cloudformation/) y el archivo template es `cloudformation.yaml` en la raiz de repositorio, para hacer el despliegue de la infra usaremos un script en bash especifico para esto, en la consola escribimos y ejecutamos el siguiente comando
```
bash scripts/setup_infra.sh
```
Este script se encarga de desplegar el stack en cloud formation y crear la infraestructura base que usaremos para desplegar nuesta app, en aws podremos ver el stack de cloud formation creandose

<img src='https://github.com/CrissAlvarezH/nps-survey/blob/main/docs/imgs/aws-cloudformation-stak.png'/>

Una vez el stack pasa a estar en **CREATE_COMPLETE** ya tenemos la infra base para desplegar.

### 2. Crear imagen docker y subir a AWS ECR

El paso anterior creó, entre otras cosas, un Task definition en ECS que apunta a un repository en ECR el cual contendrá la imagen docker de nuestra aplicación, en este paso vamos a subir esa imagen docker para que podamos crear un Task con este Task definition y poner en producción el proyecto, para esto el script a usar es el siguiente

```
bash scripts/deploy_to_ecr.sh <aws account id> <aws region>
```
Como podemos notar, necesitamos pasar dos parametros al script, el primero es el id de la cuenta de aws y el segundo la region donde se encuentra nuestra infra creada del paso anterior.

### 3. Lanzar Task en ECS

Despues de ejecutar los pasos anteriores tendremos la infraestructura creada en AWS, lo siguiente es configurar el Task definition creado en el paso 1 con el nombre `aws-ecs-npssurvey-app` y configurar las variables de entorno del proyecto, para saber cuales son tenemos el archivo `.env.example`, aquí podemos configurar las credenciales de la base de datos quer puede ser por ejemplo una db instance en RDS o cualquier otro base de datos Postgres que considere conveniente, el levantamiento de la base de datos es a discreción del usuario.

Lo ultimo por hacer es lanzar el Task en el cluster `aws-ecs-npssurvey-app` de ECS creando via IAC y tomar la dirección IP publica del task para hacer uso del API del proyecto.


# Api

## Colección de Postman

Cada uno de los endpoint del api estan documentados en una colección de Postman el cual podemos importar usando el archivo `docs/postman_collection.json`, una vez importado tendremos una carpeta en Postman como esta:

<img src='https://github.com/CrissAlvarezH/nps-survey/blob/main/docs/imgs/postman-collection.png'/>

Donde veremos que cada request tiene un ejemplo donde se explica como usarla y que respuesta esperar de ella.


# Tests

Para correr los test podemos usar `make` y correr el comando
```
make test
```
O en caso de no tene `make` instalado, usamos el siguiente comando
```
docker compose up database -d

python manage.py test
```

Una vez terminamos de ejecutar los test debemos apagar el contenedor de la base de datos (si usamos `make` esto no es necesario), para esto ejecutamos

```
docker compose down
```
