#!/bin/bash

# 🔧 Установка MCP серверов для Live AI

echo "=== Установка MCP серверов для Live AI ==="
echo ""

# Проверка claude CLI
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI не установлен"
    echo "Установите: npm install -g @anthropic-ai/claude-cli"
    exit 1
fi

echo "📦 Устанавливаем необходимые MCP серверы..."
echo ""

# 1. Sequential Thinking - для глубокого мышления
echo "1️⃣ Sequential Thinking (глубокое мышление)..."
claude mcp add sequential-thinking https://github.com/cprima/mcp-sequential-thinking --scope user

# 2. Telegram Live - для общения в Telegram
echo ""
echo "2️⃣ Telegram Live (интеграция с Telegram)..."
echo "⚠️  Требует настройки переменных окружения в .env"
claude mcp add telegram-live file:///Users/larry/Claude/TG_BRIDGE/TG_MINIMAL/src --scope user

# 3. YouTube Transcript (опционально)
echo ""
echo "3️⃣ YouTube Transcript (опционально)..."
claude mcp add youtube-transcript npx @kimtaeyoon83/mcp-server-youtube-transcript --scope user

echo ""
echo "✅ MCP серверы установлены!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте .env файл с токенами Telegram"
echo "2. Запустите ./start для начала работы"
echo "3. Запустите ./setup_cron.sh для автономности"