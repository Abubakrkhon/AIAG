"""
Text Processor - Text cleaning, chunking, and preprocessing utilities
"""
from typing import List, Dict, Any, Optional
import re
from loguru import logger


class TextProcessor:
    """
    Utility class for text preprocessing and processing.
    
    Capabilities:
    - Text cleaning (remove noise, normalize)
    - Chunking (split into manageable pieces)
    - Token counting
    - Language detection
    - Text normalization
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.logger = logger.bind(component="text_processor")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that don't add meaning
        text = re.sub(r'[^\w\s.,!?;:()\-–—\'\"@#$%&*+=/\\<>]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Normalize dashes
        text = text.replace('–', '-').replace('—', '-')
        
        # Remove URLs (optional, keep if needed)
        # text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove email addresses (optional)
        # text = re.sub(r'\S+@\S+', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        self.logger.debug(f"Cleaned text from {len(text)} to {len(text)} chars")
        return text
    
    def chunk_text(
        self,
        text: str,
        chunk_size: Optional[int] = None,
        overlap: Optional[int] = None,
        strategy: str = "overlap"
    ) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: Text to split
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            strategy: Chunking strategy ("overlap", "sentence", "paragraph")
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.chunk_overlap
        
        if not text:
            return []
        
        if strategy == "overlap":
            return self._chunk_overlap(text, chunk_size, overlap)
        elif strategy == "sentence":
            return self._chunk_sentences(text, chunk_size)
        elif strategy == "paragraph":
            return self._chunk_paragraphs(text, chunk_size)
        else:
            return self._chunk_overlap(text, chunk_size, overlap)
    
    def _chunk_overlap(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Chunk with overlapping content"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def _chunk_sentences(self, text: str, chunk_size: int) -> List[str]:
        """Chunk by sentences"""
        import re
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _chunk_paragraphs(self, text: str, chunk_size: int) -> List[str]:
        """Chunk by paragraphs"""
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            if len(paragraph) <= chunk_size:
                if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                    current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = paragraph
            else:
                # Large paragraph, split it
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                # Split large paragraph by sentences
                sub_chunks = self._chunk_sentences(paragraph, chunk_size)
                chunks.extend(sub_chunks)
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text (approximate).
        
        Args:
            text: Text to count tokens
            
        Returns:
            Approximate token count
        """
        # Rough approximation: 1 token ≈ 4 characters in English
        # For more accuracy, use tiktoken library
        try:
            import tiktoken
            encoder = tiktoken.get_encoding("cl100k_base")
            return len(encoder.encode(text))
        except ImportError:
            # Fallback estimation
            return len(text) // 4
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (e.g., 'en', 'ru')
        """
        # Simple heuristic based on character ranges
        cyrillic_chars = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
        latin_chars = sum(1 for c in text if 'a' <= c <= 'z' or 'A' <= c <= 'Z')
        
        if cyrillic_chars > latin_chars * 0.5:
            return 'ru'
        elif latin_chars > 0:
            return 'en'
        else:
            return 'unknown'
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract keywords from text.
        
        Args:
            text: Text to analyze
            top_n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction using word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stopwords (simple list)
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'that', 'this', 'it', 'as', 'if', 'then', 'than', 'so', 'such',
            'что', 'и', 'в', 'на', 'с', 'для', 'от', 'по', 'при', 'под', 'над',
            'из', 'о', 'об', 'а', 'но', 'или', 'же', 'бы', 'был', 'была', 'было',
            'есть', 'будет', 'будут', 'этот', 'эта', 'это', 'эти', 'как', 'так'
        }
        
        word_freq = {}
        for word in words:
            if word not in stopwords and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_n]]
    
    def summarize_sentences(self, text: str, num_sentences: int = 3) -> str:
        """
        Create simple extractive summary.
        
        Args:
            text: Text to summarize
            num_sentences: Number of sentences in summary
            
        Returns:
            Summary text
        """
        import re
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Score sentences by position and length
        scored = []
        for i, sent in enumerate(sentences):
            score = 0
            
            # First sentences are important
            if i < 3:
                score += 3 - i
            
            # Long sentences (but not too long) often have more info
            length_score = min(len(sent) / 100, 2)
            score += length_score
            
            scored.append((score, sent))
        
        # Get top sentences
        scored.sort(reverse=True)
        top_sentences = [sent for score, sent in scored[:num_sentences]]
        
        # Reorder by original position
        top_sentences_ordered = [
            sent for sent in sentences 
            if sent in top_sentences
        ]
        
        return ' '.join(top_sentences_ordered)
    
    def remove_duplicates(self, text: str) -> str:
        """Remove duplicate lines and paragraphs"""
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and line_stripped not in seen:
                seen.add(line_stripped)
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
