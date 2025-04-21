"""
Text preprocessing utilities for resume parsing.
"""

import re
from typing import List, Optional


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing.
    
    Args:
        text: Input text to clean.
        
    Returns:
        Cleaned text.
    """
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def remove_special_chars(text: str, keep_chars: str = "") -> str:
    """
    Remove special characters from text.
    
    Args:
        text: Input text.
        keep_chars: Special characters to keep (e.g. ".-_").
        
    Returns:
        Text with special characters removed.
    """
    pattern = r'[^a-zA-Z0-9\s' + re.escape(keep_chars) + r']'
    text = re.sub(pattern, '', text)
    return clean_text(text)


def extract_email_addresses(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Input text.
        
    Returns:
        List of extracted email addresses.
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers from text.
    
    Args:
        text: Input text.
        
    Returns:
        List of extracted phone numbers.
    """
    # Simple pattern for phone numbers
    # This will need to be expanded for different formats
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # International
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US/Canada
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # Simple
        r'\d{5}[-.\s]?\d{6}'  # Some international formats
    ]
    
    results = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        results.extend(matches)
    
    # Remove duplicates while preserving order
    unique_results = []
    for phone in results:
        if phone not in unique_results:
            unique_results.append(phone)
    
    return unique_results


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.
    
    Args:
        text: Input text.
        
    Returns:
        List of extracted URLs.
    """
    patterns = [
        # URLs with http/https prefix
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
        # URLs starting with www.
        r'www\.[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z0-9]+(?:[-a-zA-Z0-9/_\.]+)?',
        # URLs like linkedin.com/in/username
        r'(?:linkedin\.com|github\.com|bitbucket\.org|twitter\.com)[-a-zA-Z0-9/_\.]+',
        # Other common domains
        r'(?:[a-zA-Z0-9][-a-zA-Z0-9]*\.)+(?:com|org|net|edu|io|gov|mil|co|info)(?:[-a-zA-Z0-9/_\.]+)?'
    ]
    
    results = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        results.extend(matches)
    
    # Remove duplicates while preserving order
    unique_results = []
    for url in results:
        if url not in unique_results:
            unique_results.append(url)
    
    return unique_results


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text: Input text.
        
    Returns:
        List of sentences.
    """
    # Simple sentence splitter
    # More advanced sentence splitting could use NLTK or spaCy
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    return re.split(pattern, text)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Input text.
        
    Returns:
        Text with normalized whitespace.
    """
    # Replace multiple lines with a single line
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    # Replace tab characters with spaces
    text = re.sub(r'\t', ' ', text)
    
    return text.strip()


def remove_urls(text: str) -> str:
    """
    Remove URLs from text.
    
    Args:
        text: Input text.
        
    Returns:
        Text with URLs removed.
    """
    # Update to use the same patterns as extract_urls
    patterns = [
        # URLs with http/https prefix
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
        # URLs starting with www.
        r'www\.[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z0-9]+(?:[-a-zA-Z0-9/_\.]+)?',
        # URLs like linkedin.com/in/username
        r'(?:linkedin\.com|github\.com|bitbucket\.org|twitter\.com)[-a-zA-Z0-9/_\.]+',
        # Other common domains
        r'(?:[a-zA-Z0-9][-a-zA-Z0-9]*\.)+(?:com|org|net|edu|io|gov|mil|co|info)(?:[-a-zA-Z0-9/_\.]+)?'
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    
    return text 