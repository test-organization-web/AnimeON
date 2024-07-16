PG_DB ?= anime_on_10
PG_USER ?= user_test_10
PG_PASSWORD ?= Qwerty123

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
	docker-compose exec db sh -c 'psql --username=postgres --dbname=postgres -c "CREATE DATABASE $(PG_DB);"'
	docker-compose rm -s -f db

create-db-user:
	docker-compose exec db sh \
			-c 'psql --username=postgres --dbname=postgres -c "CREATE USER $(PG_USER) WITH PASSWORD '"'$(PG_PASSWORD)'"' SUPERUSER;"'
	docker-compose exec db sh -c 'psql --username=postgres --dbname=postgres -c "GRANT ALL PRIVILEGES ON DATABASE $(PG_DB) to $(PG_USER);"'


rm-db:
	docker-compose exec db sh \
			-c "psql --username=postgres --dbname=postgres -c 'drop database if exists $(PG_DB);'"

create-app:
	docker-compose up -d api
	docker-compose exec api sh -c 'python manage.py startapp $(app_name) apps/$(app_name)'

path = apps
test:
	docker-compose run --rm api test --keepdb -v 2 $(path)

RELEASES_FILE ?= anime_on/releases.txt
write-versions-file:
	git for-each-ref --count=10 --sort='-creatordate' --format='%(refname:strip=2)==>%(contents)===' 'refs/tags' > $(RELEASES_FILE)
