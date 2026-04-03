"""
Image/OCR Parser using Tesseract
"""
import pytesseract
from PIL import Image
from typing import Dict, List
from pathlib import Path
import cv2
import numpy as np


class OCRParser:
    def __init__(self, lang: str = 'rus+eng'):
        self.supported_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']
        self.language = lang
    
    def parse(self, image_path: str, preprocess: bool = True) -> Dict[str, any]:
        """
        Extract text from image using OCR
        
        Args:
            image_path: path to image file
            preprocess: apply image preprocessing for better accuracy
            
        Returns:
            Dict with:
            - text: extracted text
            - blocks: text blocks with positions
            - metadata: image info
        """
        image_file = Path(image_path)
        
        if not image_file.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Load image
        img = cv2.imread(str(image_file))
        
        if preprocess:
            img = self._preprocess_image(img)
        
        # Convert to PIL for pytesseract
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Get detailed OCR data
        ocr_data = pytesseract.image_to_data(img_pil, lang=self.language, output_type=pytesseract.Output.DICT)
        
        # Extract full text
        full_text = pytesseract.image_to_string(img_pil, lang=self.language)
        
        # Extract text blocks with positions
        blocks = self._extract_blocks(ocr_data)
        
        return {
            'text': full_text.strip(),
            'blocks': blocks,
            'metadata': {
                'source': str(image_file),
                'width': img.shape[1],
                'height': img.shape[0],
                'type': 'image'
            },
            'source': str(image_file),
            'type': 'image'
        }
    
    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        
        # Apply thresholding
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _extract_blocks(self, ocr_data: Dict) -> List[Dict]:
        """Extract text blocks with bounding boxes"""
        blocks = []
        
        n_boxes = len(ocr_data['level'])
        
        current_block = None
        current_text = []
        
        for i in range(n_boxes):
            if int(ocr_data['conf'][i]) > 60:  # Confidence threshold
                text = ocr_data['text'][i].strip()
                
                if text:
                    if current_block is None:
                        current_block = {
                            'left': ocr_data['left'][i],
                            'top': ocr_data['top'][i],
                            'width': ocr_data['width'][i],
                            'height': ocr_data['height'][i],
                            'texts': []
                        }
                    
                    current_text.append(text)
                    
                    # Check if we should start a new block (significant position change)
                    if i < n_boxes - 1:
                        next_left = ocr_data['left'][i + 1]
                        next_top = ocr_data['top'][i + 1]
                        
                        if abs(next_top - current_block['top']) > 20:
                            # New block
                            blocks.append({
                                'bbox': {
                                    'left': current_block['left'],
                                    'top': current_block['top'],
                                    'width': current_block['width'],
                                    'height': current_block['height']
                                },
                                'text': ' '.join(current_text)
                            })
                            
                            current_block = None
                            current_text = []
        
        # Add last block
        if current_text:
            blocks.append({
                'bbox': {
                    'left': current_block['left'],
                    'top': current_block['top'],
                    'width': current_block['width'],
                    'height': current_block['height']
                },
                'text': ' '.join(current_text)
            })
        
        return blocks
