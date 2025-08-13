import asyncio
import numpy as np
from typing import Dict, List, Optional
from multi_method_extractor import BaseExtractor, ExtractionResult, SpacyYakeExtractor, RakeExtractor, TfIdfExtractor

class HybridEnsembleExtractor(BaseExtractor):
    """Intelligent combination of multiple methods"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "hybrid_ensemble"
        
        # Initialize base extractors
        self.extractors = {
            'spacy_yake': SpacyYakeExtractor(config),
            'rake': RakeExtractor(config),
            'tfidf': TfIdfExtractor(config)
        }
        
        # Method weights based on performance characteristics
        self.method_weights = {
            'spacy_yake': 0.4,
            'rake': 0.2,
            'tfidf': 0.2,
            'keybert': 0.2  # Higher weight but conditional
        }
    
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        # Run multiple methods concurrently
        tasks = []
        for name, extractor in self.extractors.items():
            tasks.append(self._safe_extract(extractor, text))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        valid_results = [r for r in results if isinstance(r, ExtractionResult) and r.keywords]
        
        if not valid_results:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'All methods failed', 'method': 'hybrid_ensemble'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        # Combine results using weighted voting
        combined_keywords = self._combine_results(valid_results)
        
        # Calculate ensemble confidence
        ensemble_confidence = self._calculate_ensemble_confidence(valid_results)
        
        return ExtractionResult(
            keywords=combined_keywords,
            metadata={
                'method': 'hybrid_ensemble',
                'methods_used': [r.method_name for r in valid_results],
                'consensus_score': ensemble_confidence,
                'total_methods': len(valid_results)
            },
            performance_metrics={
                'avg_processing_time': np.mean([r.processing_time for r in valid_results]),
                'total_memory': sum([r.memory_usage for r in valid_results])
            },
            method_name=self.method_name,
            processing_time=0,
            memory_usage=0,
            confidence_score=ensemble_confidence
        )
    
    async def _safe_extract(self, extractor: BaseExtractor, text: str) -> Optional[ExtractionResult]:
        """Safely run extraction with timeout"""
        try:
            # Add timeout for slow methods
            return await asyncio.wait_for(extractor.extract(text), timeout=10.0)
        except asyncio.TimeoutError:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'timeout', 'method': extractor.method_name},
                performance_metrics={},
                method_name=extractor.method_name,
                processing_time=10.0,
                memory_usage=0,
                confidence_score=0.0
            )
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': extractor.method_name},
                performance_metrics={},
                method_name=extractor.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _combine_results(self, results: List[ExtractionResult]) -> List[Dict]:
        """Combine keywords from multiple methods using weighted voting"""
        keyword_scores = {}
        
        for result in results:
            method_weight = self.method_weights.get(result.method_name, 0.1)
            
            for kw in result.keywords:
                keyword_text = kw['keyword'].lower()
                
                if keyword_text not in keyword_scores:
                    keyword_scores[keyword_text] = {
                        'total_score': 0,
                        'method_count': 0,
                        'methods': [],
                        'original_keyword': kw['keyword']
                    }
                
                keyword_scores[keyword_text]['total_score'] += kw['score'] * method_weight
                keyword_scores[keyword_text]['method_count'] += 1
                keyword_scores[keyword_text]['methods'].append(result.method_name)
        
        # Sort by combined score
        sorted_keywords = sorted(
            keyword_scores.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        # Format final results
        combined_keywords = []
        for i, (keyword_text, data) in enumerate(sorted_keywords[:20]):
            combined_keywords.append({
                'keyword': data['original_keyword'],
                'score': data['total_score'],
                'rank': i + 1,
                'type': 'ensemble',
                'relevance': data['total_score'],
                'method_consensus': data['method_count'],
                'contributing_methods': data['methods']
            })
        
        return combined_keywords
    
    def _calculate_ensemble_confidence(self, results: List[ExtractionResult]) -> float:
        """Calculate overall confidence based on method agreement"""
        if not results:
            return 0.0
        
        # Weight by individual method confidence
        weighted_confidence = sum(
            r.confidence_score * self.method_weights.get(r.method_name, 0.1)
            for r in results
        )
        
        # Bonus for method agreement
        method_count_bonus = min(len(results) / 4, 1.0)  # Max bonus at 4+ methods
        
        return min(weighted_confidence * (1 + method_count_bonus), 1.0)
