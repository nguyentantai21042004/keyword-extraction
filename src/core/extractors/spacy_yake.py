"""
SpaCy + YAKE keyword extraction implementation
"""

import numpy as np
from typing import Dict, List, Optional
from ..base_extractor import BaseExtractor, ExtractionResult

class SpacyYakeExtractor(BaseExtractor):
    """Primary method - spaCy + YAKE combination for keyword extraction"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config)
        self.method_name = "spacy_yake"
        self.nlp = None
        self.yake_extractor = None
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize spaCy and YAKE models with error handling"""
        try:
            import spacy
            import yake
            
            # Load spaCy model with fallback
            model_name = self.config.get('spacy_model', 'en_core_web_sm')
            try:
                self.nlp = spacy.load(model_name)
                self.logger.info(f"Loaded spaCy model: {model_name}")
            except OSError:
                self.logger.warning(f"Model {model_name} not found, attempting download")
                spacy.cli.download(model_name)
                self.nlp = spacy.load(model_name)
            
            # Initialize YAKE with configurable parameters
            yake_config = {
                'lan': self.config.get('yake_language', 'en'),
                'n': self.config.get('yake_n', 2),
                'dedupLim': self.config.get('yake_dedup_lim', 0.8),
                'top': self.config.get('yake_max_keywords', 30),
                'features': None
            }
            
            self.yake_extractor = yake.KeywordExtractor(**yake_config)
            self.logger.info(f"Initialized YAKE with config: {yake_config}")
            
        except ImportError as e:
            self.logger.error(f"Failed to import required libraries: {e}")
            self.nlp = None
            self.yake_extractor = None
        except Exception as e:
            self.logger.error(f"Unexpected error during model initialization: {e}")
            self.nlp = None
            self.yake_extractor = None
        
    @BaseExtractor._measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        """Extract keywords using spaCy + YAKE combination"""
        
        # Validate input
        if not self.validate_text(text):
            return ExtractionResult(
                method_name=self.method_name,
                success=False,
                error_message="Invalid input text",
                metadata={'error': 'Invalid input text'}
            )
        
        # Check if models are loaded
        if not self.nlp or not self.yake_extractor:
            return ExtractionResult(
                method_name=self.method_name,
                success=False,
                error_message="Models not initialized",
                metadata={'error': 'Models not loaded'}
            )
        
        try:
            # Process with spaCy for linguistic features
            doc = self.nlp(text)
            
            # Extract linguistic features
            entities = self._extract_entities(doc)
            noun_chunks = self._extract_noun_chunks(doc)
            
            # Extract statistical keywords with YAKE
            yake_keywords = self.yake_extractor.extract_keywords(text)
            
            # Combine and score all keywords
            keywords = self._combine_keyword_sources(yake_keywords, entities, noun_chunks)
            
            # Normalize and validate keywords
            keywords = self._normalize_keywords(keywords)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(keywords, entities, noun_chunks)
            
            # Limit results based on configuration
            max_keywords = self.config.get('max_keywords', 30)
            final_keywords = keywords[:max_keywords]
            
            return ExtractionResult(
                keywords=final_keywords,
                metadata={
                    'method': self.method_name,
                    'entities_count': len(entities),
                    'noun_chunks_count': len(noun_chunks),
                    'yake_keywords_count': len(yake_keywords),
                    'total_candidates': len(keywords),
                    'final_count': len(final_keywords)
                },
                method_name=self.method_name,
                confidence_score=confidence,
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Error during extraction: {str(e)}")
            return ExtractionResult(
                method_name=self.method_name,
                success=False,
                error_message=str(e),
                metadata={'error': str(e)}
            )
    
    def _extract_entities(self, doc) -> List[tuple]:
        """Extract and filter named entities"""
        entities = []
        for ent in doc.ents:
            # Filter entities by quality criteria
            if (len(ent.text.split()) <= 3 and 
                len(ent.text.strip()) > 1 and
                not ent.text.isdigit()):
                entities.append((ent.text.strip(), ent.label_))
        return entities[:15]  # Limit to top 15
    
    def _extract_noun_chunks(self, doc) -> List[str]:
        """Extract and filter noun chunks"""
        chunks = []
        for chunk in doc.noun_chunks:
            # Filter chunks by relevance criteria
            if (len(chunk.text.split()) >= 2 and 
                len(chunk.text.split()) <= 4 and
                len(chunk.text.strip()) > 3):
                chunks.append(chunk.text.strip())
        return chunks[:20]  # Limit to top 20
    
    def _combine_keyword_sources(self, yake_keywords: List[tuple], 
                               entities: List[tuple], 
                               noun_chunks: List[str]) -> List[Dict]:
        """Combine keywords from different sources with appropriate scoring"""
        keywords = []
        
        # Add YAKE keywords (statistical)
        for i, (keyword, score) in enumerate(yake_keywords):
            keywords.append({
                'keyword': keyword.strip(),
                'score': 1.0 - score,  # YAKE: lower is better, so invert
                'rank': i + 1,
                'type': 'statistical',
                'relevance': 1.0 - score
            })
        
        # Add named entities (linguistic)
        entity_score = self.config.get('entity_weight', 0.7)
        for entity, label in entities:
            keywords.append({
                'keyword': entity,
                'score': entity_score,
                'rank': len(keywords) + 1,
                'type': f'entity_{label.lower()}',
                'relevance': entity_score
            })
        
        # Add noun chunks (syntactic)
        chunk_score = self.config.get('chunk_weight', 0.5)
        for chunk in noun_chunks:
            keywords.append({
                'keyword': chunk,
                'score': chunk_score,
                'rank': len(keywords) + 1,
                'type': 'syntactic',
                'relevance': chunk_score
            })
        
        # Sort by score descending
        keywords.sort(key=lambda x: x['score'], reverse=True)
        
        # Re-rank after sorting
        for i, kw in enumerate(keywords):
            kw['rank'] = i + 1
        
        return keywords
    
    def _calculate_confidence(self, keywords: List[Dict], 
                            entities: List[tuple], 
                            noun_chunks: List[str]) -> float:
        """Calculate confidence score based on extraction quality"""
        if not keywords:
            return 0.0
        
        # Base confidence from keyword count and quality
        keyword_count_score = min(len(keywords) / 30.0, 1.0)
        
        # Diversity bonus from different source types
        source_types = set(kw['type'] for kw in keywords)
        diversity_bonus = min(len(source_types) / 4.0, 0.2)
        
        # Entity quality bonus
        entity_types = set(label for _, label in entities) if entities else set()
        entity_bonus = min(len(entity_types) / 5.0, 0.15)
        
        # Score distribution quality
        scores = [kw['score'] for kw in keywords]
        score_variance = np.var(scores) if len(scores) > 1 else 0
        variance_bonus = min(score_variance, 0.15)
        
        # Combine all factors
        confidence = keyword_count_score + diversity_bonus + entity_bonus + variance_bonus
        return min(confidence, 1.0)
