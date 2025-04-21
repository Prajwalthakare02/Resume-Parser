from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from src.resume_parser.resume_parser import ResumeParser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc', 'txt'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_resume():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Parse the resume
            parser = ResumeParser()
            parsed_data = parser.parse(filepath)
            
            # Debug: Print the structure of parsed_data
            print("\nParsed data structure:", parsed_data.keys())
            print("\nContact info:", parsed_data.get('contact_info', {}))
            print("\nRaw text sample:", parsed_data.get('raw_text', '')[:200] + "...")
            print("\nSkills data:", parsed_data.get('skills', {}))
            print("\nExperience data:", parsed_data.get('experience', []))
            
            # Get raw text for further processing
            raw_text = parsed_data.get('raw_text', '')
            
            # Extract name from raw text
            name = extract_name(raw_text)
            
            # Extract or supplement contact information from raw text
            contact_info = parsed_data.get('contact_info', {})
            emails = contact_info.get('emails', [])
            phones = contact_info.get('phones', [])
            urls = contact_info.get('urls', [])
            
            # If contact info is missing, try direct extraction from raw text
            if not emails and not phones and not urls:
                # Extract using regex
                import re
                # Email extraction
                email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
                emails.extend([email for email in email_matches if email not in emails])
                
                # Phone extraction
                phone_matches = re.findall(r'(\+\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', raw_text)
                for phone_match in phone_matches:
                    full_phone = ''.join(phone_match).strip()
                    if full_phone and full_phone not in phones:
                        phones.append(full_phone)
                
                # URL extraction
                url_matches = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw_text)
                urls.extend([url for url in url_matches if url not in urls])
                
                # LinkedIn URL extraction
                linkedin_matches = re.findall(r'linkedin\.com/\w+/[\w-]+', raw_text)
                for match in linkedin_matches:
                    linkedin_url = f"https://{match}" if not match.startswith('http') else match
                    if linkedin_url not in urls:
                        urls.append(linkedin_url)
            
            # Extract skills from both skills data and raw text
            skills_data = parsed_data.get('skills', {})
            # Add raw text to skills_data for fallback extraction
            if isinstance(skills_data, dict):
                skills_data['raw_text'] = raw_text
            
            # Transform data to match front-end expectations
            transformed_data = {
                # Basic information
                'name': name,
                'summary': extract_summary(raw_text),
                
                # Contact information
                'email': emails,
                'phone': phones,
                'linkedin': extract_linkedin(urls),
                'websites': [url for url in urls if 'linkedin.com' not in url.lower()],
                
                # Education
                'education': transform_education(parsed_data.get('education', [])),
                
                # Experience
                'experience': transform_experience(parsed_data.get('experience', [])),
                
                # Skills
                'skills': extract_skills(skills_data),
                
                # Projects
                'projects': transform_projects(parsed_data.get('projects', [])),
                
                # Certifications
                'certifications': transform_certifications(parsed_data.get('certifications', []))
            }
            
            # Clean up the file
            os.remove(filepath)
            
            # Debug: Print the transformed data
            print("\nTransformed data:")
            print(f"Name: {transformed_data['name']}")
            print(f"Contact: {transformed_data['email']}, {transformed_data['phone']}")
            print(f"Skills: {transformed_data['skills']}")
            print(f"Experience: {[{k:v for k,v in exp.items() if v} for exp in transformed_data['experience']]}")
            
            return jsonify(transformed_data)
        except Exception as e:
            # Clean up the file
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"\nException during parsing: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

def extract_name(text):
    """Extract name from resume text (better extraction logic)"""
    if not text:
        return None
    
    lines = text.strip().split('\n')
    if not lines:
        return None
        
    # Try common name patterns at the top of resume
    import re
    
    # Look for a typical name pattern in the first 5 lines
    for i in range(min(5, len(lines))):
        line = lines[i].strip()
        
        # Skip empty lines and lines that are too long or too short
        if not line or len(line) > 50 or len(line) < 3:
            continue
            
        # Skip lines that look like headers, titles or contact info
        if re.search(r'^(EDUCATION|EXPERIENCE|SKILLS|PROJECTS|CERTIFICATIONS|SUMMARY|PROFILE|OBJECTIVE)', 
                    line, re.IGNORECASE):
            continue
            
        # Skip lines that contain typical non-name content
        if re.search(r'@|www\.|http|\.com|\.net|\.org|[0-9]{3}[-\s][0-9]{3}[-\s][0-9]{4}', line):
            continue
            
        # If line contains 1-4 words, it might be a name
        words = line.split()
        if 1 <= len(words) <= 4:
            # Check if any word looks like a typical name (capital first letter, rest lowercase)
            if any(re.match(r'^[A-Z][a-z]+$', word) for word in words):
                return line
    
    # If no name found with the above logic, try using the first non-empty line
    for line in lines:
        if line.strip():
            return line.strip()
            
    return None

