"""
Setup file for the resume parser.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resume-parser",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to extract information from resumes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resume-parser",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=2.11.1",
        "python-docx>=0.8.11",
        "pytesseract>=0.3.9",
        "Pillow>=9.0.0",
        "spacy>=3.5.0",
        "nltk>=3.8",
    ],
    entry_points={
        "console_scripts": [
            "resume-parser=resume_parser.cli:main",
        ],
    },
) 