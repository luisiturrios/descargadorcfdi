FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/www/descargador

WORKDIR /var/www/descargador

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt