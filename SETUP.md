# 🚀 Инструкция по установке

## Зависимости

### 1. Bridge API (обязательно)
Bridge должен быть установлен в `/Users/larry/Claude/BRIDGE`
```bash
# Если Bridge в другом месте, измените путь в файле life (строка 6)
BRIDGE_DIR="/path/to/your/BRIDGE"
```

### 2. telegram-live-mcp сервер (обязательно)
```bash
# Клонировать репозиторий
git clone https://github.com/LarryAI001/telegram-live-mcp.git
cd telegram-live-mcp

# Установить зависимости
npm install

# Добавить в Claude Code
claude mcp add telegram-live-mcp /полный/путь/к/telegram-live-mcp --scope user
```

### 3. Настройка Telegram бота
В telegram-live-mcp создайте `.env`:
```
BOT_TOKEN=ваш_токен_бота
USER_ID=ваш_telegram_id
```

## Проверка установки

1. Убедитесь что Bridge работает:
```bash
ls /Users/larry/Claude/BRIDGE/core/bridge_api.sh
```

2. Проверьте MCP сервер:
```bash
claude mcp list
# Должен показать telegram-live-mcp
```

3. Запустите life:
```bash
./life
```

## Альтернатива: Standalone версия

Если хотите полностью независимую версию без Bridge, можно переписать life для прямой работы с Claude CLI. Дайте знать если это нужно!