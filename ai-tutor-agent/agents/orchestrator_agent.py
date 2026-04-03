"""
Main Orchestrator Agent - Coordinates all other agents
"""
from typing import Dict, List, Any, Optional
from pathlib import Path

from .reader_agent import ReaderAgent
from .teacher_agent import TeacherAgent
from .examiner_agent import ExaminerAgent
from .anki_agent import AnkiAgent


class OrchestratorAgent:
    """
    Main coordinator agent that manages the entire learning pipeline.
    Routes tasks to specialized agents and combines results.
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        
        # Initialize specialized agents
        self.reader = ReaderAgent(llm_client)
        self.teacher = TeacherAgent(llm_client)
        self.examiner = ExaminerAgent(llm_client)
        self.anki = AnkiAgent(llm_client)
        
        # Processing state
        self.current_content = None
        self.analysis = None
    
    def process_content(self, content: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        Main entry point - process content through full pipeline
        
        Args:
            content: text content to process
            metadata: optional metadata about the content
            
        Returns:
            Dict with all generated materials
        """
        self.current_content = content
        
        # Step 1: Analyze content with Reader Agent
        print("📖 Analyzing content...")
        analysis_result = self.reader.execute({
            'text': content,
            'metadata': metadata or {}
        })
        self.analysis = analysis_result['analysis']
        
        # Step 2: Generate all outputs
        results = {
            'analysis': self.analysis,
            'metadata': metadata or {},
            'outputs': {}
        }
        
        # Generate summary/notes
        print("📒 Generating summary...")
        results['outputs']['summary'] = self.generate_summary(content)
        
        # Generate simple explanations
        print("🎯 Creating simple explanations...")
        results['outputs']['explanations'] = self.generate_explanations(content)
        
        # Generate flashcards
        print("🧠 Creating flashcards...")
        results['outputs']['flashcards'] = self.generate_flashcards(content)
        
        # Generate tests
        print("📝 Creating tests...")
        results['outputs']['tests'] = self.generate_tests(content)
        
        # Generate diagrams/schemas
        print("🧩 Creating schemas...")
        results['outputs']['schemas'] = self.generate_schemas(content)
        
        return results
    
    def generate_summary(self, content: str, format: str = 'structured') -> Dict:
        """Generate structured summary/notes"""
        
        prompt = f"""Создай структурированный конспект по этому материалу.

Формат:
# Тема
## Определение
## Механизм/Принцип работы
## Ключевые факты
## Примеры/Применение
## Важные моменты для запоминания

Материал:
{content[:8000]}

Ответь в формате Markdown с чёткой структурой.
"""
        
        response = self._call_llm(prompt)
        
        return {
            'format': format,
            'content': response,
            'type': 'summary'
        }
    
    def generate_explanations(self, content: str, levels: List[str] = None) -> Dict:
        """Generate explanations at different complexity levels"""
        
        if levels is None:
            levels = ['child', 'beginner', 'intermediate']
        
        explanations = {}
        
        # Get main topics from analysis
        main_topic = self.analysis.get('main_topic', 'Основная тема') if self.analysis else 'Тема'
        
        for level in levels:
            result = self.teacher.execute({
                'concept': main_topic,
                'context': content[:4000],
                'level': level
            })
            explanations[level] = result['explanation']
        
        return {
            'main_topic': main_topic,
            'explanations': explanations,
            'type': 'explanations'
        }
    
    def generate_flashcards(self, content: str, count: int = 20) -> Dict:
        """Generate Anki flashcards"""
        
        result = self.anki.execute({
            'content': content,
            'card_types': ['basic', 'cloze'],
            'count': count,
            'deck_name': f"AI Tutor - {self.analysis.get('main_topic', 'Topic')}" if self.analysis else 'AI Tutor Deck'
        })
        
        return {
            'cards': result['cards'],
            'deck_name': result['deck_name'],
            'count': result['count'],
            'type': 'flashcards'
        }
    
    def generate_tests(self, content: str, question_count: int = 10) -> Dict:
        """Generate test questions"""
        
        result = self.examiner.execute({
            'content': content,
            'question_types': ['multiple_choice', 'true_false', 'short_answer'],
            'difficulty': 'medium',
            'count': question_count
        })
        
        return {
            'questions': result['questions'],
            'metadata': result['metadata'],
            'type': 'tests'
        }
    
    def generate_schemas(self, content: str) -> Dict:
        """Generate visual schemas/diagrams (as text descriptions)"""
        
        prompt = f"""Создай схемы и диаграммы для этого материала.

Предоставь:
1. Flowchart (блок-схема процесса)
2. Mind map (интеллект-карта)
3. Таблицы сравнения/классификации
4. Иерархические структуры

Материал:
{content[:6000]}

Ответь в формате JSON:
{{
    "flowcharts": [
        {{
            "title": "...",
            "steps": ["шаг 1 → шаг 2 → шаг 3"],
            "description": "..."
        }}
    ],
    "mindmaps": [
        {{
            "center": "центральная тема",
            "branches": [
                {{"name": "ветка 1", "children": ["подпункт 1", "подпункт 2"]}}
            ]
        }}
    ],
    "tables": [
        {{
            "title": "...",
            "headers": ["...", "..."],
            "rows": [["...", "..."]]
        }}
    ],
    "hierarchies": [
        {{
            "root": "...",
            "levels": [{{"level": 1, "items": ["..."]}}]
        }}
    ]
}}
"""
        
        response = self._call_llm(prompt)
        
        try:
            schemas = self._parse_json_response(response)
        except:
            schemas = {
                'flowcharts': [],
                'mindmaps': [],
                'tables': [],
                'hierarchies': [],
                'raw': response
            }
        
        return {
            **schemas,
            'type': 'schemas'
        }
    
    def create_clinical_case(self, topic: str = None) -> Dict:
        """Create a clinical/practical case study"""
        
        if not self.current_content:
            raise ValueError("No content loaded. Call process_content first.")
        
        return self.examiner.create_clinical_case(
            self.current_content,
            topic or self.analysis.get('main_topic') if self.analysis else None
        )
    
    def export_all(self, output_dir: str, formats: List[str] = None) -> Dict[str, str]:
        """
        Export all generated materials to files
        
        Args:
            output_dir: directory to save files
            formats: list of formats ('md', 'json', 'apkg')
            
        Returns:
            Dict mapping format to file paths
        """
        if formats is None:
            formats = ['md', 'json']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        exported_files = {}
        
        # Export as Markdown
        if 'md' in formats:
            md_content = self._to_markdown()
            md_file = output_path / "learning_material.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            exported_files['markdown'] = str(md_file)
        
        # Export as JSON
        if 'json' in formats:
            import json
            json_file = output_path / "learning_material.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self._to_dict(), f, ensure_ascii=False, indent=2)
            exported_files['json'] = str(json_file)
        
        # Export Anki cards
        if 'apkg' in formats and 'flashcards' in self.current_outputs:
            apkg_file = output_path / "flashcards.apkg"
            self.anki.export_to_apkg(
                self.current_outputs['flashcards']['cards'],
                self.current_outputs['flashcards']['deck_name'],
                str(apkg_file)
            )
            exported_files['anki'] = str(apkg_file)
        
        return exported_files
    
    def _to_markdown(self) -> str:
        """Convert all outputs to Markdown format"""
        md = []
        
        # Title
        if self.analysis:
            md.append(f"# {self.analysis.get('main_topic', 'Учебный материал')}\n")
        
        # Summary
        if hasattr(self, 'current_outputs') and 'summary' in self.current_outputs:
            md.append("## 📒 Конспект\n")
            md.append(self.current_outputs['summary']['content'])
            md.append("\n")
        
        # Explanations
        if hasattr(self, 'current_outputs') and 'explanations' in self.current_outputs:
            md.append("## 🎯 Объяснения\n")
            for level, exp in self.current_outputs['explanations'].get('explanations', {}).items():
                md.append(f"### Уровень: {level}\n")
                md.append(exp.get('simple_explanation', ''))
                md.append("\n")
        
        # Flashcards
        if hasattr(self, 'current_outputs') and 'flashcards' in self.current_outputs:
            md.append("## 🧠 Карточки для запоминания\n")
            for i, card in enumerate(self.current_outputs['flashcards']['cards'][:10], 1):
                md.append(f"**{i}.** {card['front']}\n")
                if card['back']:
                    md.append(f"*Ответ:* {card['back']}\n")
                md.append("\n")
        
        return '\n'.join(md)
    
    def _to_dict(self) -> Dict:
        """Convert all outputs to dictionary"""
        return getattr(self, 'current_outputs', {})
    
    def _call_llm(self, prompt: str, **kwargs) -> str:
        """Call LLM directly"""
        messages = [
            {"role": "system", "content": "Ты - полезный ассистент для создания учебных материалов."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm_client.chat.completions.create(
            model=self.llm_client.model,
            messages=messages,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from LLM response"""
        import json
        import re
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            code_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if code_match:
                return json.loads(code_match.group(1))
            
            raise
