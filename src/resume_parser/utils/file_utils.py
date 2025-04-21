"""
File utilities for the resume parser.
"""

import os
import pathlib
from typing import Dict, List, Optional, Union


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        File extension (lowercase, without the dot).
    """
    return os.path.splitext(file_path)[1].lower().lstrip('.')


def is_supported_file(file_path: str, supported_extensions: Optional[List[str]] = None) -> bool:
    """
    Check if a file is supported based on its extension.
    
    Args:
        file_path: Path to the file.
        supported_extensions: List of supported extensions (without the dot).
            Defaults to ['pdf', 'docx', 'txt'].
            
    Returns:
        True if the file is supported, False otherwise.
    """
    if supported_extensions is None:
        supported_extensions = ['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png']
    
    extension = get_file_extension(file_path)
    return extension in supported_extensions


def get_file_info(file_path: str) -> Dict:
    """
    Get basic information about a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        Dictionary with file information.
    """
    file_path = os.path.abspath(file_path)
    stat = os.stat(file_path)
    
    return {
        'name': os.path.basename(file_path),
        'path': file_path,
        'extension': get_file_extension(file_path),
        'size_bytes': stat.st_size,
        'created': stat.st_ctime,
        'modified': stat.st_mtime,
        'accessed': stat.st_atime,
        'is_file': os.path.isfile(file_path),
        'is_dir': os.path.isdir(file_path)
    }


def is_image_file(file_path: str) -> bool:
    """
    Check if a file is an image.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        True if the file is an image, False otherwise.
    """
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif']
    extension = get_file_extension(file_path)
    return extension in image_extensions


def is_pdf_file(file_path: str) -> bool:
    """
    Check if a file is a PDF.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        True if the file is a PDF, False otherwise.
    """
    return get_file_extension(file_path) == 'pdf'


def is_docx_file(file_path: str) -> bool:
    """
    Check if a file is a DOCX.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        True if the file is a DOCX, False otherwise.
    """
    return get_file_extension(file_path) == 'docx'


def is_text_file(file_path: str) -> bool:
    """
    Check if a file is a text file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        True if the file is a text file, False otherwise.
    """
    text_extensions = ['txt', 'text', 'md', 'markdown', 'rst']
    extension = get_file_extension(file_path)
    return extension in text_extensions


def get_absolute_path(file_path: str) -> str:
    """
    Get the absolute path of a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        Absolute path of the file.
    """
    return os.path.abspath(file_path)


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to the directory.
    """
    os.makedirs(directory_path, exist_ok=True)


def list_files_by_extension(directory_path: str, extension: str) -> List[str]:
    """
    List all files with a specific extension in a directory.
    
    Args:
        directory_path: Path to the directory.
        extension: File extension to filter by (without the dot).
        
    Returns:
        List of file paths.
    """
    files = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(f'.{extension.lower()}'):
            files.append(file_path)
    return files 