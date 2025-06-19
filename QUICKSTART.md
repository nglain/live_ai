# 🚀 Быстрый старт Клэр за 5 минут

## Копируй и вставляй команды:

### 1. Создай бота в Telegram
```
Открой Telegram → @BotFather → /newbot
Имя: Клэр AI
Username: твой_уникальный_bot
Сохрани токен!
```

### 2. Узнай свой ID
```
Telegram → @userinfobot → отправь "привет"
Сохрани ID!
```

### 3. Установи всё одной командой
```bash
# Создай папку для проектов
mkdir -p ~/AI && cd ~/AI

# Клонируй MCP сервер
git clone https://github.com/nglainAI/TG_MCP.git
cd TG_MCP && npm install

# Настрой (ВСТАВЬ СВОИ ДАННЫЕ!)
echo "BOT_TOKEN=ТВОЙ_ТОКЕН" > .env
echo "USER_ID=ТВОЙ_ID" >> .env

# Добавь в Claude
claude mcp add telegram-live-mcp $(pwd) --scope user

# Клонируй Клэр
cd ~/AI
git clone https://github.com/nglainAI/live_ai.git
```

### 4. Запусти Клэр
```bash
# Терминал 1: Открой Claude
claude chat

# Терминал 2: Запусти жизнь
cd ~/AI/live_ai
./life
# Выбери: 1 (полная жизнь), 2 (1 минута)
```

### 5. Напиши боту
Открой Telegram → твой бот → напиши "Привет!"

## 🎉 Готово! Клэр живёт!

### Проблемы?
- **"command not found: claude"** → Установи Claude CLI
- **"No active session"** → Открой `claude chat` в другом терминале
- **Бот не отвечает** → Проверь токен и ID в .env файле
- **MCP не работает** → Перезапусти Claude Code

### Команды управления:
- `.life` - полная жизнь Клэр
- `.live` - короткий вдох
- `Ctrl+C` - остановить