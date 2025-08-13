"""
TF-IDF keyword extraction implementation
"""

import re
import numpy as np
from typing import Dict, List, Tuple
from ..base_extractor import BaseExtractor, ExtractionResult

class TfIdfExtractor(BaseExtractor):
    """Statistical baseline method"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "tf_idf"
        
    @BaseExtractor._measure_performance  
    async def extract(self, text: str) -> ExtractionResult:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            
            # Enhanced preprocessing for better phrase detection
            processed_text = self._preprocess_for_tfidf(text)
            
            # Create corpus with multiple perspectives
            corpus = self._create_tfidf_corpus(processed_text)
            
            # Enhanced TF-IDF with better phrase detection
            vectorizer = TfidfVectorizer(
                stop_words=list(ENGLISH_STOP_WORDS),
                ngram_range=(1, 3),  # Include trigrams
                max_features=100,
                min_df=1,
                token_pattern=r'\b[a-zA-Z][a-zA-Z\s]*[a-zA-Z]\b|\b[a-zA-Z]+\b'
            )
            
            tfidf_matrix = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Post-process to get better keywords
            processed_keywords = self._post_process_tfidf_keywords(
                feature_names, mean_scores, processed_text
            )
            
            # Create final keyword list
            keywords = [
                {
                    'keyword': keyword,
                    'score': score,
                    'rank': rank + 1,
                    'type': 'tfidf_term',
                    'relevance': score
                }
                for rank, (keyword, score) in enumerate(processed_keywords[:20])
            ]
            
            confidence = np.max([score for _, score in processed_keywords]) if processed_keywords else 0.0
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'tf_idf_enhanced',
                    'vocab_size': len(feature_names),
                    'corpus_size': len(corpus),
                    'ngram_range': '(1,3)'
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=confidence
            )
            
        except ImportError:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'scikit-learn not available', 'method': 'tf_idf'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': 'tf_idf'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _preprocess_for_tfidf(self, text: str) -> str:
        """Enhanced preprocessing for TF-IDF"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Expand common abbreviations
        abbreviations = {
            'AI': 'artificial intelligence',
            'ML': 'machine learning',
            'NLP': 'natural language processing',
            'API': 'application programming interface',
            'UI': 'user interface',
            'UX': 'user experience'
        }
        
        for abbrev, full in abbreviations.items():
            text = re.sub(r'\b' + abbrev + r'\b', full, text, flags=re.IGNORECASE)
        
        return text
    
    def _create_tfidf_corpus(self, text: str) -> List[str]:
        """Create corpus with multiple perspectives for better TF-IDF"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Create corpus with different perspectives
        corpus = []
        
        # Original text
        corpus.append(text)
        
        # Individual sentences
        corpus.extend(sentences)
        
        # N-gram variations
        words = text.split()
        for n in [2, 3]:
            if len(words) >= n:
                ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
                corpus.extend(ngrams)
        
        return corpus
    
    def _post_process_tfidf_keywords(self, feature_names: List[str], scores: np.ndarray, original_text: str) -> List[Tuple[str, float]]:
        """Post-process TF-IDF keywords for better quality"""
        # Combine features with scores
        feature_scores = list(zip(feature_names, scores))
        
        # Filter and enhance scores
        processed = []
        original_lower = original_text.lower()
        
        for feature, score in feature_scores:
            if score > 0.01:  # Minimum threshold
                # Boost score for features that appear in original text
                if feature.lower() in original_lower:
                    score *= 1.2
                
                # Boost score for longer phrases
                if len(feature.split()) > 1:
                    score *= 1.1
                
                processed.append((feature, score))
        
        # Sort by enhanced scores
        processed.sort(key=lambda x: x[1], reverse=True)
        
        return processed[:25]  # Return top 25
