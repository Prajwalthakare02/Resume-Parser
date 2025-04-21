"""
Education extraction module for extracting education details from resumes.
"""

import re
from typing import Dict, List, Optional, Tuple

from resume_parser.utils import text_preprocessing


class EducationExtractor:
    """
    Extract education details from resume text.
    """

    # Common degree patterns
    DEGREE_PATTERNS = [
        r"(?i)(?:^|\s)(B\.Tech|Bachelor of Technology)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(B\.E\.|Bachelor of Engineering)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Bachelor of Engineering in [A-Za-z\s]+)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(B\.Sc\.|Bachelor of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(B\.S\.|B\.S\.? in .+?|Bachelor of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Bachelor of Science in)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Bachelor of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(B\.A\.|Bachelor of Arts)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(B\.Com\.|Bachelor of Commerce)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.Tech|Master of Technology)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.E\.|Master of Engineering)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.Sc\.|Master of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.S\.|M\.S\.? in .+?|Master of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Master of Science in)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Master of Science)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.A\.|Master of Arts)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(M\.Com\.|Master of Commerce)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(MBA|Master of Business Administration)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Ph\.D\.|Doctor of Philosophy)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Diploma|Associate Degree)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(HSC|12th|XII|Higher Secondary)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(SSC|10th|X|Secondary)(?:\s|$|,|\.)"
    ]

    # Full degree indicators for better separation
    FULL_DEGREE_INDICATORS = [
        r"(?i)(Bachelor[''']s degree|Master[''']s degree|Doctorate|Ph\.D|MBA)",
        r"(?i)(B\.S\.|B\.A\.|B\.Tech|B\.E\.|M\.S\.|M\.A\.|M\.Tech|M\.B\.A|Associate's|A\.A\.|A\.S\.)",
        r"(?i)(Bachelor of|Master of|Doctor of|Associate of)"
    ]

    # Institution name patterns
    INSTITUTION_PATTERNS = [
        r"(?i)(?:^|\s)(University|College|Institute|School)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Academy|Education|Educational|Vidyalaya)(?:\s|$|,|\.)"
    ]

    # Common universities and colleges for direct matching
    COMMON_INSTITUTIONS = [
        "Harvard University", "Yale University", "Princeton University",
        "Stanford University", "Massachusetts Institute of Technology", "MIT",
        "California Institute of Technology", "Columbia University",
        "University of Chicago", "University of Pennsylvania", "Penn",
        "University of California, Berkeley", "Cornell University",
        "University of Michigan", "University of Cambridge", "University of Oxford",
        "Imperial College London", "ETH Zurich", "National University of Singapore",
        "Tsinghua University", "University of Toronto", "Carnegie Mellon University",
        "New York University", "Marathwada Mitra Mandal's College", "Marathwada Mitra Mandal"
    ]

    # Date patterns
    DATE_PATTERNS = [
        r"(?i)(?:^|\s)(\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*present|\d{4}\s*-\s*ongoing)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(\d{4})(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}(?:\s|$|,|\.)"
    ]

    # GPA/Score patterns
    SCORE_PATTERNS = [
        r"(?i)(?:^|\s|:)(GPA|CGPA|Percentage|Score|Marks)[\s:]*(\d+\.\d+|\d+\.|\d+)[%]?(?:[\s/]|$|,|\.)",
        r"(?i)(?:^|\s)(\d+\.\d+|\d+)[/](\d+\.\d+|\d+)(?:\s|$|,|\.)",
        r"(?i)(?:^|\s)(\d+\.\d+|\d+)[%](?:\s|$|,|\.)",
        r"(?i)(Cum Laude|Magna Cum Laude|Summa Cum Laude|Distinction|Merit|First Class|Second Class)"
    ]

    # Field of study patterns - improved to avoid false positives
    FIELD_PATTERNS = [
        # Only look for field patterns after degree keywords to avoid false positives
        r"(?i)(?:degree|bachelor|master|ms|ma|mba|phd|bs|ba)\s+in\s+([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\n)",
        r"(?i)(?:majoring|majored)\s+in\s+([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\n)",
        r"(?i)(?:studied|study|studies)\s+in\s+([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\n)",
        r"(?i)(?:in|of)\s+([A-Za-z][A-Za-z\s]+?)(?:\s+(?:from|at|in)\s+(?:the\s+)?(?:university|college|institute|school))",
    ]

    # List of common fields of study to verify extracted fields
    COMMON_FIELDS = [
        "computer science", "information technology", "electrical engineering", 
        "mechanical engineering", "civil engineering", "chemical engineering",
        "biology", "chemistry", "physics", "mathematics", "statistics", 
        "business administration", "finance", "economics", "accounting", 
        "marketing", "management", "psychology", "sociology", "history", 
        "english", "literature", "communications", "journalism", "political science",
        "international relations", "philosophy", "education", "nursing", "medicine", 
        "law", "criminal justice", "art", "design", "music", "theater", "film",
        "architecture", "agriculture", "environmental science", "geography",
        "anthropology", "linguistics", "information systems", "data science",
        "artificial intelligence", "machine learning", "cybersecurity"
    ]

    # Concentration/specialization patterns
    CONCENTRATION_PATTERNS = [
        r"(?i)(Concentration|Specialization|Focus|Major|Track|Emphasis)(?:: | in )([A-Za-z\s]+?)(?:,|\.|$|\n)",
        r"(?i)(?:with|,) ([A-Za-z\s]+) (Concentration|Specialization|Focus|Major|Track|Emphasis)(?:,|\.|$|\n)",
    ]

    def __init__(self):
        """Initialize the education extractor."""
        self.degree_patterns = [re.compile(pattern) for pattern in self.DEGREE_PATTERNS]
        self.full_degree_indicators = [re.compile(pattern) for pattern in self.FULL_DEGREE_INDICATORS]
        self.institution_patterns = [re.compile(pattern) for pattern in self.INSTITUTION_PATTERNS]
        self.date_patterns = [re.compile(pattern) for pattern in self.DATE_PATTERNS]
        self.score_patterns = [re.compile(pattern) for pattern in self.SCORE_PATTERNS]
        self.field_patterns = [re.compile(pattern) for pattern in self.FIELD_PATTERNS]
        self.concentration_patterns = [re.compile(pattern) for pattern in self.CONCENTRATION_PATTERNS]
        
        # Precompile common institution pattern for faster matching
        common_inst_pattern = "|".join([re.escape(inst) for inst in self.COMMON_INSTITUTIONS])
        self.common_inst_regex = re.compile(f"(?i)({common_inst_pattern})")
        
        # Precompile common fields pattern for verification
        self.common_fields_pattern = re.compile(f"(?i)\\b({'|'.join(self.COMMON_FIELDS)})\\b")

    def extract_education(self, text: str) -> List[Dict]:
        """
        Extract education details from text.
        
        Args:
            text: Education section text.
            
        Returns:
            List of dictionaries containing education details.
        """
        # If text is empty or too short, return empty list
        if not text or len(text) < 10:
            return []
            
        education_entries = []
        
        # Split the text into potential education entries
        entries = self._split_education_entries(text)
        
        # If the split didn't produce good results, try a more aggressive approach
        if len(entries) <= 1 and len(text) > 100:
            # Look for degree indicators that likely start a new entry
            entries = self._split_by_degree_indicators(text)
        
        for entry in entries:
            # Clean the entry text
            clean_entry = text_preprocessing.clean_text(entry)
            
            if not clean_entry:
                continue
                
            # Extract details from the entry
            degree = self._extract_degree(clean_entry)
            field_of_study = self._extract_field_of_study(clean_entry)
            concentration = self._extract_concentration(clean_entry)
            institution = self._extract_institution(clean_entry)
            dates = self._extract_dates(clean_entry)
            score = self._extract_score(clean_entry)
            
            # Validate field of study to prevent false positives
            if field_of_study and not self._is_valid_field(field_of_study):
                field_of_study = None
            
            # Combine degree and field if both are found
            if degree and field_of_study and "in" not in degree.lower():
                degree = f"{degree} in {field_of_study}"
            
            # Add concentration if found
            if degree and concentration and "concentration" not in degree.lower():
                degree = f"{degree}, {concentration} Concentration"
            
            # Fallback for common formats
            if not degree and not institution:
                lines = entry.split('\n')
                if len(lines) >= 2:
                    # First line might be degree
                    first_line = lines[0].strip()
                    # Check for common degree keywords in first line
                    if any(keyword in first_line.lower() for keyword in 
                           ["bachelor", "master", "degree", "bs", "ms", "ba", "ma", "phd"]):
                        degree = first_line
                    
                    # Second line might be institution
                    second_line = lines[1].strip()
                    # Check for common institution keywords in second line
                    if any(keyword in second_line.lower() for keyword in 
                           ["university", "college", "institute", "school"]):
                        institution = second_line
            
            # Only add entries that have at least degree or institution
            if degree or institution:
                education_entry = {
                    "degree": degree,
                    "institution": institution,
                    "dates": dates,
                    "score": score,
                    "raw_text": clean_entry
                }
                
                education_entries.append(education_entry)
                
        return education_entries
    
    def _is_valid_field(self, field: str) -> bool:
        """
        Validate if the extracted field of study is a common academic discipline.
        
        Args:
            field: Extracted field of study.
            
        Returns:
            True if valid, False otherwise.
        """
        # Check if it's too short (likely a false positive)
        if len(field) < 4:
            return False
            
        # Check if it's a common word that's not a field of study
        common_words = ["the", "and", "with", "from", "also", "have", "this", "that", "there"]
        if field.lower() in common_words:
            return False
            
        # Check against our list of common fields
        if self.common_fields_pattern.search(field):
            return True
            
        # Check for common field-like patterns
        if re.search(r"(?i)(science|engineering|studies|technology|arts|management|design|analysis|systems)", field):
            return True
            
        return False
        
    def _split_education_entries(self, text: str) -> List[str]:
        """
        Split education text into separate entries.
        
        Args:
            text: Education section text.
            
        Returns:
            List of education entry texts.
        """
        # Try to split by double line breaks first
        entries = re.split(r'\n\s*\n', text)
        
        # If that didn't work well, try looking for educational patterns
        if len(entries) <= 1:
            # Look for patterns that indicate the start of a new entry
            potential_split_points = []
            
            # Common degree indicators often start a new entry
            for pattern in self.degree_patterns:
                for match in pattern.finditer(text):
                    match_pos = match.start()
                    # Check if the match is at the beginning of a line
                    if match_pos == 0 or text[match_pos-1] == '\n':
                        potential_split_points.append(match_pos)
            
            # Add the beginning and end of text
            potential_split_points = sorted(list(set(potential_split_points)))
            if 0 not in potential_split_points:
                potential_split_points.insert(0, 0)
            potential_split_points.append(len(text))
            
            # Extract entries based on split points
            entries = []
            for i in range(len(potential_split_points) - 1):
                start = potential_split_points[i]
                end = potential_split_points[i+1]
                entry = text[start:end].strip()
                if entry:
                    entries.append(entry)
        
        # If that still didn't work well, try single line breaks
        if len(entries) <= 1:
            entries = re.split(r'\n', text)
            
        # Filter out empty entries
        return [entry.strip() for entry in entries if entry.strip()]
    
    def _split_by_degree_indicators(self, text: str) -> List[str]:
        """
        Split text by detecting likely degree indicators.
        
        Args:
            text: Education section text.
            
        Returns:
            List of education entry texts.
        """
        entries = []
        split_positions = [0]
        
        # Find positions of full degree indicators that might start a new education entry
        for pattern in self.full_degree_indicators:
            for match in pattern.finditer(text):
                position = match.start()
                # Check if it's at the beginning of a line
                if position == 0 or text[position-1] in ['\n', '.', ',', ';']:
                    split_positions.append(position)
        
        # Add end of text
        split_positions.append(len(text))
        split_positions = sorted(list(set(split_positions)))
        
        # Create entries from split positions
        for i in range(len(split_positions) - 1):
            start = split_positions[i]
            end = split_positions[i+1]
            entry = text[start:end].strip()
            if entry:
                entries.append(entry)
        
        return entries
        
    def _extract_degree(self, text: str) -> Optional[str]:
        """
        Extract degree from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted degree or None.
        """
        # First look for exact matches of "Bachelor of Engineering in Computer Engineering"
        exact_match = re.search(r"Bachelor of Engineering in Computer Engineering", text)
        if exact_match:
            return exact_match.group(0)
            
        # Check for patterns in our defined list
        for pattern in self.degree_patterns:
            match = pattern.search(text)
            if match:
                # Get the matched degree
                degree = match.group(1)
                
                # Look for field of study immediately after the degree
                field_match = re.search(f"{re.escape(degree)}\\s+in\\s+([A-Za-z][A-Za-z\\s]+?)(?:,|\\.|$|\\n)", text)
                if field_match:
                    return f"{degree} in {field_match.group(1)}"
                
                return degree
        
        # If no matches were found, check for common degree keywords
        degree_keywords = [
            "Bachelor", "Master", "PhD", "Doctorate", "Associate", "Certificate", "Diploma"
        ]
        
        for keyword in degree_keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text, re.IGNORECASE):
                # Try to extract the full degree phrase
                match = re.search(r"\b" + re.escape(keyword) + r"[\w\s]+(?:,|\.|$|\n)", text, re.IGNORECASE)
                if match:
                    return match.group(0).strip().rstrip(",.;")
                return keyword
                
        return None
        
    def _extract_field_of_study(self, text: str) -> Optional[str]:
        """
        Extract field of study from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted field of study or None.
        """
        # Check if there's a degree-related keyword first
        has_degree_keyword = False
        for keyword in ["degree", "bachelor", "master", "phd", "bs", "ms", "ba", "ma", "education", "studies", "major"]:
            if keyword in text.lower():
                has_degree_keyword = True
                break
        
        if not has_degree_keyword:
            return None
            
        # Try to extract field of study
        for pattern in self.field_patterns:
            match = pattern.search(text)
            if match:
                field = match.group(1).strip()
                # Validate the field
                if self._is_valid_field(field):
                    return field
                
        # Check for common fields directly
        common_field_match = self.common_fields_pattern.search(text)
        if common_field_match:
            return common_field_match.group(0)
                
        return None
    
    def _extract_concentration(self, text: str) -> Optional[str]:
        """
        Extract concentration or specialization from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted concentration or None.
        """
        for pattern in self.concentration_patterns:
            match = pattern.search(text)
            if match:
                # Different patterns have different group arrangements
                if len(match.groups()) >= 2:
                    return match.group(2).strip()
                return match.group(1).strip()
                
        return None
        
    def _extract_institution(self, text: str) -> Optional[str]:
        """
        Extract institution name from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted institution name or None.
        """
        # Check for common universities and colleges by direct matching
        common_match = self.common_inst_regex.search(text)
        if common_match:
            return common_match.group(1)
            
        # Check for specific university names with University/College, etc.
        university_match = re.search(r"(?i)([A-Za-z\s&]+(?:University|College|Institute|School))", text)
        if university_match:
            return university_match.group(1).strip()
            
        # Check if there are common institution keywords
        institution_present = False
        for pattern in self.institution_patterns:
            if pattern.search(text):
                institution_present = True
                break
                
        if not institution_present:
            # Try lines that could contain university names
            lines = text.split("\n")
            for line in lines:
                if "university" in line.lower() or "college" in line.lower() or "institute" in line.lower():
                    # Split by common separators to isolate the institution name
                    parts = re.split(r'[|,]', line)
                    for part in parts:
                        if "university" in part.lower() or "college" in part.lower() or "institute" in part.lower():
                            return part.strip()
            
            return None
            
        # Split by common separators and check each segment
        segments = re.split(r'[,;|\n]', text)
        for segment in segments:
            clean_segment = segment.strip()
            
            # Look for segments that have institution keywords
            for pattern in self.institution_patterns:
                if pattern.search(clean_segment):
                    return clean_segment
                    
        # If no specific segment found, return first non-degree segment
        for segment in segments:
            clean_segment = segment.strip()
            
            # Skip segments that are just degree names
            is_degree = False
            for pattern in self.degree_patterns:
                if pattern.search(clean_segment):
                    is_degree = True
                    break
                    
            if not is_degree and clean_segment:
                return clean_segment
                
        return None
        
    def _extract_dates(self, text: str) -> List[str]:
        """
        Extract dates from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted dates.
        """
        # First look for date ranges in format "YYYY - YYYY"
        date_range_match = re.search(r"(\d{4})\s*-\s*(\d{4}|\s*Present|\s*Current)", text)
        if date_range_match:
            if date_range_match.group(2) and date_range_match.group(2).strip() in ["Present", "Current"]:
                return [f"{date_range_match.group(1)} - Present"]
            elif date_range_match.group(2) and date_range_match.group(2).strip().isdigit():
                return [f"{date_range_match.group(1)} - {date_range_match.group(2).strip()}"]
            else:
                return [date_range_match.group(1)]
        
        # If no date range found, look for individual dates
        dates = []
        for pattern in self.date_patterns:
            for match in pattern.finditer(text):
                date = match.group(0).strip()
                if date not in dates:
                    dates.append(date)
                    
        return dates
        
    def _extract_score(self, text: str) -> Optional[str]:
        """
        Extract GPA or score from text.
        
        Args:
            text: Education entry text.
            
        Returns:
            Extracted score or None.
        """
        # First look for more specific patterns like "GPA: 3.9/4.0"
        gpa_match = re.search(r"(?i)GPA\s*(?::|of|=)?\s*(\d+\.\d+)[/]?(?:\d+\.\d+)?", text)
        if gpa_match:
            gpa_value = gpa_match.group(1)
            return f"GPA: {gpa_value}"
        
        # Look for honors mentions
        honors_match = re.search(r"(?i)(Cum Laude|Magna Cum Laude|Summa Cum Laude|with Honors|with Distinction|with High Distinction)", text)
        if honors_match:
            return honors_match.group(1)
        
        # Check other score patterns
        for pattern in self.score_patterns:
            match = pattern.search(text)
            if match:
                # Return the entire match
                return match.group(0).strip()
                
        return None 