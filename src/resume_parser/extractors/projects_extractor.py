"""
Projects extraction module for extracting project details from resumes.
"""

import re
from typing import Dict, List, Optional

from resume_parser.utils import text_preprocessing


class ProjectsExtractor:
    """
    Extract project details from resume text.
    """

    # Date patterns
    DATE_PATTERNS = [
        r"(?i)(?:^|\s)(\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*present|\d{4}\s*-\s*ongoing)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\s*-\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\s*-\s*(Present|Ongoing|Current)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(\d{4})(?:\s|$|,|\.)"
    ]

    # Technology/tool patterns
    TECHNOLOGY_PATTERNS = [
        r"(?i)(?:^|\s)(Technologies|Tools|Tech Stack|Built with|Developed using|Implemented using|Stack)(?:\s|:|$)",
        r"(?i)(?:^|\s)(using|with|in|through)\s+([A-Za-z0-9, ]+)(?:\s|$|\.)"
    ]

    # Bullet points patterns
    BULLET_PATTERNS = [
        r"(?:^|\n)\s*[•\-*]",   # Common bullet point markers
        r"(?:^|\n)\s*\d+\.",    # Numbered lists
        r"(?:^|\n)\s*\[\+\]",   # Some markdown-style bullets
    ]

    def __init__(self):
        """Initialize the projects extractor."""
        self.date_patterns = [re.compile(pattern) for pattern in self.DATE_PATTERNS]
        self.technology_patterns = [re.compile(pattern) for pattern in self.TECHNOLOGY_PATTERNS]
        self.bullet_patterns = [re.compile(pattern) for pattern in self.BULLET_PATTERNS]

    def extract_projects(self, text: str) -> List[Dict]:
        """
        Extract project details from text.
        
        Args:
            text: Projects section text.
            
        Returns:
            List of dictionaries containing project details.
        """
        project_entries = []
        
        # Split the text into potential project entries
        entries = self._split_project_entries(text)
        
        for entry in entries:
            # Clean the entry text
            clean_entry = text_preprocessing.clean_text(entry)
            
            if not clean_entry:
                continue
                
            # Extract details from the entry
            project_name = self._extract_project_name(entry)
            date_range = self._extract_date_range(clean_entry)
            technologies = self._extract_technologies(clean_entry)
            description = self._extract_description(entry)
            
            # Only add entries that have at least a project name
            if project_name:
                project_entry = {
                    "name": project_name,
                    "date_range": date_range,
                    "technologies": technologies,
                    "description": description,
                    "raw_text": clean_entry
                }
                
                project_entries.append(project_entry)
                
        return project_entries
        
    def _split_project_entries(self, text: str) -> List[str]:
        """
        Split project text into separate entries.
        
        Args:
            text: Projects section text.
            
        Returns:
            List of project entry texts.
        """
        # Try to split by double line breaks first
        entries = re.split(r'\n\s*\n', text)
        
        # If that didn't work well, try single line breaks when followed by a capitalized word
        # (which is often a new project name)
        if len(entries) <= 1:
            entry_start_pattern = re.compile(r'\n([A-Z][a-zA-Z0-9 ]+)[\s:–-]')
            
            entry_starts = [0]  # Start of text
            for match in entry_start_pattern.finditer(text):
                entry_starts.append(match.start())
                
            entry_starts.append(len(text))  # End of text
            
            entries = []
            for i in range(len(entry_starts) - 1):
                start = entry_starts[i]
                end = entry_starts[i+1]
                entry = text[start:end].strip()
                if entry:
                    entries.append(entry)
        
        # Filter out empty entries
        return [entry.strip() for entry in entries if entry.strip()]
        
    def _extract_project_name(self, text: str) -> Optional[str]:
        """
        Extract project name from text.
        
        Args:
            text: Project entry text.
            
        Returns:
            Extracted project name or None.
        """
        # Project name is typically the first line or before the first colon
        lines = text.split('\n')
        first_line = lines[0] if lines else ""
        
        # Check if the first line contains a project name
        if ":" in first_line:
            return first_line.split(":", 1)[0].strip()
        else:
            # Split by common separators and return the first segment
            segments = re.split(r'[,;|\n]', first_line)
            return segments[0].strip() if segments else None
        
    def _extract_date_range(self, text: str) -> Optional[str]:
        """
        Extract date range from text.
        
        Args:
            text: Project entry text.
            
        Returns:
            Extracted date range or None.
        """
        for pattern in self.date_patterns:
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
                
        return None
        
    def _extract_technologies(self, text: str) -> List[str]:
        """
        Extract technologies used in the project.
        
        Args:
            text: Project entry text.
            
        Returns:
            List of technologies.
        """
        technologies = []
        
        # Look for technology sections
        for pattern in self.technology_patterns:
            match = pattern.search(text)
            if match:
                # If it's the "using/with" pattern, extract the technologies
                if match.group(1).lower() in ["using", "with", "in", "through"] and len(match.groups()) > 1:
                    tech_text = match.group(2)
                    for tech in tech_text.split(","):
                        clean_tech = tech.strip()
                        if clean_tech and clean_tech not in technologies:
                            technologies.append(clean_tech)
                else:
                    # Find the text after the technology keyword until the end of line
                    start_pos = match.end()
                    end_pos = text.find('\n', start_pos)
                    if end_pos == -1:
                        end_pos = len(text)
                    
                    tech_text = text[start_pos:end_pos].strip()
                    if ":" in tech_text:
                        tech_text = tech_text.split(":", 1)[1].strip()
                    
                    # Split by commas or other separators
                    for tech in re.split(r'[,;]', tech_text):
                        clean_tech = tech.strip()
                        if clean_tech and clean_tech not in technologies:
                            technologies.append(clean_tech)
        
        return technologies
        
    def _extract_description(self, text: str) -> List[str]:
        """
        Extract project description.
        
        Args:
            text: Project entry text.
            
        Returns:
            List of description points.
        """
        description = []
        
        # Look for bullet points
        for pattern in self.bullet_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                # Find the start of the bullet point
                start = match.end()
                
                # Find the end (next bullet or end of text)
                end = len(text)
                for end_match in pattern.finditer(text[start:]):
                    end = start + end_match.start()
                    break
                
                # Extract the bullet point text
                bullet_text = text[start:end].strip()
                if bullet_text and bullet_text not in description:
                    description.append(bullet_text)
        
        # If no bullet points found, try to extract description from lines after the first line
        if not description:
            lines = text.split('\n')
            if len(lines) > 1:
                # Skip the first line (typically project name)
                for line in lines[1:]:
                    clean_line = line.strip()
                    if clean_line and clean_line not in description:
                        description.append(clean_line)
        
        return description 