FROM python:3.9
LABEL maintainer="imjoseangel"

RUN mkdir /app
ADD nbaapi.py /app/main.py
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt && chmod +x /app/main.py && useradd -u 1001 none
USER none

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
