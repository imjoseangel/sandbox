FROM python:3.10.3
LABEL maintainer="imjoseangel"

RUN mkdir -p /app/templates
ADD main.py /app/main.py
ADD templates/index.html /app/templates/index.html
ADD templates/layout.html /app/templates/layout.html
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt && chmod +x /app/main.py && useradd -u 1001 none
USER none

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
