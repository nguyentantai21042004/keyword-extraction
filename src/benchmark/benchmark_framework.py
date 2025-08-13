"""
Enhanced comprehensive benchmarking and comparison framework
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from ..core import (
    ExtractionMethod, SpacyYakeExtractor, RakeExtractor, 
    TextRankExtractor, TfIdfExtractor, KeyBertExtractor
)
from ..core.ensemble import HybridEnsembleExtractor
import time
import psutil
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExtractionBenchmark:
    """Enhanced comprehensive benchmarking and comparison framework"""
    
    def __init__(self):
        self.extractors = {
            ExtractionMethod.SPACY_YAKE: SpacyYakeExtractor(),
            ExtractionMethod.RAKE_NLTK: RakeExtractor(),
            ExtractionMethod.TEXTRANK: TextRankExtractor(),
            ExtractionMethod.TF_IDF: TfIdfExtractor(),
            ExtractionMethod.KEYBERT: KeyBertExtractor(),
            ExtractionMethod.HYBRID_ENSEMBLE: HybridEnsembleExtractor()
        }
        
        self.test_cases = []
        self.results = []
        self.performance_metrics = {}
        
        # Enhanced configuration
        self.config = {
            'max_timeout': 30,  # seconds
            'memory_monitoring': True,
            'accuracy_threshold': 0.1,  # Minimum accuracy to consider
            'confidence_threshold': 0.3,  # Minimum confidence to consider
            'enable_vietnamese_support': True,
            'multilingual_processing': True
        }
    
    def add_test_case(self, text: str, expected_keywords: List[str] = None, category: str = "general", 
                      language: str = "en", complexity: str = "medium"):
        """Add test case for benchmarking with enhanced metadata"""
        
        # Detect language if not specified
        if language == "auto":
            language = self._detect_language(text)
        
        test_case = {
            'text': text,
            'expected_keywords': expected_keywords or [],
            'category': category,
            'language': language,
            'complexity': complexity,
            'text_length': len(text),
            'word_count': len(text.split()),
            'has_social_elements': '#' in text or '@' in text,
            'has_emojis': any(ord(char) > 127 for char in text),
            'has_special_chars': any(not char.isalnum() and not char.isspace() for char in text)
        }
        
        self.test_cases.append(test_case)
        logger.info(f"Added test case: {category} ({language}) - {len(text)} chars")
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on character patterns"""
        
        # Count Vietnamese characters
        vietnamese_chars = sum(1 for char in text if char in 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ')
        
        # Count English characters
        english_chars = sum(1 for char in text if char.isascii() and char.isalpha())
        
        if vietnamese_chars > 0:
            return "vi"
        elif english_chars > len(text) * 0.7:
            return "en"
        else:
            return "mixed"
    
    async def run_comprehensive_benchmark(self) -> pd.DataFrame:
        """Run all methods on all test cases with enhanced monitoring"""
        
        logger.info(f"Starting comprehensive benchmark with {len(self.test_cases)} test cases")
        
        all_results = []
        
        for test_case in self.test_cases:
            logger.info(f"Processing test case: {test_case['id'] if 'id' in test_case else test_case['category']}")
            
            for method_name, extractor in self.extractors.items():
                try:
                    # Run extraction with timeout and monitoring
                    result = await self._run_extraction_with_monitoring(
                        extractor, test_case, method_name
                    )
                    
                    if result:
                        all_results.append(result)
                        
                except Exception as e:
                    logger.error(f"Error in {method_name}: {e}")
                    continue
        
        # Convert to DataFrame
        results_df = pd.DataFrame(all_results)
        
        # Calculate additional metrics
        if not results_df.empty:
            results_df = self._calculate_enhanced_metrics(results_df)
        
        logger.info(f"Benchmark completed. Total results: {len(results_df)}")
        return results_df
    
    async def _run_extraction_with_monitoring(self, extractor, test_case: Dict, method_name: str) -> Dict:
        """Run extraction with comprehensive monitoring"""
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Run extraction with timeout
            extraction_result = await asyncio.wait_for(
                extractor.extract(test_case['text']), 
                timeout=self.config['max_timeout']
            )
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Calculate metrics
            processing_time = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Calculate accuracy
            accuracy = self._calculate_accuracy(
                extraction_result.keywords, 
                test_case['expected_keywords']
            )
            
            # Create result record
            result = {
                'method': method_name.value if hasattr(method_name, 'value') else str(method_name),
                'text_id': test_case.get('id', f"{test_case['category']}_{test_case['language']}"),
                'category': test_case['category'],
                'language': test_case['language'],
                'complexity': test_case['complexity'],
                'text_length': test_case['text_length'],
                'word_count': test_case['word_count'],
                'extracted_keywords': [kw['keyword'] for kw in extraction_result.keywords],
                'expected_keywords': test_case['expected_keywords'],
                'accuracy': accuracy,
                'confidence_score': extraction_result.confidence_score,
                'processing_time': processing_time,
                'memory_usage': memory_usage,
                'keywords_count': len(extraction_result.keywords),
                'success': accuracy > self.config['accuracy_threshold'],
                'metadata': extraction_result.metadata
            }
            
            return result
            
        except asyncio.TimeoutError:
            logger.warning(f"Timeout for {method_name} on test case {test_case['category']}")
            return None
        except Exception as e:
            logger.error(f"Error in {method_name}: {e}")
            return None
    
    def _calculate_accuracy(self, extracted_keywords: List[Dict], expected_keywords: List[str]) -> float:
        """Calculate accuracy using multiple metrics"""
        
        if not expected_keywords:
            return 0.0
        
        extracted_texts = [kw['keyword'].lower() for kw in extracted_keywords]
        expected_lower = [kw.lower() for kw in expected_keywords]
        
        # Exact match
        exact_matches = sum(1 for kw in extracted_texts if kw in expected_lower)
        exact_accuracy = exact_matches / len(expected_keywords)
        
        # Partial match (substring)
        partial_matches = 0
        for expected in expected_lower:
            for extracted in extracted_texts:
                if expected in extracted or extracted in expected:
                    partial_matches += 1
                    break
        
        partial_accuracy = partial_matches / len(expected_keywords)
        
        # Combined accuracy (weighted)
        combined_accuracy = 0.7 * exact_accuracy + 0.3 * partial_accuracy
        
        return combined_accuracy
    
    def _calculate_enhanced_metrics(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate additional performance metrics"""
        
        # Method performance summary
        method_summary = results_df.groupby('method').agg({
            'accuracy': ['mean', 'std'],
            'processing_time': ['mean', 'std'],
            'memory_usage': ['mean', 'std'],
            'confidence_score': ['mean', 'std'],
            'success': 'mean'
        }).round(4)
        
        # Category performance
        category_performance = results_df.groupby('category').agg({
            'accuracy': 'mean',
            'success': 'mean'
        }).round(4)
        
        # Language performance
        language_performance = results_df.groupby('language').agg({
            'accuracy': 'mean',
            'success': 'mean'
        }).round(4)
        
        # Store metrics for later use
        self.performance_metrics = {
            'method_summary': method_summary,
            'category_performance': category_performance,
            'language_performance': language_performance
        }
        
        return results_df
    
    def save_benchmark_results(self, filename: str = "benchmark_results.csv"):
        """Save benchmark results to CSV"""
        if hasattr(self, 'results_df') and not self.results_df.empty:
            self.results_df.to_csv(filename, index=False)
            logger.info(f"Results saved to {filename}")
    
    def save_benchmark_report(self, filename: str = "benchmark_report.json"):
        """Save comprehensive benchmark report"""
        import json
        
        report = {
            'summary': {
                'total_test_cases': len(self.test_cases),
                'total_results': len(self.results) if hasattr(self, 'results') else 0,
                'methods_tested': list(self.extractors.keys()),
                'categories_tested': list(set(tc['category'] for tc in self.test_cases)),
                'languages_tested': list(set(tc['language'] for tc in self.test_cases))
            },
            'performance_metrics': self.performance_metrics,
            'configuration': self.config
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Report saved to {filename}")
    
    def get_best_method(self, metric: str = 'accuracy') -> str:
        """Get the best performing method for a given metric"""
        if not hasattr(self, 'results_df') or self.results_df.empty:
            return None
        
        method_performance = self.results_df.groupby('method')[metric].mean()
        best_method = method_performance.idxmax()
        best_score = method_performance.max()
        
        return best_method, best_score
