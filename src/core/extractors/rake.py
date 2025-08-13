"""
RAKE keyword extraction implementation
"""

import re
from typing import Dict, List, Tuple
from ..base_extractor import BaseExtractor, ExtractionResult

class RakeExtractor(BaseExtractor):
    """Improved RAKE method for better keyword extraction"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "rake_nltk"
        self.rake = None
        self._load_rake()
        
    def _load_rake(self):
        """Load improved RAKE extractor"""
        try:
            from rake_nltk import Rake
            import nltk
            
            # Enhanced RAKE with better configuration
            self.rake = Rake(
                stopwords='english',
                include_repeated_phrases=False
            )
        except ImportError:
            print("Warning: rake-nltk not available. RAKE method unavailable.")
            self.rake = None
        
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        if not self.rake:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'RAKE not available', 'method': 'rake_nltk'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            # Enhanced text preprocessing for better extraction
            enhanced_text = self._preprocess_text(text)
            
            self.rake.extract_keywords_from_text(enhanced_text)
            phrases = self.rake.get_ranked_phrases_with_scores()
            
            # Post-process to get better keyword phrases
            processed_keywords = self._post_process_keywords(phrases, text)
            
            keywords = [
                {
                    'keyword': keyword,
                    'score': score,
                    'rank': i + 1,
                    'type': 'rake_phrase',
                    'relevance': min(score / 10, 1.0)
                }
                for i, (score, keyword) in enumerate(processed_keywords[:20])
            ]
            
            confidence = self._calculate_rake_confidence(processed_keywords)
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'total_phrases': len(phrases),
                    'method': 'rake_nltk',
                    'language': 'en'
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,  # Will be filled by decorator
                memory_usage=0,     # Will be filled by decorator
                confidence_score=confidence
            )
            
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': 'rake_nltk'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _preprocess_text(self, text: str) -> str:
        """Enhanced text preprocessing for better RAKE extraction"""
        # Expand common abbreviations for better phrase detection
        abbreviations = {
            'AI': 'artificial intelligence',
            'ML': 'machine learning',
            'NLP': 'natural language processing',
            'API': 'application programming interface',
            'UI': 'user interface',
            'UX': 'user experience'
        }
        
        enhanced_text = text
        for abbrev, full in abbreviations.items():
            enhanced_text = re.sub(r'\b' + abbrev + r'\b', full, enhanced_text, flags=re.IGNORECASE)
        
        # Add periods to force sentence breaks for better phrase detection
        enhanced_text = re.sub(r'([.!?])\s*$', r'\1', enhanced_text)
        if not enhanced_text.endswith(('.', '!', '?')):
            enhanced_text += '.'
            
        return enhanced_text
    
    def _post_process_keywords(self, phrases: List, original_text: str) -> List:
        """Post-process RAKE phrases to get better keywords"""
        if not phrases:
            return []
        
        processed = []
        original_lower = original_text.lower()
        
        for score, phrase in phrases:
            # Accept all phrases with reasonable scores
            if score > 0.5:  # Lower threshold
                # Split long phrases into meaningful parts
                phrase_words = phrase.split()
                if len(phrase_words) > 3:
                    # For very long phrases, extract important subphrases
                    for i in range(len(phrase_words) - 1):
                        subphrase = ' '.join(phrase_words[i:i+2])
                        if subphrase.lower() in original_lower:
                            processed.append((score * 0.8, subphrase))
                else:
                    processed.append((score, phrase))
        
        # Sort by score and return top results
        processed.sort(key=lambda x: x[0], reverse=True)
        return processed[:25]  # Return top 25 processed phrases
    
    def _calculate_rake_confidence(self, processed_keywords: List) -> float:
        """Calculate confidence score for RAKE method"""
        if not processed_keywords:
            return 0.0
        
        # Base confidence from average score
        avg_score = sum(score for score, _ in processed_keywords) / len(processed_keywords)
        base_confidence = min(avg_score / 10.0, 1.0)  # Normalize to 0-1
        
        # Bonus for phrase diversity
        phrase_lengths = [len(phrase.split()) for _, phrase in processed_keywords]
        avg_length = sum(phrase_lengths) / len(phrase_lengths)
        length_bonus = min(avg_length / 3.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for number of keywords
        count_bonus = min(len(processed_keywords) / 20.0, 0.1)  # Max 0.1 bonus
        
        confidence = base_confidence + length_bonus + count_bonus
        return min(confidence, 1.0)
