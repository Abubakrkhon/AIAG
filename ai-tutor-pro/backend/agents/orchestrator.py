"""
Orchestrator Agent - Coordinates all other agents
Manages the complete content processing pipeline
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base import BaseAgent, AgentResponse


class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator agent that coordinates all specialized agents.
    
    Pipeline:
    1. Reader Agent - Analyze content
    2. Teacher Agent - Generate explanations
    3. Examiner Agent - Create tests
    4. Anki Agent - Generate flashcards
    5. Schema Agent - Create visual schemas
    
    Returns unified response with all generated materials.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("orchestrator", config)
        self.logger = logger.bind(agent="orchestrator")
        
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Orchestrator Agent",
            "version": "1.0.0",
            "capabilities": [
                "pipeline_orchestration",
                "multi_agent_coordination",
                "unified_output",
                "parallel_processing"
            ],
            "pipeline_stages": [
                "content_analysis",
                "explanation_generation",
                "test_creation",
                "flashcard_generation",
                "schema_creation"
            ]
        }
    
    async def process(self, input_data: str, **kwargs) -> AgentResponse:
        """
        Process content through the full pipeline.
        
        Args:
            input_data: Content to process
            **kwargs: Processing options
            
        Returns:
            Unified response with all generated materials
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
            
            result = {
                "content_preview": input_data[:500],
                "language": language,
                "stages_completed": [],
                "summary": None,
                "explanations": {},
                "tests": [],
                "flashcards": [],
                "schemas": []
            }
            
            # Stage 1: Content Analysis (Reader Agent)
            if options.get("analyze", True):
                self.logger.info("Stage 1: Content analysis")
                reader_result = await self._run_reader(input_data, options, language)
                if reader_result.success:
                    result["summary"] = reader_result.data
                    result["stages_completed"].append("analysis")
            
            # Stage 2: Explanations (Teacher Agent)
            if options.get("explain", True):
                self.logger.info("Stage 2: Generating explanations")
                teacher_result = await self._run_teacher(input_data, options, language)
                if teacher_result.success:
                    result["explanations"] = teacher_result.data
                    result["stages_completed"].append("explanations")
            
            # Stage 3: Tests (Examiner Agent)
            if options.get("test", True):
                self.logger.info("Stage 3: Creating tests")
                examiner_result = await self._run_examiner(input_data, options, language)
                if examiner_result.success:
                    result["tests"] = examiner_result.data.get("questions", [])
                    result["stages_completed"].append("tests")
            
            # Stage 4: Flashcards (Anki Agent)
            if options.get("flashcards", True):
                self.logger.info("Stage 4: Generating flashcards")
                anki_result = await self._run_anki(input_data, options, language)
                if anki_result.success:
                    result["flashcards"] = anki_result.data.get("cards", [])
                    result["stages_completed"].append("flashcards")
            
            # Stage 5: Schemas (Schema Agent - placeholder)
            if options.get("schema", True):
                self.logger.info("Stage 5: Creating schemas")
                schema_result = await self._run_schema(input_data, options, language)
                if schema_result.success:
                    result["schemas"] = schema_result.data.get("schemas", [])
                    result["stages_completed"].append("schemas")
            
            self.logger.info(f"Pipeline completed: {len(result['stages_completed'])} stages")
            
            return AgentResponse(
                success=True,
                data=result,
                message=f"Processed content through {len(result['stages_completed'])} stages",
                metadata={
                    "stages_completed": result["stages_completed"],
                    "total_flashcards": len(result["flashcards"]),
                    "total_tests": len(result["tests"])
                }
            )
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                message=f"Pipeline error: {str(e)}"
            )
    
    async def _run_reader(self, content: str, options: Dict, language: str) -> AgentResponse:
        """Run Reader Agent"""
        from .reader import ReaderAgent
        
        reader = ReaderAgent()
        return await reader.process(
            content,
            options=options,
            language=language
        )
    
    async def _run_teacher(self, content: str, options: Dict, language: str) -> AgentResponse:
        """Run Teacher Agent"""
        from .teacher import TeacherAgent
        
        teacher = TeacherAgent()
        level = options.get("explanation_level", "beginner")
        
        return await teacher.process(
            content,
            options={"level": level, "include_examples": True},
            language=language
        )
    
    async def _run_examiner(self, content: str, options: Dict, language: str) -> AgentResponse:
        """Run Examiner Agent"""
        from .examiner import ExaminerAgent
        
        examiner = ExaminerAgent()
        num_questions = options.get("num_questions", 10)
        difficulty = options.get("difficulty", "medium")
        
        return await examiner.process(
            content,
            options={
                "question_types": ["multiple_choice", "true_false"],
                "num_questions": num_questions,
                "difficulty": difficulty
            },
            language=language
        )
    
    async def _run_anki(self, content: str, options: Dict, language: str) -> AgentResponse:
        """Run Anki Agent"""
        from .anki import AnkiAgent
        
        anki = AnkiAgent()
        num_cards = options.get("num_flashcards", 20)
        
        return await anki.process(
            content,
            options={
                "card_types": ["basic", "cloze"],
                "num_cards": num_cards
            },
            language=language
        )
    
    async def _run_schema(self, content: str, options: Dict, language: str) -> AgentResponse:
        """Run Schema Agent (placeholder)"""
        # For now, return simple structured data
        return AgentResponse(
            success=True,
            data={
                "schemas": [
                    {
                        "type": "mindmap",
                        "title": "Content Overview",
                        "nodes": [
                            {"id": "root", "label": "Main Topic", "children": []}
                        ]
                    }
                ]
            },
            message="Schema generated"
        )
    
    async def process_all(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method for API usage"""
        response = await self.process(content, options=options)
        return response.data if response.success else {}
