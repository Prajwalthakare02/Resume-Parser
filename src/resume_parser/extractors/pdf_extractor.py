"""
PDF text extraction module using pypdf (migrated from PyPDF2).
"""

import os
from typing import Dict, List, Optional

try:
    # Try to import from pypdf first (new recommended library)
    import pypdf
    USING_PYPDF = True
except ImportError:
    # Fall back to PyPDF2 if pypdf is not installed
    import PyPDF2
    USING_PYPDF = False


class PDFExtractor:
    """
    Extract text content from PDF files.
    """

    def __init__(self):
        """Initialize the PDF extractor."""
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If the file is not a valid PDF.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        text = ""
        
        try:
            with open(file_path, "rb") as file:
                if USING_PYPDF:
                    # Use pypdf library
                    pdf_reader = pypdf.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        # pypdf has a simpler extract_text method without parameters
                        text += page.extract_text() + "\n"
                else:
                    # Use PyPDF2 library (legacy support)
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        # PyPDF2 3.0.1+ no longer needs these parameters
                        text += page.extract_text() + "\n"
                    
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
        
    def extract_metadata(self, file_path: str) -> Dict:
        """
        Extract metadata from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Dictionary containing PDF metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            with open(file_path, "rb") as file:
                if USING_PYPDF:
                    # Use pypdf library
                    pdf_reader = pypdf.PdfReader(file)
                    metadata = pdf_reader.metadata
                    
                    # Convert metadata to regular dictionary
                    meta_dict = {}
                    if metadata:
                        # In pypdf, metadata is directly a dictionary-like object
                        for key, value in metadata.items():
                            meta_dict[key] = value
                    
                    # Add document info
                    meta_dict["pages"] = len(pdf_reader.pages)
                else:
                    # Use PyPDF2 (legacy support)
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata = pdf_reader.metadata
                    
                    # Convert metadata to regular dictionary
                    meta_dict = {}
                    if metadata:
                        for key in metadata:
                            meta_dict[key] = metadata[key]
                    
                    # Add document info
                    meta_dict["pages"] = len(pdf_reader.pages)
                
                return meta_dict
        except Exception as e:
            raise Exception(f"Error reading PDF metadata: {e}") 