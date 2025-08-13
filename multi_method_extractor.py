import asyncio
import time
import psutil
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np

class ExtractionMethod(Enum):
    SPACY_YAKE = "spacy_yake"
    RAKE_NLTK = "rake_nltk" 
    TEXTRANK = "textrank"
    KEYBERT = "keybert"
    TF_IDF = "tf_idf"
    HYBRID_ENSEMBLE = "hybrid_ensemble"

@dataclass
class ExtractionResult:
    keywords: List[Dict]
    metadata: Dict
    performance_metrics: Dict
    method_name: str
    processing_time: float
    memory_usage: float
    confidence_score: float

class BaseExtractor(ABC):
    """Abstract base class for all extraction methods"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.method_name = ""
        
    @abstractmethod
    async def extract(self, text: str) -> ExtractionResult:
        pass
    
    def _measure_performance(self, func):
        """Decorator to measure performance metrics"""
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            try:
                result = await func(*args, **kwargs)
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                result.processing_time = end_time - start_time
                result.memory_usage = end_memory - start_memory
                
                return result
                
            except Exception as e:
                return ExtractionResult(
                    keywords=[],
                    metadata={'error': str(e)},
                    performance_metrics={},
                    method_name=self.method_name,
                    processing_time=time.time() - start_time,
                    memory_usage=0,
                    confidence_score=0.0
                )
        return wrapper

class SpacyYakeExtractor(BaseExtractor):
    """Primary method - spaCy + YAKE combination"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "spacy_yake"
        self.nlp = None
        self.yake_extractor = None
        self._load_models()
        
    def _load_models(self):
        """Load spaCy and YAKE models"""
        try:
            import spacy
            import yake
            
            # Load spaCy model
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Download if not available
                spacy.cli.download("en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            # Initialize YAKE
            self.yake_extractor = yake.KeywordExtractor(
                lan="en", 
                n=1, 
                dedupLim=0.9, 
                top=20, 
                features=None
            )
            
        except ImportError as e:
            print(f"Warning: {e}. spaCy+YAKE method unavailable.")
            self.nlp = None
            self.yake_extractor = None
        
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        if not self.nlp or not self.yake_extractor:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'Models not loaded', 'method': 'spacy_yake'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            # Process with spaCy
            doc = self.nlp(text)
            
            # Extract named entities and noun chunks
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            
            # Extract keywords with YAKE
            yake_keywords = self.yake_extractor.extract_keywords(text)
            
            # Combine and rank results
            keywords = []
            
            # Add YAKE keywords
            for i, (keyword, score) in enumerate(yake_keywords):
                keywords.append({
                    'keyword': keyword,
                    'score': 1 - score,  # YAKE scores are lower = better
                    'rank': i + 1,
                    'type': 'yake_keyword',
                    'relevance': 1 - score
                })
            
            # Add named entities
            for i, (entity, label) in enumerate(entities[:10]):
                keywords.append({
                    'keyword': entity,
                    'score': 0.8,
                    'rank': len(keywords) + 1,
                    'type': f'entity_{label.lower()}',
                    'relevance': 0.8
                })
            
            # Sort by score
            keywords.sort(key=lambda x: x['score'], reverse=True)
            
            # Re-rank
            for i, kw in enumerate(keywords[:20]):
                kw['rank'] = i + 1
            
            confidence = self._calculate_spacy_yake_confidence(keywords, entities, noun_chunks)
            
            return ExtractionResult(
                keywords=keywords[:20],
                metadata={
                    'method': 'spacy_yake',
                    'entities_count': len(entities),
                    'noun_chunks_count': len(noun_chunks),
                    'yake_keywords_count': len(yake_keywords)
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
                metadata={'error': str(e), 'method': 'spacy_yake'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_spacy_yake_confidence(self, keywords: List[Dict], entities: List, noun_chunks: List) -> float:
        """Calculate confidence based on extraction quality"""
        if not keywords:
            return 0.0
        
        # Base confidence from YAKE scores
        yake_scores = [kw['score'] for kw in keywords if kw['type'] == 'yake_keyword']
        base_confidence = np.mean(yake_scores) if yake_scores else 0.5
        
        # Bonus for entity detection
        entity_bonus = min(len(entities) / 10, 0.2)
        
        # Bonus for noun chunks
        chunk_bonus = min(len(noun_chunks) / 20, 0.1)
        
        return min(base_confidence + entity_bonus + chunk_bonus, 1.0)

class RakeExtractor(BaseExtractor):
    """Fast baseline method"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "rake_nltk"
        self.rake = None
        self._load_rake()
        
    def _load_rake(self):
        """Load RAKE extractor"""
        try:
            from rake_nltk import Rake
            self.rake = Rake()
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
            self.rake.extract_keywords_from_text(text)
            phrases = self.rake.get_ranked_phrases_with_scores()
            
            keywords = [
                {
                    'keyword': phrase,
                    'score': score,
                    'rank': i + 1,
                    'type': 'rake_phrase',
                    'relevance': min(score / 10, 1.0)
                }
                for i, (score, phrase) in enumerate(phrases[:20])
            ]
            
            confidence = self._calculate_rake_confidence(phrases)
            
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
    
    def _calculate_rake_confidence(self, phrases: List) -> float:
        if not phrases:
            return 0.0
        scores = [score for score, _ in phrases]
        return min(np.mean(scores) / 10, 1.0)

class TextRankExtractor(BaseExtractor):
    """Graph-based method for comparison"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "textrank"
        
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        try:
            from textrank import TextRank4Keyword
            
            tr4w = TextRank4Keyword()
            tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
            
            keywords = [
                {
                    'keyword': word,
                    'score': score,
                    'rank': i + 1,
                    'type': 'textrank_keyword',
                    'relevance': score
                }
                for i, (word, score) in enumerate(tr4w.get_keywords(20, word_min_len=2))
            ]
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'textrank',
                    'window_size': 4,
                    'pos_tags': ['NOUN', 'PROPN']
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=self._calculate_textrank_confidence(keywords)
            )
            
        except ImportError:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'TextRank not available', 'method': 'textrank'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': 'textrank'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_textrank_confidence(self, keywords: List) -> float:
        if not keywords:
            return 0.0
        scores = [kw['score'] for kw in keywords]
        return np.mean(scores) if scores else 0.0

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
            
            # Simple TF-IDF on sentences
            sentences = text.split('.')
            if len(sentences) < 2:
                sentences = [text]
                
            vectorizer = TfidfVectorizer(
                stop_words=list(ENGLISH_STOP_WORDS),
                ngram_range=(1, 2),
                max_features=50
            )
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Create keyword list
            keywords = [
                {
                    'keyword': feature_names[i],
                    'score': mean_scores[i],
                    'rank': rank + 1,
                    'type': 'tfidf_term',
                    'relevance': mean_scores[i]
                }
                for rank, i in enumerate(np.argsort(mean_scores)[::-1][:20])
                if mean_scores[i] > 0
            ]
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'tf_idf',
                    'vocab_size': len(feature_names),
                    'sentences_count': len(sentences)
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=np.max(mean_scores) if len(mean_scores) > 0 else 0.0
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
                top_k=20,
                use_maxsum=True,
                nr_candidates=20,
                diversity=0.5
            )
            
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
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'keybert',
                    'model': 'all-MiniLM-L6-v2',
                    'semantic_similarity': True
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=np.mean([kw['score'] for kw in keywords]) if keywords else 0.0
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
