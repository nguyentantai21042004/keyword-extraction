"""
Tests for keyword extraction algorithms
"""

import unittest
import asyncio
from src.core.extractors import SpacyYakeExtractor

class TestExtractors(unittest.TestCase):
    """Test cases for extractor classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_text = "Machine learning algorithms for natural language processing applications in social media sentiment analysis."
        self.expected_keywords = ['machine learning', 'algorithms', 'natural language processing', 'social media', 'sentiment analysis']
    
    def test_spacy_yake_extractor_initialization(self):
        """Test SpacyYakeExtractor initialization"""
        extractor = SpacyYakeExtractor()
        self.assertEqual(extractor.method_name, "spacy_yake")
    
    async def test_extraction_async(self):
        """Test async extraction methods"""
        extractor = SpacyYakeExtractor()
        try:
            result = await extractor.extract(self.test_text)
            self.assertIsNotNone(result)
            self.assertIsInstance(result.keywords, list)
            self.assertTrue(result.success)
        except Exception as e:
            self.fail(f"Extractor {extractor.method_name} failed: {e}")

if __name__ == '__main__':
    unittest.main()
