#!/usr/bin/env bash
set -e

echo ">>> Устанавливаем uv"
curl -LsSf https://astral.sh/uv/install.sh | sh || echo "Ошибка при установке uv"

echo ">>> Загружаем окружение"
export PATH="$HOME/.local/bin:$PATH"

echo ">>> Устанавливаем зависимости"
uv sync || echo "Ошибка при установке зависимостей"
