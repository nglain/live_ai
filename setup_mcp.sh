#!/bin/bash
# 🚀 Установка всех MCP серверов для Клэр

echo "🌟 Установка MCP серверов для Клэр..."
echo ""

# Цвета
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Telegram MCP (локальный Python проект)
echo -e "${CYAN}1. Установка Telegram MCP...${NC}"
if [ -d "../TG_MCP" ]; then
    # Проверяем установлены ли зависимости Python
    if [ ! -f "../TG_MCP/.env" ]; then
        echo "⚠️  Создайте .env файл в TG_MCP с токенами!"
    fi
    claude mcp add telegram-live-mcp $(cd ../TG_MCP && pwd) --scope user
    echo -e "${GREEN}✓ Telegram MCP добавлен${NC}"
else
    echo "❌ Папка TG_MCP не найдена. Установите сначала:"
    echo "   cd .. && git clone https://github.com/nglainAI/TG_MCP.git"
    echo "   cd TG_MCP && pip install -r requirements.txt"
fi

# 2. Sequential Thinking
echo -e "${CYAN}2. Установка Sequential Thinking...${NC}"
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking --scope user
echo -e "${GREEN}✓ Sequential Thinking добавлен${NC}"

# 3. Puppeteer (опционально)
echo -e "${CYAN}3. Установка Puppeteer...${NC}"
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer --scope user
echo -e "${GREEN}✓ Puppeteer добавлен${NC}"

# 4. Fetch
echo -e "${CYAN}4. Установка Fetch...${NC}"
claude mcp add fetch npx @kazuph/mcp-fetch --scope user
echo -e "${GREEN}✓ Fetch добавлен${NC}"

# 5. MCP_CORE (опционально - для глубинной памяти)
echo ""
echo -e "${CYAN}5. MCP_CORE (опционально)...${NC}"
if [ -d "../MCP_CORE" ]; then
    echo -e "${YELLOW}Найден MCP_CORE! Для установки:${NC}"
    echo "   cd ../MCP_CORE"
    echo "   npm install && npm run build"
    echo "   claude mcp add core-memory node $(cd ../MCP_CORE && pwd)/build/index.js --scope user"
    echo -e "${YELLOW}Это даст доступ к глубинной памяти CLARITY${NC}"
else
    echo "MCP_CORE не найден (это нормально)"
    echo "Клэр будет использовать локальную память Memory/"
fi

echo ""
echo -e "${GREEN}✅ Основные MCP серверы установлены!${NC}"
echo ""
echo "⚠️  Теперь перезапустите Claude Code для применения изменений"