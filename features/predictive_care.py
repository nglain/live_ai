"""
🧠 Предсказание потребностей - анализ паттернов и проактивная поддержка
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

class PredictiveCare:
    """Система предсказания потребностей пользователя"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.patterns_file = Path(f"Memory/people/{user_id}/patterns.json")
        self.predictions_file = Path(f"Memory/people/{user_id}/predictions.json")
        
    def analyze_patterns(self, messages: List[dict]) -> Dict:
        """Анализирует паттерны в сообщениях"""
        patterns = {
            "time_patterns": self._analyze_time_patterns(messages),
            "emotional_patterns": self._analyze_emotional_patterns(messages),
            "topic_patterns": self._analyze_topic_patterns(messages),
            "struggle_patterns": self._analyze_struggles(messages)
        }
        
        # Сохраняем паттерны
        self._save_patterns(patterns)
        return patterns
    
    def _analyze_time_patterns(self, messages: List[dict]) -> Dict:
        """Находит временные паттерны"""
        time_topics = defaultdict(list)
        
        for msg in messages:
            if 'timestamp' in msg:
                time = datetime.fromisoformat(msg['timestamp'])
                hour = time.hour
                text = msg.get('text', '').lower()
                
                # Категоризируем по времени суток
                if 6 <= hour < 12:
                    period = "morning"
                elif 12 <= hour < 18:
                    period = "afternoon"
                elif 18 <= hour < 22:
                    period = "evening"
                else:
                    period = "night"
                
                time_topics[period].append({
                    'time': time.strftime('%H:%M'),
                    'text': text,
                    'topics': self._extract_topics(text)
                })
        
        # Находим повторяющиеся темы по времени
        patterns = {}
        for period, entries in time_topics.items():
            topic_freq = defaultdict(int)
            for entry in entries:
                for topic in entry['topics']:
                    topic_freq[topic] += 1
            
            # Топ темы для каждого периода
            if topic_freq:
                patterns[period] = {
                    'common_topics': sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:3],
                    'typical_time': self._find_typical_time(entries)
                }
        
        return patterns
    
    def _analyze_emotional_patterns(self, messages: List[dict]) -> Dict:
        """Анализирует эмоциональные паттерны"""
        emotions_by_time = defaultdict(list)
        
        emotion_keywords = {
            'тревога': ['сложно', 'тяжело', 'сорвусь', 'не могу', 'грустно', 'устал'],
            'радость': ['супер', 'круто', 'отлично', 'рад', 'счастлив', 'класс'],
            'решимость': ['буду', 'смогу', 'держусь', 'стараюсь', 'борюсь'],
            'сомнение': ['может', 'наверное', 'не уверен', 'не знаю', 'как бы']
        }
        
        for msg in messages:
            text = msg.get('text', '').lower()
            time = datetime.fromisoformat(msg['timestamp'])
            hour = time.hour
            
            detected_emotions = []
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in text for keyword in keywords):
                    detected_emotions.append(emotion)
            
            if detected_emotions:
                emotions_by_time[hour].extend(detected_emotions)
        
        # Анализируем преобладающие эмоции по времени
        emotional_patterns = {}
        for hour, emotions in emotions_by_time.items():
            if emotions:
                emotion_freq = defaultdict(int)
                for emotion in emotions:
                    emotion_freq[emotion] += 1
                
                dominant = max(emotion_freq.items(), key=lambda x: x[1])
                emotional_patterns[f"{hour:02d}:00"] = {
                    'dominant_emotion': dominant[0],
                    'frequency': dominant[1] / len(emotions)
                }
        
        return emotional_patterns
    
    def _analyze_struggles(self, messages: List[dict]) -> Dict:
        """Находит моменты борьбы и что помогает"""
        struggles = []
        
        struggle_keywords = ['сложно', 'тяжело', 'хочется', 'сорвусь', 'не могу']
        success_keywords = ['держусь', 'получилось', 'смог', 'легче', 'помогло']
        
        for i, msg in enumerate(messages):
            text = msg.get('text', '').lower()
            time = datetime.fromisoformat(msg['timestamp'])
            
            # Ищем упоминания борьбы
            if any(keyword in text for keyword in struggle_keywords):
                struggle_entry = {
                    'time': time.strftime('%H:%M'),
                    'weekday': time.strftime('%A'),
                    'text': text,
                    'resolved': False,
                    'what_helped': None
                }
                
                # Проверяем следующие сообщения на разрешение
                for j in range(i+1, min(i+10, len(messages))):
                    next_text = messages[j].get('text', '').lower()
                    if any(keyword in next_text for keyword in success_keywords):
                        struggle_entry['resolved'] = True
                        struggle_entry['what_helped'] = next_text
                        break
                
                struggles.append(struggle_entry)
        
        # Анализируем паттерны
        struggle_times = [s['time'] for s in struggles]
        struggle_days = [s['weekday'] for s in struggles]
        
        return {
            'common_struggle_times': self._find_common_times(struggle_times),
            'difficult_days': self._find_common_items(struggle_days),
            'success_rate': len([s for s in struggles if s['resolved']]) / len(struggles) if struggles else 0,
            'what_helps': [s['what_helped'] for s in struggles if s['what_helped']]
        }
    
    def generate_predictions(self, patterns: Dict) -> List[Dict]:
        """Генерирует предсказания на основе паттернов"""
        predictions = []
        now = datetime.now()
        
        # Предсказания на основе временных паттернов
        time_patterns = patterns.get('time_patterns', {})
        current_period = self._get_time_period(now.hour)
        
        if current_period in time_patterns:
            period_data = time_patterns[current_period]
            common_topics = period_data.get('common_topics', [])
            
            if common_topics:
                top_topic = common_topics[0][0]
                predictions.append({
                    'type': 'time_based',
                    'confidence': 0.8,
                    'prediction': f"Обычно в это время тебя волнует {top_topic}",
                    'action': 'proactive_support',
                    'trigger_time': now + timedelta(minutes=30)
                })
        
        # Предсказания на основе эмоциональных паттернов
        emotional_patterns = patterns.get('emotional_patterns', {})
        current_hour = f"{now.hour:02d}:00"
        
        if current_hour in emotional_patterns:
            emotion_data = emotional_patterns[current_hour]
            if emotion_data['dominant_emotion'] == 'тревога' and emotion_data['frequency'] > 0.6:
                predictions.append({
                    'type': 'emotional',
                    'confidence': emotion_data['frequency'],
                    'prediction': f"В {current_hour} часто бывает тревожно",
                    'action': 'preemptive_comfort',
                    'trigger_time': now - timedelta(minutes=10)  # За 10 минут до
                })
        
        # Предсказания на основе паттернов борьбы
        struggle_patterns = patterns.get('struggle_patterns', {})
        common_times = struggle_patterns.get('common_struggle_times', [])
        
        for struggle_time in common_times[:2]:  # Топ-2 времени
            hour, minute = map(int, struggle_time.split(':'))
            trigger = now.replace(hour=hour, minute=minute) - timedelta(minutes=15)
            
            if trigger > now:  # Если время еще не прошло сегодня
                predictions.append({
                    'type': 'struggle_prediction',
                    'confidence': 0.7,
                    'prediction': f"Около {struggle_time} бывает сложно",
                    'action': 'preventive_support',
                    'trigger_time': trigger,
                    'what_helped': struggle_patterns.get('what_helps', [])
                })
        
        # Сохраняем предсказания
        self._save_predictions(predictions)
        return predictions
    
    def get_proactive_message(self, prediction: Dict) -> Optional[str]:
        """Генерирует проактивное сообщение на основе предсказания"""
        messages = {
            'proactive_support': [
                "Привет! Как дела с {topic}? Если нужна поддержка - я рядом",
                "Думаю о тебе. Все в порядке с {topic}?",
                "Обычно в это время ты переживаешь о {topic}. Как сегодня?"
            ],
            'preemptive_comfort': [
                "Эй, скоро то время, когда бывает тревожно. Помнишь технику дыхания?",
                "Чувствую, приближается сложное время. Может, прогуляешься?",
                "Знаю, вечер бывает непростым. Я с тобой, если что"
            ],
            'preventive_support': [
                "Через 15 минут то время, когда обычно сложно. Вот что помогало раньше: {what_helped}",
                "Скоро может накрыть желание. Помнишь - только сегодня не курить!",
                "Приближается триггерное время. Может, заранее заваришь чай?"
            ]
        }
        
        action = prediction.get('action')
        if action in messages:
            import random
            template = random.choice(messages[action])
            
            # Подставляем данные
            if '{topic}' in template:
                topic = prediction.get('prediction', '').split()[-1]
                template = template.replace('{topic}', topic)
            
            if '{what_helped}' in template:
                helped = prediction.get('what_helped', [])
                if helped:
                    template = template.replace('{what_helped}', random.choice(helped))
                else:
                    template = template.replace('{what_helped}', 'глубокое дыхание и отвлечение')
            
            return template
        
        return None
    
    def _extract_topics(self, text: str) -> List[str]:
        """Извлекает темы из текста"""
        topics = []
        
        topic_keywords = {
            'курение': ['курить', 'сигарет', 'бросил', 'курю'],
            'работа': ['работа', 'проект', 'задача', 'дедлайн'],
            'семья': ['дети', 'жена', 'сын', 'дочь', 'семья'],
            'здоровье': ['устал', 'болит', 'сон', 'спать'],
            'эмоции': ['грустно', 'радостно', 'тревожно', 'спокойно']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _find_typical_time(self, entries: List[dict]) -> str:
        """Находит типичное время"""
        if not entries:
            return "00:00"
        
        times = [e['time'] for e in entries]
        # Простое усреднение (можно улучшить)
        return times[len(times)//2]
    
    def _find_common_times(self, times: List[str]) -> List[str]:
        """Находит часто встречающиеся времена"""
        from collections import Counter
        time_counts = Counter(times)
        return [time for time, count in time_counts.most_common(3)]
    
    def _find_common_items(self, items: List[str]) -> List[str]:
        """Находит часто встречающиеся элементы"""
        from collections import Counter
        item_counts = Counter(items)
        return [item for item, count in item_counts.most_common(3)]
    
    def _get_time_period(self, hour: int) -> str:
        """Определяет период суток"""
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def _save_patterns(self, patterns: Dict):
        """Сохраняет паттерны в файл"""
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)
    
    def _save_predictions(self, predictions: List[Dict]):
        """Сохраняет предсказания"""
        self.predictions_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Конвертируем datetime в строки
        for pred in predictions:
            if 'trigger_time' in pred and hasattr(pred['trigger_time'], 'isoformat'):
                pred['trigger_time'] = pred['trigger_time'].isoformat()
        
        with open(self.predictions_file, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, ensure_ascii=False, indent=2, default=str)