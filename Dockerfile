# syntax=docker/dockerfile:1@sha256:87999aa3d42bdc6bea60565083ee17e86d1f3339802f543c0d03998580f9cb89

FROM ghcr.io/astral-sh/uv:latest@sha256:0f36cb9361a3346885ca3677e3767016687b5a170c1a6b88465ec14aefec90aa AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian12-nonroot@sha256:64d3b4434324068026d02704f8efeab8d518f091d55a0112ae915c553240c2b4 AS uv
COPY --link --from=distroless-uv /uv /uvx \
    /usr/local/bin/
ENV PATH="/home/nonroot/.local/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1

FROM uv AS build
# install ananta
ARG ver_ananta
RUN uv --no-progress tool install "ananta[speed]==${ver_ananta}"

# install sshconfig_to_ananta
# renovate: datasource=pypi depName=tomli-w
ARG TOMLI_W_VERSION=1.2.0
COPY --link --chown=65532:65532 /src/ /home/nonroot/sshconfig_to_ananta/src/
RUN --mount=type=bind,source=README.md,target=/home/nonroot/sshconfig_to_ananta/README.md \
    --mount=type=bind,source=pyproject.toml,target=/home/nonroot/sshconfig_to_ananta/pyproject.toml \
    uv --no-progress tool install --with "tomli-w==${TOMLI_W_VERSION}" \
        /home/nonroot/sshconfig_to_ananta/


FROM mirror.gcr.io/icecodexi/bash-toybox:debian12@sha256:40ca19e19f3e575ae3760d7d114b5a7d435ffdc2e9ae41273f819cce277f59df AS assets
FROM gcr.io/distroless/python3-debian12:latest@sha256:2fdb05402a2cf21cf78fdb3ba4c5db167241e9e498140f5bf689d7efb773731f
ARG ver_anata_helper
LABEL org.opencontainers.image.version="${ver_anata_helper}" \
      org.opencontainers.image.source="https://github.com/IceCodeNew/anata-no-minato"

COPY --link --chmod=0755 ./docker-entrypoint.sh /usr/local/bin/
# toybox + bash(ash) + catatonit
COPY --link --from=assets /usr/bin/             /usr/bin/

COPY --link --from=build --chown=65532:65532 \
                          /home/nonroot/.local/ /home/nonroot/.local/

SHELL ["/usr/bin/bash", "-o", "pipefail", "-c"]
RUN rm -rf /bin/ && ln -sf /usr/bin /bin

USER nonroot:nonroot
WORKDIR /home/nonroot/
ENV TZ=Asia/Taipei
ENV PATH="/home/nonroot/.local/bin:${PATH}"

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
