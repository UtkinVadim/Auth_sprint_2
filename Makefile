.PHONY: env dbs down init_app migrations run_local run_debug init_app run_app run_prod run_tests tests prod down_tests down_prod create_admin

env:
	cp .env.template .env

dbs:
	docker compose up postgres_auth -d --build
	docker compose up redis_auth -d --build
	docker exec -it postgres_auth psql -U postgres

down:
	docker compose down

init_db:
	cd src && alembic upgrade head

migrations:
	cd src && alembic revision --autogenerate

run_local:
	cd src && python run.py

run_debug:
	cd src && python run.py -d

init_app:
	docker-compose up --build -d postgres_auth
	docker-compose up --build -d redis_auth

run_app:
	docker-compose up --build -d auth_api
	docker exec -it auth_api alembic upgrade head

run_prod:
	docker compose up --build -d

run_tests:
	docker compose -f docker-compose.tests.yaml up --build

down_tests:
	docker compose -f docker-compose.tests.yaml down

down_prod:
	docker compose -f docker-compose.yaml down

create_admin:
	docker exec -it auth_api python run.py --create-admin


tests: env run_tests
prod: env run_prod
