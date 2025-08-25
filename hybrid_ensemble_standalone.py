"""
Standalone Hybrid Ensemble Keyword Extraction Algorithm
====================================================

This file contains a complete, self-contained implementation of the Hybrid Ensemble
keyword extraction method. You can copy this entire file to any other project
and use it directly.

Features:
- Combines multiple extraction methods intelligently
- Concurrent execution for better performance
- Weighted voting system for result combination
- Automatic fallback if some methods fail
- Comprehensive error handling
- Performance monitoring

Dependencies:
- spacy
- yake
- rake-nltk
- scikit-learn
- numpy
- psutil

Usage:
    extractor = HybridEnsembleExtractor()
    result = await extractor.extract("Your text here")
    print(result.keywords)
"""

import asyncio
import time
import psutil
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class KeywordResult:
    """Individual keyword result"""
    keyword: str
    score: float
    rank: int
    type: str
    relevance: float
    methods_used: Optional[List[str]] = None

@dataclass
class ExtractionResult:
    """Complete extraction result"""
    keywords: List[KeywordResult]
    metadata: Dict
    performance_metrics: Dict
    method_name: str
    processing_time: float
    memory_usage: float
    confidence_score: float

class ExtractionMethod(Enum):
    """Available extraction methods"""
    HYBRID_ENSEMBLE = "hybrid_ensemble"
    SPACY_YAKE = "spacy_yake"
    RAKE = "rake"
    TFIDF = "tfidf"

# ============================================================================
# PERFORMANCE MONITORING DECORATOR
# ============================================================================

def measure_performance(func):
    """Decorator to measure performance metrics"""
    async def wrapper(self, *args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = await func(self, *args, **kwargs)
            
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

# ============================================================================
# BASE EXTRACTOR INTERFACE
# ============================================================================

class BaseExtractor:
    """Base interface for all extractors"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.method_name = ""
    
    async def extract(self, text: str) -> ExtractionResult:
        """Extract keywords from text"""
        raise NotImplementedError

# ============================================================================
# SPA CY + YAKE EXTRACTOR
# ============================================================================

class SpacyYakeExtractor(BaseExtractor):
    """spaCy + YAKE hybrid extractor"""
    
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
                spacy.cli.download("en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            # Initialize YAKE
            self.yake_extractor = yake.KeywordExtractor(
                lan="en", 
                n=2,
                dedupLim=0.8,
                top=30,
                features=None
            )
            
        except ImportError:
            self.nlp = None
            self.yake_extractor = None
    
    async def extract(self, text: str) -> ExtractionResult:
        if not self.nlp or not self.yake_extractor:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'Models not loaded'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            # Process with spaCy
            doc = self.nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            
            # Extract keywords with YAKE
            yake_keywords = self.yake_extractor.extract_keywords(text)
            
            # Combine results
            keywords = []
            
            # Add YAKE keywords
            for i, (keyword, score) in enumerate(yake_keywords):
                keywords.append(KeywordResult(
                    keyword=keyword,
                    score=1 - score,
                    rank=i + 1,
                    type='yake_keyword',
                    relevance=1 - score
                ))
            
            # Add named entities
            for i, (entity, label) in enumerate(entities[:15]):
                if len(entity.split()) <= 3:
                    keywords.append(KeywordResult(
                        keyword=entity,
                        score=0.7,
                        rank=len(keywords) + 1,
                        type=f'entity_{label.lower()}',
                        relevance=0.7
                    ))
            
            # Add noun chunks
            for i, chunk in enumerate(noun_chunks[:20]):
                if len(chunk.split()) >= 2:
                    keywords.append(KeywordResult(
                        keyword=chunk,
                        score=0.5,
                        rank=len(keywords) + 1,
                        type='noun_chunk',
                        relevance=0.5
                    ))
            
            # Sort by score
            keywords.sort(key=lambda x: x.score, reverse=True)
            
            # Re-rank
            for i, kw in enumerate(keywords[:30]):
                kw.rank = i + 1
            
            confidence = self._calculate_confidence(keywords, entities, noun_chunks)
            
            return ExtractionResult(
                keywords=keywords[:30],
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
                metadata={'error': str(e)},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_confidence(self, keywords: List[KeywordResult], entities: List, noun_chunks: List) -> float:
        """Calculate confidence score"""
        if not keywords:
            return 0.0
        
        base_confidence = min(len(keywords) / 30.0, 1.0)
        entity_types = set(label for _, label in entities)
        entity_bonus = min(len(entity_types) / 5.0, 0.2)
        
        if noun_chunks:
            avg_chunk_length = sum(len(chunk.split()) for chunk in noun_chunks) / len(noun_chunks)
            chunk_bonus = min(avg_chunk_length / 3.0, 0.1)
        else:
            chunk_bonus = 0.0
        
        confidence = base_confidence + entity_bonus + chunk_bonus
        return min(confidence, 1.0)

# ============================================================================
# RAKE EXTRACTOR
# ============================================================================

class RakeExtractor(BaseExtractor):
    """RAKE keyword extractor"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "rake"
        self.rake = None
        self._load_rake()
    
    def _load_rake(self):
        """Load RAKE extractor"""
        try:
            from rake_nltk import Rake
            self.rake = Rake(stopwords='english', include_repeated_phrases=False)
        except ImportError:
            self.rake = None
    
    async def extract(self, text: str) -> ExtractionResult:
        if not self.rake:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'RAKE not available'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            self.rake.extract_keywords_from_text(text)
            phrases = self.rake.get_ranked_phrases_with_scores()
            
            keywords = []
            for i, (score, phrase) in enumerate(phrases[:20]):
                keywords.append(KeywordResult(
                    keyword=phrase,
                    score=score,
                    rank=i + 1,
                    type='rake_phrase',
                    relevance=min(score / 10, 1.0)
                ))
            
            confidence = self._calculate_confidence(keywords)
            
            return ExtractionResult(
                keywords=keywords,
                metadata={'total_phrases': len(phrases)},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=confidence
            )
            
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e)},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_confidence(self, keywords: List[KeywordResult]) -> float:
        """Calculate confidence score"""
        if not keywords:
            return 0.0
        
        avg_score = sum(kw.score for kw in keywords) / len(keywords)
        base_confidence = min(avg_score / 10.0, 1.0)
        
        phrase_lengths = [len(kw.keyword.split()) for kw in keywords]
        avg_length = sum(phrase_lengths) / len(phrase_lengths)
        length_bonus = min(avg_length / 3.0, 0.2)
        
        count_bonus = min(len(keywords) / 20.0, 0.1)
        
        confidence = base_confidence + length_bonus + count_bonus
        return min(confidence, 1.0)

