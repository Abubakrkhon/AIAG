"""
Text Preprocessor and Chunker
"""
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata"""
    content: str
    chunk_id: int
    start_pos: int
    end_pos: int
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TextPreprocessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean(self, text: str) -> str:
        """Clean text from artifacts and normalize"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove special characters that might be artifacts
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove page numbers (common patterns)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove headers/footers (lines with only numbers or very short)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if len(stripped) > 3 or not stripped.isdigit():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def chunk(self, text: str, preserve_sentences: bool = True) -> List[TextChunk]:
        """
        Split text into overlapping chunks
        
        Args:
            text: input text
            preserve_sentences: try to split on sentence boundaries
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunk_content = text[start:].strip()
                if chunk_content:
                    chunks.append(TextChunk(
                        content=chunk_content,
                        chunk_id=chunk_id,
                        start_pos=start,
                        end_pos=len(text),
                        metadata={'is_last': True}
                    ))
                break
            
            # Try to find a good splitting point
            if preserve_sentences:
                # Look for sentence boundary
                best_split = self._find_sentence_boundary(text, start, end)
                if best_split > start:
                    end = best_split
            
            chunk_content = text[start:end].strip()
            
            if chunk_content:
                chunks.append(TextChunk(
                    content=chunk_content,
                    chunk_id=chunk_id,
                    start_pos=start,
                    end_pos=end,
                    metadata={'is_last': False}
                ))
                chunk_id += 1
            
            # Move start with overlap
            start = end - self.chunk_overlap
        
        return chunks
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """Find the best sentence boundary near the end of chunk"""
        # Search backwards from end for sentence endings
        search_start = max(start, end - 200)  # Look back up to 200 chars
        
        candidates = []
        
        # Look for common sentence endings
        for pattern in [r'[.!?]\s', r'[.!?]\n', r'[.!?]$']:
            for match in re.finditer(pattern, text[search_start:end]):
                candidates.append(search_start + match.end())
        
        if candidates:
            # Return the latest sentence boundary
            return max(candidates)
        
        # If no sentence boundary found, try paragraph break
        para_match = re.search(r'\n\n', text[search_start:end])
        if para_match:
            return search_start + para_match.start()
        
        # No good boundary found, return original end
        return end
    
    def extract_structure(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structural elements from text
        
        Returns:
            Dict with lists of:
            - headings
            - definitions
            - lists
            - code_blocks
        """
        structure = {
            'headings': [],
            'definitions': [],
            'lists': [],
            'code_blocks': [],
            'tables': []
        }
        
        lines = text.split('\n')
        
        # Extract headings (Markdown style)
        for line in lines:
            if line.startswith('#'):
                structure['headings'].append(line.strip())
            elif line.startswith('**') and '**:' in line:
                structure['definitions'].append(line.strip())
            elif re.match(r'^\s*[-*•]\s', line) or re.match(r'^\s*\d+\.\s', line):
                structure['lists'].append(line.strip())
            elif line.startswith('```'):
                structure['code_blocks'].append(line.strip())
        
        return structure
