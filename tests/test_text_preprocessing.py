"""
Unit tests for text preprocessing functions.
"""

import unittest

from resume_parser.utils import text_preprocessing


class TestTextPreprocessing(unittest.TestCase):
    """Test text preprocessing functions."""

    def test_clean_text(self):
        """Test cleaning text."""
        # Test removing extra whitespace
        self.assertEqual(
            text_preprocessing.clean_text("  This   has  extra   spaces  "),
            "This has extra spaces"
        )
        
        # Test with newlines
        self.assertEqual(
            text_preprocessing.clean_text("Line 1\n  Line 2\n\nLine 3"),
            "Line 1 Line 2 Line 3"
        )

    def test_remove_special_chars(self):
        """Test removing special characters."""
        # Test basic removal
        self.assertEqual(
            text_preprocessing.remove_special_chars("Hello, world!"),
            "Hello world"
        )
        
        # Test keeping specified characters
        self.assertEqual(
            text_preprocessing.remove_special_chars("Hello, world!", keep_chars=",!"),
            "Hello, world!"
        )
        
        # Test with complex characters
        self.assertEqual(
            text_preprocessing.remove_special_chars("Resume: John's CV (2023) - $60K+"),
            "Resume Johns CV 2023  60K"
        )

    def test_extract_email_addresses(self):
        """Test extracting email addresses."""
        # Test basic email
        self.assertEqual(
            text_preprocessing.extract_email_addresses("Contact me at test@example.com"),
            ["test@example.com"]
        )
        
        # Test multiple emails
        self.assertEqual(
            text_preprocessing.extract_email_addresses(
                "Email: test@example.com or alternative@email.co.uk"
            ),
            ["test@example.com", "alternative@email.co.uk"]
        )
        
        # Test no emails
        self.assertEqual(
            text_preprocessing.extract_email_addresses("No email here"),
            []
        )
        
        # Test complex text
        self.assertEqual(
            text_preprocessing.extract_email_addresses(
                "Contact info:\nName: John Doe\nEmail: john.doe123@company-name.org\nPhone: 123-456-7890"
            ),
            ["john.doe123@company-name.org"]
        )

    def test_extract_phone_numbers(self):
        """Test extracting phone numbers."""
        # Test basic phone number
        self.assertEqual(
            text_preprocessing.extract_phone_numbers("Call me at 123-456-7890"),
            ["123-456-7890"]
        )
        
        # Test multiple formats
        self.assertEqual(
            sorted(text_preprocessing.extract_phone_numbers(
                "Phone: (123) 456-7890 or 987.654.3210 or +1 234 567 8901"
            )),
            sorted(["(123) 456-7890", "987.654.3210", "+1 234 567 8901"])
        )
        
        # Test no phone numbers
        self.assertEqual(
            text_preprocessing.extract_phone_numbers("No phone number here"),
            []
        )

    def test_extract_urls(self):
        """Test extracting URLs."""
        # Test basic URL
        self.assertEqual(
            text_preprocessing.extract_urls("Visit http://example.com"),
            ["http://example.com"]
        )
        
        # Test multiple URLs
        self.assertEqual(
            text_preprocessing.extract_urls(
                "Links: https://github.com/user and http://linkedin.com/in/user"
            ),
            ["https://github.com/user", "http://linkedin.com/in/user"]
        )
        
        # Test no URLs
        self.assertEqual(
            text_preprocessing.extract_urls("No URL here"),
            []
        )

    def test_split_into_sentences(self):
        """Test splitting text into sentences."""
        # Test basic splitting
        self.assertEqual(
            text_preprocessing.split_into_sentences("This is one sentence. This is another."),
            ["This is one sentence", " This is another", ""]
        )
        
        # Test with other punctuation
        self.assertEqual(
            text_preprocessing.split_into_sentences("Hello! How are you? I'm fine."),
            ["Hello", " How are you", " I'm fine", ""]
        )

    def test_normalize_whitespace(self):
        """Test normalizing whitespace."""
        # Test basic normalization
        self.assertEqual(
            text_preprocessing.normalize_whitespace("Line 1\n\nLine 2\n\n\nLine 3"),
            "Line 1\nLine 2\nLine 3"
        )
        
        # Test with spaces and tabs
        self.assertEqual(
            text_preprocessing.normalize_whitespace("  Spaces   and\t\ttabs  "),
            "Spaces and tabs"
        )

    def test_remove_urls(self):
        """Test removing URLs."""
        # Test basic removal
        self.assertEqual(
            text_preprocessing.remove_urls("Visit http://example.com for more info."),
            "Visit  for more info."
        )
        
        # Test multiple URLs
        self.assertEqual(
            text_preprocessing.remove_urls(
                "Check https://site1.com and http://site2.com for details."
            ),
            "Check  and  for details."
        )
        
        # Test no URLs
        self.assertEqual(
            text_preprocessing.remove_urls("No URL here"),
            "No URL here"
        )


if __name__ == "__main__":
    unittest.main() 