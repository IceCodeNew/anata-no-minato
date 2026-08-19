# syntax=mirror.gcr.io/docker/dockerfile:1.25.0@sha256:0adf442eae370b6087e08edc7c50b552d80ddf261576f4ebd6421006b2461f12

FROM ghcr.io/astral-sh/uv:0.11.28@sha256:0f36cb9361a3346885ca3677e3767016687b5a170c1a6b88465ec14aefec90aa AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian-nonroot@sha256:57d4dd45d8c926d2562c0fa30824f5dd18d8b308348e11d8e703e976d2cf52fc AS uv
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


FROM mirror.gcr.io/icecodexi/bash-toybox:0.8.14@sha256:e10a18dc2c3c37bb7abda29b9f05479d65fdd08563fd95ebafb5e958e5435cea AS assets
FROM gcr.io/distroless/python3-debian13:latest@sha256:b340f07acd3692d739cbc28450b8876b4770ee01967aa9e4193c3bcec7bd235e
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
