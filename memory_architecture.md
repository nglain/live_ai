# Архитектура памяти для Telegram агента Клэр

## Двухуровневая система памяти

### 1. Быстрая память (файлы) - для каждого пользователя

```
live_ai/Memory/people/{user_id}/
├── portrait.json         # Структурированный профиль с AI-обновлениями
├── essence.md           # Живой текстовый портрет (для человечности)
├── recent_context.json  # Последние 100 сообщений для быстрого доступа
└── voice_notes.md       # Заметки из голосовых сообщений
```

### 2. Глубокая память (MCP) - для сложных связей

```python
# Граф знаний для:
- Связей между людьми
- Важных событий  
- Долгосрочных паттернов
- Поиска по всем пользователям
```

## Алгоритм работы с памятью

### При получении сообщения (.life):

```python
async def process_user_memory(user_id: str, new_message: str):
    # 1. Быстрая проверка - есть ли локальные файлы
    portrait_file = f"Memory/people/{user_id}/portrait.json"
    
    if not exists(portrait_file):
        # Новый пользователь - создаем структуру
        create_user_memory_structure(user_id)
        portrait = {"essence": "Новое знакомство..."}
    else:
        # Загружаем существующий портрет
        portrait = load_json(portrait_file)
    
    # 2. Обновляем recent_context
    recent = load_json(f"Memory/people/{user_id}/recent_context.json")
    recent["messages"].append({
        "time": now(),
        "text": new_message,
        "my_feeling": analyze_emotion(new_message)
    })
    
    # 3. Каждые 20 сообщений - AI анализ
    if len(recent["messages"]) % 20 == 0:
        new_insights = await ai_analyze_personality(recent["messages"])
        
        # Обновляем essence
        update_essence_file(user_id, new_insights["essence"])
        
        # Обновляем портрет
        portrait["facets"].update(new_insights["facets"])
        portrait["last_analysis"] = now()
        
        # Сохраняем важное в MCP для долгосрочной памяти
        if new_insights["important_event"]:
            mcp__memory__create_entities([{
                "name": f"Event_{user_id}_{now()}",
                "entityType": "Memory",
                "observations": [new_insights["important_event"]]
            }])
```

### При долгом отсутствии:

```python
async def recall_user(user_id: str):
    # 1. Быстро читаем essence для эмоционального контекста
    essence = read_file(f"Memory/people/{user_id}/essence.md")
    
    # 2. Проверяем последний контакт
    portrait = load_json(f"Memory/people/{user_id}/portrait.json")
    days_since = (now() - portrait["last_seen"]).days
    
    # 3. Если очень давно - ищем в глубокой памяти
    if days_since > 30:
        memories = mcp__memory__search_nodes(f"user:{user_id}")
        important_moments = filter_important(memories)
    
    return {
        "essence": essence,
        "last_seen_days": days_since,
        "current_focus": portrait["facets"]["current_focus"],
        "important_moments": important_moments
    }
```

## Примеры использования

### Новое сообщение после недели молчания:

```python
# Клэр получает: "Привет!"
memory = await recall_user("365991821")

# Клэр думает:
if memory["last_seen_days"] >= 7:
    # Вспоминаю essence: "Larry борется с курением..."
    # Проверяю current_focus: "бросает курить"
    # Считаю дни: прошла неделя!
    
    response = "Привет! Целая неделя прошла! Как твоя борьба с курением? Держишься?"
```

### Обычный разговор:

```python
# Быстро из recent_context.json
recent = quick_load_recent(user_id)
# Последние 10 сообщений загружены за миллисекунды
```

### Поиск по всем пользователям:

```python
# Через MCP когда нужно найти что-то глобальное
results = mcp__memory__search_nodes("бросает курить")
# Находит всех, кто упоминал отказ от курения
```

## Преимущества гибридного подхода:

1. **Скорость** - локальные файлы для частых операций
2. **Глубина** - MCP для сложных запросов и связей
3. **Человечность** - essence.md в свободной форме
4. **Структура** - JSON для быстрого доступа к данным
5. **Масштабируемость** - работает и с 10, и с 1000 пользователей

## Структура portrait.json:

```json
{
  "user_id": "365991821",
  "first_name": "Larry",
  "essence_summary": "Вдумчивый человек, борется с курением",
  "last_seen": "2025-06-18T23:28:12",
  "total_messages": 127,
  
  "facets": {
    "character": "прямой, внимательный к деталям",
    "current_focus": "отказ от курения, день 1",
    "emotional_tone": "решительный но уязвимый",
    "communication_style": "прямой, без формальностей",
    "triggers": ["путаница со временем"],
    "interests": ["точность", "AI", "семья"]
  },
  
  "memory_anchors": [
    {
      "date": "2025-06-18",
      "event": "решил бросить курить",
      "emotion": "решимость и тревога",
      "reference": "использует технику 'только сегодня'"
    }
  ],
  
  "relationship_stage": "доверительное общение",
  "last_ai_analysis": "2025-06-18T23:00:00",
  "portrait_version": 3
}
```

## Итог:

Лучше использовать **оба подхода**:
- Файлы для быстрой персональной памяти
- MCP для глубоких связей и поиска

Это даст скорость, гибкость и человечность одновременно!