FROM python:3.11-slim
LABEL maintainer="imjoseangel"


WORKDIR /app

ADD run.py config.toml requirements.txt .
RUN pip install -r requirements.txt && chmod +x /app/run.py && useradd -u 1001 none
USER none

ENTRYPOINT ["python", "run.py"]
