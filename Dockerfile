# syntax=mirror.gcr.io/docker/dockerfile:1.25.0@sha256:0adf442eae370b6087e08edc7c50b552d80ddf261576f4ebd6421006b2461f12

FROM ghcr.io/astral-sh/uv:0.11.28@sha256:0f36cb9361a3346885ca3677e3767016687b5a170c1a6b88465ec14aefec90aa AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian-nonroot@sha256:0c5c768b459a07b9b668fd0919d7e52a8a64a493e45d1132025ea25294f99fcb AS uv
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


FROM mirror.gcr.io/icecodexi/bash-toybox:0.8.14@sha256:8dfe2229d2855e09bce8304cdcc84be90cd2026fe78d30e03efd328bd0bc7b6f AS assets
FROM gcr.io/distroless/python3-debian13:latest@sha256:d7658786080d0ad01686028fdf6f2fea1c15485ff48f74f3af80b8d46ba6fe39
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