def extract_summary(text):
    """Extract summary section from resume"""
    # Look for summary/objective sections
    import re
    summary_match = re.search(r'(?i)(SUMMARY|PROFILE|OBJECTIVE)\s*:?\s*(.*?)(?=\n\s*[A-Z]{2,}|\Z)', 
                             text, re.DOTALL)
    if summary_match:
        return summary_match.group(2).strip()
    return None

def extract_linkedin(urls):
    """Extract LinkedIn URL if present"""
    for url in urls:
        if 'linkedin.com' in url.lower():
            return url
    return None

def transform_education(education_list):
    """Transform education data to front-end format"""
    result = []
    for edu in education_list:
        entry = {
            'degree': edu.get('degree'),
            'institution': edu.get('institution'),
            'date': edu.get('date_range'),
            'gpa': edu.get('gpa')
        }
        result.append(entry)
    return result

def transform_experience(experience_list):
    """Transform experience data to front-end format"""
    print(f"\nExperience list type: {type(experience_list)}")
    print(f"Experience list content: {experience_list}")
    
    result = []
    for exp in experience_list:
        print(f"Experience entry: {exp}")
        # Handle different possible key names for job title
        job_title = None
        if 'job_title' in exp:
            job_title = exp['job_title']
        elif 'title' in exp:
            job_title = exp['title']
        elif 'position' in exp:
            job_title = exp['position']
        
        # Handle different possible key names for company
        company = None
        if 'company' in exp:
            company = exp['company']
        elif 'employer' in exp:
            company = exp['employer']
        elif 'organization' in exp:
            company = exp['organization']
        
        # Handle different possible key names for date
        date = None
        if 'date_range' in exp:
            date = exp['date_range']
        elif 'date' in exp:
            date = exp['date']
        elif 'duration' in exp:
            date = exp['duration']
        
        # Join responsibilities into a description
        description = None
        if 'responsibilities' in exp and exp['responsibilities']:
            if isinstance(exp['responsibilities'], list):
                description = '\n'.join(['• ' + item for item in exp['responsibilities']])
            elif isinstance(exp['responsibilities'], str):
                description = exp['responsibilities']
        elif 'description' in exp:
            if isinstance(exp['description'], list):
                description = '\n'.join(['• ' + item for item in exp['description']])
            elif isinstance(exp['description'], str):
                description = exp['description']
        
        # If we have at least a company or job title, add the entry
        if job_title or company:
            entry = {
                'title': job_title,
                'company': company,
                'date': date,
                'description': description
            }
            result.append(entry)
    
    return result

