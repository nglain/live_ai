#!/bin/bash

# 🤖 Life Daemon - Автономный запуск жизненного цикла Клэр

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

LOG_FILE="logs/life_daemon.log"
mkdir -p logs state

echo "=== Life Daemon запущен: $(date) ===" >> "$LOG_FILE"

# Сначала проверяем здоровье
python3 autonomy/health_monitor.py 2>&1 | tee -a "$LOG_FILE"

# Читаем статус здоровья
HEALTH_STATUS=$(head -n1 state/claude_health.txt 2>/dev/null || echo "UNKNOWN")

if [ "$HEALTH_STATUS" = "HEALTHY" ] || [ "$HEALTH_STATUS" = "RESTARTED" ]; then
    echo "Claude здоров, выполняем .life" >> "$LOG_FILE"
    # Пытаемся выполнить .life
    if ! timeout 60 claude --no-markdown ".life" 2>&1 | tee -a "$LOG_FILE"; then
        echo "Команда .life завершилась с ошибкой, перезапускаем" >> "$LOG_FILE"
        ./autonomy/start --force --quiet
        # Повторная попытка после перезапуска
        timeout 60 claude --no-markdown ".life" 2>&1 | tee -a "$LOG_FILE" || true
    fi
else
    echo "Claude нездоров ($HEALTH_STATUS), используем orchestrator" >> "$LOG_FILE"
    python3 autonomy/life_orchestrator.py 2>&1 | tee -a "$LOG_FILE"
fi

echo "=== Life Daemon завершен: $(date) ===" >> "$LOG_FILE"

# Обновляем время последней успешной операции
date -Iseconds > state/last_success.txt

echo "" >> "$LOG_FILE"