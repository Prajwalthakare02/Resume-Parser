"""
TXT text extraction module for plain text files.
"""

import os
from typing import Dict, Optional


class TxtExtractor:
    """
    Extract text content from TXT files.
    """

    def __init__(self):
        """Initialize the TXT extractor."""
        pass
    
    def extract_text(self, file_path: str, encoding: str = "utf-8") -> str:
        """
        Extract text from a plain text file.

        Args:
            file_path: Path to the TXT file.
            encoding: Text encoding (default: utf-8).

        Returns:
            Extracted text content.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnicodeDecodeError: If the file cannot be decoded with the specified encoding.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, "r", encoding=encoding) as file:
                text = file.read()
            return text
        except UnicodeDecodeError as e:
            # Re-raise the original exception instead of creating a new one
            # or try with a different encoding
            try:
                # Try with a more permissive encoding as fallback
                with open(file_path, "r", encoding="latin-1") as file:
                    text = file.read()
                return text
            except Exception:
                # If fallback fails too, re-raise the original exception
                raise e
    
    def extract_metadata(self, file_path: str) -> Dict:
        """
        Extract basic metadata from a TXT file.

        Args:
            file_path: Path to the TXT file.

        Returns:
            Dictionary containing basic file metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stats = os.stat(file_path)
        
        metadata = {
            "size_bytes": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime,
            "accessed": stats.st_atime
        }
        
        # Try to get line count and word count
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                lines = text.split("\n")
                words = text.split()
                
                metadata["line_count"] = len(lines)
                metadata["word_count"] = len(words)
                metadata["char_count"] = len(text)
        except Exception:
            # If there's an error reading the file, skip these metrics
            pass
            
        return metadata 