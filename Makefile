PG_USER ?= user_test
PG_PASSWORD ?= Qwerty123
PG_DB ?= anime_on

run:
	docker-compose up

run-d:
	docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose build

mm:
	docker-compose run --rm api migrate

mm-fake:
	docker-compose run --rm api migrate --fake

mkm:
	docker-compose run --rm api makemigrations

mkm-m: mkm mm

bash:
	docker-compose run --rm --entrypoint="" api sh

create-db:
	docker-compose up -d db
	docker-compose exec db sh \
			-c 'psql --username=postgres --dbname=postgres -c "CREATE USER $(PG_USER) WITH PASSWORD '"'$(PG_PASSWORD)'"';"'
	docker-compose exec db sh -c 'psql --username=postgres --dbname=postgres -c "CREATE DATABASE $(PG_DB);"'
	docker-compose rm -s -f db

rm-db:
	docker-compose exec db sh \
			-c "psql --username=postgres --dbname=postgres -c 'drop database if exists $(PG_DB);'"
