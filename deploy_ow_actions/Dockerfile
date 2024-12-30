FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    zip \
    unzip \
    virtualenv \
    docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz && \
    tar -zxvf OpenWhisk_CLI-1.2.0-linux-amd64.tgz && \
    chmod +x wsk && \
    mv wsk /usr/local/bin/ && \
    rm OpenWhisk_CLI-1.2.0-linux-amd64.tgz

COPY deploy_ow_actions.sh /app/deploy_ow_actions.sh
RUN chmod +x /app/deploy_ow_actions.sh

COPY actions /app/actions