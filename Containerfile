FROM alpine:latest

RUN apk add py3-pip && \
    python3 -m pip install --break-system-packages pygithub requests

COPY ./run.py .

HEALTHCHECK --interval=1m --timeout=3s \
  CMD pidof python3 || exit 1

ENTRYPOINT ["./run.py"]
