import json
import sys
from resume_parser.resume_parser import ResumeParser

def main():
    pdf_path = r"C:\Users\Asus\OneDrive\Desktop\Prajwal_Thakare_7741091975.pdf"
    parser = ResumeParser()
    
    try:
        result = parser.parse(pdf_path)
        
        # Format the output in a more readable way
        formatted_output = {
            "Personal Information": {
                "Emails": result['contact_info']['emails'],
                "Phone Numbers": result['contact_info']['phones'],
                "URLs": result['contact_info']['urls']
            },
            "Sections Found": result['sections'],
            "Education": [
                {
                    "Degree": edu.get('degree', 'Not Found'),
                    "Institution": edu.get('institution', 'Not Found'),
                    "Dates": edu.get('dates', []),
                    "Score": edu.get('score', 'Not Found')
                }
                for edu in result['education']
            ],
            "Experience": [
                {
                    "Job Title": exp.get('job_title', 'Not Found'),
                    "Company": exp.get('company', 'Not Found'),
                    "Date Range": exp.get('date_range', 'Not Found'),
                    "Responsibilities": exp.get('responsibilities', [])[:3]  # Show first 3 responsibilities
                }
                for exp in result['experience']
            ],
            "Skills": {
                "Technical Skills": {k: v for k, v in result['skills'].get('technical', {}).items()},
                "Soft Skills": result['skills'].get('soft', []),
                "Other Skills": result['skills'].get('other', [])
            },
            "Projects": [
                {
                    "Name": proj.get('name', 'Not Found'),
                    "Date": proj.get('date_range', 'Not Found'),
                    "Technologies": proj.get('technologies', []),
                    "Description": proj.get('description', [])[:2]  # Show first 2 description points
                }
                for proj in result['projects']
            ],
            "Certifications": [
                {
                    "Name": cert.get('name', 'Not Found'),
                    "Issuer": cert.get('issuer', 'Not Found'),
                    "Date": cert.get('date', 'Not Found')
                }
                for cert in result['certifications']
            ]
        }
        
        print(json.dumps(formatted_output, indent=4))
    except Exception as e:
        print(f"Error parsing resume: {e}")

if __name__ == "__main__":
    main() 