"""
Constants for the Keyword Extraction Framework
"""

# Extraction method names
EXTRACTION_METHODS = {
    'SPACY_YAKE': 'spacy_yake',
    'RAKE_NLTK': 'rake_nltk',
    'TEXTRANK': 'textrank',
    'KEYBERT': 'keybert',
    'TF_IDF': 'tf_idf',
    'HYBRID_ENSEMBLE': 'hybrid_ensemble'
}

# Text categories
TEXT_CATEGORIES = {
    'SOCIAL_MEDIA': 'social_media',
    'BUSINESS': 'business',
    'TECHNICAL': 'technical',
    'SHORT_TEXT': 'short_text',
    'CUSTOM': 'custom'
}

# Language codes
LANGUAGES = {
    'ENGLISH': 'en',
    'VIETNAMESE': 'vi'
}

# Complexity levels
COMPLEXITY_LEVELS = {
    'LOW': 'low',
    'MEDIUM': 'medium',
    'HIGH': 'high',
    'VERY_HIGH': 'very_high'
}

# Performance metrics
PERFORMANCE_METRICS = {
    'PROCESSING_TIME': 'processing_time',
    'MEMORY_USAGE': 'memory_usage',
    'CONFIDENCE_SCORE': 'confidence_score',
    'ACCURACY': 'accuracy',
    'SUCCESS_RATE': 'success_rate'
}

# File extensions
FILE_EXTENSIONS = {
    'CSV': 'csv',
    'JSON': 'json',
    'TXT': 'txt',
    'PNG': 'png',
    'PDF': 'pdf'
}

# Default values
DEFAULT_VALUES = {
    'MAX_KEYWORDS': 20,
    'TIMEOUT_SECONDS': 30,
    'CONFIDENCE_THRESHOLD': 0.5,
    'DIVERSITY_THRESHOLD': 0.8
}

# Error messages
ERROR_MESSAGES = {
    'MODEL_LOAD_FAILED': 'Failed to load model: {}',
    'EXTRACTION_FAILED': 'Keyword extraction failed: {}',
    'INVALID_TEXT': 'Invalid text input: {}',
    'TIMEOUT_ERROR': 'Operation timed out after {} seconds',
    'MEMORY_ERROR': 'Insufficient memory for operation'
}

# Success messages
SUCCESS_MESSAGES = {
    'EXTRACTION_COMPLETED': 'Keyword extraction completed successfully',
    'BENCHMARK_COMPLETED': 'Benchmark completed successfully',
    'OPTIMIZATION_COMPLETED': 'Optimization completed successfully',
    'VISUALIZATION_CREATED': 'Visualization created successfully'
}
