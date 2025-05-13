# syntax=docker/dockerfile:1@sha256:9857836c9ee4268391bb5b09f9f157f3c91bb15821bb77969642813b0d00518d

FROM ghcr.io/astral-sh/uv:latest@sha256:87a04222b228501907f487b338ca6fc1514a93369bfce6930eb06c8d576e58a4 AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian-nonroot@sha256:5c78e689b216e24073ea2dfe274c8ce5e7e5b2c5992551fe8fa5dd5cfd5409ab AS build
COPY --link --from=distroless-uv /uv /uvx \
    /usr/local/bin/
ENV PATH="/home/nonroot/.local/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1

RUN uv tool install 'ananta[speed]'


FROM mirror.gcr.io/icecodexi/bash-toybox:latest@sha256:c157e41bb84d84b23e2ad09d7dafcd6648f1adec77d3f4979fb2ba738b77c6ac AS assets
FROM gcr.io/distroless/python3:latest@sha256:224c734ca6de7cef2350e82ff9e01b4b56ce22ca3cbef3936018bfb171a7c6de
ARG VER_ANATA_NO_MINATO
LABEL org.icecodexi.ananta.version="${VER_ANATA_NO_MINATO}"

COPY --link --chmod=0755 ./docker-entrypoint.sh /usr/local/bin/
# toybox + bash(ash) + catatonit
COPY --link --from=assets /usr/bin/             /usr/bin/

COPY --link --chmod=0755 ./sshconfig_to_ananta/ /home/nonroot/sshconfig_to_ananta/
COPY --link --from=build  /home/nonroot/.local/ /home/nonroot/.local/

SHELL ["/usr/bin/bash", "-o", "pipefail", "-c"]
RUN rm -rf /bin/ && ln -sf /usr/bin /bin

USER nonroot:nonroot
WORKDIR /home/nonroot/
ENV TZ=Asia/Taipei
ENV PATH="/home/nonroot/.local/bin:${PATH}"

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
