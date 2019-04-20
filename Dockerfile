FROM python:3.7.3

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt uwsgi

COPY . .

EXPOSE 8000