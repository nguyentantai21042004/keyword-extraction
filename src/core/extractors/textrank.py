"""
TextRank keyword extraction implementation
"""

from typing import Dict, List
from ..base_extractor import BaseExtractor, ExtractionResult

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
        
        # Build co-occurrence matrix
        word_freq = Counter(candidate_words)
        co_occurrence = defaultdict(int)
        
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            sentence_candidates = [word for word in tokens if word in word_freq]
            
            for i, word1 in enumerate(sentence_candidates):
                for j in range(i + 1, min(i + self.window_size + 1, len(sentence_candidates))):
                    word2 = sentence_candidates[j]
                    if word1 != word2:
                        co_occurrence[(word1, word2)] += 1
                        co_occurrence[(word2, word1)] += 1
        
        # Build graph
        G = nx.Graph()
        for word in word_freq:
            G.add_node(word, weight=word_freq[word])
        
        for (word1, word2), weight in co_occurrence.items():
            G.add_edge(word1, word2, weight=weight)
        
        # Calculate TextRank scores
        try:
            scores = nx.pagerank(G, alpha=0.85, max_iter=100)
        except:
            # Fallback to degree centrality if pagerank fails
            scores = nx.degree_centrality(G)
        
        # Create keyword results
        keywords = []
        for word, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]:
            keywords.append({
                'keyword': word,
                'score': score,
                'rank': len(keywords) + 1,
                'type': 'textrank_keyword',
                'relevance': min(score * 10, 1.0)  # Normalize score
            })
        
        return keywords
    
    def _calculate_textrank_confidence(self, keywords: List[Dict]) -> float:
        """Calculate confidence score for TextRank method"""
        if not keywords:
            return 0.0
        
        # Base confidence from average score
        avg_score = sum(kw['score'] for kw in keywords) / len(keywords)
        base_confidence = min(avg_score * 5, 1.0)  # Normalize to 0-1
        
        # Bonus for keyword diversity
        unique_keywords = len(set(kw['keyword'] for kw in keywords))
        diversity_bonus = min(unique_keywords / 15.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for number of keywords
        count_bonus = min(len(keywords) / 20.0, 0.1)  # Max 0.1 bonus
        
        confidence = base_confidence + diversity_bonus + count_bonus
        return min(confidence, 1.0)
