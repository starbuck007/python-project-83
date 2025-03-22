#!/usr/bin/env bash
set -e

if [ -f .env ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        if [[ ! -z "$line" && ! "$line" =~ ^# ]]; then
            key=$(echo "$line" | cut -d= -f1)
            value=$(echo "$line" | cut -d= -f2-)
            export "$key=$value"
        fi
    done < .env
fi

echo ">>> Устанавливаем uv"
curl -LsSf https://astral.sh/uv/install.sh | sh || echo "Ошибка при установке uv"

echo ">>> Загружаем окружение"
export PATH="$HOME/.local/bin:$PATH"

echo ">>> Устанавливаем зависимости"
uv sync || echo "Ошибка при установке зависимостей"

echo ">>> Создаем таблицы в базе данных"
psql "$DATABASE_URL" -f database.sql || echo "Ошибка при создании таблиц"
