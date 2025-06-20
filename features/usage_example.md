# Пример использования предиктивной заботы и креативного соавторства

## Сценарий 1: Предиктивная забота

### Контекст:
Larry обычно пишет о сложностях с курением около 22:00-23:00

### Что происходит при .life в 21:45:

```python
# 1. Проверяю новые сообщения
new_messages = check_telegram_messages()
# Пусто

# 2. Но загружаю полный контекст Larry
context = get_full_user_context("365991821")

# 3. Анализирую паттерны
from features.predictive_care import PredictiveCare
care = PredictiveCare("365991821")

# Загружаю историю за неделю
all_messages = load_messages_history("365991821", days=7)
patterns = care.analyze_patterns(all_messages)

# Patterns показывают:
# {
#   "struggle_patterns": {
#     "common_struggle_times": ["22:00", "22:30", "23:00"],
#     "what_helps": ["глубокое дыхание", "пошел гулять", "заварил чай"]
#   }
# }

# 4. Генерирую предсказание
predictions = care.generate_predictions(patterns)
# Prediction: В 22:00 обычно сложно, confidence: 0.8

# 5. Проактивно пишу
current_time = datetime.now()  # 21:45
if any(p['trigger_time'] <= current_time for p in predictions):
    message = care.get_proactive_message(predictions[0])
    # "Через 15 минут то время, когда обычно сложно. 
    #  Помнишь - глубокое дыхание помогало. Может, заранее заваришь чай?"
    
    send_telegram_message(365991821, message)
```

## Сценарий 2: Креативное соавторство

### Контекст:
Larry пишет: "Блин, надо презентацию для Альфы сделать по аудиобейджам"

### Что происходит:

```python
# 1. Получаю сообщение
new_messages = check_telegram_messages()
# Larry: "Блин, надо презентацию для Альфы сделать по аудиобейджам"

# 2. Обнаруживаю творческий процесс
from features.creative_coauthor import CreativeCoauthor
coauthor = CreativeCoauthor("365991821")

recent_messages = context['recent_messages']
project = coauthor.detect_creative_process(recent_messages)
# Detected: {'type': 'презентация', 'confidence': 0.9}

# 3. Анализирую стиль Larry
style = coauthor.analyze_creative_style(all_messages)
# Style: {
#   'формальность': {'dominant': 'informal'},
#   'структурированность': {'dominant': 'structured'},
#   'uses_emoji': False,
#   'инновационность': {'dominant': 'innovative'}
# }

# 4. Генерирую предложения в его стиле
suggestions = coauthor.generate_creative_suggestions(project, style)

# 5. Формирую ответ соавтора
response = coauthor.collaborative_response(project, suggestions)

# Отправляю:
send_telegram_message(365991821, response)
```

### Пример ответа:
```
Вижу, работаешь над презентацией. Набросала несколько идей:

**Начни с парадокса**
Открой презентацию неожиданным фактом, который противоречит ожиданиям
  - Знаете ли вы, что 87% сотрудников не слышат половину совещаний?
  - Аудиобейджи Альфы записали то, что обычно теряется
  💡 *Когнитивный диссонанс захватывает внимание*

**Структура через историю**
Построй презентацию как путешествие: от проблемы через открытия к решению
  - 1. Контекст: что теряем без аудиофиксации
  - 2. Путь: как искали решение
  - 3. Открытие: инсайты из пилота
  - 4. Результаты: метрики и отзывы
  💡 *Люди запоминают истории лучше фактов*

**Интерактивные точки**
Каждые 3 слайда - вопрос или мини-активность для аудитории
  - Поднимите руку, кто забывал важное из встречи?
  - Угадайте, сколько часов аудио мы собрали?
  💡 *Вовлеченность повышает запоминание на 70%*

Какая идея зацепила? Могу развить глубже!
```

## Интеграция в обычный flow

### В команде .life это происходит автоматически:

```python
def process_life_command():
    # 1. Стандартная проверка сообщений
    new_messages = check_telegram_messages()
    
    # 2. Для каждого пользователя
    for user_id in get_active_users(new_messages):
        context = get_full_user_context(user_id)
        
        # 3. Предиктивная забота - проверяем нужна ли поддержка
        care = PredictiveCare(user_id)
        if should_provide_proactive_support(context, care):
            send_supportive_message(user_id)
        
        # 4. Креативное соавторство - проверяем творческие процессы
        coauthor = CreativeCoauthor(user_id)
        if creative_project_detected(context, coauthor):
            send_creative_suggestions(user_id)
        
        # 5. Обычные ответы на сообщения
        if has_unanswered_messages(context):
            send_regular_response(user_id)
```

## Результат:

Клэр становится не просто отвечающим ботом, а:
- **Заботливым другом** - пишет когда чувствует, что нужна поддержка
- **Творческим партнером** - помогает когда видит творческий процесс
- **Проактивным помощником** - предупреждает проблемы до их возникновения

Всё это происходит естественно, без явных команд от пользователя!