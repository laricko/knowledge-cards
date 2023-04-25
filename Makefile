backend_shell:
	docker exec -it cards_backend sh

psql:
	docker exec -it cards_db psql -U postgres

lint:
	isort app --src=app/ --skip=app/alembic --profile=black && black app --exclude=app/alembic

test:
	docker exec -it cards_backend pytest -s

dump:
	docker exec -t cards_db pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

dump_restore:
	cat $(file) | docker exec -i cards_db psql -U postgres

run_dev:
	docker-compose -f docker-compose.dev.yml up

migrate:
	docker exec -it cards_backend alembic upgrade head

makemigrations:
	docker exec -it cards_backend alembic revision --autogenerate -m $(message)

