FROM python:3.11-slim
LABEL maintainer="imjoseangel"

WORKDIR /app

ADD run.py requirements.txt ./
RUN pip install -r requirements.txt && useradd -u 1001 none

USER none

ENTRYPOINT ["python", "run.py"]
