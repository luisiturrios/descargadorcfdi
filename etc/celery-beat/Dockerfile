FROM python:3.6.9

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY ./src /usr/src/app

EXPOSE 3031

CMD ["celery", "-A", "descargador", "beat", "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]