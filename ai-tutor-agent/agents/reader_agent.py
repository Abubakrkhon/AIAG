"""
Reader Agent - Reads and analyzes input content
"""
from typing import Dict, List, Any
from .base_agent import BaseAgent


class ReaderAgent(BaseAgent):
    """
    Agent responsible for reading and understanding input content.
    Extracts key information, identifies structure, and prepares data for other agents.
    """
    
    def __init__(self, llm_client):
        super().__init__(llm_client, name="ReaderAgent")
        self.system_prompt = """Ты - умный читатель-аналитик. Твоя задача:
1. Внимательно прочитать предоставленный учебный материал
2. Выделять ключевые концепции, термины и определения
3. Понимать логическую структуру материала
4. Идентифицировать связи между концепциями
5. Определять уровень сложности материала

Отвечай структурированно и точно."""
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input content and extract structured information
        
        Args:
            input_data: dict with 'text' and optional 'metadata'
            
        Returns:
            Dict with analyzed content structure
        """
        text = input_data.get('text', '')
        metadata = input_data.get('metadata', {})
        
        if not text or len(text.strip()) == 0:
            raise ValueError("Empty text provided")
        
        # Analyze the text
        analysis = self._analyze_content(text)
        
        return {
            'original_text': text,
            'metadata': metadata,
            'analysis': analysis,
            'source_type': metadata.get('type', 'unknown')
        }
    
    def _analyze_content(self, text: str) -> Dict[str, Any]:
        """Use LLM to analyze content structure"""
        
        prompt = f"""Проанализируй следующий учебный материал и выдели:

1. ОСНОВНУЮ ТЕМУ - о чём этот материал?
2. КЛЮЧЕВЫЕ КОНЦЕПЦИИ - главные идеи (список)
3. ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ - все важные термины с определениями
4. СТРУКТУРУ - как организован материал (разделы, подразделы)
5. УРОВЕНЬ СЛОЖНОСТИ - beginner/intermediate/advanced
6. ПРЕДПОЛАГАЕМУЮ АУДИТОРИЮ - для кого этот материал

Текст для анализа:
{text[:8000]}  # Limit to avoid token limits

Ответь в формате JSON:
{{
    "main_topic": "...",
    "key_concepts": ["...", "..."],
    "terms": [{{"term": "...", "definition": "..."}}],
    "structure": ["...", "..."],
    "difficulty": "beginner/intermediate/advanced",
    "audience": "..."
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            analysis = self._parse_json_response(response)
        except Exception as e:
            # Fallback to basic analysis
            analysis = {
                'main_topic': 'Не определено',
                'key_concepts': [],
                'terms': [],
                'structure': ['Основной текст'],
                'difficulty': 'intermediate',
                'audience': 'Студенты',
                'parse_error': str(e)
            }
        
        return analysis
    
    def extract_key_points(self, text: str, max_points: int = 10) -> List[str]:
        """Extract key points from text"""
        
        prompt = f"""Выдели {max_points} главных идей из этого текста:

{text[:6000]}

Ответь списком в формате JSON:
["идея 1", "идея 2", ...]
"""
        
        response = self._call_llm(prompt)
        
        try:
            return self._parse_json_response(response)
        except:
            return []
