#!/bin/bash

# 🎯 Минималистичная настройка автономной жизни Клэр

echo "=== Настройка Life Daemon для Клэр ==="

# Делаем скрипты исполняемыми
chmod +x life_daemon.sh

# Добавляем life daemon (каждые 5 минут)
LIFE_CRON="*/5 * * * * cd /Users/larry/Claude/TG_AGENT_PERSONALITY/autonomy && ./life_daemon.sh"

# Добавляем watchdog (каждые 10 минут)
WATCHDOG_CRON="*/10 * * * * cd /Users/larry/Claude/TG_AGENT_PERSONALITY/autonomy && python3 watchdog.py"

# Получаем текущий crontab
CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

# Добавляем life daemon если нет
if ! echo "$CURRENT_CRON" | grep -q "life_daemon.sh"; then
    (echo "$CURRENT_CRON"; echo "$LIFE_CRON") | crontab -
    echo "✅ Life daemon добавлен в cron"
else
    echo "⚠️  Life daemon уже настроен"
fi

# Обновляем crontab снова
CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

# Добавляем watchdog если нет
if ! echo "$CURRENT_CRON" | grep -q "watchdog.py"; then
    (echo "$CURRENT_CRON"; echo "$WATCHDOG_CRON") | crontab -
    echo "✅ Watchdog добавлен в cron"
else
    echo "⚠️  Watchdog уже настроен"
fi

echo ""
echo "📋 Текущие задания cron:"
crontab -l | grep -E "(life_daemon|watchdog)"

echo ""
echo "✨ Готово! Клэр теперь автономна."
echo ""
echo "Команды управления:"
echo "  crontab -l        # посмотреть задания"
echo "  crontab -e        # редактировать"
echo "  crontab -r        # удалить все"