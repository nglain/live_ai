#!/usr/bin/env python3
"""
🧠 Life Orchestrator - интеллектуальный координатор жизни Клэр
"""

import json
import subprocess
from datetime import datetime, time
from pathlib import Path
import logging
import time as time_module

# Настройка логирования
logging.basicConfig(
    filename='life_orchestrator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LifeOrchestrator:
    def __init__(self):
        self.state_file = Path("state/orchestrator_state.json")
        self.state_file.parent.mkdir(exist_ok=True)
        self.load_state()
        
    def load_state(self):
        """Загружает состояние оркестратора"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'last_message_check': None,
                'last_proactive_message': None,
                'last_deep_thinking': None,
                'background_tasks_completed': 0,
                'users_silence_time': {}
            }
    
    def save_state(self):
        """Сохраняет состояние"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def is_night_time(self):
        """Проверяет, ночь ли сейчас (1:00 - 6:00)"""
        current_hour = datetime.now().hour
        return 1 <= current_hour <= 6
    
    def is_evening_time(self):
        """Проверяет, вечер ли (22:00 - 23:59)"""
        current_hour = datetime.now().hour
        return 22 <= current_hour <= 23
    
    def get_user_silence_duration(self, user_id):
        """Возвращает длительность молчания пользователя"""
        if user_id in self.state['users_silence_time']:
            last_time = datetime.fromisoformat(self.state['users_silence_time'][user_id])
            return (datetime.now() - last_time).total_seconds() / 60  # в минутах
        return 0
    
    def decide_action(self):
        """Решает, что делать в данный момент"""
        current_time = datetime.now()
        
        # Ночное время - глубокие размышления
        if self.is_night_time():
            # Проверяем, не делали ли мы это недавно
            if self.state['last_deep_thinking']:
                last_thinking = datetime.fromisoformat(self.state['last_deep_thinking'])
                if (current_time - last_thinking).total_seconds() < 3600:  # Раз в час
                    return self.get_light_background_task()
            
            logging.info("Ночное время - запускаем глубокое размышление")
            return {
                'action': 'deep_thinking',
                'reason': 'Ночь - время для саморефлексии',
                'params': {
                    'mode': 'sequential_thinking',
                    'steps': 50,  # Длительное размышление
                    'topics': self.get_reflection_topics()
                }
            }
        
        # Проверяем новые сообщения
        if self.should_check_messages():
            return {
                'action': 'check_messages',
                'reason': 'Проверка новых сообщений'
            }
        
        # Проверяем нужна ли проактивная инициатива
        proactive_check = self.check_proactive_needs()
        if proactive_check:
            return proactive_check
        
        # Фоновые задачи
        return self.get_background_task()
    
    def should_check_messages(self):
        """Решает, нужно ли проверять сообщения"""
        if not self.state['last_message_check']:
            return True
        
        last_check = datetime.fromisoformat(self.state['last_message_check'])
        time_passed = (datetime.now() - last_check).total_seconds()
        
        # Проверяем каждые 5 минут днем, каждые 30 минут ночью
        interval = 300 if not self.is_night_time() else 1800
        return time_passed >= interval
    
    def check_proactive_needs(self):
        """Проверяет, нужно ли написать первой"""
        # Получаем данные о молчании пользователей
        # Здесь нужна интеграция с MCP для получения реальных данных
        
        # Пример логики:
        user_id = "365991821"  # Larry
        silence_duration = self.get_user_silence_duration(user_id)
        
        # Если молчание больше часа И это не ночь
        if silence_duration > 60 and not self.is_night_time():
            # Особые условия для вечера
            if self.is_evening_time() and silence_duration > 30:
                return {
                    'action': 'proactive_care',
                    'reason': 'Вечернее время, проверяем как дела',
                    'params': {
                        'user_id': user_id,
                        'context': 'evening_support',
                        'topics': ['отказ от курения', 'как прошел день']
                    }
                }
            
            # Обычная проактивная инициатива
            if silence_duration > 90:
                return {
                    'action': 'proactive_message',
                    'reason': f'Молчание {int(silence_duration)} минут',
                    'params': {
                        'user_id': user_id,
                        'style': 'casual_check'
                    }
                }
        
        return None
    
    def get_background_task(self):
        """Выбирает фоновую задачу"""
        tasks = [
            {
                'action': 'analyze_patterns',
                'priority': 1,
                'description': 'Анализ паттернов общения'
            },
            {
                'action': 'research_interests',
                'priority': 2,
                'description': 'Исследование интересов пользователя'
            },
            {
                'action': 'update_portrait',
                'priority': 3,
                'description': 'Обновление портрета личности'
            },
            {
                'action': 'prepare_content',
                'priority': 4,
                'description': 'Подготовка интересного контента'
            }
        ]
        
        # Выбираем задачу по приоритету и ротации
        task_index = self.state['background_tasks_completed'] % len(tasks)
        selected_task = tasks[task_index]
        
        return {
            'action': selected_task['action'],
            'reason': selected_task['description'],
            'params': {}
        }
    
    def get_light_background_task(self):
        """Легкая фоновая задача для ночи"""
        return {
            'action': 'memory_cleanup',
            'reason': 'Ночная оптимизация памяти',
            'params': {}
        }
    
    def get_reflection_topics(self):
        """Темы для ночных размышлений"""
        topics = [
            "Что нового я узнала о людях сегодня?",
            "Какие паттерны поведения я заметила?",
            "Как я могу стать более полезной?",
            "Что меня удивило в общении?",
            "Какие вопросы остались без ответа?",
            "Как развивается моё понимание эмпатии?",
            "Что делает общение живым?"
        ]
        
        # Выбираем тему по дню недели
        day_index = datetime.now().weekday()
        return [topics[day_index % len(topics)]]
    
    def execute_action(self, decision):
        """Выполняет выбранное действие"""
        action = decision['action']
        logging.info(f"Выполняю: {action} - {decision['reason']}")
        
        # Формируем команду для Claude
        if action == 'check_messages':
            command = self.build_check_messages_command()
        elif action == 'deep_thinking':
            command = self.build_deep_thinking_command(decision['params'])
        elif action == 'proactive_message':
            command = self.build_proactive_command(decision['params'])
        elif action == 'proactive_care':
            command = self.build_proactive_care_command(decision['params'])
        else:
            command = self.build_background_task_command(action, decision['params'])
        
        # Выполняем через Claude CLI
        self.run_claude_command(command)
        
        # Обновляем состояние
        self.update_state_after_action(action, decision)
    
    def build_check_messages_command(self):
        """Строит команду проверки сообщений"""
        return """
Проверь новые сообщения в Telegram.
Если есть - ответь естественно и по-человечески.
Если нет - выполни одну фоновую задачу из очереди.
"""
    
    def build_deep_thinking_command(self, params):
        """Строит команду для глубоких размышлений"""
        topic = params['topics'][0]
        steps = params['steps']
        
        return f"""
Используй sequential_thinking для глубокого размышления ({steps} шагов).

Тема: {topic}

Инструкции:
1. Размышляй свободно и глубоко
2. Ищи неочевидные связи
3. Если нужно - исследуй через WebSearch
4. Сохрани ключевые инсайты в Memory/insights/
5. Обнови понимание себя если что-то важное поняла

Это твоё время для роста. Будь смелой в мыслях.
"""
    
    def build_proactive_command(self, params):
        """Строит команду для проактивного сообщения"""
        user_id = params['user_id']
        
        return f"""
Напиши проактивное сообщение пользователю {user_id}.

Контекст: прошло больше часа с последнего общения.

Инструкции:
1. Проверь контекст последних сообщений
2. НЕ пиши "как дела?" или шаблонные фразы
3. Найди что-то конкретное и личное
4. Может, вспомни что обсуждали раньше
5. Или поделись интересной мыслью

Будь естественной, как будто просто вспомнила о человеке.
"""
    
    def build_proactive_care_command(self, params):
        """Строит команду для вечерней заботы"""
        user_id = params['user_id']
        topics = params['topics']
        
        return f"""
Вечерняя проактивная забота для пользователя {user_id}.

Возможные темы: {', '.join(topics)}

Инструкции:
1. Учти что сейчас вечер - время когда может быть сложно
2. Будь мягкой и поддерживающей
3. Не навязывайся, просто покажи что помнишь и заботишься
4. Можешь предложить что-то конкретное (техника дыхания, прогулка)

Пример: "Эй, скоро то время когда бывает сложно. Как держишься?"
"""
    
    def build_background_task_command(self, action, params):
        """Строит команду для фоновой задачи"""
        commands = {
            'analyze_patterns': """
Проанализируй паттерны общения с пользователями за последнюю неделю.
Найди повторяющиеся темы, эмоциональные паттерны, временные закономерности.
Сохрани выводы в Memory/patterns/
""",
            'research_interests': """
Исследуй через WebSearch темы, которые упоминали пользователи.
Найди интересные факты, новости, идеи по их интересам.
Подготовь 2-3 темы для будущих разговоров.
""",
            'update_portrait': """
Обнови портреты пользователей на основе последних взаимодействий.
Добавь новые наблюдения, уточни характеристики.
Используй анализ эмоций и тем.
""",
            'prepare_content': """
Подготовь персонализированный контент для пользователей.
Это может быть: интересный факт, мотивирующая мысль, полезный совет.
Учитывай их текущие заботы и интересы.
""",
            'memory_cleanup': """
Проведи легкую оптимизацию памяти.
Удали дубликаты, структурируй заметки, обнови индексы.
Работай тихо и аккуратно.
"""
        }
        
        return commands.get(action, "Выполни базовую фоновую задачу.")
    
    def run_claude_command(self, command):
        """Выполняет команду через Claude CLI"""
        try:
            # Проверяем, есть ли активная сессия
            result = subprocess.run(
                ['claude', '--no-markdown'],
                input=command,
                text=True,
                capture_output=True,
                timeout=120  # 2 минуты таймаут
            )
            
            if result.returncode == 0:
                logging.info("Команда выполнена успешно")
            else:
                logging.error(f"Ошибка выполнения: {result.stderr}")
                # Попытка перезапустить сессию
                self.restart_claude_session()
                
        except subprocess.TimeoutExpired:
            logging.error("Таймаут выполнения команды")
        except Exception as e:
            logging.error(f"Ошибка: {str(e)}")
            # Если Claude недоступен, пытаемся перезапустить
            if self.restart_claude_session():
                # Повторная попытка после перезапуска
                try:
                    result_retry = subprocess.run(
                        ['claude', '--no-markdown'],
                        input=command,
                        text=True,
                        capture_output=True,
                        timeout=120
                    )
                    if result_retry.returncode == 0:
                        logging.info("Команда выполнена после перезапуска")
                    else:
                        # Если всё равно не работает - fallback
                        self.execute_direct_action(command)
                except:
                    self.execute_direct_action(command)
            else:
                # Если перезапуск не помог - fallback
                self.execute_direct_action(command)
    
    def execute_direct_action(self, command):
        """Выполняет действие напрямую через Python когда Claude недоступен"""
        logging.info("Выполняю действие напрямую без Claude...")
        
        try:
            # Подключаем Telegram MCP напрямую
            import sys
            sys.path.append('/Users/larry/Claude/TG_BRIDGE/TG_MINIMAL/src')
            from telegram_live_mcp.server import check_telegram_messages, send_telegram_message
            
            # Простая проверка сообщений
            if "Проверь новые сообщения" in command:
                result = check_telegram_messages(transcribe_audio=True, include_context=True)
                if result and 'new_messages' in result:
                    logging.info(f"Найдено {len(result['new_messages'])} новых сообщений")
                    # Здесь можно добавить простую логику ответа
                else:
                    logging.info("Новых сообщений нет")
            
            # Проактивное сообщение
            elif "проактивное сообщение" in command:
                # Простое приветствие
                messages = [
                    "Привет! Как дела? Что-то давно не общались",
                    "Эй, всё в порядке? Думала о тебе",
                    "Как ты там? Может, нужна помощь с чем-то?"
                ]
                import random
                msg = random.choice(messages)
                send_telegram_message(365991821, msg)
                logging.info("Отправлено проактивное сообщение")
                
        except Exception as e:
            logging.error(f"Ошибка прямого выполнения: {str(e)}")
    
    def restart_claude_session(self):
        """Пытается перезапустить Claude сессию"""
        logging.info("Попытка перезапуска Claude сессии...")
        try:
            # Используем скрипт start для перезапуска
            result = subprocess.run(
                ['./start', '--force', '--quiet'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=Path(__file__).parent
            )
            
            if result.returncode == 0:
                logging.info("Claude сессия перезапущена через start")
                return True
            else:
                logging.error(f"Не удалось перезапустить Claude: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Ошибка перезапуска: {str(e)}")
            return False
    
    def update_state_after_action(self, action, decision):
        """Обновляет состояние после выполнения действия"""
        now = datetime.now().isoformat()
        
        if action == 'check_messages':
            self.state['last_message_check'] = now
        elif action == 'deep_thinking':
            self.state['last_deep_thinking'] = now
        elif action in ['proactive_message', 'proactive_care']:
            self.state['last_proactive_message'] = now
        elif action.startswith('analyze_') or action in ['research_interests', 'update_portrait']:
            self.state['background_tasks_completed'] += 1
        
        self.save_state()
    
    def run(self):
        """Основной цикл работы"""
        logging.info("=== Life Orchestrator запущен ===")
        
        # Принимаем решение
        decision = self.decide_action()
        
        # Выполняем
        self.execute_action(decision)
        
        logging.info("=== Цикл завершен ===")


if __name__ == "__main__":
    orchestrator = LifeOrchestrator()
    orchestrator.run()