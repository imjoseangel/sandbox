# K8S Listener
FROM python:3.10.2
LABEL maintainer="imjoseangel"

ADD main.py /usr/local/sbin/main
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt && chmod +x /usr/local/sbin/main && useradd -u 1001 none
USER none

EXPOSE 8080

ENTRYPOINT ["main"]
