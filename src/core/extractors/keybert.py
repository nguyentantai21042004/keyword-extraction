"""
KeyBERT keyword extraction implementation
"""

from typing import Dict, List
from ..base_extractor import BaseExtractor, ExtractionResult

class KeyBertExtractor(BaseExtractor):
    """High-accuracy method for comparison (load on demand)"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "keybert"
        self.model = None
        
    def _load_model(self):
        """Lazy loading để tiết kiệm memory"""
        if self.model is None:
            try:
                from keybert import KeyBERT
                from sentence_transformers import SentenceTransformer
                
                # Use lightweight model
                sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.model = KeyBERT(model=sentence_model)
            except ImportError:
                self.model = "unavailable"
    
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        self._load_model()
        
        if self.model == "unavailable":
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'KeyBERT not available', 'method': 'keybert'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            keyword_tuples = self.model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                use_maxsum=True,
                nr_candidates=20,
                diversity=0.5
            )[:20]  # Limit to top 20
            
            keywords = [
                {
                    'keyword': keyword,
                    'score': score,
                    'rank': i + 1,
                    'type': 'keybert_semantic',
                    'relevance': score
                }
                for i, (keyword, score) in enumerate(keyword_tuples)
            ]
            
            confidence = self._calculate_keybert_confidence(keywords)
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'keybert_semantic',
                    'model': 'all-MiniLM-L6-v2',
                    'diversity': 0.5
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=confidence
            )
            
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': 'keybert'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_keybert_confidence(self, keywords: List[Dict]) -> float:
        """Calculate confidence score for KeyBERT method"""
        if not keywords:
            return 0.0
        
        # Base confidence from average score
        avg_score = sum(kw['score'] for kw in keywords) / len(keywords)
        base_confidence = min(avg_score, 1.0)  # KeyBERT scores are already 0-1
        
        # Bonus for keyword diversity
        unique_keywords = len(set(kw['keyword'] for kw in keywords))
        diversity_bonus = min(unique_keywords / 15.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for number of keywords
        count_bonus = min(len(keywords) / 20.0, 0.1)  # Max 0.1 bonus
        
        confidence = base_confidence + diversity_bonus + count_bonus
        return min(confidence, 1.0)
