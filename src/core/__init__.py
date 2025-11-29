"""
Core functionality for the Keyword Extraction Framework
"""

from .base_extractor import BaseExtractor, ExtractionResult, ExtractionMethod
from .extractors import SpacyYakeExtractor

__all__ = [
    'BaseExtractor', 'ExtractionResult', 'ExtractionMethod',
    'SpacyYakeExtractor'
]
