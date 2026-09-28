[![Actions Status](https://github.com/APavlenkoDevOps/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/APavlenkoDevOps/devops-engineer-from-scratch-project-313/actions)
[![Python Checks](https://github.com/APavlenkoDevOps/devops-engineer-from-scratch-project-313/actions/workflows/test.yml/badge.svg)](https://github.com/APavlenkoDevOps/devops-engineer-from-scratch-project-313/actions)

# Сокращатель ссылок

Учебный проект Hexlet: REST API для коротких ссылок на FastAPI и PostgreSQL.

Демо: https://devops-engineer-from-scratch-project-313-ps1s.onrender.com

## Требования

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Node.js (только для запуска фронтенда через `make dev`)

## Запуск

```bash
uv sync
make run
```

Приложение запустится на http://localhost:8080. Проверка: http://localhost:8080/ping вернёт `pong`.

Запуск вместе с фронтендом: `make dev`.

## Переменные окружения

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `DATABASE_URL` | Строка подключения к PostgreSQL | `sqlite:///./test.db` |
| `BASE_URL` | Базовый адрес для поля `short_url` | `http://localhost:8080` |
| `SENTRY_DSN` | Мониторинг ошибок (необязательно) | не задана |

Локально переменные можно положить в файл `.env` (он в `.gitignore`).

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/ping` | Проверка, возвращает `pong` |
| GET | `/api/links` | Список ссылок |
| POST | `/api/links` | Создать ссылку |
| GET | `/api/links/{id}` | Получить ссылку |
| PUT | `/api/links/{id}` | Обновить ссылку |
| DELETE | `/api/links/{id}` | Удалить ссылку |
| GET | `/r/{short_name}` | Редирект на исходный адрес (302) |

## Проверки

```bash
make lint   # линтер ruff
make test   # тесты pytest
make check  # оба сразу
```

## Docker

```bash
docker build -t project313 .
docker run --rm -p 8080:80 project313
```