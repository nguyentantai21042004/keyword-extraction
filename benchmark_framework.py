import pandas as pd
import numpy as np
from typing import Dict, List
from multi_method_extractor import (
    ExtractionMethod, SpacyYakeExtractor, RakeExtractor, 
    TextRankExtractor, TfIdfExtractor, KeyBertExtractor
)
from hybrid_ensemble import HybridEnsembleExtractor

class ExtractionBenchmark:
    """Comprehensive benchmarking and comparison framework"""
    
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
    
    def add_test_case(self, text: str, expected_keywords: List[str] = None, category: str = "general"):
        """Add test case for benchmarking"""
        self.test_cases.append({
            'text': text,
            'expected_keywords': expected_keywords or [],
            'category': category,
            'text_length': len(text),
            'has_social_elements': '#' in text or '@' in text
        })
    
    async def run_comprehensive_benchmark(self) -> pd.DataFrame:
        """Run all methods on all test cases"""
        benchmark_results = []
        
        for i, test_case in enumerate(self.test_cases):
            print(f"Processing test case {i+1}/{len(self.test_cases)}")
            
            for method, extractor in self.extractors.items():
                try:
                    result = await extractor.extract(test_case['text'])
                    
                    # Calculate accuracy if ground truth available
                    accuracy = self._calculate_accuracy(
                        result.keywords, 
                        test_case['expected_keywords']
                    ) if test_case['expected_keywords'] else None
                    
                    benchmark_results.append({
                        'test_case_id': i,
                        'method': method.value,
                        'text_category': test_case['category'],
                        'text_length': test_case['text_length'],
                        'has_social_elements': test_case['has_social_elements'],
                        'processing_time': result.processing_time,
                        'memory_usage': result.memory_usage,
                        'confidence_score': result.confidence_score,
                        'keywords_count': len(result.keywords),
                        'accuracy': accuracy,
                        'top_keywords': [kw['keyword'] for kw in result.keywords[:5]],
                        'avg_keyword_score': np.mean([kw['score'] for kw in result.keywords]) if result.keywords else 0,
                        'success': len(result.keywords) > 0
                    })
                    
                except Exception as e:
                    benchmark_results.append({
                        'test_case_id': i,
                        'method': method.value,
                        'text_category': test_case['category'],
                        'error': str(e),
                        'success': False
                    })
        
        return pd.DataFrame(benchmark_results)
    
    def _calculate_accuracy(self, extracted_keywords: List[Dict], expected_keywords: List[str]) -> float:
        """Calculate accuracy based on expected keywords"""
        if not expected_keywords:
            return None
        
        extracted_set = set([kw['keyword'].lower() for kw in extracted_keywords])
        expected_set = set([kw.lower() for kw in expected_keywords])
        
        if not expected_set:
            return 1.0 if not extracted_set else 0.0
        
        intersection = extracted_set.intersection(expected_set)
        precision = len(intersection) / len(extracted_set) if extracted_set else 0
        recall = len(intersection) / len(expected_set)
        
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    def generate_performance_report(self, results_df: pd.DataFrame) -> Dict:
        """Generate comprehensive performance analysis"""
        
        # Overall performance by method
        method_performance = results_df.groupby('method').agg({
            'processing_time': ['mean', 'std', 'min', 'max'],
            'memory_usage': ['mean', 'std', 'min', 'max'],
            'confidence_score': ['mean', 'std'],
            'keywords_count': ['mean', 'std'],
            'accuracy': ['mean', 'std'],
            'success': 'mean'
        }).round(4)
        
        # Performance by text category
        category_performance = results_df.groupby(['method', 'text_category']).agg({
            'processing_time': 'mean',
            'confidence_score': 'mean',
            'accuracy': 'mean'
        }).round(4)
        
        # Social media performance
        social_performance = results_df[results_df['has_social_elements'] == True].groupby('method').agg({
            'processing_time': 'mean',
            'confidence_score': 'mean',
            'accuracy': 'mean'
        }).round(4)
        
        return {
            'overall_performance': method_performance,
            'category_performance': category_performance,
            'social_media_performance': social_performance,
            'summary_stats': {
                'total_test_cases': len(self.test_cases),
                'methods_tested': len(self.extractors),
                'avg_processing_time_by_method': results_df.groupby('method')['processing_time'].mean().to_dict(),
                'success_rate_by_method': results_df.groupby('method')['success'].mean().to_dict()
            }
        }

def create_research_test_dataset():
    """Create comprehensive test dataset for research"""
    
    test_cases = [
        # Social Media Cases
        {
            'text': "Just discovered #sustainablefashion trends! @patagonia's new eco-line is amazing 🌱",
            'expected_keywords': ['sustainable fashion', 'patagonia', 'eco-line', 'trends'],
            'category': 'social_media'
        },
        {
            'text': "Need insights on influencer marketing for beauty brands targeting Gen Z #beautytech #influencer",
            'expected_keywords': ['influencer marketing', 'beauty brands', 'gen z', 'beautytech'],
            'category': 'social_media'
        },
        
        # Business Cases  
        {
            'text': "Market analysis of renewable energy sector shows significant growth in solar and wind power technologies",
            'expected_keywords': ['market analysis', 'renewable energy', 'solar power', 'wind power'],
            'category': 'business'
        },
        
        # Technical Cases
        {
            'text': "Machine learning algorithms for natural language processing applications in social media sentiment analysis",
            'expected_keywords': ['machine learning', 'natural language processing', 'sentiment analysis'],
            'category': 'technical'
        },
        
        # Short Text Cases
        {
            'text': "AI startup funding trends 2024",
            'expected_keywords': ['ai startup', 'funding trends'],
            'category': 'short_text'
        }
    ]
    
    return test_cases

# Usage for research
async def run_research_benchmark():
    benchmark = ExtractionBenchmark()
    
    # Add test cases
    test_cases = create_research_test_dataset()
    for case in test_cases:
        benchmark.add_test_case(
            case['text'], 
            case['expected_keywords'], 
            case['category']
        )
    
    # Run benchmark
    results_df = await benchmark.run_comprehensive_benchmark()
    
    # Generate report
    performance_report = benchmark.generate_performance_report(results_df)
    
    # Save results for thesis
    results_df.to_csv('keyword_extraction_benchmark_results.csv', index=False)
    
    return results_df, performance_report
