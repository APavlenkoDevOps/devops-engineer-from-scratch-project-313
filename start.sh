#!/usr/bin/env sh
set -e

# Запускаем FastAPI бэкенд в фоновом режиме на порту 8080
uvicorn main:app --host 127.0.0.1 --port 8080 &

# Запускаем Nginx на переднем плане (порт 80)
exec nginx -g 'daemon off;'