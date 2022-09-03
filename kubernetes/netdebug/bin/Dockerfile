ARG build_for=linux/amd64,linux/arm64
FROM python:alpine3.10 as base

LABEL maintainer="imjoseangel"

RUN apk add --no-cache \
    gcc libffi-dev musl-dev

RUN mkdir /app
COPY dnsresolv.py /app/dnsresolv.py
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && chmod +x /app/dnsresolv.py && adduser -S none
USER none

WORKDIR /app

ENTRYPOINT ["python", "dnsresolv.py"]
