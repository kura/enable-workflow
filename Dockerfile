# FROM ghcr.io/linuxserver/baseimage-ubuntu:jammy
FROM ghcr.io/linuxserver/baseimage-alpine:3.16

RUN \
    apk add py3-pip && \
    python3 -m pip install pygithub requests && \
    rm -rf \
      /tmp/* \
      /var/lib/apt/lists/* \
      /var/tmp/* \
      /root/.cache

COPY ./run.py .
CMD ["./run.py"]
