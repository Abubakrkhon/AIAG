"""
Teacher Agent - Explains concepts in simple terms
"""
from typing import Dict, List, Any
from .base_agent import BaseAgent


class TeacherAgent(BaseAgent):
    """
    Agent responsible for explaining concepts at different levels.
    Can explain like you're 5, like a student, or like an expert.
    """
    
    def __init__(self, llm_client):
        super().__init__(llm_client, name="TeacherAgent")
        self.system_prompt = """Ты - опытный преподаватель и наставник. Твоя задача:
1. Объяснять сложные концепции простым языком
2. Адаптировать объяснение под уровень ученика
3. Использовать аналогии и примеры из жизни
4. Проверять понимание через вопросы
5. Поддерживать и мотивировать

Говори дружелюбно, понятно и с энтузиазмом."""
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate explanation based on content and desired level
        
        Args:
            input_data: dict with:
                - concept: what to explain
                - context: additional context/material
                - level: 'child', 'beginner', 'intermediate', 'expert'
                
        Returns:
            Dict with explanation and examples
        """
        concept = input_data.get('concept', '')
        context = input_data.get('context', '')
        level = input_data.get('level', 'beginner')
        
        if not concept:
            raise ValueError("No concept provided")
        
        explanation = self._generate_explanation(concept, context, level)
        
        return {
            'concept': concept,
            'level': level,
            'explanation': explanation,
            'type': 'explanation'
        }
    
    def _generate_explanation(self, concept: str, context: str, level: str) -> Dict[str, Any]:
        """Generate explanation at specified level"""
        
        level_prompts = {
            'child': """Объясни это так, как будто говоришь с ребёнком 5 лет:
- Используй простые слова
- Приводи примеры из повседневной жизни (игры, игрушки, животные)
- Будь кратким и весёлым
- Используй аналогии""",
            
            'beginner': """Объясни это для начинающего студента:
- Избегай сложного жаргона или объясняй его
- Используй понятные аналогии
- Приводи практические примеры
- Разбей на логические шаги""",
            
            'intermediate': """Объясни это для студента с базовыми знаниями:
- Можно использовать терминологию
- Показывай связи с другими концепциями
- Приводи технические детали
- Объясняй 'почему' а не только 'что'""",
            
            'expert': """Объясни это для продвинутого специалиста:
- Используй полную техническую терминологию
- Покажи нюансы и исключения
- Обсуди современные исследования/подходы
- Сравни разные точки зрения"""
        }
        
        prompt = f"""{level_prompts.get(level, level_prompts['beginner'])}

Концепция для объяснения: {concept}
{"Дополнительный контекст: " + context[:3000] if context else ""}

Дай развёрнутое объяснение в формате JSON:
{{
    "simple_explanation": "объяснение в 2-3 предложениях",
    "detailed_explanation": "полное объяснение",
    "analogy": "понятная аналогия",
    "examples": ["пример 1", "пример 2"],
    "key_points": ["главный пункт 1", "главный пункт 2"],
    "common_misconceptions": ["распространённое заблуждение 1"]
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            return self._parse_json_response(response)
        except Exception as e:
            return {
                'simple_explanation': response[:500],
                'detailed_explanation': response,
                'analogy': '',
                'examples': [],
                'key_points': [],
                'common_misconceptions': [],
                'error': str(e)
            }
    
    def explain_like_im_five(self, concept: str, context: str = '') -> str:
        """Convenience method for ELI5 explanations"""
        result = self.execute({
            'concept': concept,
            'context': context,
            'level': 'child'
        })
        return result['explanation'].get('simple_explanation', '')
    
    def create_analogy(self, concept: str, familiar_domain: str = 'everyday life') -> str:
        """Create an analogy for a concept"""
        
        prompt = f"""Создай понятную аналогию для концепции "{concept}".
Используй примеры из области: {familiar_domain}.

Объясни:
1. Саму аналогию
2. Как она соотносится с оригинальной концепцией
3. Где аналогия перестаёт работать (ограничения)

Ответь в формате JSON:
{{
    "analogy": "...",
    "mapping": "...",
    "limitations": "..."
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            result = self._parse_json_response(response)
            return result.get('analogy', response)
        except:
            return response
