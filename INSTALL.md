# 🛠️ Полная инструкция установки

## Требования
- Python 3.8+
- pip
- Claude CLI
- Node.js (для некоторых MCP серверов)

## Пошаговая установка

### 1. Клонируйте репозитории
```bash
mkdir -p ~/AI && cd ~/AI
git clone https://github.com/nglainAI/TG_MCP.git
git clone https://github.com/nglainAI/live_ai.git
```

### 2. Установите TG_MCP (Python проект)
```bash
cd ~/AI/TG_MCP

# Установите зависимости Python
pip install -r requirements.txt
# или если pip3:
pip3 install -r requirements.txt

# Создайте конфигурацию
cat > .env << EOF
BOT_TOKEN=ваш_токен_от_BotFather
USER_ID=ваш_telegram_id
EOF
```

### 3. Установите MCP серверы
```bash
cd ~/AI/live_ai

# Автоматическая установка всех MCP
./setup_mcp.sh

# ИЛИ вручную:
claude mcp add telegram-live-mcp ~/AI/TG_MCP --scope user
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking --scope user
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer --scope user
claude mcp add fetch npx @kazuph/mcp-fetch --scope user
```

### 4. Перезапустите Claude Code
Закройте и откройте Claude Code для применения изменений.

### 5. Запустите Клэр
```bash
# Терминал 1
claude chat

# Терминал 2
cd ~/AI/live_ai
./life
```

## Решение проблем

### "npm install" не работает в TG_MCP
TG_MCP - это Python проект! Используйте:
```bash
pip install -r requirements.txt
```

### "pip: command not found"
Установите pip:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3-pip

# macOS
brew install python3

# или используйте pip3
pip3 install -r requirements.txt
```

### "claude: command not found"
Установите Claude CLI с https://claude.ai/download

### MCP серверы не работают
1. Проверьте установку: `claude mcp list`
2. Перезапустите Claude Code
3. Убедитесь что пути правильные