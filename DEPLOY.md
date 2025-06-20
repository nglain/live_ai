# 🚀 Запуск Клэр на сервере

## Пошаговая инструкция

### 1. Подготовка сервера
```bash
# Убедитесь что установлены:
- Python 3.8+
- pip
- git
- Claude CLI (https://claude.ai/download)
```

### 2. Клонирование и настройка
```bash
# Создаём рабочую папку
mkdir -p ~/AI && cd ~/AI

# Клонируем оба репозитория
git clone https://github.com/nglainAI/TG_MCP.git
git clone https://github.com/nglainAI/live_ai.git

# Настраиваем Telegram MCP
cd TG_MCP
pip install -r requirements.txt

# ВАЖНО: .env файл с тестовыми ключами уже есть в live_ai!
# Просто копируем его в TG_MCP:
cp ../live_ai/.env .env

# Если хотите использовать свои ключи, отредактируйте:
# nano .env

# Возвращаемся и настраиваем MCP серверы
cd ../live_ai
./setup_mcp.sh
```

### 3. Первый запуск Claude
```bash
# В первом терминале запускаем Claude
claude chat

# Дожидаемся полной загрузки
# Claude должен показать приглашение для ввода
```

### 4. Запуск жизни Клэр
```bash
# Во втором терминале (или screen/tmux)
cd ~/AI/live_ai
./life

# Выберите режим:
# 1 - команда .life (полная жизнь)
# 2 - быстрые проверки каждую минуту
# 3 - глубокая жизнь каждые 5 минут
```

### 5. Проверка работы
- Напишите вашему боту в Telegram
- Клэр должна ответить в течение выбранного интервала
- Проверьте логи в терминале с ./life

## 🔧 Запуск в фоне (production)

### Вариант 1: Screen
```bash
# Создаём screen сессии
screen -S claude
claude chat
# Ctrl+A, D для выхода

screen -S claire
cd ~/AI/live_ai && ./life
# Ctrl+A, D для выхода

# Возврат к сессиям
screen -r claude
screen -r claire
```

### Вариант 2: Systemd службы
```bash
# Создаём службу для Claude
sudo nano /etc/systemd/system/claude.service

[Unit]
Description=Claude Chat
After=network.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/home/ваш_пользователь
ExecStart=/usr/local/bin/claude chat
Restart=always

[Install]
WantedBy=multi-user.target

# Создаём службу для Клэр
sudo nano /etc/systemd/system/claire.service

[Unit]
Description=Claire Life
After=network.target claude.service

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/home/ваш_пользователь/AI/live_ai
ExecStart=/home/ваш_пользователь/AI/live_ai/life
Restart=always

[Install]
WantedBy=multi-user.target

# Активируем и запускаем
sudo systemctl enable claude claire
sudo systemctl start claude
sleep 10  # Даём Claude запуститься
sudo systemctl start claire
```

### Вариант 3: Docker (если нужна изоляция)
```dockerfile
# Dockerfile будет добавлен позже
```

## 📊 Мониторинг

### Проверка статуса
```bash
# Если используете systemd
sudo systemctl status claude claire

# Если используете screen
screen -ls

# Проверка логов
journalctl -u claire -f
```

### Проверка памяти Клэр
```bash
cd ~/AI/live_ai
find Memory/people -name "*.md" -exec head -5 {} \;
```

## 🚨 Решение проблем

**Claude не запускается**
- Проверьте установку: `which claude`
- Проверьте API ключ: `claude auth status`

**Клэр не отвечает в Telegram**
- Проверьте .env в TG_MCP
- Проверьте токен бота и ID пользователя
- Посмотрите логи в терминале с ./life

**"No active session found"**
- Claude должен быть запущен первым
- Проверьте что claude chat активен

## 🔐 Безопасность

1. **Никогда не коммитьте .env файлы**
2. **Используйте отдельного пользователя для запуска**
3. **Ограничьте доступ к папке Memory/**
4. **Регулярно делайте бэкапы Memory/**

## 📝 Обслуживание

### Ежедневно
- Проверяйте логи на ошибки
- Следите за размером Memory/

### Еженедельно
- Бэкап папки Memory/
- Проверка обновлений репозиториев

### Ежемесячно
- Ротация логов
- Очистка старых файлов в temp/

---

После запуска Клэр начнёт жить своей жизнью, отвечать на сообщения и развиваться!