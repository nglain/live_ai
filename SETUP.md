# 🚀 Инструкция по установке

## Зависимости

### 1. Claude CLI (обязательно)
Должен быть установлен и настроен:
```bash
# Проверка установки
claude --version

# Должна быть активная сессия
claude chat
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

1. Убедитесь что Claude CLI работает:
```bash
claude api "Привет"
# Должен вернуть ответ
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

## Преимущества автономной версии

✅ Никаких внешних зависимостей кроме Claude CLI
✅ Простой и понятный bash скрипт
✅ Легко модифицировать под свои нужды
✅ Работает на любой системе с bash