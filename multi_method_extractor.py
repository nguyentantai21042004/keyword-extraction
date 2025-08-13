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
    
    @staticmethod
    def _measure_performance(func):
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
            
            # Initialize YAKE with OPTIMIZED parameters (High Recall configuration)
            self.yake_extractor = yake.KeywordExtractor(
                lan="en", 
                n=2,                    # Bigrams for better phrase extraction
                dedupLim=0.8,           # Allow more diversity
                top=30,                 # More keywords
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
            
            # Add named entities with OPTIMIZED weights
            for i, (entity, label) in enumerate(entities[:15]):  # Increased from 10
                # Filter entities by length for better quality
                if len(entity.split()) <= 3:  # Only entities with <= 3 words
                    keywords.append({
                        'keyword': entity,
                        'score': 0.7,  # Reduced from 0.8 for balance
                        'rank': len(keywords) + 1,
                        'type': f'entity_{label.lower()}',
                        'relevance': 0.7
                    })
            
            # Add noun chunks with OPTIMIZED weights
            for i, chunk in enumerate(noun_chunks[:20]):  # Increased from 15
                # Filter chunks by minimum length for relevance
                if len(chunk.split()) >= 2:  # Only chunks with >= 2 words
                    keywords.append({
                        'keyword': chunk,
                        'score': 0.5,  # Reduced from 0.6 for balance
                        'rank': len(keywords) + 1,
                        'type': 'noun_chunk',
                        'relevance': 0.5
                    })
            
            # Sort by score
            keywords.sort(key=lambda x: x['score'], reverse=True)
            
            # Re-rank with increased limit
            for i, kw in enumerate(keywords[:30]):  # Increased from 20
                kw['rank'] = i + 1
            
            confidence = self._calculate_spacy_yake_confidence(keywords, entities, noun_chunks)
            
            return ExtractionResult(
                keywords=keywords[:30],  # Increased from 20
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
        
        # Bonus for entity detection (OPTIMIZED)
        entity_bonus = min(len(entities) / 15, 0.2)  # Adjusted divisor
        
        # Bonus for noun chunks (OPTIMIZED)
        chunk_bonus = min(len(noun_chunks) / 25, 0.1)  # Adjusted divisor
        
        # Additional bonus for keyword diversity
        keyword_types = set(kw['type'] for kw in keywords)
        diversity_bonus = min(len(keyword_types) / 5, 0.1)
        
        return min(base_confidence + entity_bonus + chunk_bonus + diversity_bonus, 1.0)

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
        import re
        
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
                        for j in range(i + 2, min(i + 4, len(phrase_words) + 1)):
                            subphrase = ' '.join(phrase_words[i:j])
                            if len(subphrase.split()) >= 2:
                                processed.append((score * 0.8, subphrase))
                    # Also add the full phrase
                    processed.append((score, phrase))
                else:
                    # Add phrases as-is
                    processed.append((score, phrase))
        
        # If still no results, fall back to single important words
        if not processed and phrases:
            for score, phrase in phrases[:5]:  # Take top 5 regardless
                processed.append((score, phrase))
        
        # If still no results, extract individual important words
        if not processed:
            import re
            words = re.findall(r'\b[a-zA-Z]{3,}\b', original_text.lower())
            important_words = ['machine', 'learning', 'ai', 'data', 'analysis', 'startup', 'funding', 'trends', 
                             'technology', 'innovation', 'digital', 'social', 'media', 'sustainable', 'fashion',
                             'energy', 'blockchain', 'cloud', 'intelligence', 'processing', 'language']
            
            for word in words:
                if word in important_words or len(word) >= 5:
                    # Assign a base score based on word importance and length
                    score = 2.0 if word in important_words else 1.0
                    if len(word) > 6:
                        score *= 1.2
                    processed.append((score, word))
        
        # Sort by enhanced scores and remove duplicates
        processed.sort(key=lambda x: x[0], reverse=True)
        seen = set()
        final_processed = []
        for score, phrase in processed:
            if phrase.lower() not in seen:
                seen.add(phrase.lower())
                final_processed.append((score, phrase))
        
        return final_processed[:10]  # Return top 10
    
    def _calculate_rake_confidence(self, phrases: List) -> float:
        if not phrases:
            return 0.0
        scores = [score for score, _ in phrases]
        base_confidence = min(np.mean(scores) / 10, 1.0)
        
        # Boost confidence if we have good phrases
        if len(phrases) >= 3:
            base_confidence = min(base_confidence * 1.2, 1.0)
        
        return base_confidence

class TextRankExtractor(BaseExtractor):
    """Improved English-optimized TextRank implementation"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.method_name = "textrank"
        self.window_size = config.get('window_size', 4) if config else 4
        
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        try:
            import networkx as nx
            import nltk
            from nltk.tokenize import word_tokenize, sent_tokenize
            from nltk.corpus import stopwords
            from nltk.tag import pos_tag
            from collections import defaultdict, Counter
            import itertools
            
            # Download required NLTK data if not present
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
            
            # Extract keywords using improved TextRank
            keywords = self._extract_textrank_keywords(text)
            
            return ExtractionResult(
                keywords=keywords,
                metadata={
                    'method': 'textrank_english',
                    'window_size': self.window_size,
                    'implementation': 'networkx_nltk'
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=self._calculate_textrank_confidence(keywords)
            )
            
        except ImportError as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': f'Dependencies not available: {e}', 'method': 'textrank'},
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
    
    def _extract_textrank_keywords(self, text: str) -> List[Dict]:
        """Extract keywords using English-optimized TextRank"""
        import networkx as nx
        import nltk
        from nltk.tokenize import word_tokenize, sent_tokenize
        from nltk.corpus import stopwords
        from nltk.tag import pos_tag
        from collections import defaultdict
        import itertools
        
        # Preprocess text
        sentences = sent_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        
        # Extract candidate words
        candidate_words = []
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            pos_tags = pos_tag(tokens)
            
            # Filter for nouns, adjectives, and proper nouns
            candidates = [word for word, pos in pos_tags 
                         if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS'] 
                         and word not in stop_words 
                         and len(word) > 2
                         and word.isalpha()]
            candidate_words.extend(candidates)
        
        if not candidate_words:
            return []
        
        # Build co-occurrence graph
        graph = nx.Graph()
        word_freq = defaultdict(int)
        
        for sentence in sentences:
            tokens = [word for word in word_tokenize(sentence.lower()) 
                     if word in candidate_words]
            
            # Add nodes
            for word in tokens:
                graph.add_node(word)
                word_freq[word] += 1
            
            # Add edges within window
            for i, word1 in enumerate(tokens):
                for j in range(i + 1, min(i + self.window_size + 1, len(tokens))):
                    word2 = tokens[j]
                    if word1 != word2:
                        if graph.has_edge(word1, word2):
                            graph[word1][word2]['weight'] += 1
                        else:
                            graph.add_edge(word1, word2, weight=1)
        
        if not graph.nodes():
            return []
        
        # Apply PageRank algorithm
        try:
            pagerank_scores = nx.pagerank(graph, weight='weight', max_iter=100, tol=1e-4)
        except:
            # Fallback to degree centrality if PageRank fails
            pagerank_scores = nx.degree_centrality(graph)
        
        # Combine with frequency information
        combined_scores = {}
        for word, score in pagerank_scores.items():
            freq_bonus = min(word_freq[word] / 10.0, 0.5)  # Frequency bonus
            combined_scores[word] = score + freq_bonus
        
        # Sort and format results
        sorted_words = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        keywords = []
        for i, (word, score) in enumerate(sorted_words[:20]):
            keywords.append({
                'keyword': word,
                'score': score,
                'rank': i + 1,
                'type': 'textrank_keyword',
                'relevance': score
            })
        
        return keywords
    
    def _calculate_textrank_confidence(self, keywords: List) -> float:
        if not keywords:
            return 0.0
        scores = [kw['score'] for kw in keywords]
        return min(np.mean(scores), 1.0) if scores else 0.0

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
            import re
            
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
        import re
        
        # Preserve important phrases by replacing spaces with underscores
        important_phrases = [
            'machine learning', 'natural language processing', 'artificial intelligence',
            'data science', 'deep learning', 'computer vision', 'sentiment analysis',
            'social media', 'supply chain', 'digital transformation', 'blockchain technology',
            'cloud computing', 'user experience', 'user interface', 'startup funding',
            'sustainable fashion', 'renewable energy', 'climate change'
        ]
        
        processed_text = text.lower()
        for phrase in important_phrases:
            processed_text = processed_text.replace(phrase, phrase.replace(' ', '_'))
        
        return processed_text
    
    def _create_tfidf_corpus(self, text: str) -> List[str]:
        """Create corpus with multiple perspectives"""
        import re
        
        corpus = []
        
        # Original text
        corpus.append(text)
        
        # Split by sentences
        sentences = re.split(r'[.!?]+', text)
        corpus.extend([s.strip() for s in sentences if len(s.strip()) > 10])
        
        # Split by semantic chunks (phrases between commas)
        chunks = re.split(r'[,;]+', text)
        corpus.extend([c.strip() for c in chunks if len(c.strip()) > 5])
        
        # Create artificial sentences to boost important terms
        words = text.split()
        if len(words) > 5:
            # Take sliding windows of words
            for i in range(0, len(words) - 4, 3):
                window = ' '.join(words[i:i+5])
                corpus.append(window)
        
        return [doc for doc in corpus if doc.strip()]
    
    def _post_process_tfidf_keywords(self, feature_names, scores, original_text: str) -> List:
        """Post-process TF-IDF results for better keywords"""
        import re
        
        # Combine features with scores
        feature_scores = list(zip(feature_names, scores))
        
        # Filter and enhance
        processed = []
        original_lower = original_text.lower()
        
        for feature, score in feature_scores:
            if score <= 0:
                continue
                
            # Restore original phrases (replace underscores back with spaces)
            clean_feature = feature.replace('_', ' ')
            
            # Boost scores for multi-word phrases
            word_count = len(clean_feature.split())
            if word_count > 1:
                score *= 1.5  # Boost multi-word phrases
            
            # Boost if exact phrase appears in original text
            if clean_feature in original_lower:
                score *= 1.3
            
            # Filter out very short single words with low scores
            if word_count == 1 and len(clean_feature) < 3 and score < 0.1:
                continue
            
            processed.append((clean_feature, score))
        
        # Sort by enhanced scores
        processed.sort(key=lambda x: x[1], reverse=True)
        
        # Remove duplicates while preserving order
        seen = set()
        final_keywords = []
        for keyword, score in processed:
            if keyword.lower() not in seen:
                seen.add(keyword.lower())
                final_keywords.append((keyword, score))
        
        return final_keywords

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
