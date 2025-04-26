# syntax=docker/dockerfile:1

FROM mirror.gcr.io/icecodexi/bash-toybox:latest AS assets
COPY --link --chmod=0755 ./dummy_ananta.sh /usr/local/bin/ananta
SHELL ["/usr/bin/bash", "-o", "pipefail", "-c"]
