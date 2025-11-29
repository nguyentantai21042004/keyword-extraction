# Project Context

## Purpose
SMAP Keyword Extraction Framework - A production-ready keyword extraction system focused on the SpaCy + YAKE method. The framework provides high-performance keyword extraction with 76.2% overall performance and 38.21% accuracy across diverse text domains. Supports English and Vietnamese text processing.

**Note**: This project is being refactored to focus exclusively on the SpaCy + YAKE extractor with complete logic and comprehensive tests. Other extractors (RAKE, TF-IDF, TextRank, KeyBERT, Hybrid Ensemble) will be removed.

## Tech Stack
- **Python 3.8+** - Core language
- **spaCy 3.4+** - Natural language processing and linguistic feature extraction
- **YAKE 0.4.8+** - Statistical keyword extraction algorithm
- **NumPy 1.21+** - Numerical computations
- **Pandas 1.3+** - Data processing and analysis
- **Matplotlib 3.5+ / Seaborn 0.11+** - Data visualization
- **PyYAML 6.0+** - Configuration management
- **psutil 5.8+** - System and performance monitoring
- **pytest 6.2+ / pytest-asyncio 0.18+** - Testing framework
- **Black 22.0+** - Code formatting
- **Flake8 4.0+** - Linting
- **mypy 0.950+** - Type checking

## Project Conventions

### Code Style
- **Type hints**: Use type hints for all function parameters and return values
- **Async/await**: All extraction methods are async for better performance
- **Dataclasses**: Use `@dataclass` for configuration and result objects
- **Naming**: 
  - Classes: PascalCase (e.g., `SpacyYakeExtractor`)
  - Functions/methods: snake_case (e.g., `extract_keywords`)
  - Constants: UPPER_SNAKE_CASE
- **Docstrings**: All public classes and methods should have docstrings
- **Formatting**: Use Black for code formatting
- **Line length**: Follow PEP 8 (typically 88-100 characters with Black)

### Architecture Patterns
- **Abstract Base Classes**: All extractors inherit from `BaseExtractor` with abstract `extract()` method
- **Configuration Management**: Centralized YAML-based configuration via `ConfigManager`
- **Result Objects**: Structured `ExtractionResult` dataclass containing keywords, metadata, and performance metrics
- **Performance Monitoring**: Built-in decorator `_measure_performance` tracks processing time and memory usage
- **Error Handling**: Graceful error handling with error messages in result objects
- **Logging**: Structured logging with context managers (`LogContext`)
- **Modular Design**: Clear separation between core extractors, utilities, configuration, and analysis modules

### Testing Strategy
- **Framework**: pytest with pytest-asyncio for async tests
- **Test Structure**: 
  - Unit tests for individual extractor methods
  - Integration tests for full extraction pipeline
  - Performance tests for benchmarking
- **Test Coverage**: Focus on comprehensive tests for SpaCy + YAKE extractor
- **Test Data**: Use diverse text samples from different domains (social media, technical, business, academic, Vietnamese)
- **Async Testing**: All extraction tests use async/await patterns
- **Fixtures**: Reusable test fixtures for common test scenarios

### Git Workflow
- **Branching**: Feature branches for new functionality, main branch for stable code
- **Commits**: Descriptive commit messages following conventional commits format
- **Code Review**: All changes should be reviewed before merging

## Domain Context
- **Keyword Extraction**: The process of automatically identifying important terms and phrases from text
- **SpaCy + YAKE Method**: Combines linguistic features (named entities, noun chunks) from spaCy with statistical keyword extraction from YAKE
- **Multilingual Support**: Primary support for English and Vietnamese text
- **Text Domains**: 
  - Social media (hashtags, mentions, short text)
  - Technical documentation
  - Business reports
  - Academic papers
  - Challenging texts (low keyword density)
- **Performance Metrics**: 
  - Accuracy: Percentage of correctly extracted keywords
  - Processing time: Milliseconds per extraction
  - Memory usage: MB consumed during processing
  - Confidence score: Quality indicator (0.0-1.0)
- **Keyword Types**: 
  - Statistical (from YAKE)
  - Named entities (PERSON, ORG, GPE, etc.)
  - Syntactic (noun chunks)

## Important Constraints
- **Text Length Limit**: Maximum 10,000 characters per text input
- **Processing Timeout**: 30 seconds default timeout per extraction
- **Memory Monitoring**: Track memory usage to prevent resource exhaustion
- **Model Dependencies**: Requires spaCy language models (e.g., `en_core_web_sm`) to be downloaded separately
- **Python Version**: Minimum Python 3.8 required
- **Async Operations**: All extraction operations must be async for scalability
- **Result Validation**: All extracted keywords must be non-empty strings
- **Configuration**: YAML-based configuration with fallback to defaults

## External Dependencies
- **spaCy Models**: 
  - `en_core_web_sm` - English small model (default)
  - Models must be downloaded via `python -m spacy download <model>`
- **YAKE Library**: Statistical keyword extraction algorithm
- **NLTK Data**: Required for some text processing utilities (punkt, stopwords)
- **System Resources**: 
  - CPU for NLP processing
  - RAM for model loading and text processing
  - Disk space for model storage (~50MB for small models)
