#!/usr/bin/env sh
set -e

# Запускаем FastAPI бэкенд на порту 8080 локально
uvicorn main:app --host 127.0.0.1 --port 8080 &

# Ждем 2 секунды, чтобы uvicorn поднялся
sleep 2

# Запускаем Nginx на переднем плане (порт 80)
exec nginx -g 'daemon off;'