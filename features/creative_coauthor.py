"""
💡 Креативный соавтор - помогает в творческих процессах
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

class CreativeCoauthor:
    """Система креативного соавторства"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.projects_file = Path(f"Memory/people/{user_id}/creative_projects.json")
        self.style_file = Path(f"Memory/people/{user_id}/creative_style.json")
        self.ideas_file = Path(f"Memory/people/{user_id}/ideas_bank.json")
        
    def detect_creative_process(self, messages: List[dict]) -> Optional[Dict]:
        """Определяет, работает ли человек над чем-то творческим"""
        creative_keywords = {
            'презентация': ['презентация', 'слайды', 'powerpoint', 'выступление'],
            'текст': ['пишу', 'статья', 'пост', 'текст', 'черновик'],
            'идея': ['придумать', 'идея', 'концепция', 'предложить'],
            'проект': ['проект', 'план', 'стратегия', 'roadmap'],
            'дизайн': ['дизайн', 'макет', 'визуал', 'оформление']
        }
        
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        
        for msg in recent_messages:
            text = msg.get('text', '').lower()
            
            for project_type, keywords in creative_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return {
                        'type': project_type,
                        'detected_in': text,
                        'timestamp': msg.get('timestamp'),
                        'confidence': self._calculate_confidence(text, keywords)
                    }
        
        return None
    
    def analyze_creative_style(self, messages: List[dict]) -> Dict:
        """Анализирует творческий стиль человека"""
        style_indicators = {
            'формальность': {
                'formal': ['уважаемый', 'просим', 'необходимо', 'следует'],
                'informal': ['привет', 'короче', 'типа', 'круто']
            },
            'структурированность': {
                'structured': ['во-первых', 'пункт', 'раздел', '1.', '•'],
                'freeform': ['кстати', 'да и', 'ну и', 'вообще']
            },
            'эмоциональность': {
                'emotional': ['!', ')', 'очень', 'супер', 'обожаю'],
                'neutral': ['.', 'является', 'представляет', 'содержит']
            },
            'инновационность': {
                'innovative': ['новый', 'уникальный', 'прорыв', 'революция'],
                'traditional': ['классический', 'проверенный', 'стандартный']
            }
        }
        
        style_profile = {}
        
        # Анализируем тексты
        all_text = ' '.join([msg.get('text', '') for msg in messages])
        
        for dimension, indicators in style_indicators.items():
            scores = {}
            for style, keywords in indicators.items():
                score = sum(1 for keyword in keywords if keyword in all_text.lower())
                scores[style] = score
            
            # Определяем доминирующий стиль
            if sum(scores.values()) > 0:
                dominant = max(scores.items(), key=lambda x: x[1])
                style_profile[dimension] = {
                    'dominant': dominant[0],
                    'strength': dominant[1] / sum(scores.values())
                }
        
        # Дополнительные характеристики
        style_profile['avg_message_length'] = sum(len(msg.get('text', '')) for msg in messages) / len(messages) if messages else 0
        style_profile['uses_emoji'] = any('😀' <= char <= '🙏' for msg in messages for char in msg.get('text', ''))
        style_profile['uses_english'] = bool(re.search(r'[a-zA-Z]{3,}', all_text))
        
        # Сохраняем профиль стиля
        self._save_style(style_profile)
        return style_profile
    
    def generate_creative_suggestions(self, project: Dict, style: Dict) -> List[Dict]:
        """Генерирует креативные предложения на основе стиля"""
        suggestions = []
        project_type = project.get('type')
        
        if project_type == 'презентация':
            suggestions.extend(self._generate_presentation_ideas(project, style))
        elif project_type == 'текст':
            suggestions.extend(self._generate_text_ideas(project, style))
        elif project_type == 'идея':
            suggestions.extend(self._generate_concept_ideas(project, style))
        elif project_type == 'проект':
            suggestions.extend(self._generate_project_ideas(project, style))
        
        # Адаптируем под стиль
        adapted_suggestions = []
        for suggestion in suggestions:
            adapted = self._adapt_to_style(suggestion, style)
            adapted_suggestions.append(adapted)
        
        # Сохраняем в банк идей
        self._save_ideas(adapted_suggestions)
        
        return adapted_suggestions
    
    def _generate_presentation_ideas(self, project: Dict, style: Dict) -> List[Dict]:
        """Генерирует идеи для презентации"""
        detected_text = project.get('detected_in', '')
        
        ideas = [
            {
                'type': 'structure',
                'title': 'Структура через историю',
                'description': 'Построй презентацию как путешествие: от проблемы через открытия к решению',
                'framework': ['Контекст и боль', 'Путь поиска', 'Момент озарения', 'Решение', 'Результаты'],
                'why_works': 'Люди запоминают истории лучше фактов'
            },
            {
                'type': 'hook',
                'title': 'Начни с парадокса',
                'description': 'Открой презентацию неожиданным фактом, который противоречит ожиданиям',
                'examples': [
                    'Знаете ли вы, что 90% инноваций проваливаются не из-за технологий?',
                    'Самые успешные компании тратят на исследования меньше всех'
                ],
                'why_works': 'Когнитивный диссонанс захватывает внимание'
            },
            {
                'type': 'visual',
                'title': 'Правило 10-20-30',
                'description': '10 слайдов, 20 минут, шрифт 30pt минимум',
                'details': 'Заставляет фокусироваться на главном',
                'why_works': 'Ограничения стимулируют креативность'
            },
            {
                'type': 'engagement',
                'title': 'Интерактивные точки',
                'description': 'Каждые 3 слайда - вопрос или мини-активность для аудитории',
                'examples': [
                    'Поднимите руку, кто сталкивался с...',
                    'Напишите в чат одним словом...',
                    'Как вы думаете, сколько...'
                ],
                'why_works': 'Вовлеченность повышает запоминание на 70%'
            },
            {
                'type': 'memorable',
                'title': 'Метафора-якорь',
                'description': 'Выбери одну сильную метафору и проведи через всю презентацию',
                'examples': [
                    'Бизнес как экосистема',
                    'Проект как путешествие',
                    'Команда как оркестр'
                ],
                'why_works': 'Единая метафора создает целостность'
            }
        ]
        
        return ideas
    
    def _generate_text_ideas(self, project: Dict, style: Dict) -> List[Dict]:
        """Генерирует идеи для текстов"""
        ideas = [
            {
                'type': 'angle',
                'title': 'Переверни перспективу',
                'description': 'Расскажи историю от лица неожиданного участника',
                'examples': [
                    'От лица продукта, а не пользователя',
                    'От лица проблемы, которую решаем',
                    'Из будущего, оглядываясь назад'
                ],
                'why_works': 'Свежий угол цепляет внимание'
            },
            {
                'type': 'structure',
                'title': 'AIDA для вовлечения',
                'description': 'Attention → Interest → Desire → Action',
                'framework': [
                    'Захват внимания: провокация или вопрос',
                    'Интерес: раскрытие интриги',
                    'Желание: показ выгоды',
                    'Действие: четкий призыв'
                ],
                'why_works': 'Проверенная веками структура'
            }
        ]
        return ideas
    
    def _generate_concept_ideas(self, project: Dict, style: Dict) -> List[Dict]:
        """Генерирует концептуальные идеи"""
        ideas = [
            {
                'type': 'brainstorm',
                'title': 'SCAMPER метод',
                'description': 'Систематический подход к генерации идей',
                'framework': {
                    'S': 'Substitute - что можно заменить?',
                    'C': 'Combine - что можно объединить?',
                    'A': 'Adapt - что можно адаптировать?',
                    'M': 'Modify - что можно изменить?',
                    'P': 'Put to other uses - как еще использовать?',
                    'E': 'Eliminate - что можно убрать?',
                    'R': 'Reverse - что можно перевернуть?'
                },
                'why_works': 'Структурированный креатив дает больше идей'
            }
        ]
        return ideas
    
    def _generate_project_ideas(self, project: Dict, style: Dict) -> List[Dict]:
        """Генерирует идеи для проектов"""
        ideas = [
            {
                'type': 'framework',
                'title': 'Jobs To Be Done',
                'description': 'Фокус на задачах, а не функциях',
                'questions': [
                    'Какую работу люди нанимают этот продукт делать?',
                    'Что они делали до этого?',
                    'Какой прогресс они хотят достичь?'
                ],
                'why_works': 'Помогает найти настоящую ценность'
            }
        ]
        return ideas
    
    def _adapt_to_style(self, suggestion: Dict, style: Dict) -> Dict:
        """Адаптирует предложение под стиль пользователя"""
        adapted = suggestion.copy()
        
        # Адаптация по формальности
        formality = style.get('формальность', {}).get('dominant', 'neutral')
        if formality == 'informal':
            # Делаем язык более разговорным
            if 'description' in adapted:
                adapted['description'] = adapted['description'].replace('Используйте', 'Используй')
                adapted['description'] = adapted['description'].replace('необходимо', 'нужно')
        
        # Адаптация по структурированности
        structure = style.get('структурированность', {}).get('dominant', 'neutral')
        if structure == 'structured' and 'framework' in adapted:
            # Добавляем нумерацию
            if isinstance(adapted['framework'], list):
                adapted['framework'] = [f"{i+1}. {item}" for i, item in enumerate(adapted['framework'])]
        
        # Добавляем эмодзи если человек их использует
        if style.get('uses_emoji', False):
            adapted['title'] = self._add_relevant_emoji(adapted['title'], adapted.get('type', ''))
        
        return adapted
    
    def _add_relevant_emoji(self, text: str, suggestion_type: str) -> str:
        """Добавляет подходящие эмодзи"""
        emoji_map = {
            'structure': '🏗️',
            'hook': '🎣',
            'visual': '🎨',
            'engagement': '🤝',
            'memorable': '💎',
            'angle': '🔄',
            'brainstorm': '🧠',
            'framework': '📋'
        }
        
        emoji = emoji_map.get(suggestion_type, '💡')
        return f"{emoji} {text}"
    
    def collaborative_response(self, current_project: Dict, suggestions: List[Dict]) -> str:
        """Формирует ответ соавтора"""
        project_type = current_project.get('type', 'проект')
        
        # Выбираем топ-3 предложения
        top_suggestions = suggestions[:3]
        
        response_parts = []
        
        # Вступление
        openings = [
            f"Вижу, ты работаешь над {project_type}. Набросала несколько идей:",
            f"О, {project_type}! У меня есть пара неожиданных углов:",
            f"Думаешь над {project_type}? Вот что пришло в голову:"
        ]
        
        import random
        response_parts.append(random.choice(openings))
        response_parts.append("")
        
        # Предложения
        for i, suggestion in enumerate(top_suggestions, 1):
            response_parts.append(f"**{suggestion['title']}**")
            response_parts.append(suggestion['description'])
            
            if 'framework' in suggestion:
                if isinstance(suggestion['framework'], list):
                    for item in suggestion['framework']:
                        response_parts.append(f"  - {item}")
                elif isinstance(suggestion['framework'], dict):
                    for key, value in suggestion['framework'].items():
                        response_parts.append(f"  - **{key}**: {value}")
            
            if 'why_works' in suggestion:
                response_parts.append(f"  💡 *{suggestion['why_works']}*")
            
            response_parts.append("")
        
        # Завершение
        closings = [
            "Какая идея зацепила? Могу развить глубже!",
            "Выбирай что резонирует - додумаем вместе",
            "Это просто направления. Твой контекст сделает их уникальными"
        ]
        
        response_parts.append(random.choice(closings))
        
        return "\n".join(response_parts)
    
    def _calculate_confidence(self, text: str, keywords: List[str]) -> float:
        """Рассчитывает уверенность в определении"""
        matches = sum(1 for keyword in keywords if keyword in text.lower())
        return min(matches / len(keywords), 1.0)
    
    def _save_style(self, style: Dict):
        """Сохраняет стиль пользователя"""
        self.style_file.parent.mkdir(parents=True, exist_ok=True)
        style['last_updated'] = datetime.now().isoformat()
        
        with open(self.style_file, 'w', encoding='utf-8') as f:
            json.dump(style, f, ensure_ascii=False, indent=2)
    
    def _save_ideas(self, ideas: List[Dict]):
        """Сохраняет идеи в банк"""
        self.ideas_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Загружаем существующие идеи
        existing_ideas = []
        if self.ideas_file.exists():
            with open(self.ideas_file, 'r', encoding='utf-8') as f:
                existing_ideas = json.load(f)
        
        # Добавляем новые с временными метками
        for idea in ideas:
            idea['generated_at'] = datetime.now().isoformat()
            existing_ideas.append(idea)
        
        # Сохраняем обновленный банк
        with open(self.ideas_file, 'w', encoding='utf-8') as f:
            json.dump(existing_ideas, f, ensure_ascii=False, indent=2)
    
    def load_project_history(self) -> List[Dict]:
        """Загружает историю проектов"""
        if self.projects_file.exists():
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []