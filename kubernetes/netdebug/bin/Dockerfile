ARG build_for=linux/amd64,linux/arm64
FROM python:alpine3.10 as base

LABEL maintainer="imjoseangel"

RUN mkdir /app
COPY dnsrequest.py /app/dnsrequest.py
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && chmod +x /app/dnsrequest.py && adduser -S none
USER none

WORKDIR /app

ENTRYPOINT ["python", "dnsrequest.py"]