# ============================================================================
# TF-IDF EXTRACTOR
# ============================================================================

class TfIdfExtractor(BaseExtractor):
    """TF-IDF keyword extractor"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "tfidf"
    
    async def extract(self, text: str) -> ExtractionResult:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            
            # Create corpus
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if not sentences:
                sentences = [text]
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(
                stop_words=list(ENGLISH_STOP_WORDS),
                ngram_range=(1, 3),
                max_features=100,
                min_df=1
            )
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Create keywords
            feature_scores = list(zip(feature_names, mean_scores))
            feature_scores.sort(key=lambda x: x[1], reverse=True)
            
            keywords = []
            for i, (feature, score) in enumerate(feature_scores[:20]):
                keywords.append(KeywordResult(
                    keyword=feature,
                    score=score,
                    rank=i + 1,
                    type='tfidf_term',
                    relevance=score
                ))
            
            confidence = np.max([score for _, score in feature_scores]) if feature_scores else 0.0
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'vocab_size': len(feature_names),
                    'corpus_size': len(sentences)
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
                metadata={'error': 'scikit-learn not available'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e)},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )

# ============================================================================
# HYBRID ENSEMBLE EXTRACTOR
# ============================================================================

class HybridEnsembleExtractor(BaseExtractor):
    """
    Intelligent combination of multiple extraction methods
    
    This ensemble approach:
    1. Runs multiple methods concurrently for efficiency
    2. Combines results using weighted voting
    3. Provides consensus scoring for reliability
    4. Handles method failures gracefully
    
    Advantages:
    - Higher accuracy than individual methods
    - Robust to individual method failures
    - Consensus-based confidence scoring
    - Configurable method weights
    
    Best for:
    - High-accuracy requirements
    - Production environments
    - Research and comparison
    - Critical applications
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the ensemble extractor with easy-to-use configuration
        
        Args:
            config: Optional configuration dictionary with intuitive parameters:
                   - 'method_weights': Dict of method weights (0.0-1.0, sum should be ~1.0)
                   - 'timeout': Timeout for individual methods (5-60s, default: 10s)
                   - 'max_keywords': Maximum final keywords (10-100, default: 25)
                   - 'verbose': Show detailed logs (True/False, default: False)
        
        Examples:
            # Balanced mode (default)
            extractor = HybridEnsembleExtractor()
            
            # High accuracy mode
            extractor = HybridEnsembleExtractor({
                'method_weights': {'spacy_yake': 0.6, 'rake': 0.2, 'tfidf': 0.2},
                'max_keywords': 50
            })
            
            # Fast mode
            extractor = HybridEnsembleExtractor({
                'timeout': 5.0,
                'max_keywords': 15
            })
        """
        super().__init__(config)
        self.method_name = "hybrid_ensemble"
        self.verbose = self.config.get('verbose', False)
        
        # Validate and set configuration with clear defaults
        self._setup_configuration()
        
        # Initialize base extractors
        self.extractors = {
            'spacy_yake': SpacyYakeExtractor(config),
            'rake': RakeExtractor(config),
            'tfidf': TfIdfExtractor(config)
        }
    
    def _setup_configuration(self):
        """Setup and validate configuration with clear defaults"""
        # Timeout with validation
        timeout = self.config.get('timeout', 10.0)
        if not isinstance(timeout, (int, float)) or timeout < 5.0 or timeout > 60.0:
            if self.verbose:
                print(f"⚠️  Invalid timeout '{timeout}', using 10.0 instead (range: 5-60s)")
            self.timeout = 10.0
        else:
            self.timeout = timeout
        
        # Max keywords with validation
        max_keywords = self.config.get('max_keywords', 25)
        if not isinstance(max_keywords, int) or max_keywords < 10 or max_keywords > 100:
            if self.verbose:
                print(f"⚠️  Invalid max_keywords '{max_keywords}', using 25 instead (range: 10-100)")
            self.max_keywords = 25
        else:
            self.max_keywords = max_keywords
        
        # Method weights with validation
        method_weights = self.config.get('method_weights', {
            'spacy_yake': 0.4,  # Highest weight - best accuracy
            'rake': 0.2,        # Medium weight - good speed
            'tfidf': 0.2,       # Medium weight - reliable baseline
        })
        
        # Validate weights
        total_weight = sum(method_weights.values())
        if abs(total_weight - 1.0) > 0.1:  # Allow small deviation
            if self.verbose:
                print(f"⚠️  Weights sum to {total_weight:.2f}, normalizing to 1.0")
            # Normalize weights
            for method in method_weights:
                method_weights[method] /= total_weight
        
        self.method_weights = method_weights
        
        if self.verbose:
            print(f"🔧 Ensemble configuration loaded:")
            print(f"   - Timeout: {self.timeout}s")
            print(f"   - Max keywords: {self.max_keywords}")
            print(f"   - Method weights: {self.method_weights}")
    
    def get_config(self) -> Dict:
        """Get current configuration"""
        return {
            'timeout': self.timeout,
            'max_keywords': self.max_keywords,
            'method_weights': self.method_weights.copy(),
            'verbose': self.verbose
        }
    
    def update_config(self, new_config: Dict) -> bool:
        """Update configuration dynamically"""
        try:
            old_config = self.get_config()
            old_config.update(new_config)
            
            # Re-initialize with new config
            self.config = old_config
            self._setup_configuration()
            
            if self.verbose:
                print("✅ Configuration updated successfully")
            return True
        except Exception as e:
            if self.verbose:
                print(f"❌ Failed to update configuration: {e}")
            return False
    
    @measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        """
        Extract keywords using ensemble approach
        
        Args:
            text: Input text to extract keywords from
            
        Returns:
            ExtractionResult with combined keywords and ensemble metrics
        """
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
                'total_methods': len(valid_results),
                'method_weights': self.method_weights,
                'timeout': self.timeout
            },
            performance_metrics={
                'avg_processing_time': np.mean([r.processing_time for r in valid_results]),
                'total_memory': sum([r.memory_usage for r in valid_results]),
                'method_success_rate': len(valid_results) / len(self.extractors)
            },
            method_name=self.method_name,
            processing_time=0,  # Will be filled by decorator
            memory_usage=0,     # Will be filled by decorator
            confidence_score=ensemble_confidence
        )
    
    async def _safe_extract(self, extractor: BaseExtractor, text: str) -> Optional[ExtractionResult]:
        """Safely run extraction with timeout"""
        try:
            # Add timeout for slow methods
            return await asyncio.wait_for(extractor.extract(text), timeout=self.timeout)
        except asyncio.TimeoutError:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'timeout', 'method': extractor.method_name},
                performance_metrics={},
                method_name=extractor.method_name,
                processing_time=self.timeout,
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
    
    def _combine_results(self, results: List[ExtractionResult]) -> List[KeywordResult]:
        """Combine results from multiple methods using weighted voting"""
        keyword_scores = {}
        
        for result in results:
            weight = self.method_weights.get(result.method_name, 0.1)
            
            for keyword_info in result.keywords:
                keyword = keyword_info.keyword.lower()
                score = keyword_info.score * weight
                
                if keyword in keyword_scores:
                    keyword_scores[keyword]['score'] += score
                    keyword_scores[keyword]['methods'].append(result.method_name)
                else:
                    keyword_scores[keyword] = {
                        'keyword': keyword_info.keyword,
                        'score': score,
                        'methods': [result.method_name],
                        'type': keyword_info.type
                    }
        
        # Sort by combined score
        sorted_keywords = sorted(keyword_scores.values(), key=lambda x: x['score'], reverse=True)
        
        # Format final results
        final_keywords = []
        for i, kw in enumerate(sorted_keywords[:self.max_keywords]):
            final_keywords.append(KeywordResult(
                keyword=kw['keyword'],
                score=kw['score'],
                rank=i + 1,
                type=f"ensemble_{kw['type']}",
                relevance=min(kw['score'], 1.0),
                methods_used=kw['methods']
            ))
        
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
            all_keywords.extend([kw.keyword.lower() for kw in result.keywords])
        
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
    
    def get_method_status(self) -> Dict:
        """Get status of all methods"""
        status = {}
        for name, extractor in self.extractors.items():
            if hasattr(extractor, 'get_model_info'):
                status[name] = extractor.get_model_info()
            else:
                status[name] = {'status': 'ready'}
        return status

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

async def example_usage():
    """Example of how to use the HybridEnsembleExtractor"""
    
    # Initialize ensemble extractor
    config = {
        'method_weights': {
            'spacy_yake': 0.4,
            'rake': 0.3,
            'tfidf': 0.3
        },
        'timeout': 15.0,
        'max_keywords': 30
    }
    
    extractor = HybridEnsembleExtractor(config)
    
    # Check method status
    method_status = extractor.get_method_status()
    print(f"🔍 Method Status:")
    for method, status in method_status.items():
        print(f"   - {method}: {status}")
    
    # Example text
    text = """
    Machine Learning and Artificial Intelligence are revolutionizing industries worldwide. 
    Companies like Google, Microsoft, and OpenAI are at the forefront of AI research. 
    Natural Language Processing (NLP) has made significant breakthroughs in understanding 
    human language. Deep learning models are achieving unprecedented accuracy in tasks 
    like image recognition, speech synthesis, and language translation.
    """
    
    # Extract keywords using ensemble
    print(f"\n🔍 Extracting keywords using ensemble approach...")
    result = await extractor.extract(text)
    
    # Display results
    print(f"\n✅ Ensemble extraction completed!")
    print(f"📊 Performance:")
    print(f"   - Processing time: {result.processing_time:.4f}s")
    print(f"   - Memory usage: {result.memory_usage:.2f} MB")
    print(f"   - Confidence score: {result.confidence_score:.3f}")
    print(f"   - Keywords found: {len(result.keywords)}")
    print(f"   - Methods used: {result.metadata['methods_used']}")
    
    print(f"\n🏷️ Top Ensemble Keywords:")
    for i, kw in enumerate(result.keywords[:15]):
        methods_str = ', '.join(kw.methods_used) if kw.methods_used else 'unknown'
        print(f"   {i+1:2d}. {kw.keyword:<25} [{kw.type:<15}] Score: {kw.score:.3f} | Methods: {methods_str}")
    
    print(f"\n📋 Ensemble Metadata:")
    for key, value in result.metadata.items():
        if key != 'method_weights':  # Skip long config dict
            print(f"   - {key}: {value}")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
