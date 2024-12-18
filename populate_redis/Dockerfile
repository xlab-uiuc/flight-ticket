FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV REDIS_HOST=owdev-redis.openwhisk.svc.cluster.local
ENV REDIS_PORT=6379
ENV REDIS_DB=1