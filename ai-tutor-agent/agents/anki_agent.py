"""
Anki Card Generator Agent
Creates flashcards in Anki format
"""
from typing import Dict, List, Any
import uuid
from .base_agent import BaseAgent


class AnkiAgent(BaseAgent):
    """
    Agent responsible for creating Anki flashcards.
    Supports multiple card types: basic, cloze, reverse.
    """
    
    def __init__(self, llm_client):
        super().__init__(llm_client, name="AnkiAgent")
        self.system_prompt = """Ты - эксперт по созданию эффективных карточек для запоминания.
Твоя задача:
1. Создавать карточки по принципу активной реколлекции
2. Делать вопросы конкретными и однозначными
3. Использовать интервальное повторение принципы
4. Избегать излишней сложности на одной карточке
5. Включать контекст когда нужно

Следуй принципам SuperMemo-2."""
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Anki cards from content
        
        Args:
            input_data: dict with:
                - content: source material
                - card_types: list of desired types (basic, cloze, reverse)
                - count: approximate number of cards
                - deck_name: name for the deck
                
        Returns:
            Dict with generated cards in Anki format
        """
        content = input_data.get('content', '')
        card_types = input_data.get('card_types', ['basic'])
        count = input_data.get('count', 20)
        deck_name = input_data.get('deck_name', 'AI Tutor Deck')
        
        if not content:
            raise ValueError("No content provided")
        
        cards = self._generate_cards(content, card_types, count, deck_name)
        
        return {
            'cards': cards,
            'deck_name': deck_name,
            'count': len(cards),
            'type': 'anki_cards'
        }
    
    def _generate_cards(self, content: str, card_types: List[str], 
                       count: int, deck_name: str) -> List[Dict]:
        """Generate Anki cards using LLM"""
        
        type_descriptions = {
            'basic': 'Базовая карточка: Вопрос → Ответ',
            'cloze': 'Карточка с пропуском: заполни пропущенное слово/фразу',
            'reverse': 'Обратная карточка: Ответ → Вопрос (для двунаправленного обучения)'
        }
        
        requested_types = [card_types[0]] if card_types else ['basic']
        
        prompt = f"""Создай карточки Anki для запоминания следующего материала.

Типы карточек: {[types_descriptions.get(t, t) for t in requested_types]}
Количество: примерно {count} карточек
Колода: {deck_name}

Материал:
{content[:8000]}

Принципы создания хороших карточек:
1. Одна идея = одна карточка
2. Вопросы должны быть конкретными и однозначными
3. Ответы должны быть краткими
4. Используй свои слова, не копируй текст
5. Для cloze: выбирай ключевые термины/понятия

Ответь в формате JSON массива:
[
    {{
        "id": "unique_id",
        "type": "basic|cloze|reverse",
        "front": "вопрос или текст с пропуском [c1::пропуск]",
        "back": "ответ",
        "tags": ["тег1", "тег2"],
        "extra": "дополнительная информация (опционально)"
    }}
]

Для cloze карточек используй формат: [c1::правильный_ответ]
"""
        
        response = self._call_llm(prompt)
        
        try:
            cards = self._parse_json_response(response)
            if isinstance(cards, dict):
                cards = [cards]
            
            # Add UUIDs and ensure required fields
            for card in cards:
                if 'id' not in card:
                    card['id'] = str(uuid.uuid4())
                if 'tags' not in card:
                    card['tags'] = [deck_name.replace(' ', '_')]
                if 'extra' not in card:
                    card['extra'] = ''
            
            return cards
            
        except Exception as e:
            # Fallback: create basic cards
            return self._create_fallback_cards(content, count, deck_name)
    
    def _create_fallback_cards(self, content: str, count: int, deck_name: str) -> List[Dict]:
        """Create basic fallback cards"""
        lines = content.split('\n')
        cards = []
        
        for i, line in enumerate(lines[:count]):
            if len(line.strip()) > 20:  # Skip very short lines
                cards.append({
                    'id': str(uuid.uuid4()),
                    'type': 'basic',
                    'front': f'Что означает: {line[:100]}?',
                    'back': f'Объяснение для: {line[:100]}',
                    'tags': [deck_name.replace(' ', '_')],
                    'extra': ''
                })
        
        return cards
    
    def export_to_apkg(self, cards: List[Dict], deck_name: str, output_path: str) -> str:
        """
        Export cards to Anki .apkg format
        
        Note: This requires the genanki library
        """
        try:
            import genanki
        except ImportError:
            raise ImportError("Please install genanki: pip install genanki")
        
        # Create deck
        deck = genanki.Deck(
            deck_id=hash(deck_name) & 0xffffffff,
            name=deck_name
        )
        
        # Create model for basic cards
        model = genanki.Model(
            model_id=hash(f"{deck_name}_model") & 0xffffffff,
            name='AI Tutor Model',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
                {'name': 'Extra'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Front}}\n\n{{#Extra}}<div style="font-size: 0.9em; color: #666;">{{Extra}}</div>{{/Extra}}',
                    'afmt': '{{FrontSide}}\n\n<hr id="answer">\n\n{{Back}}',
                },
            ]
        )
        
        # Add cards to deck
        for card_data in cards:
            if card_data['type'] == 'cloze':
                # Use cloze model for cloze cards
                cloze_model = genanki.Model(
                    model_id=hash(f"{deck_name}_cloze") & 0xffffffff,
                    name='Cloze Model',
                    fields=[{'name': 'Text'}, {'name': 'Extra'}],
                    templates=[{
                        'name': 'Cloze',
                        'qfmt': '{{cloze:Text}}\n\n{{#Extra}}<div style="font-size: 0.9em; color: #666;">{{Extra}}</div>{{/Extra}}',
                        'afmt': '{{cloze:Text}}\n\n<hr id="answer">\n\n{{Extra}}',
                    }]
                )
                
                note = genanki.Note(
                    model=cloze_model,
                    fields=[card_data['front'], card_data.get('extra', '')],
                    tags=card_data.get('tags', [])
                )
            else:
                note = genanki.Note(
                    model=model,
                    fields=[
                        card_data['front'],
                        card_data['back'],
                        card_data.get('extra', '')
                    ],
                    tags=card_data.get('tags', [])
                )
            
            deck.add_note(note)
        
        # Write package
        genanki.Package(deck).write_to_file(output_path)
        
        return output_path
    
    def generate_cloze_from_text(self, text: str, max_cards: int = 10) -> List[Dict]:
        """
        Automatically generate cloze deletion cards from text
        Identifies key terms and creates fill-in-the-blank cards
        """
        
        prompt = f"""Создай cloze карточки из этого текста.
Найди ключевые термины, понятия и важные факты.
Создай максимум {max_cards} карточек.

Текст:
{text[:4000]}

Для каждой карточки замени ключевое слово/фразу на [c1::слово]

Ответь в формате JSON:
[
    {{
        "text_with_cloze": "предложение с [c1::пропуском]",
        "hint": "подсказка что это (опционально)",
        "tags": ["тег"]
    }}
]
"""
        
        response = self._call_llm(prompt)
        
        try:
            result = self._parse_json_response(response)
            cards = []
            
            for item in result:
                cards.append({
                    'id': str(uuid.uuid4()),
                    'type': 'cloze',
                    'front': item.get('text_with_cloze', ''),
                    'back': '',  # Cloze cards don't need separate back
                    'tags': item.get('tags', []),
                    'extra': item.get('hint', '')
                })
            
            return cards
            
        except:
            return []
