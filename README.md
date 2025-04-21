# Resume Parser

A web-based application that extracts and analyzes information from resumes in various formats (PDF, DOCX, TXT) using natural language processing and machine learning techniques.

## Features

- **Multi-format Support**: Parse resumes in PDF, DOCX, DOC, and TXT formats
- **Comprehensive Extraction**: Extract key information including:
  - Contact details (name, email, phone, LinkedIn)
  - Education history
  - Work experience
  - Skills (technical and soft skills)
  - Projects
  - Certifications
- **User-friendly Interface**: Clean Bootstrap-based UI for easy uploading and viewing results
- **Advanced Text Processing**: Uses NLP techniques for accurate information extraction

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Libraries**:
  - PyPDF2/pypdf for PDF extraction
  - Custom extractors for different document formats
  - Regular expressions for pattern matching
  - NLP techniques for text processing

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Prajwalthakare02/Resume-Parser.git
   cd Resume-Parser
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Upload a resume file (PDF, DOCX, DOC, or TXT format)
2. Click "Parse Resume"
3. View the extracted information organized in sections

## Project Structure

- `app.py`: Main Flask application
- `src/resume_parser/`: Core parsing functionality
  - `resume_parser.py`: Main parser implementation
  - `extractors/`: Specialized extractors for different content types
  - `utils/`: Utility functions and helpers
- `templates/`: HTML templates for the web interface
- `static/`: Static assets (CSS, JS, images)
- `uploads/`: Temporary storage for uploaded files (auto-cleaned)
- `tests/`: Unit and integration tests

## Future Enhancements

- Adding more document format support
- Implementing machine learning for improved accuracy
- Adding resume scoring and recommendation features
- Support for multiple languages
- Batch processing of multiple resumes

## License

MIT License

## Author

Prajwal Thakare
