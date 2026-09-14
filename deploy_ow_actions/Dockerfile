ARG PYTHON_RUNTIME_IMAGE=ghcr.io/sregym/flight-ticket-python-runtime:20260911-multiarch@sha256:263cf7a52da1b0a9c8e45825b2574f578c811e791f234499af839a588d255f8a
# Build ZIPs inside the target architecture's actual action runtime. The
# Kubernetes deployment job only uploads these artifacts; it needs no daemon.
FROM ${PYTHON_RUNTIME_IMAGE} AS packages
WORKDIR /build
COPY actions /build/actions
COPY package_actions.py requirements.lock.txt /build/
RUN python package_actions.py actions /packages --constraints requirements.lock.txt

FROM ubuntu:20.04
ARG TARGETARCH
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates wget unzip \
    && rm -rf /var/lib/apt/lists/*
RUN wget -q "https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-${TARGETARCH}.tgz" -O /tmp/wsk.tgz \
    && tar -xzf /tmp/wsk.tgz -C /usr/local/bin wsk \
    && chmod +x /usr/local/bin/wsk \
    && rm /tmp/wsk.tgz

COPY deploy_ow_actions.sh /app/deploy_ow_actions.sh
ARG PYTHON_RUNTIME_IMAGE
ENV PYTHON_RUNTIME_IMAGE=${PYTHON_RUNTIME_IMAGE}
RUN chmod +x /app/deploy_ow_actions.sh
COPY actions /app/actions
COPY --from=packages /packages/ /app/actions/
