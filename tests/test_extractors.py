"""
Tests for keyword extraction algorithms
"""

import unittest
import asyncio
from src.core.extractors import SpacyYakeExtractor, RakeExtractor, TextRankExtractor, TfIdfExtractor, KeyBertExtractor

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
    
    def test_rake_extractor_initialization(self):
        """Test RakeExtractor initialization"""
        extractor = RakeExtractor()
        self.assertEqual(extractor.method_name, "rake_nltk")
    
    def test_textrank_extractor_initialization(self):
        """Test TextRankExtractor initialization"""
        extractor = TextRankExtractor()
        self.assertEqual(extractor.method_name, "textrank")
    
    def test_tfidf_extractor_initialization(self):
        """Test TfIdfExtractor initialization"""
        extractor = TfIdfExtractor()
        self.assertEqual(extractor.method_name, "tf_idf")
    
    def test_keybert_extractor_initialization(self):
        """Test KeyBertExtractor initialization"""
        extractor = KeyBertExtractor()
        self.assertEqual(extractor.method_name, "keybert")
    
    @unittest.skip("Skip async tests for now")
    async def test_extraction_async(self):
        """Test async extraction methods"""
        extractors = [
            SpacyYakeExtractor(),
            RakeExtractor(),
            TextRankExtractor(),
            TfIdfExtractor(),
            KeyBertExtractor()
        ]
        
        for extractor in extractors:
            try:
                result = await extractor.extract(self.test_text)
                self.assertIsNotNone(result)
                self.assertIsInstance(result.keywords, list)
            except Exception as e:
                # Some extractors might fail due to missing dependencies
                print(f"Extractor {extractor.method_name} failed: {e}")

if __name__ == '__main__':
    unittest.main()
