FROM python:3.10-slim

COPY app/ /app/
COPY requirements.txt /app/requirements.txt
COPY config/ /config/
WORKDIR /app

RUN apt-get update && apt-get install -y nano
RUN pip3 install -r /app/requirements.txt

ENV ANURA_CREDENTIALS=/config/anura-credentials.env \
    GBQ_CREDENTIALS=/config/big-query-credentials.env \
    LOG_PATH=/app/log \
    TZ=America/Argentina/Buenos_Aires \
    DEBUG=False
