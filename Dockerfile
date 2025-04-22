# syntax=docker/dockerfile:1

FROM mirror.gcr.io/icecodexi/python:debian-nonroot AS build
RUN uv tool install 'ananta[speed]'


FROM mirror.gcr.io/icecodexi/bash-toybox:latest AS assets
FROM gcr.io/distroless/python3:latest
COPY --link --chmod=0755 ./docker-entrypoint.sh /usr/local/bin/
# toybox + bash(ash) + catatonit
COPY --link --from=assets /usr/bin/             /usr/bin/
COPY --link --from=build  /home/nonroot/.local/ /home/nonroot/.local/

SHELL ["/usr/bin/bash", "-o", "pipefail", "-c"]
RUN rm -rf /bin/ && ln -sf /usr/bin /bin

USER nonroot:nonroot
WORKDIR /home/nonroot/
ENV TZ=Asia/Taipei
ENV PATH="/home/nonroot/.local/bin:${PATH}"

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
