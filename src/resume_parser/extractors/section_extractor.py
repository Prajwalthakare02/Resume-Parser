"""
Section extraction module for identifying resume sections.
"""

import re
from typing import Dict, List


class SectionExtractor:
    """
    Extract and identify sections from resume text.
    """

    # List of common section titles with variations
    SECTION_TITLES = {
        'header': [
            r'^\s*(?:name|personal\s+information|contact(?:\s+information)?)\s*$',
            r'^\s*(?:profile|summary|professional\s+summary|executive\s+summary|career\s+summary)\s*$'
        ],
        'profile': [
            r'^\s*(?:profile|summary|about\s+me|professional\s+summary|executive\s+summary|career\s+summary)\s*$',
            r'^\s*(?:career\s+objective|objective|career\s+goal|professional\s+profile)\s*$'
        ],
        'experience': [
            r'^\s*(?:experience|work\s+experience|professional\s+experience|employment(?:\s+history)?|work\s+history)\s*$',
            r'^\s*(?:career(?:\s+history)?|professional\s+background|relevant\s+experience|professional\s+history)\s*$',
            r'^\s*EXPERIENCE\s*$',  # Add specific uppercase pattern
            r'^\s*WORK\s+EXPERIENCE\s*$',  # Add specific uppercase pattern
            r'^\s*(?:internship|internships|intern\s+experience)\s*$',  # Add internship patterns
            r'^\s*INTERNSHIP\s*$'  # Add specific uppercase internship pattern
        ],
        'education': [
            r'^\s*(?:education(?:al)?(?:\s+background|(?:\s+and\s+training)?)?|academic(?:s|(?:\s+background)?))\s*$',
            r'^\s*(?:qualifications|educational\s+qualifications|schooling)\s*$',
            r'^\s*(?:degrees?|academic\s+degrees?)\s*$',
            r'^\s*EDUCATION\s*$'  # Add specific uppercase pattern
        ],
        'skills': [
            r'^\s*(?:(?:technical\s+)?skills|(?:core\s+)?competenc(?:y|ies)|areas\s+of\s+expertise|expertise)\s*$',
            r'^\s*(?:technical|languages|computer|professional|specialized|specific|special)\s+skills\s*$',
            r'^\s*(?:skill\s+set|skill\s+summary|technical\s+expertise|technical\s+proficiencies)\s*$',
            r'^\s*(?:technologies|tools|software|programming\s+languages|languages|frameworks|platforms)\s*$',
            r'^\s*SKILLS\s*$'  # Add specific uppercase pattern
        ],
        'certifications': [
            r'^\s*(?:certifications?|professional\s+certifications?|accreditations?|credentials?)\s*$',
            r'^\s*(?:licenses?|professional\s+licenses?|technical\s+certifications?)\s*$',
            r'^\s*CERTIFICATIONS\s*$'  # Add specific uppercase pattern
        ],
        'projects': [
            r'^\s*(?:projects?|personal\s+projects?|academic\s+projects?|key\s+projects?)\s*$',
            r'^\s*(?:portfolio|work\s+samples|relevant\s+projects|professional\s+projects?)\s*$',
            r'^\s*PROJECTS\s*$'  # Add specific uppercase pattern
        ],
        'publications': [
            r'^\s*(?:publications?|research(?:\s+publications?)?|papers|articles|conference\s+(?:papers|presentations))\s*$',
            r'^\s*(?:journals?|published\s+works?|scholarly\s+works?|academic\s+(?:publications?|papers))\s*$'
        ],
        'awards': [
            r'^\s*(?:awards?|honors?|recognitions?|achievements?|accomplishments?)\s*$',
            r'^\s*(?:prizes?|scholarships?|fellowships?|grants?|academic\s+honors?)\s*$'
        ],
        'languages': [
            r'^\s*(?:languages?|language\s+skills?|language\s+proficiency|linguistic\s+proficiency)\s*$',
            r'^\s*(?:foreign\s+languages?|spoken\s+languages?|language\s+fluency)\s*$'
        ],
        'interests': [
            r'^\s*(?:interests?|hobbies?|activities|personal\s+interests?|other\s+interests?)\s*$',
            r'^\s*(?:extracurricular\s+activities|personal\s+activities|leisure\s+activities)\s*$'
        ],
        'references': [
            r'^\s*(?:references?|professional\s+references?|character\s+references?)\s*$',
            r'^\s*(?:recommendations?|endorsements?|referees?)\s*$'
        ],
        'volunteer': [
            r'^\s*(?:volunteer(?:\s+experience)?|community\s+service|community\s+involvement)\s*$',
            r'^\s*(?:social\s+work|civic\s+activities|philanthropy|voluntary\s+work)\s*$'
        ]
    }

    # Visual section separators in resumes
    SECTION_SEPARATORS = [
        r'^[\s\-_=]{3,}$',          # Lines of dashes, underscores, equals
        r'^[\*\+\#]{3,}$',          # Lines of asterisks, plus or hash symbols
        r'^[\-\=]{2,}\s*[\w\s]+\s*[\-\=]{2,}$'  # Section title surrounded by separators
    ]

    def __init__(self):
        """Initialize the section extractor."""
        # Compile regex patterns for faster matching
        self.compiled_sections = {}
        for section, patterns in self.SECTION_TITLES.items():
            self.compiled_sections[section] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        
        self.separator_patterns = [re.compile(pattern) for pattern in self.SECTION_SEPARATORS]
        
        # Add special case patterns for all uppercase section headers without regex flags
        # This helps catch section headers like "EXPERIENCE" exactly as they appear
        self.uppercase_patterns = {
            'experience': re.compile(r'^\s*EXPERIENCE\s*$'),
            'education': re.compile(r'^\s*EDUCATION\s*$'),
            'skills': re.compile(r'^\s*SKILLS\s*$'),
            'projects': re.compile(r'^\s*PROJECTS\s*$'),
            'certifications': re.compile(r'^\s*CERTIFICATIONS\s*$')
        }

    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract sections from resume text.
        
        Args:
            text: Resume text.
            
        Returns:
            Dictionary with section names as keys and section texts as values.
        """
        # First identify all potential section boundaries
        section_boundaries = self._identify_section_boundaries(text)
        
        # Extract sections based on boundaries
        sections = {}
        
        # If no sections were identified, return the whole text as "unknown"
        if not section_boundaries:
            sections["unknown"] = text.strip()
            return sections
        
        # Extract section text based on start and end positions
        for i, (section_name, start_pos) in enumerate(section_boundaries):
            # Determine end position of this section
            if i < len(section_boundaries) - 1:
                end_pos = section_boundaries[i + 1][1]
            else:
                end_pos = len(text)
            
            section_text = text[start_pos:end_pos].strip()
            
            # Ensure section_name is not None and section_text is not empty
            if section_name and section_text:
                # Remove the section title from the text content
                section_text = self._clean_section_title(section_text, section_name)
                
                # If a section with this name already exists, append the text
                if section_name in sections:
                    sections[section_name] += "\n\n" + section_text
                else:
                    sections[section_name] = section_text
        
        # Perform post-processing to separate overlapping sections
        sections = self._post_process_sections(sections)
        
        return sections
    
    def _identify_section_boundaries(self, text: str) -> List:
        """
        Identify section boundaries in text.
        
        Args:
            text: Resume text.
            
        Returns:
            List of tuples containing section name and start position.
        """
        section_boundaries = []
        
        # Split the text into lines for analysis
        lines = text.split('\n')
        
        current_position = 0
        header_found = False
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            line_start_pos = current_position
            
            # Skip completely empty lines or short lines that are just separators
            if not line_clean or len(line_clean) < 2:
                current_position += len(line) + 1  # +1 for the newline
                continue
            
            # Check if the line is a visual separator
            is_separator = False
            for pattern in self.separator_patterns:
                if pattern.match(line_clean):
                    is_separator = True
                    break
            
            # If it's a separator, check the next line for a section title
            if is_separator and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                section_name = self._identify_section_title(next_line)
                if section_name:
                    section_boundaries.append((section_name, current_position))
            
            # Check for exact uppercase matches first (higher priority)
            uppercase_section = None
            for section, pattern in self.uppercase_patterns.items():
                if pattern.match(line_clean):
                    uppercase_section = section
                    break
                    
            if uppercase_section:
                # Handle the special case of the header (beginning of resume)
                if not header_found and line_start_pos < 200:  # Assume header is near the beginning
                    if not section_boundaries or section_boundaries[0][0] != 'header':
                        section_boundaries.insert(0, ('header', 0))
                        header_found = True
                
                # Add this uppercase section boundary
                section_boundaries.append((uppercase_section, current_position))
            else:
                # Otherwise check for regular section title patterns
                section_name = self._identify_section_title(line_clean)
                if section_name:
                    # Handle the special case of the header (beginning of resume)
                    if not header_found and line_start_pos < 200:  # Assume header is near the beginning
                        if not section_boundaries or section_boundaries[0][0] != 'header':
                            section_boundaries.insert(0, ('header', 0))
                            header_found = True
                    
                    # Add this section boundary
                    section_boundaries.append((section_name, current_position))
            
            current_position += len(line) + 1  # +1 for the newline
        
        # If no sections were identified and text isn't empty, use heuristics
        if not section_boundaries and text.strip():
            section_boundaries = self._fallback_section_identification(text, lines)
        
        return section_boundaries
    
    def _fallback_section_identification(self, text: str, lines: List[str]) -> List:
        """
        Fallback method to identify sections when standard detection fails.
        
        Args:
            text: Resume text.
            lines: List of lines from the text.
            
        Returns:
            List of tuples containing section name and start position.
        """
        section_boundaries = []
        
        # Assume the beginning is a header section
        section_boundaries.append(('header', 0))
        
        # Look for patterns that might indicate sections without explicit titles
        current_position = 0
        
        for i, line in enumerate(lines):
            line_clean = line.strip().lower()
            
            # Education keywords
            if (re.search(r'\b(degree|university|college|school|gpa|bachelor|master|phd|diploma)\b', line_clean) and 
                not any(section[0] == 'education' for section in section_boundaries)):
                section_boundaries.append(('education', current_position))
            
            # Experience keywords
            elif (re.search(r'\b(experience|work|job|position|employer|company|responsibilities)\b', line_clean) and 
                  not any(section[0] == 'experience' for section in section_boundaries)):
                section_boundaries.append(('experience', current_position))
            
            # Skills keywords
            elif (re.search(r'\b(skills|proficient|expertise|competenc|abilities)\b', line_clean) and 
                  not any(section[0] == 'skills' for section in section_boundaries)):
                section_boundaries.append(('skills', current_position))
            
            # Certifications keywords
            elif (re.search(r'\b(certification|certified|license|accredit|credential)\b', line_clean) and 
                  not any(section[0] == 'certifications' for section in section_boundaries)):
                section_boundaries.append(('certifications', current_position))
            
            current_position += len(line) + 1  # +1 for the newline
        
        return section_boundaries
    
    def _identify_section_title(self, line: str) -> str:
        """
        Identify if a line is a section title.
        
        Args:
            line: Line of text.
            
        Returns:
            Section name if the line is a section title, None otherwise.
        """
        # Clean the line to standardize matching
        clean_line = line.strip().lower()
        
        # Remove common formatting characters
        clean_line = re.sub(r'[:\-_=*#•■□▪▫]', '', clean_line).strip()
        
        # Try to match with known section titles
        for section, patterns in self.compiled_sections.items():
            for pattern in patterns:
                if pattern.match(clean_line):
                    return section
        
        # Look for capitalized words that might be section headers
        if (clean_line.isupper() or clean_line.istitle()) and len(clean_line) < 30:
            # Map common uppercase/titlecase headers to our section names
            if re.search(r'\b(EXPERIENCE|WORK|EMPLOYMENT|PROFESSIONAL)\b', line):
                return 'experience'
            elif re.search(r'\b(EDUCATION|ACADEMIC|QUALIFICATION|DEGREE)\b', line):
                return 'education'
            elif re.search(r'\b(SKILL|COMPETENC|EXPERTISE|PROFICIENC)\b', line):
                return 'skills'
            elif re.search(r'\b(CERTIFICATE|CERTIFICATION|LICENSE|CREDENTIAL)\b', line):
                return 'certifications'
            elif re.search(r'\b(PROJECT|PORTFOLIO|CASE STUD)\b', line):
                return 'projects'
            elif re.search(r'\b(LANGUAGE)\b', line) and not re.search(r'\b(PROGRAMMING|COMPUTER)\b', line):
                return 'languages'
            
        return None
    
    def _clean_section_title(self, section_text: str, section_name: str) -> str:
        """
        Clean the section title from the section text.
        
        Args:
            section_text: Section text.
            section_name: Section name.
            
        Returns:
            Section text without the title.
        """
        lines = section_text.split('\n')
        
        # Check if the first line contains the section title
        if lines and self._identify_section_title(lines[0]) == section_name:
            return '\n'.join(lines[1:]).strip()
        
        # Check if the second line is a section title (in case the first is a separator)
        if len(lines) > 1 and self._identify_section_title(lines[1]) == section_name:
            return '\n'.join(lines[2:]).strip()
        
        return section_text
    
    def _post_process_sections(self, sections: Dict[str, str]) -> Dict[str, str]:
        """
        Perform post-processing on extracted sections to ensure accuracy.
        
        Args:
            sections: Dictionary of extracted sections.
            
        Returns:
            Processed sections dictionary.
        """
        processed_sections = {}
        
        # Process each section
        for section_name, section_text in sections.items():
            # Handle education/certifications overlap
            if section_name == 'education' and 'certifications' not in sections:
                # Check for certification keywords in education section
                cert_match = re.search(r'(?i)(\n|^)\s*(certification|certified|credential|license|accredit)', section_text)
                if cert_match:
                    # Split the section at the certification keyword
                    split_pos = cert_match.start()
                    
                    # Keep the text before the split as education
                    processed_sections['education'] = section_text[:split_pos].strip()
                    
                    # Add the rest as certifications
                    processed_sections['certifications'] = section_text[split_pos:].strip()
                    continue
            
            # Add the section as is if no special processing was needed
            processed_sections[section_name] = section_text
        
        return processed_sections 