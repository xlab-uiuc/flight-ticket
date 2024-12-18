FROM python:3.12-slim

WORKDIR /app

COPY run-all.py /app/run-all.py
COPY requirements.txt /app/requirements.txt
COPY ow.config /app/ow.config

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz && \
    tar -zxvf OpenWhisk_CLI-1.2.0-linux-amd64.tgz && \
    chmod +x wsk && \
    mv wsk /usr/local/bin/ && \
    rm OpenWhisk_CLI-1.2.0-linux-amd64.tgz

RUN set -a && \
    . /app/ow.config && \
    wsk property set --apihost "$WSK_API_HOST" --auth "$WSK_AUTH_KEY"

ENV REDIS_HOST=owdev-redis.openwhisk.svc.cluster.local
ENV REDIS_PORT=6379
ENV REDIS_DB=1

# We're using a k8s job that runs this, might change back later after testing
# CMD ["python", "/app/run-all.py", "--minutes", "1"]