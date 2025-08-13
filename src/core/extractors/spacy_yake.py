"""
SpaCy + YAKE keyword extraction implementation
"""

from typing import Dict, List
from ..base_extractor import BaseExtractor, ExtractionResult

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
        """Calculate confidence score for spaCy+YAKE method"""
        if not keywords:
            return 0.0
        
        # Base confidence from keyword quality
        base_confidence = min(len(keywords) / 30.0, 1.0)  # Normalize to 0-1
        
        # Bonus for entity diversity
        entity_types = set(label for _, label in entities)
        entity_bonus = min(len(entity_types) / 5.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for noun chunk quality
        avg_chunk_length = sum(len(chunk.split()) for chunk in noun_chunks) / max(len(noun_chunks), 1)
        chunk_bonus = min(avg_chunk_length / 3.0, 0.1)  # Max 0.1 bonus
        
        # Final confidence
        confidence = base_confidence + entity_bonus + chunk_bonus
        return min(confidence, 1.0)
