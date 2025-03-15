#!/usr/bin/env bash
set -e

echo ">>> Устанавливаем uv"
curl -LsSf https://astral.sh/uv/install.sh | sh || echo "Ошибка при установке uv"

echo ">>> Загружаем окружение"
export PATH="$HOME/.local/bin:$PATH"

echo ">>> Устанавливаем зависимости"
uv pip install flask gunicorn psycopg validators python-dotenv requests beautifulsoup4 || echo "Ошибка при установке зависимостей"

echo ">>> Создаем таблицы в базе данных"
psql $DATABASE_URL -f database.sql || echo "Ошибка при создании таблиц"
