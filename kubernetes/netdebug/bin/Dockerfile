ARG build_for=linux/amd64,linux/arm64
FROM python:alpine3.10 as base

LABEL maintainer="imjoseangel"

RUN mkdir /app
COPY dnsbench.py /app/dnsbench.py
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && chmod +x /app/dnsbench.py && adduser -S none
USER none

WORKDIR /app

ENTRYPOINT ["python", "dnsbench.py"]
