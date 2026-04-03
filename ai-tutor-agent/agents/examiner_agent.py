"""
Examiner Agent - Creates tests and quizzes
"""
from typing import Dict, List, Any
import uuid
from .base_agent import BaseAgent


class ExaminerAgent(BaseAgent):
    """
    Agent responsible for creating tests, quizzes, and assessments.
    Supports multiple question types including clinical cases.
    """
    
    def __init__(self, llm_client):
        super().__init__(llm_client, name="ExaminerAgent")
        self.system_prompt = """Ты - опытный экзаменатор и создатель тестов. Твоя задача:
1. Создавать качественные вопросы для проверки знаний
2. Использовать разные форматы вопросов
3. Включать клинические/практические кейсы
4. Делать вопросы разной сложности
5. Предоставлять подробные объяснения ответов

Будь строгим но справедливым."""
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate test/quiz based on content
        
        Args:
            input_data: dict with:
                - content: source material
                - question_types: list of desired types
                - difficulty: easy/medium/hard
                - count: number of questions
                
        Returns:
            Dict with generated questions
        """
        content = input_data.get('content', '')
        question_types = input_data.get('question_types', ['multiple_choice'])
        difficulty = input_data.get('difficulty', 'medium')
        count = input_data.get('count', 10)
        
        if not content:
            raise ValueError("No content provided")
        
        questions = self._generate_questions(
            content, 
            question_types, 
            difficulty, 
            count
        )
        
        return {
            'questions': questions,
            'metadata': {
                'difficulty': difficulty,
                'count': len(questions),
                'types': question_types
            },
            'type': 'test'
        }
    
    def _generate_questions(self, content: str, types: List[str], 
                           difficulty: str, count: int) -> List[Dict]:
        """Generate questions using LLM"""
        
        type_mapping = {
            'multiple_choice': 'Вопросы с выбором ответа (A/B/C/D)',
            'true_false': 'Верно/Неверно',
            'short_answer': 'Краткий ответ',
            'clinical_case': 'Клинический случай/кейс',
            'matching': 'Соответствие терминов и определений',
            'fill_blank': 'Заполнить пропуск'
        }
        
        requested_types = [type_mapping.get(t, t) for t in types]
        
        prompt = f"""Создай тест по следующему материалу.

Требования:
- Количество вопросов: {count}
- Типы вопросов: {', '.join(requested_types)}
- Сложность: {difficulty}

Материал:
{content[:8000]}

Для каждого вопроса укажи:
1. Тип вопроса
2. Текст вопроса
3. Варианты ответов (если применимо)
4. Правильный ответ
5. Подробное объяснение почему этот ответ правильный
6. Сложность (easy/medium/hard)
7. Темы которые проверяет вопрос

Ответь ТОЛЬКО в формате JSON массива:
[
    {{
        "id": "unique_id",
        "type": "multiple_choice|true_false|short_answer|clinical_case|matching|fill_blank",
        "question": "текст вопроса",
        "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}} или null,
        "correct_answer": "A|B|C|D или текст ответа",
        "explanation": "объяснение",
        "difficulty": "easy|medium|hard",
        "topics": ["тема 1", "тема 2"]
    }}
]
"""
        
        response = self._call_llm(prompt)
        
        try:
            questions = self._parse_json_response(response)
            if isinstance(questions, dict):
                questions = [questions]
            
            # Add UUIDs if missing
            for q in questions:
                if 'id' not in q:
                    q['id'] = str(uuid.uuid4())
            
            return questions
            
        except Exception as e:
            # Fallback: create basic questions
            return self._create_fallback_questions(content, count)
    
    def _create_fallback_questions(self, content: str, count: int) -> List[Dict]:
        """Create basic questions if JSON parsing fails"""
        return [{
            'id': str(uuid.uuid4()),
            'type': 'multiple_choice',
            'question': f'Вопрос {i+1} по материалу',
            'options': {'A': 'Вариант 1', 'B': 'Вариант 2', 'C': 'Вариант 3', 'D': 'Вариант 4'},
            'correct_answer': 'A',
            'explanation': 'Объяснение будет добавлено позже',
            'difficulty': 'medium',
            'topics': []
        } for i in range(count)]
    
    def create_clinical_case(self, content: str, topic: str = None) -> Dict:
        """
        Create a detailed clinical/practical case study
        
        Special format for medical/professional education
        """
        
        prompt = f"""Создай детальный клинический/практический кейс.

{"Тема: " + topic if topic else ""}

На основе материала:
{content[:6000]}

Кейс должен включать:
1. Описание ситуации/пациента
2. Симптомы/проблемы
3. Вопросы для анализа
4. Правильный подход к решению
5. Объяснение логики решения
6. Альтернативные варианты и почему они хуже
7. Ключевые обучающие моменты

Формат JSON:
{{
    "title": "название кейса",
    "scenario": "описание ситуации",
    "symptoms": ["симптом 1", "симптом 2"],
    "questions": ["вопрос 1", "вопрос 2"],
    "solution": {{"approach": "...", "steps": ["шаг 1", "шаг 2"]}},
    "explanation": "почему это правильное решение",
    "alternatives": [{{"option": "...", "why_wrong": "..."}}],
    "learning_points": ["момент 1", "момент 2"]
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            return self._parse_json_response(response)
        except:
            return {
                'title': 'Клинический кейс',
                'scenario': response[:1000],
                'symptoms': [],
                'questions': [],
                'solution': {},
                'explanation': '',
                'alternatives': [],
                'learning_points': []
            }
    
    def evaluate_answer(self, question: Dict, user_answer: str) -> Dict:
        """Evaluate a user's answer"""
        
        prompt = f"""Оцени ответ студента.

Вопрос: {question.get('question', '')}
Правильный ответ: {question.get('correct_answer', '')}
Объяснение правильного ответа: {question.get('explanation', '')}

Ответ студента: {user_answer}

Оцени:
1. Правильность (0-100%)
2. Что правильно в ответе
3. Что неправильно или отсутствует
4. Рекомендации по улучшению

JSON формат:
{{
    "score": 0-100,
    "is_correct": true/false,
    "correct_parts": "...",
    "incorrect_parts": "...",
    "feedback": "...",
    "recommendations": ["совет 1", "совет 2"]
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            return self._parse_json_response(response)
        except:
            return {
                'score': 50,
                'is_correct': False,
                'correct_parts': '',
                'incorrect_parts': '',
                'feedback': response[:500],
                'recommendations': []
            }
