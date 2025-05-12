# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:latest AS distroless-uv
FROM mirror.gcr.io/icecodexi/python:debian-nonroot AS build
COPY --link --from=distroless-uv /uv /uvx \
    /usr/local/bin/
ENV PATH="/home/nonroot/.local/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1

RUN uv tool install 'ananta[speed]'


FROM mirror.gcr.io/icecodexi/bash-toybox:latest AS assets
FROM gcr.io/distroless/python3:latest
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
