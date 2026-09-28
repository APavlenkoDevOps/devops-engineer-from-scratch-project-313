#!/usr/bin/env sh
set -e

# Бэкенд слушает строго локальный адрес 127.0.0.1
uvicorn main:app --host 127.0.0.1 --port 8080 &

# Ждем 2 секунды для запуска FastAPI
sleep 2

# Nginx запускается на порту 80
exec nginx -g 'daemon off;'