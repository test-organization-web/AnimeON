FROM python:3

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev gnupg g++ make cmake unzip curl unixodbc unixodbc-dev autoconf automake libtool git gettext
RUN pip install psycopg2

ARG BASE_DIR="/app"
WORKDIR ${BASE_DIR}

# Create folder for dependencies
ARG DEPENDENCIES_DIR="/dependencies"
RUN mkdir -p ${DEPENDENCIES_DIR}

# Create a group and user
RUN addgroup -S animeON && adduser -S animeon -G animeON

# make "animeon" owner of FUNCTION_DIR and DEPENDENCIES_DIR
RUN chown -R animeon:animeON ${BASE_DIR}
RUN chown -R animeon:animeON ${DEPENDENCIES_DIR}

# Tell docker that all future commands should run as the "animeon" user
USER animeon

# Create function log directory
RUN mkdir -m a=rwx -p ${BASE_DIR}/logs

COPY requirements.txt ${BASE_DIR}/
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt --target "${DEPENDENCIES_DIR}"

# aws cli doesn't work without this
ENV PATH=$PATH:${BASE_DIR}:${DEPENDENCIES_DIR}:${DEPENDENCIES_DIR}/bin
ENV PYTHONPATH=$PYTHONPATH:${BASE_DIR}:${DEPENDENCIES_DIR}:${DEPENDENCIES_DIR}/bin

COPY --chown=animeon:animeON . ${BASE_DIR}/

ARG version=unknown
RUN echo $version && sed -i "s/##VERSION##/$version/g" anime_on/settings.py

ENTRYPOINT [ "/usr/local/bin/python", "manage.py" ]
