"""
OCR extraction module using pytesseract.
"""

import os
from typing import Dict, List, Optional, Tuple

import pytesseract
from PIL import Image


class OCRExtractor:
    """
    Extract text content from images using OCR.
    """

    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize the OCR extractor.
        
        Args:
            tesseract_cmd: Path to tesseract executable.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def extract_text(self, file_path: str, lang: str = "eng") -> str:
        """
        Extract text from an image using OCR.

        Args:
            file_path: Path to the image file.
            lang: Language for OCR (default: eng).

        Returns:
            Extracted text content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid image.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error processing image with OCR: {e}")
    
    def extract_text_with_coordinates(self, file_path: str, lang: str = "eng") -> List[Dict]:
        """
        Extract text with bounding box coordinates.

        Args:
            file_path: Path to the image file.
            lang: Language for OCR (default: eng).

        Returns:
            List of dictionaries with text and coordinates.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            image = Image.open(file_path)
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                # Skip empty text
                if int(data['conf'][i]) > 0 and data['text'][i].strip():
                    text_data = {
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]),
                        'coordinates': {
                            'x': data['left'][i],
                            'y': data['top'][i],
                            'width': data['width'][i],
                            'height': data['height'][i]
                        },
                        'line_num': data['line_num'][i],
                        'block_num': data['block_num'][i],
                        'page_num': data['page_num'][i]
                    }
                    results.append(text_data)
            
            return results
        except Exception as e:
            raise ValueError(f"Error processing image with OCR: {e}")
    
    def extract_metadata(self, file_path: str) -> Dict:
        """
        Extract image metadata.

        Args:
            file_path: Path to the image file.

        Returns:
            Dictionary containing image metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            image = Image.open(file_path)
            
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "width": image.width,
                "height": image.height,
                "size_bytes": os.path.getsize(file_path)
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and callable(image._getexif):
                exif = image._getexif()
                if exif:
                    metadata["exif"] = exif
            
            return metadata
        except Exception as e:
            raise ValueError(f"Error extracting image metadata: {e}") 