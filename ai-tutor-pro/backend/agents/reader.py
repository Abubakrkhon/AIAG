"""
Reader Agent - Analyzes and processes input content
Extracts key information, terms, definitions, and concepts
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base import BaseAgent, AgentResponse
from ..utils.llm_client import LLMClient
from ..utils.text_processor import TextProcessor


class ReaderAgent(BaseAgent):
    """
    Agent responsible for reading and analyzing content.
    
    Capabilities:
    - Extract main topics and concepts
    - Identify key terms and definitions
    - Summarize content
    - Detect content structure
    - Extract important facts
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("reader", config)
        self.llm = LLMClient()
        self.text_processor = TextProcessor()
        
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Reader Agent",
            "version": "1.0.0",
            "capabilities": [
                "content_analysis",
                "topic_extraction",
                "term_identification",
                "summarization",
                "structure_detection",
                "fact_extraction"
            ],
            "supported_formats": ["text", "markdown", "html"],
            "languages": ["en", "ru", "de", "fr", "es"]
        }
    
    async def process(self, input_data: str, **kwargs) -> AgentResponse:
        """
        Process content and extract structured information.
        
        Args:
            input_data: Text content to analyze
            **kwargs: Additional options
                - extract_terms: bool
                - generate_summary: bool
                - detect_structure: bool
                - language: str
                
        Returns:
            AgentResponse with extracted information
        """
        try:
            if not self.validate_input(input_data):
                return AgentResponse(
                    success=False,
                    data=None,
                    message="Invalid input data"
                )
            
            options = kwargs.get("options", {})
            language = kwargs.get("language", "ru")
            
            # Preprocess text
            cleaned_text = self.text_processor.clean_text(input_data)
            chunks = self.text_processor.chunk_text(
                cleaned_text,
                chunk_size=options.get("chunk_size", 1000),
                overlap=options.get("overlap", 200)
            )
            
            result = {
                "original_length": len(input_data),
                "cleaned_length": len(cleaned_text),
                "chunks_count": len(chunks),
                "language": language
            }
            
            # Extract main topics
            if options.get("extract_topics", True):
                topics = await self._extract_topics(cleaned_text, language)
                result["topics"] = topics
            
            # Extract terms and definitions
            if options.get("extract_terms", True):
                terms = await self._extract_terms(cleaned_text, language)
                result["terms"] = terms
            
            # Generate summary
            if options.get("generate_summary", True):
                summary = await self._generate_summary(cleaned_text, language)
                result["summary"] = summary
            
            # Detect structure
            if options.get("detect_structure", True):
                structure = await self._detect_structure(cleaned_text, language)
                result["structure"] = structure
            
            # Extract key facts
            if options.get("extract_facts", True):
                facts = await self._extract_facts(cleaned_text, language)
                result["facts"] = facts
            
            self.logger.info(f"Successfully processed content: {len(cleaned_text)} chars")
            
            return AgentResponse(
                success=True,
                data=result,
                message="Content analyzed successfully",
                metadata={
                    "processing_time": 0.0,
                    "model_used": self.llm.model_name
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing content: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                message=f"Processing error: {str(e)}"
            )
    
    async def _extract_topics(self, text: str, language: str) -> List[str]:
        """Extract main topics from text"""
        prompt = f"""
        Выдели основные темы и разделы из следующего текста.
        Верни список из 5-10 ключевых тем на языке: {language}.
        
        Текст:
        {text[:3000]}
        
        Формат ответа: JSON массив строк.
        """
        
        response = await self.llm.generate(prompt, max_tokens=500)
        topics = self.llm.parse_json(response, default=[])
        return topics if isinstance(topics, list) else []
    
    async def _extract_terms(self, text: str, language: str) -> List[Dict[str, str]]:
        """Extract key terms and their definitions"""
        prompt = f"""
        Найди все важные термины и их определения в тексте.
        Для каждого термина укажи:
        - term: сам термин
        - definition: краткое определение
        - context: контекст использования
        
        Текст:
        {text[:4000]}
        
        Формат ответа: JSON массив объектов.
        """
        
        response = await self.llm.generate(prompt, max_tokens=1500)
        terms = self.llm.parse_json(response, default=[])
        return terms if isinstance(terms, list) else []
    
    async def _generate_summary(self, text: str, language: str) -> Dict[str, str]:
        """Generate different types of summaries"""
        prompt = f"""
        Создай структурированный конспект текста на языке: {language}.
        
        Включи:
        1. Краткое содержание (2-3 предложения)
        2. Основные идеи (списком)
        3. Ключевые выводы
        
        Текст:
        {text[:4000]}
        
        Формат ответа: JSON объект с полями: brief, main_ideas, conclusions.
        """
        
        response = await self.llm.generate(prompt, max_tokens=800)
        summary = self.llm.parse_json(
            response,
            default={"brief": "", "main_ideas": [], "conclusions": []}
        )
        return summary
    
    async def _detect_structure(self, text: str, language: str) -> Dict[str, Any]:
        """Detect document structure"""
        prompt = f"""
        Определи структуру документа.
        Найди:
        - заголовки разных уровней
        - списки
        - таблицы
        - важные блоки
        
        Текст:
        {text[:3000]}
        
        Формат ответа: JSON объект с полями: headings, lists, tables, sections.
        """
        
        response = await self.llm.generate(prompt, max_tokens=600)
        structure = self.llm.parse_json(
            response,
            default={"headings": [], "lists": [], "tables": [], "sections": []}
        )
        return structure
    
    async def _extract_facts(self, text: str, language: str) -> List[str]:
        """Extract key facts from text"""
        prompt = f"""
        Выдели важные факты и утверждения из текста.
        Верни список из 10-20 ключевых фактов на языке: {language}.
        
        Текст:
        {text[:3000]}
        
        Формат ответа: JSON массив строк.
        """
        
        response = await self.llm.generate(prompt, max_tokens=800)
        facts = self.llm.parse_json(response, default=[])
        return facts if isinstance(facts, list) else []
