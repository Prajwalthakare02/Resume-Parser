"""
Unit tests for file utilities.
"""

import os
import tempfile
import unittest

from resume_parser.utils import file_utils


class TestFileUtils(unittest.TestCase):
    """Test file utilities."""

    def setUp(self):
        """Set up test files."""
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.temp_dir.name
        
        # Create test files
        self.pdf_file = os.path.join(self.temp_path, "test.pdf")
        self.docx_file = os.path.join(self.temp_path, "test.docx")
        self.txt_file = os.path.join(self.temp_path, "test.txt")
        self.jpg_file = os.path.join(self.temp_path, "test.jpg")
        self.unknown_file = os.path.join(self.temp_path, "test.xyz")
        
        # Create empty files
        for file_path in [self.pdf_file, self.docx_file, self.txt_file, self.jpg_file, self.unknown_file]:
            with open(file_path, "w") as f:
                f.write("test")

    def tearDown(self):
        """Clean up test files."""
        self.temp_dir.cleanup()

    def test_get_file_extension(self):
        """Test getting file extension."""
        self.assertEqual(file_utils.get_file_extension(self.pdf_file), "pdf")
        self.assertEqual(file_utils.get_file_extension(self.docx_file), "docx")
        self.assertEqual(file_utils.get_file_extension(self.txt_file), "txt")
        self.assertEqual(file_utils.get_file_extension(self.jpg_file), "jpg")
        self.assertEqual(file_utils.get_file_extension("file.PDF"), "pdf")  # Test case sensitivity
        self.assertEqual(file_utils.get_file_extension("file"), "")  # Test file without extension

    def test_is_supported_file(self):
        """Test checking if a file is supported."""
        self.assertTrue(file_utils.is_supported_file(self.pdf_file))
        self.assertTrue(file_utils.is_supported_file(self.docx_file))
        self.assertTrue(file_utils.is_supported_file(self.txt_file))
        self.assertTrue(file_utils.is_supported_file(self.jpg_file))
        self.assertFalse(file_utils.is_supported_file(self.unknown_file))
        
        # Test with custom supported extensions
        self.assertTrue(file_utils.is_supported_file(self.pdf_file, ["pdf"]))
        self.assertFalse(file_utils.is_supported_file(self.docx_file, ["pdf"]))

    def test_get_file_info(self):
        """Test getting file information."""
        info = file_utils.get_file_info(self.pdf_file)
        self.assertEqual(info["name"], "test.pdf")
        self.assertEqual(info["extension"], "pdf")
        self.assertTrue(info["is_file"])
        self.assertFalse(info["is_dir"])
        self.assertGreater(info["size_bytes"], 0)

    def test_is_file_type(self):
        """Test file type checking functions."""
        self.assertTrue(file_utils.is_pdf_file(self.pdf_file))
        self.assertFalse(file_utils.is_pdf_file(self.docx_file))
        
        self.assertTrue(file_utils.is_docx_file(self.docx_file))
        self.assertFalse(file_utils.is_docx_file(self.pdf_file))
        
        self.assertTrue(file_utils.is_text_file(self.txt_file))
        self.assertFalse(file_utils.is_text_file(self.pdf_file))
        
        self.assertTrue(file_utils.is_image_file(self.jpg_file))
        self.assertFalse(file_utils.is_image_file(self.pdf_file))

    def test_list_files_by_extension(self):
        """Test listing files by extension."""
        # Create additional PDF files
        pdf_file2 = os.path.join(self.temp_path, "test2.pdf")
        with open(pdf_file2, "w") as f:
            f.write("test")
        
        pdf_files = file_utils.list_files_by_extension(self.temp_path, "pdf")
        self.assertEqual(len(pdf_files), 2)
        self.assertTrue(self.pdf_file in pdf_files or os.path.abspath(self.pdf_file) in pdf_files)
        
        # Test with non-existent extension
        xyz_files = file_utils.list_files_by_extension(self.temp_path, "xyz")
        self.assertEqual(len(xyz_files), 1)


if __name__ == "__main__":
    unittest.main() 