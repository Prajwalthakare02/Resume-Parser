"""
Alternative test for the ResumeParser class with different data.
"""

import os
import tempfile
import unittest

from resume_parser.resume_parser import ResumeParser


class TestResumeParserAlt(unittest.TestCase):
    """Test the ResumeParser class with different data."""

    def setUp(self):
        """Set up test files."""
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.temp_dir.name
        
        # Create a sample resume in text format with different format
        self.sample_resume_txt = os.path.join(self.temp_path, "alt_resume.txt")
        with open(self.sample_resume_txt, "w") as f:
            f.write(self._generate_alt_resume())
        
        # Initialize the resume parser
        self.parser = ResumeParser()

    def tearDown(self):
        """Clean up test files."""
        self.temp_dir.cleanup()

    def _generate_alt_resume(self):
        """Generate an alternative sample resume text."""
        return """
JANE SMITH
------------------
jane.smith@domain.com | (123) 456-7890 | Los Angeles, CA 90001
www.janesmith.com | linkedin.com/in/janesmith

PROFESSIONAL SUMMARY
------------------
Senior Data Scientist with 8+ years of experience implementing machine learning solutions for enterprise clients. 
Expertise in NLP, computer vision, and predictive analytics. Strong communicator adept at translating 
complex technical concepts for non-technical stakeholders.

SKILLS
------------------
• Programming: Python, R, SQL, JavaScript
• ML Frameworks: TensorFlow, PyTorch, scikit-learn, Keras
• Big Data: Spark, Hadoop, Kafka, AWS EMR
• Cloud: AWS (Certified Solutions Architect), GCP, Azure
• Data Visualization: Tableau, PowerBI, D3.js

EXPERIENCE
------------------
Lead Data Scientist
DataCorp Analytics, Inc. | Los Angeles, CA
05/2019 - Present

* Architected and deployed production ML systems that increased client revenue by 27%
* Led team of 5 data scientists in developing NLP solutions for customer service automation
* Created anomaly detection algorithms that reduced fraud by 35% for financial clients
* Improved model training time by 45% through infrastructure optimization

Data Scientist
TechStart Solutions | San Francisco, CA
06/2015 - 04/2019

* Developed predictive models for customer churn that improved retention by 18%
* Built recommendation systems increasing average order value by 24%
* Created internal dashboard tools for non-technical teams to leverage ML insights
* Collaborated with product teams to define data strategy and KPIs

Junior Data Analyst
Insight Data Systems | Portland, OR
01/2013 - 05/2015

* Performed exploratory data analysis and built visualization dashboards
* Assisted senior team members with ETL processes and data cleaning
* Developed automated reporting systems for executive stakeholders

EDUCATION
------------------
M.S. in Computer Science, Machine Learning Concentration
Stanford University | 2012 - 2014
GPA: 3.9/4.0

B.S. in Statistics
University of Washington | 2008 - 2012
GPA: 3.8/4.0, Magna Cum Laude

CERTIFICATIONS
------------------
• AWS Certified Solutions Architect - Professional (2021)
• Google Cloud Professional Data Engineer (2020)
• TensorFlow Developer Certificate (2019)
"""

    def test_parse_text_resume_alt(self):
        """Test parsing an alternative format text resume."""
        # Parse the sample resume
        result = self.parser.parse(self.sample_resume_txt)
        
        # Check basic structure
        self.assertIn('file_info', result)
        self.assertIn('raw_text', result)
        self.assertIn('preprocessed_text', result)
        self.assertIn('contact_info', result)
        self.assertIn('education', result)
        self.assertIn('experience', result)
        self.assertIn('skills', result)
        
        # Check contact information
        contact_info = result['contact_info']
        self.assertIn('jane.smith@domain.com', contact_info['emails'])
        self.assertIn('(123) 456-7890', contact_info['phones'])
        self.assertIn('www.janesmith.com', contact_info['urls'])
        self.assertIn('linkedin.com/in/janesmith', contact_info['urls'])
        
        # Check education
        self.assertTrue(len(result['education']) > 0)
        edu = result['education'][0]
        self.assertIn('Computer Science', edu.get('degree', ''))
        self.assertIn('Stanford University', edu.get('institution', ''))
        
        # Check experience
        self.assertTrue(len(result['experience']) > 0)
        exp = result['experience'][0]
        self.assertIn('Data Scientist', exp.get('job_title', ''))
        self.assertIn('DataCorp Analytics', exp.get('company', ''))
        
        # Check skills
        skills = result['skills']
        self.assertTrue(len(skills.get('all', [])) > 0)


if __name__ == "__main__":
    unittest.main() 