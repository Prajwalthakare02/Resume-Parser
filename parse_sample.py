import os
import tempfile
import json
from resume_parser.resume_parser import ResumeParser

def generate_sample_resume():
    """Generate a sample resume text."""
    return """
John Doe
123 Main Street, New York, NY 10001
Email: john.doe@example.com
Phone: (555) 123-4567
LinkedIn: https://linkedin.com/in/johndoe

EDUCATION
Bachelor of Science in Computer Science
New York University, New York, NY
2016 - 2020
GPA: 3.8/4.0

EXPERIENCE
Software Engineer
ABC Tech, San Francisco, CA
June 2020 - Present
• Developed and maintained RESTful APIs using Python and Django
• Implemented CI/CD pipelines using Jenkins and Docker
• Collaborated with cross-functional teams to design and implement new features

Junior Developer
XYZ Solutions, New York, NY
January 2019 - May 2020
• Assisted in developing front-end components using React
• Participated in code reviews and agile development processes
• Fixed bugs and implemented minor features

SKILLS
Programming Languages: Python, JavaScript, Java, C++
Web Technologies: HTML, CSS, React, Django, Flask
Databases: PostgreSQL, MongoDB
Tools: Git, Docker, Jenkins, AWS

PROJECTS
Personal Website
2020
• Designed and developed a personal portfolio website using React
• Implemented responsive design and dark mode
• Deployed using Netlify

Inventory Management System
2019
• Created a full-stack application for inventory management
• Used Django for backend and React for frontend
• Implemented authentication and authorization

CERTIFICATIONS
AWS Certified Developer - Associate
Amazon Web Services
2021
"""

def main():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(generate_sample_resume())
        temp_file = f.name
    
    try:
        # Parse the sample resume
        parser = ResumeParser()
        result = parser.parse(temp_file)
        
        # Print the results
        print(json.dumps(result, indent=2))
        
        # Check basic structure
        print("\nBasic structure check:")
        for key in ['file_info', 'raw_text', 'preprocessed_text', 'contact_info', 
                   'education', 'experience', 'skills', 'projects', 'certifications']:
            print(f"'{key}' present: {key in result}")
            
        # Check specific content
        if 'education' in result and result['education']:
            edu = result['education'][0]
            print(f"\nEducation degree: {edu.get('degree', 'Not found')}")
            print(f"Education institution: {edu.get('institution', 'Not found')}")
            
        if 'experience' in result and result['experience']:
            exp = result['experience'][0]
            print(f"\nJob title: {exp.get('job_title', 'Not found')}")
            print(f"Company: {exp.get('company', 'Not found')}")
            
        if 'skills' in result:
            skills = result['skills']
            print(f"\nNumber of skills: {len(skills.get('all', []))}")
            
    finally:
        # Clean up the temporary file
        os.unlink(temp_file)

if __name__ == "__main__":
    main() 