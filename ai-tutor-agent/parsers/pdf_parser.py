"""
PDF Parser using PyMuPDF
"""
import fitz  # PyMuPDF
from typing import List, Dict
import re


class PDFParser:
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def parse(self, file_path: str) -> Dict[str, any]:
        """
        Parse PDF file and extract text with structure
        
        Returns:
            Dict with:
            - text: full text
            - pages: list of page texts
            - metadata: document metadata
        """
        doc = fitz.open(file_path)
        
        pages = []
        full_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages.append({
                'page_number': page_num + 1,
                'text': text
            })
            full_text.append(text)
        
        metadata = doc.metadata
        
        doc.close()
        
        return {
            'text': '\n'.join(full_text),
            'pages': pages,
            'metadata': metadata,
            'source': file_path,
            'type': 'pdf'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text from artifacts"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove page numbers and headers/footers (basic pattern)
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        return text.strip()
