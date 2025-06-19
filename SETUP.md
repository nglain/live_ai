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
git clone https://github.com/nglainAI/TG_MCP.git
cd TG_MCP

# Установить зависимости
npm install
```

### 3. Настройка Telegram бота

#### Создание бота:
1. Откройте Telegram и найдите @BotFather
2. Отправьте `/newbot`
3. Введите имя бота (например: "Клэр AI")
4. Введите username бота (например: "claire_ai_bot")
5. Сохраните токен (выглядит как `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Получение вашего ID:
1. Найдите @userinfobot в Telegram
2. Отправьте любое сообщение
3. Бот вернет ваш ID (число вроде `365991821`)

#### Создание конфигурации:
```bash
cd TG_MCP
cat > .env << EOF
BOT_TOKEN=ваш_токен_от_BotFather
USER_ID=ваш_id_от_userinfobot
EOF
```

### 4. Добавление MCP в Claude
```bash
# Из папки TG_MCP
claude mcp add telegram-live-mcp $(pwd) --scope user

# Перезапустите Claude Code после добавления
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