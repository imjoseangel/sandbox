# Azure DevOps Agent Pool Listener
FROM python:3.9.4
LABEL maintainer="imjoseangel"

ADD devopsagents.py /usr/local/sbin/devopsagents
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt && chmod +x /usr/local/sbin/devopsagents

EXPOSE 8080

ENTRYPOINT ["devopsagents"]
