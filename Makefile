up-db:
	docker compose up database -d
	docker compose build app
	sleep 4

up: up-db
	docker compose up app

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