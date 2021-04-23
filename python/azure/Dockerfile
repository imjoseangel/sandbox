# Azure DevOps Agent Pool Listener
FROM ubuntu:latest
LABEL maintainer="imjoseangel"

ARG appname=azdvpool

RUN mkdir -p /opt/${appname}

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /opt/${appname}

ADD devopsagents.py devopsagents.py
ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN useradd -u 1001 none
USER none

EXPOSE 8080

ENTRYPOINT ["python3", "/opt/azdvpool/devopsagents.py"]
