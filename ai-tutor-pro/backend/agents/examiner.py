"""
Examiner Agent - Generates tests, quizzes, and clinical cases
Supports multiple question types and difficulty levels
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base import BaseAgent, AgentResponse
from ..utils.llm_client import LLMClient


class ExaminerAgent(BaseAgent):
    """
    Agent responsible for generating assessments.
    
    Capabilities:
    - Multiple choice questions (MCQ)
    - True/False questions
    - Short answer questions
    - Essay questions
    - Clinical cases (medical)
    - Matching exercises
    - Fill-in-the-blank (Cloze)
    """
    
    QUESTION_TYPES = [
        "multiple_choice",
        "true_false",
        "short_answer",
        "essay",
        "clinical_case",
        "matching",
        "cloze"
    ]
    
    DIFFICULTY_LEVELS = ["easy", "medium", "hard", "expert"]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("examiner", config)
        self.llm = LLMClient()
        
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Examiner Agent",
            "version": "1.0.0",
            "capabilities": [
                "mcq_generation",
                "true_false_generation",
                "short_answer_generation",
                "essay_questions",
                "clinical_cases",
                "matching_exercises",
                "cloze_tests",
                "adaptive_difficulty"
            ],
            "question_types": self.QUESTION_TYPES,
            "difficulty_levels": self.DIFFICULTY_LEVELS,
            "languages": ["en", "ru", "de", "fr", "es"]
        }
    
    async def process(self, input_data: str, **kwargs) -> AgentResponse:
        """
        Generate test/quiz based on content.
        
        Args:
            input_data: Content to base questions on
            **kwargs: Additional options
                - question_types: List[str]
                - num_questions: int
                - difficulty: str
                - include_answers: bool
                - include_explanations: bool
                - language: str
                
        Returns:
            AgentResponse with generated test
        """
        try:
            if not self.validate_input(input_data):
                return AgentResponse(
                    success=False,
                    data=None,
                    message="Invalid input data"
                )
            
            options = kwargs.get("options", {})
            question_types = options.get("question_types", ["multiple_choice"])
            num_questions = options.get("num_questions", 10)
            difficulty = options.get("difficulty", "medium")
            language = kwargs.get("language", "ru")
            
            # Validate inputs
            for q_type in question_types:
                if q_type not in self.QUESTION_TYPES:
                    question_types.remove(q_type)
            
            if difficulty not in self.DIFFICULTY_LEVELS:
                difficulty = "medium"
            
            result = {
                "content_preview": input_data[:200],
                "difficulty": difficulty,
                "language": language,
                "questions": []
            }
            
            # Generate questions by type
            for q_type in question_types:
                questions_per_type = max(1, num_questions // len(question_types))
                
                if q_type == "multiple_choice":
                    questions = await self._generate_mcq(
                        input_data, questions_per_type, difficulty, language
                    )
                elif q_type == "true_false":
                    questions = await self._generate_true_false(
                        input_data, questions_per_type, difficulty, language
                    )
                elif q_type == "short_answer":
                    questions = await self._generate_short_answer(
                        input_data, questions_per_type, difficulty, language
                    )
                elif q_type == "clinical_case":
                    questions = await self._generate_clinical_case(
                        input_data, questions_per_type, difficulty, language
                    )
                elif q_type == "cloze":
                    questions = await self._generate_cloze(
                        input_data, questions_per_type, difficulty, language
                    )
                else:
                    questions = []
                
                result["questions"].extend(questions)
            
            # Shuffle questions
            import random
            random.shuffle(result["questions"])
            
            # Limit to requested number
            result["questions"] = result["questions"][:num_questions]
            
            self.logger.info(f"Generated {len(result['questions'])} questions ({difficulty})")
            
            return AgentResponse(
                success=True,
                data=result,
                message=f"Generated {len(result['questions'])} questions",
                metadata={
                    "question_count": len(result["questions"]),
                    "difficulty": difficulty,
                    "types_generated": list(set([q["type"] for q in result["questions"]]))
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error generating test: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                message=f"Generation error: {str(e)}"
            )
    
    async def _generate_mcq(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate multiple choice questions"""
        
        prompt = f"""
        Создай {num} вопросов с множественным выбором на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждого вопроса укажи:
        - id: уникальный номер
        - type: "multiple_choice"
        - question: текст вопроса
        - options: массив из 4 вариантов ответа
        - correct_answer: индекс правильного ответа (0-3)
        - explanation: объяснение правильного ответа
        
        Важно:
        - Только один правильный ответ
        - Варианты должны быть правдоподобными
        - Избегай очевидных неправильных ответов
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2500)
        questions = self.llm.parse_json(response, default=[])
        
        # Add type field if missing
        for q in questions:
            if isinstance(q, dict):
                q["type"] = "multiple_choice"
        
        return questions if isinstance(questions, list) else []
    
    async def _generate_true_false(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate true/false questions"""
        
        prompt = f"""
        Создай {num} вопросов Верно/Неверно на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждого вопроса укажи:
        - id: уникальный номер
        - type: "true_false"
        - question: утверждение
        - correct_answer: true или false
        - explanation: объяснение
        
        Сделай примерно 50% верных и 50% неверных утверждений.
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2000)
        questions = self.llm.parse_json(response, default=[])
        
        for q in questions:
            if isinstance(q, dict):
                q["type"] = "true_false"
        
        return questions if isinstance(questions, list) else []
    
    async def _generate_short_answer(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate short answer questions"""
        
        prompt = f"""
        Создай {num} вопросов с кратким ответом на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждого вопроса укажи:
        - id: уникальный номер
        - type: "short_answer"
        - question: текст вопроса
        - expected_answer: ожидаемый ответ (ключевые слова)
        - explanation: развернутое объяснение
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2000)
        questions = self.llm.parse_json(response, default=[])
        
        for q in questions:
            if isinstance(q, dict):
                q["type"] = "short_answer"
        
        return questions if isinstance(questions, list) else []
    
    async def _generate_clinical_case(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate clinical case scenarios (especially for medical topics)"""
        
        prompt = f"""
        Создай {num} клинических кейсов на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:5000]}
        
        Для каждого кейса укажи:
        - id: уникальный номер
        - type: "clinical_case"
        - title: заголовок кейса
        - scenario: описание клинической ситуации
        - patient_info: информация о пациенте (возраст, пол, жалобы)
        - questions: список вопросов к кейсу
        - answers: правильные ответы с объяснениями
        - differential_diagnosis: дифференциальный диагноз
        - key_learning_points: ключевые моменты для обучения
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=3000)
        cases = self.llm.parse_json(response, default=[])
        
        for case in cases:
            if isinstance(case, dict):
                case["type"] = "clinical_case"
        
        return cases if isinstance(cases, list) else []
    
    async def _generate_cloze(
        self,
        content: str,
        num: int,
        difficulty: str,
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate cloze (fill-in-the-blank) questions"""
        
        prompt = f"""
        Создай {num} заданий на заполнение пропусков (Cloze) на основе текста.
        Сложность: {difficulty}. Язык: {language}.
        
        Текст:
        {content[:4000]}
        
        Для каждого задания укажи:
        - id: уникальный номер
        - type: "cloze"
        - text: текст с пропусками (обозначай пропуск как ___)
        - answers: список правильных ответов для каждого пропуска
        - explanation: объяснение
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=2000)
        questions = self.llm.parse_json(response, default=[])
        
        for q in questions:
            if isinstance(q, dict):
                q["type"] = "cloze"
        
        return questions if isinstance(questions, list) else []
    
    async def grade_answer(
        self,
        question: Dict[str, Any],
        user_answer: str,
        language: str = "ru"
    ) -> Dict[str, Any]:
        """Grade a user's answer"""
        
        prompt = f"""
        Оцени ответ пользователя.
        Язык: {language}.
        
        Вопрос: {question.get('question', '')}
        Тип: {question.get('type', '')}
        Правильный ответ: {question.get('correct_answer', question.get('expected_answer', ''))}
        Объяснение: {question.get('explanation', '')}
        
        Ответ пользователя: {user_answer}
        
        Оцени ответ по шкале от 0 до 1 и дай обратную связь.
        
        Формат ответа: JSON объект с полями:
        - score: оценка от 0 до 1
        - is_correct: boolean (true если score >= 0.8)
        - feedback: развернутая обратная связь
        - suggestions: рекомендации что улучшить
        """
        
        response = await self.llm.generate(prompt, max_tokens=800)
        grading = self.llm.parse_json(
            response,
            default={"score": 0, "is_correct": False, "feedback": "", "suggestions": []}
        )
        
        return grading
