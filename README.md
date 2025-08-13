# 🎓 Enhanced Multi-Method Keyword Extraction Research Framework

A comprehensive research framework for comparing and benchmarking multiple keyword extraction methods with Vietnamese language support.

## 🏗️ Project Structure

```
smap-keyword-extraction/
├── src/                          # Source code chính
│   ├── __init__.py
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── base_extractor.py     # Base classes và interfaces
│   │   ├── extractors/           # Các thuật toán extraction
│   │   │   ├── __init__.py
│   │   │   ├── spacy_yake.py
│   │   │   ├── rake.py
│   │   │   ├── textrank.py
│   │   │   ├── tfidf.py
│   │   │   └── keybert.py
│   │   ├── ensemble/             # Ensemble methods
│   │   │   ├── __init__.py
│   │   │   └── hybrid_ensemble.py
│   │   └── utils/                # Utility functions
│   │       ├── __init__.py
│   │       ├── performance.py
│   │       └── text_processing.py
│   ├── benchmark/                 # Benchmarking framework
│   │   ├── __init__.py
│   │   ├── benchmark_framework.py
│   │   ├── test_datasets.py
│   │   └── metrics.py
│   ├── analysis/                  # Analysis và optimization
│   │   ├── __init__.py
│   │   ├── optimization_analyzer.py
│   │   └── performance_analyzer.py
│   ├── visualization/             # Visualization
│   │   ├── __init__.py
│   │   └── charts.py
│   └── config/                    # Configuration
│       ├── __init__.py
│       ├── settings.py
│       └── constants.py
├── experiments/                   # Experiments và research
│   ├── __init__.py
│   ├── guides/
│ │   ├── __init__.py
│ │   └── experiment_guide.md
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── run_complete_experiment.py
│   │   ├── run_enhanced_experiment.py
│   │   └── run_optimized_experiment.py
│   ├── results/
│   └── visualizations/
├── tests/                         # Test files
│   ├── __init__.py
│   ├── test_extractors.py
│   ├── test_benchmark.py
│   └── test_ensemble.py
├── scripts/                       # Utility scripts
│   ├── demo.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🚀 Features

### Core Algorithms
- **SpaCy + YAKE**: Primary method combining NLP and statistical extraction
- **RAKE + NLTK**: Fast baseline method for phrase extraction
- **TextRank**: Graph-based keyword extraction
- **TF-IDF**: Statistical baseline method
- **KeyBERT**: Semantic keyword extraction using transformers
- **Hybrid Ensemble**: Intelligent combination of multiple methods

### Enhanced Capabilities
- **Multilingual Support**: English and Vietnamese text processing
- **25+ Test Cases**: Comprehensive test dataset including social media, business, and technical content
- **Performance Metrics**: Processing time, memory usage, accuracy, and confidence scoring
- **Visualization**: Comprehensive charts and analysis plots
- **Optimization Analysis**: Performance gap identification and recommendations

### Research Features
- **Benchmarking Framework**: Systematic comparison of all methods
- **Domain Analysis**: Performance analysis across different text categories
- **Language Analysis**: Cross-language performance comparison
- **Complexity Analysis**: Performance based on text complexity levels

## 📦 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd smap-keyword-extraction
```

2. **Create virtual environment**:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install additional models** (if needed):
```bash
python -m spacy download en_core_web_sm
```

## 🎯 Usage

### Quick Start

Run the complete research framework:

```bash
python scripts/main.py
```

### Individual Components

```python
from src.core import SpacyYakeExtractor, RakeExtractor
from src.benchmark import ExtractionBenchmark

# Initialize extractors
extractor = SpacyYakeExtractor()

# Extract keywords
result = await extractor.extract("Your text here")
print(result.keywords)

# Run benchmark
benchmark = ExtractionBenchmark()
# Add test cases and run...
```

### Custom Configuration

```python
from src.config import METHOD_CONFIGS, OPTIMIZATION_WEIGHTS

# Customize method parameters
config = METHOD_CONFIGS['spacy_yake'].copy()
config['yake_max_keywords'] = 30

extractor = SpacyYakeExtractor(config)
```

## 📊 Output

The framework generates:

- **CSV Results**: Detailed benchmark results
- **JSON Reports**: Comprehensive analysis reports
- **Visualizations**: Performance comparison charts
- **Text Reports**: Human-readable optimization recommendations

## 🔬 Experiments

### Running Experiments

```bash
# Complete experiment
python experiments/scripts/run_complete_experiment.py

# Enhanced experiment
python experiments/scripts/run_enhanced_experiment.py

# Optimized experiment
python experiments/scripts/run_optimized_experiment.py
```

### Custom Experiments

Create your own experiment scripts in `experiments/scripts/` following the existing patterns.

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python tests/test_extractors.py
```

## 📈 Performance

### Benchmark Results

The framework provides comprehensive performance analysis:

- **Accuracy Metrics**: Precision, recall, F1-score with exact and partial matching
- **Performance Metrics**: Processing time and memory usage
- **Confidence Scoring**: Method-specific confidence evaluation
- **Cross-Domain Analysis**: Performance across different text categories

### Optimization Recommendations

Automatic identification of:
- Performance bottlenecks
- Accuracy gaps
- Memory optimization opportunities
- Processing time improvements

## 🌍 Multilingual Support

### Vietnamese Language Features

- **Character Detection**: Automatic Vietnamese diacritic recognition
- **Language-Specific Processing**: Optimized for Vietnamese text characteristics
- **Cross-Language Comparison**: Performance analysis between English and Vietnamese

### Supported Languages

- **English**: Full support with optimized models
- **Vietnamese**: Enhanced support with diacritic handling
- **Mixed Content**: Automatic language detection and processing

## 🔧 Configuration

### Method Parameters

Each extraction method can be configured independently:

```python
# SpaCy + YAKE configuration
spacy_yake_config = {
    'spacy_model': 'en_core_web_sm',
    'yake_language': 'en',
    'yake_max_keywords': 20,
    'yake_dedup_lim': 0.9
}

# RAKE configuration
rake_config = {
    'min_phrase_length': 2,
    'max_phrase_length': 4,
    'min_frequency': 1
}
```

### Optimization Weights

Customize performance evaluation criteria:

```python
# Balanced optimization
balanced_weights = {
    'processing_time': 0.20,
    'memory_usage': 0.20,
    'confidence_score': 0.20,
    'accuracy': 0.25,
    'success_rate': 0.15
}
```

## 📚 Documentation

- **Algorithm Guides**: Detailed explanations in `docs/algorithms/`
- **Experiment Guide**: Step-by-step experiment instructions
- **API Reference**: Comprehensive code documentation
- **Examples**: Usage examples and best practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Research team for algorithm implementations
- Open source community for dependencies
- Academic institutions for research support

## 📞 Contact

For questions and support:
- Create an issue in the repository
- Contact the research team
- Check the documentation

---

**Note**: This framework is designed for research purposes and may require additional dependencies for production use.
