## Local Setup

### Pre-requirements
1. docker
2. docker-compose
3. make

### First initialization
1. Create .env file with environment variables
```bash
cp .env_template .env
# edit .env file as you need
```

2. Build container
```bash
make build
```

4. Execute a command for creating database (default name of new database - "anime_on")
```bash
make create-db
make create-db-user
```

4. Apply migrations
```bash
make mm
```

5. Create superuser
```bash
make bash
python manage.py createsuperuser
# provide username, email and password by request
exit
```

### Launch project
1. Run the project
```bash
make run-d
```


## Make commands

``run`` (default) - run containers.

``run-d`` - run containers in background.

``stop`` - stop all containers.

``build`` - build or rebuild api image

``mm`` - execute 'python manage.py migrate'

``mkm`` - execute 'python manage.py makemigrations'

``mkm-m`` - runs makemigrations + migrate.

``bash`` - enter to api container.

``create-db`` - create "anime_on" database in PostgreSQL