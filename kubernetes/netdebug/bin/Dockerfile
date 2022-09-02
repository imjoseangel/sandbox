ARG build_for=linux/amd64,linux/arm64
FROM python:alpine3.10 as base

LABEL maintainer="imjoseangel"

RUN mkdir /app
COPY dnstest.py /app/dnstest.py
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && chmod +x /app/dnstest.py && adduser -S none
USER none

WORKDIR /app

ENTRYPOINT ["python", "dnstest.py"]
