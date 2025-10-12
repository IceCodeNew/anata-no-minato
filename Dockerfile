# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:latest AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian12-nonroot AS uv
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


FROM mirror.gcr.io/icecodexi/bash-toybox:debian12 AS assets
FROM gcr.io/distroless/python3-debian12:latest
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
