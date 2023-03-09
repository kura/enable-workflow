FROM alpine:latest

RUN apk add py3-pip && \
    python3 -m pip install pygithub requests

COPY ./run.py .
CMD ["./run.py"]