def extract_skills(skills_data):
    """Extract skills in a flat list"""
    # For debugging, return the skills data structure
    print(f"\nSkills data type: {type(skills_data)}")
    import re
    
    # If skills is a pure string, try to extract skills from it
    if isinstance(skills_data, str):
        if not skills_data.strip():
            return []
        # Split by commas or newlines
        skills = re.split(r'[,\n]', skills_data)
        return [skill.strip() for skill in skills if skill.strip()]
    
    # If skills has 'all' field as a list, use it
    if isinstance(skills_data, dict) and 'all' in skills_data and isinstance(skills_data['all'], list) and skills_data['all']:
        return skills_data['all']
    
    # If skills has 'all' field but it's a string, split it
    if isinstance(skills_data, dict) and 'all' in skills_data and isinstance(skills_data['all'], str) and skills_data['all']:
        skills = re.split(r'[,\n]', skills_data['all'])
        return [skill.strip() for skill in skills if skill.strip()]
    
    # If skills has technical categories, flatten them
    all_skills = []
    if isinstance(skills_data, dict) and 'technical' in skills_data:
        tech_skills = skills_data.get('technical', {})
        for category_name, category in tech_skills.items():
            if isinstance(category, list):
                all_skills.extend(category)
            elif isinstance(category, str):
                skills = re.split(r'[,\n]', category)
                all_skills.extend([skill.strip() for skill in skills if skill.strip()])
    
    # Add any soft skills
    soft_skills = skills_data.get('soft_skills', []) if isinstance(skills_data, dict) else []
    if isinstance(soft_skills, list):
        all_skills.extend(soft_skills)
    elif isinstance(soft_skills, str) and soft_skills.strip():
        skills = re.split(r'[,\n]', soft_skills)
        all_skills.extend([skill.strip() for skill in skills if skill.strip()])
    
    # Add tools if present
    tools = skills_data.get('tools_software', []) if isinstance(skills_data, dict) else []
    if isinstance(tools, list):
        all_skills.extend(tools)
    elif isinstance(tools, str) and tools.strip():
        skills = re.split(r'[,\n]', tools)
        all_skills.extend([skill.strip() for skill in skills if skill.strip()])
    
    # If we couldn't find any skills using the above methods, try direct extraction from raw text
    if not all_skills and 'raw_text' in skills_data:
        extracted_skills = extract_skills_from_raw_text(skills_data['raw_text'])
        all_skills.extend(extracted_skills)
    
    # Deduplicate and sort
    unique_skills = list(set([skill for skill in all_skills if skill]))
    return sorted(unique_skills)

def extract_skills_from_raw_text(text):
    """Extract skills directly from raw text"""
    if not text:
        return []
        
    import re
    skills = []
    
    # Common programming languages and technologies
    common_tech_skills = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Go', 'Rust',
        'HTML', 'CSS', 'SASS', 'LESS', 'Bootstrap', 'Tailwind', 
        'React', 'Angular', 'Vue', 'Next.js', 'Svelte', 'jQuery',
        'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'ASP.NET',
        'PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Redis', 'Oracle', 'SQL Server', 'Firebase',
        'Git', 'GitHub', 'GitLab', 'BitBucket', 
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Heroku', 'Vercel', 'Netlify',
        'Jenkins', 'GitHub Actions', 'CircleCI', 'Travis CI', 'CI/CD',
        'REST API', 'GraphQL', 'WebSockets', 'gRPC',
        'Agile', 'Scrum', 'Kanban', 'JIRA', 'Confluence', 'Trello',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'NumPy', 'Pandas',
        'Kubernetes', 'Terraform', 'Ansible', 'Chef', 'Puppet',
        'Linux', 'Unix', 'Windows', 'macOS',
        'Microservices', 'Serverless', 'Event-driven'
    ]
    
    # Try to find skills section
    skills_section = re.search(r'(?i)SKILLS\s*:?\s*(.*?)(?=\n\s*[A-Z]{2,}|\Z)', text, re.DOTALL)
    if skills_section:
        skills_text = skills_section.group(1).strip()
        # Split by common delimiters
        skill_items = re.split(r'[,•|\n]', skills_text)
        for item in skill_items:
            item = item.strip()
            if item and len(item) < 30:  # Reasonable length for a skill
                skills.append(item)
    
    # Also look for common tech skills throughout the text
    for skill in common_tech_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            # Use the proper casing from our list
            skills.append(skill)
    
    return skills

def transform_projects(projects_list):
    """Transform projects data to front-end format"""
    result = []
    for proj in projects_list:
        # Join description items if present
        description = None
        if proj.get('description'):
            if isinstance(proj['description'], list):
                description = ','.join(proj['description'])
            else:
                description = proj['description']
        
        entry = {
            'name': proj.get('name'),
            'date': proj.get('date'),
            'description': description
        }
        result.append(entry)
    return result

def transform_certifications(certifications_list):
    """Transform certifications data to front-end format"""
    result = []
    for cert in certifications_list:
        entry = {
            'name': cert.get('name'),
            'issuer': cert.get('issuer'),
            'date': cert.get('date')
        }
        result.append(entry)
    return result

if __name__ == '__main__':
    app.run(debug=True) 