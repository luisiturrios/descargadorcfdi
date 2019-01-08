# Descargador

[Logo](http://logomakr.com/5m6tos)

### Iniciar Modo Pruebas
```bash
docker-compose up
```

Corrar migrations
```bash
docker-compose exec descargador-web python manage.py makemigrations
docker-compose exec descargador-web python manage.py migrate
```