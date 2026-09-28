FROM python:3.12-slim

# Установка Nginx, Node.js и npm
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt-get/lists/*

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем зависимости Python и Node.js
COPY pyproject.toml uv.lock package.json package-lock.json ./

# Устанавливаем зависимости Python и фронтенд
RUN uv sync --frozen --no-cache
RUN npm ci

# Копируем фронтенд в директорию Nginx
RUN mkdir -p /var/www/html && \
    cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /var/www/html/

# Копируем исходники бэкенда и конфигурации
COPY . .

# Копируем конфиг Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Указываем PATH для виртуального окружения Python
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["/app/start.sh"]