up-db:
	docker compose up database -d
	docker compose build app
	sleep 4

up: up-db
	docker compose up app

up-prod: rm-img
	docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up app

test:
	docker compose up database -d
	sleep 3
	python manage.py test
	docker compose down

down:
	docker compose down

setup:
	docker compose up database -d
	sleep 4
	python manage.py migrate
	python manage.py create_superuser
	python manage.py insert_countries
	python manage.py insert_nps_data

clean-db: down
	docker volume ls
	docker volume rm npssurvey_dbdata
	docker volume ls

rm-img: down
	docker rmi npssurvey-app