"""
Base classes and interfaces for keyword extraction methods
"""

import asyncio
import time
import psutil
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class ExtractionResult:
    """Result of keyword extraction operation"""
    keywords: List[Dict]
    metadata: Dict
    performance_metrics: Dict
    method_name: str
    processing_time: float
    memory_usage: float
    confidence_score: float

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
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.method_name = ""
        
    @abstractmethod
    async def extract(self, text: str) -> ExtractionResult:
        """Extract keywords from text"""
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
