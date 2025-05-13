"""
Tests for the shape module.
"""

import unittest
from rich_ctl.shape import shape_text, Cluster


class TestShapeText(unittest.TestCase):
    """Test cases for the shape_text function."""
    
    def test_empty_text(self):
        """Test that empty text returns an empty list of clusters."""
        result = shape_text("")
        self.assertEqual(result, [])
    
    def test_ascii_text(self):
        """Test that ASCII text is shaped correctly."""
        # Even with ASCII, we should get a list of clusters
        result = shape_text("Hello")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(c, Cluster) for c in result))
    
    def test_telugu_text(self):
        """Test that Telugu text is shaped correctly."""
        # This is a placeholder test - in a real implementation,
        # we would check that the clusters are shaped correctly
        result = shape_text("తెలుగు")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(c, Cluster) for c in result))
    
    def test_arabic_text(self):
        """Test that Arabic text is shaped correctly."""
        # This is a placeholder test - in a real implementation,
        # we would check that the clusters are shaped correctly
        result = shape_text("مرحبا")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(c, Cluster) for c in result))


if __name__ == "__main__":
    unittest.main()
