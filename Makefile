up-db:
	docker compose up database -d
	docker compose build app
	sleep 4

up: up-db
	docker compose up app

down:
	docker compose down

clean-db: down
	docker volume ls
	docker volume rm npssurvey_dbdata
	docker volume ls