"""
Command-line interface for the resume parser.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional

from resume_parser.resume_parser import ResumeParser


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Resume Parser - Extract information from resumes"
    )
    
    parser.add_argument(
        "file",
        help="Path to the resume file (PDF, DOCX, TXT, JPG, JPEG, PNG)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file for the extracted information (JSON format)",
        type=str
    )
    
    parser.add_argument(
        "--metadata-only",
        "-m",
        help="Extract only metadata without parsing the content",
        action="store_true"
    )
    
    parser.add_argument(
        "--pretty",
        "-p",
        help="Pretty print the JSON output",
        action="store_true"
    )
    
    parser.add_argument(
        "--tesseract-cmd",
        help="Path to the Tesseract executable (for OCR)",
        type=str
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    try:
        # Initialize resume parser
        parser = ResumeParser(tesseract_cmd=args.tesseract_cmd)
        
        # Parse resume or extract metadata
        if args.metadata_only:
            result = parser.extract_metadata(args.file)
        else:
            result = parser.parse(args.file)
        
        # Determine output format
        json_kwargs = {"indent": 4} if args.pretty else {}
        
        # Output the result
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, **json_kwargs)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, **json_kwargs))
        
        return 0
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 