"""
Anki Agent - Generates flashcards for spaced repetition learning
Supports multiple card types and exports to Anki format
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base import BaseAgent, AgentResponse
from ..utils.llm_client import LLMClient


class AnkiAgent(BaseAgent):
    """
    Agent responsible for generating flashcards.
    
    Capabilities:
    - Q&A cards (front/back)
    - Cloze deletion cards
    - Image occlusion (future)
    - Basic cards with tags
    - Export to Anki (.apkg)
    - Spaced repetition scheduling
    """
    
    CARD_TYPES = ["basic", "cloze", "reverse"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("anki", config)
        self.llm = LLMClient()
        
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Anki Agent",
            "version": "1.0.0",
            "capabilities": [
                "basic_cards",
                "cloze_deletion",
                "reverse_cards",
                "tagging",
                "deck_organization",
                "export_apkg",
                "spaced_repetition"
            ],
            "card_types": self.CARD_TYPES,
            "export_formats": ["json", "csv", "apkg"],
            "languages": ["en", "ru", "de", "fr", "es"]
        }
    
    async def process(self, input_data: str, **kwargs) -> AgentResponse:
        """
        Generate flashcards from content.
        
        Args:
            input_data: Content to create cards from
            **kwargs: Additional options
                - card_types: List[str]
                - num_cards: int
                - difficulty: str (easy, medium, hard)
                - include_tags: bool
                - deck_name: str
                - language: str
                
        Returns:
            AgentResponse with generated flashcards
        """
        try:
            if not self.validate_input(input_data):
                return AgentResponse(
                    success=False,
                    data=None,
                    message="Invalid input data"
                )
            
            options = kwargs.get("options", {})
            card_types = options.get("card_types", ["basic"])
            num_cards = options.get("num_cards", 20)
            difficulty = options.get("difficulty", "medium")
            language = kwargs.get("language", "ru")
            deck_name = options.get("deck_name", "AI Tutor Deck")
            
            # Validate card types
            valid_types = []
            for ct in card_types:
                if ct in self.CARD_TYPES:
                    valid_types.append(ct)
            
            if not valid_types:
                valid_types = ["basic"]
            
            result = {
                "deck_name": deck_name,
                "language": language,
                "difficulty": difficulty,
                "cards": []
            }
            
            # Generate cards by type
            for card_type in valid_types:
                cards_per_type = max(1, num_cards // len(valid_types))
                
                if card_type == "basic":
                    cards = await self._generate_basic_cards(
                        input_data, cards_per_type, difficulty, language
                    )
                elif card_type == "cloze":
                    cards = await self._generate_cloze_cards(
                        input_data, cards_per_type, difficulty, language
                    )
                elif card_type == "reverse":
                    cards = await self._generate_reverse_cards(
                        input_data, cards_per_type, difficulty, language
                    )
                else:
                    cards = []
                
                result["cards"].extend(cards)
            
            # Add tags if requested
            if options.get("include_tags", True):
                tags = await self._generate_tags(input_data, language)
                for card in result["cards"]:
                    card["tags"] = tags[:5]  # Add up to 5 tags per card
            
            # Limit to requested number
            result["cards"] = result["cards"][:num_cards]
            
            self.logger.info(f"Generated {len(result['cards'])} flashcards")
            
            return AgentResponse(
                success=True,
                data=result,
                message=f"Generated {len(result['cards'])} flashcards",
                metadata={
                    "card_count": len(result["cards"]),
                    "card_types": list(set([c["type"] for c in result["cards"]])),
                    "deck_name": deck_name
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error generating flashcards: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                message=f"Generation error: {str(e)}"
            )
    
    async def _generate_basic_cards(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate basic Q&A flashcards"""
        
        prompt = f"""
        Создай {num} карточек с вопросами и ответами на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждой карточки укажи:
        - id: уникальный номер
        - type: "basic"
        - front: вопрос (на лицевой стороне)
        - back: ответ (на оборотной стороне)
        - extra: дополнительная информация/объяснение (опционально)
        
        Требования:
        - Вопросы должны быть четкими и конкретными
        - Ответы не должны быть слишком длинными
        - Избегай вопросов с несколькими правильными ответами
        - Фокусируйся на ключевых концепциях
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2500)
        cards = self.llm.parse_json(response, default=[])
        
        for card in cards:
            if isinstance(card, dict):
                card["type"] = "basic"
        
        return cards if isinstance(cards, list) else []
    
    async def _generate_cloze_cards(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate cloze deletion flashcards"""
        
        prompt = f"""
        Создай {num} карточек с пропусками (Cloze) на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждой карточки укажи:
        - id: уникальный номер
        - type: "cloze"
        - text: текст с пропусками в формате {{{{c1::ответ}}}}
        - hint: подсказка (опционально)
        - extra: объяснение (опционально)
        
        Пример формата пропуска:
        "Столица Франции - {{c1::Париж}}"
        "Вода состоит из {{c1::двух}} атомов водорода и {{c2::одного}} атома кислорода"
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2500)
        cards = self.llm.parse_json(response, default=[])
        
        for card in cards:
            if isinstance(card, dict):
                card["type"] = "cloze"
        
        return cards if isinstance(cards, list) else []
    
    async def _generate_reverse_cards(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate reverse flashcards (both directions)"""
        
        prompt = f"""
        Создай {num} двусторонних карточек на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждой карточки укажи:
        - id: уникальный номер
        - type: "reverse"
        - front: первая сторона
        - back: вторая сторона
        - extra: дополнительная информация
        
        Эти карточки будут использоваться в обоих направлениях:
        front→back и back→front.
        
        Выбирай термины и понятия, которые полезно знать в обоих направлениях.
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2500)
        cards = self.llm.parse_json(response, default=[])
        
        for card in cards:
            if isinstance(card, dict):
                card["type"] = "reverse"
        
        return cards if isinstance(cards, list) else []
    
    async def _generate_tags(self, content: str, language: str) -> List[str]:
        """Generate relevant tags for flashcards"""
        
        prompt = f"""
        Придумай релевантные теги для карточек на основе текста.
        Язык: {language}.
        
        Текст:
        {content[:3000]}
        
        Верни 10-15 тегов, которые помогут организовать карточки по темам.
        Теги должны быть короткими и информативными.
        
        Формат ответа: JSON массив строк.
        """
        
        response = await self.llm.generate(prompt, max_tokens=500)
        tags = self.llm.parse_json(response, default=[])
        return tags if isinstance(tags, list) else []
    
    def export_to_csv(self, cards: List[Dict[str, Any]], separator: str = ";") -> str:
        """Export cards to CSV format"""
        lines = ["type;front;back;extra;tags"]
        
        for card in cards:
            card_type = card.get("type", "basic")
            front = card.get("front", card.get("text", ""))
            back = card.get("back", "")
            extra = card.get("extra", "")
            tags = ",".join(card.get("tags", []))
            
            # Escape separators
            front = front.replace(separator, "\\;").replace("\n", " ")
            back = back.replace(separator, "\\;").replace("\n", " ")
            extra = extra.replace(separator, "\\;").replace("\n", " ")
            
            lines.append(f"{card_type}{separator}{front}{separator}{back}{separator}{extra}{separator}{tags}")
        
        return "\n".join(lines)
    
    def export_to_anki_format(self, cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert cards to Anki import format"""
        anki_cards = []
        
        for card in cards:
            card_type = card.get("type", "basic")
            
            if card_type == "cloze":
                anki_card = {
                    "note_type": "Cloze",
                    "fields": {
                        "Text": card.get("text", ""),
                        "Extra": card.get("extra", "")
                    },
                    "tags": card.get("tags", [])
                }
            else:
                anki_card = {
                    "note_type": "Basic",
                    "fields": {
                        "Front": card.get("front", ""),
                        "Back": card.get("back", ""),
                        "Extra": card.get("extra", "")
                    },
                    "tags": card.get("tags", [])
                }
            
            anki_cards.append(anki_card)
        
        return anki_cards
    
    async def calculate_spaced_repetition(
        self,
        card_id: str,
        current_interval: int,
        ease_factor: float,
        performance: int  # 0-5 scale
    ) -> Dict[str, Any]:
        """Calculate next review interval using SM-2 algorithm"""
        
        # Simplified SM-2 algorithm
        if performance >= 3:
            if current_interval == 0:
                new_interval = 1
            elif current_interval == 1:
                new_interval = 6
            else:
                new_interval = round(current_interval * ease_factor)
            
            # Adjust ease factor
            new_ease = ease_factor + (0.1 - (5 - performance) * (0.08 + (5 - performance) * 0.02))
            new_ease = max(1.3, new_ease)
        else:
            new_interval = 1
            new_ease = ease_factor
        
        return {
            "card_id": card_id,
            "next_interval": new_interval,
            "ease_factor": round(new_ease, 2),
            "next_review_date": "calculated_based_on_current_date"
        }
