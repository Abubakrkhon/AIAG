"""
Teacher Agent - Generates explanations at different complexity levels
Supports ELI5, Beginner, Intermediate, and Expert modes
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base import BaseAgent, AgentResponse
from ..utils.llm_client import LLMClient


class TeacherAgent(BaseAgent):
    """
    Agent responsible for generating educational explanations.
    
    Capabilities:
    - Explain concepts at 4 complexity levels
    - Use analogies and examples
    - Answer follow-up questions
    - Adapt to user knowledge level
    - Provide clinical cases (for medical topics)
    """
    
    COMPLEXITY_LEVELS = {
        "eli5": "Объясни как пятилетнему ребенку, очень просто с аналогиями",
        "beginner": "Объясни для начинающего студента, просто но с терминами",
        "intermediate": "Объясни для продолжающего, с деталями и нюансами",
        "expert": "Объясни для эксперта, глубоко с техническими деталями"
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("teacher", config)
        self.llm = LLMClient()
        
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Teacher Agent",
            "version": "1.0.0",
            "capabilities": [
                "multi_level_explanation",
                "analogy_generation",
                "example_generation",
                "question_answering",
                "clinical_cases",
                "adaptive_teaching"
            ],
            "complexity_levels": list(self.COMPLEXITY_LEVELS.keys()),
            "languages": ["en", "ru", "de", "fr", "es"]
        }
    
    async def process(self, input_data: str, **kwargs) -> AgentResponse:
        """
        Generate explanation for the given topic/content.
        
        Args:
            input_data: Topic or content to explain
            **kwargs: Additional options
                - level: str (eli5, beginner, intermediate, expert)
                - context: str (additional context)
                - include_examples: bool
                - include_analogies: bool
                - language: str
                
        Returns:
            AgentResponse with explanation
        """
        try:
            if not self.validate_input(input_data):
                return AgentResponse(
                    success=False,
                    data=None,
                    message="Invalid input data"
                )
            
            options = kwargs.get("options", {})
            level = options.get("level", "beginner")
            language = kwargs.get("language", "ru")
            context = options.get("context", "")
            
            # Validate complexity level
            if level not in self.COMPLEXITY_LEVELS:
                level = "beginner"
            
            explanation = await self._generate_explanation(
                topic=input_data,
                level=level,
                context=context,
                language=language,
                include_examples=options.get("include_examples", True),
                include_analogies=options.get("include_analogies", True)
            )
            
            result = {
                "topic": input_data[:200],
                "level": level,
                "level_description": self.COMPLEXITY_LEVELS[level],
                "explanation": explanation,
                "language": language
            }
            
            # Generate additional materials if requested
            if options.get("include_quiz", False):
                quiz = await self._generate_quiz(input_data, level, language)
                result["quiz"] = quiz
            
            if options.get("include_key_points", False):
                key_points = await self._extract_key_points(input_data, level, language)
                result["key_points"] = key_points
            
            self.logger.info(f"Generated {level} explanation for topic: {input_data[:50]}...")
            
            return AgentResponse(
                success=True,
                data=result,
                message=f"Explanation generated at {level} level",
                metadata={
                    "complexity_level": level,
                    "model_used": self.llm.model_name
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error generating explanation: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                message=f"Generation error: {str(e)}"
            )
    
    async def _generate_explanation(
        self,
        topic: str,
        level: str,
        context: str,
        language: str,
        include_examples: bool = True,
        include_analogies: bool = True
    ) -> Dict[str, Any]:
        """Generate explanation at specified complexity level"""
        
        instruction = self.COMPLEXITY_LEVELS[level]
        
        prompt = f"""
        {instruction}. Язык ответа: {language}.
        
        Тема для объяснения: {topic}
        
        {f"Дополнительный контекст: {context}" if context else ""}
        
        Структурируй ответ:
        1. Основное понятие (простое определение)
        2. Детальное объяснение
        {f"3. Аналогии из реальной жизни" if include_analogies else ""}
        {f"4. Практические примеры" if include_examples else ""}
        5. Важные нюансы
        6. Распространенные ошибки понимания
        
        Сделай объяснение максимально понятным и engaging.
        Используй форматирование Markdown.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2000)
        
        # Parse structured response
        explanation = {
            "full_text": response,
            "definition": "",
            "details": "",
            "analogies": [] if include_analogies else None,
            "examples": [] if include_examples else None,
            "nuances": [],
            "common_misconceptions": []
        }
        
        # Try to extract sections
        extraction_prompt = f"""
        Извлеки структурированные данные из текста:
        
        {response}
        
        Верни JSON с полями:
        - definition: основное определение (1-2 предложения)
        - details: детальное объяснение (текст)
        - analogies: список аналогий (массив строк)
        - examples: список примеров (массив строк)
        - nuances: список важных нюансов (массив строк)
        - common_misconceptions: распространенные ошибки (массив строк)
        """
        
        extraction_response = await self.llm.generate(extraction_prompt, max_tokens=1000)
        extracted = self.llm.parse_json(extraction_response, default={})
        
        for key in explanation.keys():
            if key in extracted and key != "full_text":
                explanation[key] = extracted[key]
        
        return explanation
    
    async def _generate_quiz(
        self,
        topic: str,
        level: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate quiz questions to test understanding"""
        
        prompt = f"""
        Создай 5 вопросов для проверки понимания темы на уровне "{level}".
        Язык: {language}.
        
        Тема: {topic}
        
        Для каждого вопроса укажи:
        - question: текст вопроса
        - type: тип (multiple_choice, true_false, short_answer)
        - options: варианты ответов (для multiple_choice)
        - correct_answer: правильный ответ
        - explanation: объяснение почему это правильный ответ
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=1500)
        quiz = self.llm.parse_json(response, default=[])
        return quiz if isinstance(quiz, list) else []
    
    async def _extract_key_points(
        self,
        topic: str,
        level: str,
        language: str
    ) -> List[str]:
        """Extract key points from the topic"""
        
        prompt = f"""
        Выдели 5-10 ключевых пунктов для понимания темы на уровне "{level}".
        Язык: {language}.
        
        Тема: {topic}
        
        Формат ответа: JSON массив строк.
        """
        
        response = await self.llm.generate(prompt, max_tokens=800)
        points = self.llm.parse_json(response, default=[])
        return points if isinstance(points, list) else []
    
    async def answer_question(
        self,
        question: str,
        context: str,
        level: str = "beginner",
        language: str = "ru"
    ) -> str:
        """Answer a specific question about the topic"""
        
        instruction = self.COMPLEXITY_LEVELS.get(level, self.COMPLEXITY_LEVELS["beginner"])
        
        prompt = f"""
        {instruction}. Язык: {language}.
        
        Контекст: {context}
        
        Вопрос: {question}
        
        Дай точный и понятный ответ на вопрос.
        Если информации недостаточно, скажи об этом.
        """
        
        response = await self.llm.generate(prompt, max_tokens=1000)
        return response
