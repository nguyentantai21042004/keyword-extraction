"""
Base classes and interfaces for keyword extraction methods
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union

import psutil

@dataclass
class ExtractionResult:
    """Result of keyword extraction operation"""
    keywords: List[Dict[str, Union[str, float, int]]] = field(default_factory=list)
    metadata: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    method_name: str = ""
    processing_time: float = 0.0
    memory_usage: float = 0.0
    confidence_score: float = 0.0
    success: bool = True
    error_message: Optional[str] = None

class ExtractionMethod(Enum):
    """Enumeration of available extraction methods"""
    SPACY_YAKE = "spacy_yake"
    RAKE_NLTK = "rake_nltk" 
    TEXTRANK = "textrank"
    KEYBERT = "keybert"
    TF_IDF = "tf_idf"
    HYBRID_ENSEMBLE = "hybrid_ensemble"

class BaseExtractor(ABC):
    """Abstract base class for all extraction methods"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.method_name = ""
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        
    @abstractmethod
    async def extract(self, text: str) -> ExtractionResult:
        """Extract keywords from text"""
        pass
    
    def validate_text(self, text: str) -> bool:
        """Validate input text"""
        if not isinstance(text, str):
            return False
        if not text or not text.strip():
            return False
        if len(text) > 10000:  # Max length check
            self.logger.warning(f"Text length {len(text)} exceeds recommended limit")
        return True
    
    def _normalize_keywords(self, keywords: List[Dict]) -> List[Dict]:
        """Normalize keyword format"""
        normalized = []
        for kw in keywords:
            if isinstance(kw, dict) and 'keyword' in kw:
                normalized_kw = {
                    'keyword': str(kw['keyword']).strip(),
                    'score': float(kw.get('score', 0.0)),
                    'rank': int(kw.get('rank', len(normalized) + 1)),
                    'type': str(kw.get('type', 'unknown')),
                    'relevance': float(kw.get('relevance', kw.get('score', 0.0)))
                }
                if normalized_kw['keyword']:  # Only add non-empty keywords
                    normalized.append(normalized_kw)
        return normalized
    
    @staticmethod
    def _measure_performance(func):
        """Decorator to measure performance metrics"""
        async def wrapper(self, *args, **kwargs):
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            try:
                result = await func(self, *args, **kwargs)
                
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                result.processing_time = end_time - start_time
                result.memory_usage = max(0, end_memory - start_memory)  # Ensure non-negative
                result.performance_metrics = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'memory_delta': result.memory_usage
                }
                
                return result
                
            except Exception as e:
                self.logger.error(f"Error in {self.method_name}: {str(e)}")
                return ExtractionResult(
                    method_name=self.method_name,
                    processing_time=time.perf_counter() - start_time,
                    success=False,
                    error_message=str(e),
                    metadata={'error': str(e)}
                )
        return wrapper
