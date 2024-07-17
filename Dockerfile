# It's python:3.11.5-alpine3.18
FROM python@sha256:e5d592c422d6e527cb946ae6abb1886c511a5e163d3543865f5a5b9b61c01584

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev gnupg g++ make automake git && \
    apk add postgresql-dev

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
