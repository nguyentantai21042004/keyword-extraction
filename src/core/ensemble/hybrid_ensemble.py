"""
Hybrid ensemble keyword extraction implementation
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional
from ..base_extractor import BaseExtractor, ExtractionResult
from ..extractors import SpacyYakeExtractor, RakeExtractor, TfIdfExtractor

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
        """Combine results from multiple methods using weighted voting"""
        keyword_scores = {}
        
        for result in results:
            weight = self.method_weights.get(result.method_name, 0.1)
            
            for keyword_info in result.keywords:
                keyword = keyword_info['keyword'].lower()
                score = keyword_info['score'] * weight
                
                if keyword in keyword_scores:
                    keyword_scores[keyword]['score'] += score
                    keyword_scores[keyword]['methods'].append(result.method_name)
                else:
                    keyword_scores[keyword] = {
                        'keyword': keyword_info['keyword'],
                        'score': score,
                        'methods': [result.method_name],
                        'type': keyword_info['type']
                    }
        
        # Sort by combined score
        sorted_keywords = sorted(keyword_scores.values(), key=lambda x: x['score'], reverse=True)
        
        # Format final results
        final_keywords = []
        for i, kw in enumerate(sorted_keywords[:25]):  # Top 25 combined keywords
            final_keywords.append({
                'keyword': kw['keyword'],
                'score': kw['score'],
                'rank': i + 1,
                'type': f"ensemble_{kw['type']}",
                'relevance': min(kw['score'], 1.0),
                'methods_used': kw['methods']
            })
        
        return final_keywords
    
    def _calculate_ensemble_confidence(self, results: List[ExtractionResult]) -> float:
        """Calculate confidence score for ensemble method"""
        if not results:
            return 0.0
        
        # Base confidence from average of individual confidences
        avg_confidence = np.mean([r.confidence_score for r in results])
        
        # Bonus for method diversity
        method_diversity = len(set(r.method_name for r in results))
        diversity_bonus = min(method_diversity / 4.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for consensus (methods agreeing on keywords)
        consensus_bonus = self._calculate_consensus_bonus(results)
        
        final_confidence = avg_confidence + diversity_bonus + consensus_bonus
        return min(final_confidence, 1.0)
    
    def _calculate_consensus_bonus(self, results: List[ExtractionResult]) -> float:
        """Calculate bonus for methods agreeing on keywords"""
        if len(results) < 2:
            return 0.0
        
        # Get all keywords from all methods
        all_keywords = []
        for result in results:
            all_keywords.extend([kw['keyword'].lower() for kw in result.keywords])
        
        # Count keyword frequency across methods
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Calculate consensus score
        if not keyword_counts:
            return 0.0
        
        avg_consensus = np.mean(list(keyword_counts.values()))
        max_consensus = len(results)
        
        # Normalize consensus score
        consensus_score = avg_consensus / max_consensus
        
        # Return bonus (max 0.1)
        return min(consensus_score * 0.1, 0.1)
