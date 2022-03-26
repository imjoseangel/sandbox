# OCTO-DNS
FROM python:3.10.2
LABEL maintainer="imjoseangel"

ENV PLATFORM="docker"

COPY verify /usr/local/sbin/verify
RUN mkdir config
COPY config config
COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip  && pip install -r requirements.txt \
    && chmod +x /usr/local/sbin/verify && useradd -u 1001 none

USER none

ENTRYPOINT ["verify"]
