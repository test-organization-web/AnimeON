FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
<<<<<<< HEAD
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN pip install psycopg2
=======
>>>>>>> fdfb9c8 (Updates for create auth)
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

ENTRYPOINT [ "/usr/local/bin/python", "manage.py" ]
