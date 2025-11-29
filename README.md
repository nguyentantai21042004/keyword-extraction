# 🚀 SMAP Keyword Extraction Framework

A production-ready keyword extraction framework focused on the **SpaCy + YAKE** method. Achieves **76.2% overall performance** and **38.21% accuracy** across diverse text domains. Supports English and Vietnamese text processing.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Key Features

- **🏆 High Performance**: 76.2% overall score, 38.21% accuracy
- **⚡ Fast Processing**: 15.93ms average response time
- **🌐 Multilingual**: English and Vietnamese text processing
- **🔬 Hybrid Method**: Combines NLP (spaCy) and statistical analysis (YAKE)
- **📊 Production-Ready**: Complete implementation with comprehensive tests

## 🛠️ Tech Stack

- **Python 3.8+** - Core language
- **spaCy 3.4+** - Natural language processing and linguistic feature extraction
- **YAKE 0.4.8+** - Statistical keyword extraction algorithm
- **NumPy 1.21+** - Numerical computations
- **Pandas 1.3+** - Data processing and analysis
- **Matplotlib 3.5+ / Seaborn 0.11+** - Data visualization
- **PyYAML 6.0+** - Configuration management
- **psutil 5.8+** - System and performance monitoring
- **pytest 6.2+ / pytest-asyncio 0.18+** - Testing framework

## 🏗️ Architecture

- **Abstract Base Classes**: All extractors inherit from `BaseExtractor` with abstract `extract()` method
- **Configuration Management**: Centralized YAML-based configuration via `ConfigManager`
- **Result Objects**: Structured `ExtractionResult` dataclass containing keywords, metadata, and performance metrics
- **Performance Monitoring**: Built-in decorator tracks processing time and memory usage
- **Error Handling**: Graceful error handling with error messages in result objects
- **Logging**: Structured logging with context managers
- **Modular Design**: Clear separation between core extractors, utilities, configuration, and analysis modules

## 🚀 Quick Start

### 1. Installation

```bash
# Clone and install
git clone https://github.com/nguyentantai21042004/smap-keyword-extraction.git
cd smap-keyword-extraction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run Tests

```bash
# Quick test (recommended first)
python scripts/test_simple.py

# Demo algorithms
python scripts/demo.py

# Run comprehensive experiments
python scripts/run_experiments.py
```

### 3. Use in Code

```python
import asyncio
from src.core.extractors import SpacyYakeExtractor

async def main():
    extractor = SpacyYakeExtractor()
    result = await extractor.extract("Machine learning algorithms for natural language processing.")
    print(f"Keywords: {[kw['keyword'] for kw in result.keywords]}")

asyncio.run(main())
```

## 🏆 Performance Metrics

### SpaCy + YAKE Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | **38.21%** |
| **Processing Speed** | **15.93ms** |
| **Memory Usage** | **0.99 MB** |
| **Overall Score** | **76.2%** |

### How It Works

The **SpaCy + YAKE** method combines:
- **Linguistic Features** (from spaCy): Named entities, noun chunks
- **Statistical Analysis** (from YAKE): Statistical keyword extraction
- **Intelligent Scoring**: Weighted combination of multiple keyword sources

## 🛠️ Available Commands

| Command | Purpose |
|---------|---------|
| `python scripts/test_simple.py` | Basic test |
| `python scripts/demo.py` | Quick demo |
| `python scripts/run_experiments.py` | **Run everything** |
| `python scripts/generate_charts.py` | Generate charts only |

## 🚨 Common Issues

### spaCy model error
```bash
python -m spacy download en_core_web_sm
```

### NLTK data missing
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Import module error
```bash
# Run from project root directory
cd smap-keyword-extraction
python scripts/test_simple.py
```

## 📖 Detailed Documentation

See "End-to-End Usage Guide" below for advanced usage.

---

## 📖 End-to-End Usage Guide

### Step 1: Configuration Setup

Create a custom configuration file:

```python
# config_demo.py
from src.config import ConfigManager, SpacyYakeConfig

# Create configuration manager
config_manager = ConfigManager("my_config.yaml")

# Get current config
config = config_manager.load_config()

# Customize spaCy + YAKE settings
config.spacy_yake.max_keywords = 50
config.spacy_yake.entity_weight = 0.8
config.spacy_yake.yake_n = 3  # Use trigrams

# Save configuration
config_manager.save_config(config)

print("✅ Configuration saved to my_config.yaml")
```

### Step 2: Single Text Analysis

```python
# single_analysis.py
import asyncio
from src.config import get_config_manager
from src.core.extractors import SpacyYakeExtractor
from src.core.utils import setup_logging

async def analyze_single_text():
    # Setup logging
    logger = setup_logging(__name__)
    logger.info("🚀 Starting single text analysis")
    
    # Load custom configuration
    config_manager = get_config_manager("my_config.yaml")
    extractor_config = config_manager.get_extractor_config("spacy_yake")
    
    # Initialize extractor with custom config
    extractor = SpacyYakeExtractor(extractor_config.__dict__)
    
    # Analyze business text
    business_text = """
    Our Q3 financial results show strong growth in cloud computing revenue, 
    driven by increased enterprise adoption of our AI-powered analytics platform. 
    Digital transformation initiatives across healthcare and fintech sectors 
    contributed significantly to our recurring subscription model success.
    """
    
    try:
        result = await extractor.extract(business_text)
        
        # Detailed analysis
        print("=" * 60)
        print("📈 BUSINESS TEXT ANALYSIS RESULTS")
        print("=" * 60)
        print(f"📊 Keywords found: {len(result.keywords)}")
        print(f"⏱️  Processing time: {result.processing_time:.3f}s")
        print(f"💾 Memory usage: {result.memory_usage:.2f}MB")
        print(f"🎯 Confidence score: {result.confidence_score:.1%}")
        print(f"✅ Success: {result.success}")
        print()
        
        # Group keywords by type
        keyword_types = {}
        for kw in result.keywords:
            kw_type = kw['type']
            if kw_type not in keyword_types:
                keyword_types[kw_type] = []
            keyword_types[kw_type].append(kw)
        
        # Display by type
        for kw_type, keywords in keyword_types.items():
            print(f"🏷️  {kw_type.title()} Keywords:")
            for kw in keywords[:5]:  # Top 5 per type
                print(f"   • {kw['keyword']} (score: {kw['score']:.3f})")
            print()
            
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")

# Run analysis
asyncio.run(analyze_single_text())
```

### Step 3: Batch Processing

```python
# batch_processing.py
import asyncio
from pathlib import Path
from src.core.extractors import SpacyYakeExtractor
from src.core.utils import LogContext, get_logger

async def process_batch():
    logger = get_logger(__name__)
    extractor = SpacyYakeExtractor()
    
    # Sample texts from different domains
    texts = {
        "social_media": """
        Just discovered #sustainablefashion trends! 🌱 @patagonia's new eco-line 
        is amazing. The collection features organic cotton and recycled materials. 
        #ecofriendly #fashiontech #innovation
        """,
        
        "technical": """
        Our microservices architecture leverages Kubernetes for container orchestration, 
        implementing circuit breaker patterns for fault tolerance. The API gateway 
        handles load balancing and rate limiting across distributed services.
        """,
        
        "academic": """
        This study investigates the efficacy of transformer-based models for 
        cross-lingual semantic similarity tasks. We evaluate BERT, RoBERTa, 
        and XLM-R on multilingual benchmark datasets.
        """
    }
    
    results = {}
    
    with LogContext(logger, "batch processing", level=logger.INFO):
        for domain, text in texts.items():
            logger.info(f"Processing {domain} text...")
            
            result = await extractor.extract(text)
            results[domain] = result
            
            print(f"\n📋 {domain.title()} Domain Results:")
            print(f"   Keywords: {len(result.keywords)}")
            print(f"   Top 3: {', '.join([kw['keyword'] for kw in result.keywords[:3]])}")
            print(f"   Time: {result.processing_time:.3f}s")
            print(f"   Confidence: {result.confidence_score:.1%}")
    
    # Performance summary
    print("\n📊 BATCH PROCESSING SUMMARY")
    print("=" * 50)
    avg_time = sum(r.processing_time for r in results.values()) / len(results)
    avg_confidence = sum(r.confidence_score for r in results.values()) / len(results)
    total_keywords = sum(len(r.keywords) for r in results.values())
    
    print(f"Total texts processed: {len(texts)}")
    print(f"Average processing time: {avg_time:.3f}s")
    print(f"Average confidence: {avg_confidence:.1%}")
    print(f"Total keywords extracted: {total_keywords}")

asyncio.run(process_batch())
```

### Step 4: Benchmarking

```python
# benchmark.py
import asyncio
from src.benchmark import ExtractionBenchmark
from src.benchmark.test_datasets import create_research_test_dataset

async def run_benchmark():
    print("🧪 Starting Benchmark")
    print("=" * 50)
    
    # Initialize benchmark
    benchmark = ExtractionBenchmark()
    
    # Load test dataset
    test_cases = create_research_test_dataset()
    
    # Add test cases to benchmark
    for case in test_cases:
        benchmark.add_test_case(
            text=case['text'],
            expected_keywords=case['expected_keywords'],
            category=case['category'],
            language=case.get('language', 'en')
        )
    
    print(f"📋 Loaded {len(test_cases)} test cases")
    print("🔄 Running benchmark...")
    
    # Run benchmark
    results_df = await benchmark.run_comprehensive_benchmark()
    
    # Display summary results
    print("\n📊 BENCHMARK RESULTS SUMMARY")
    print("=" * 60)
    
    # Performance metrics
    avg_accuracy = results_df['accuracy'].mean()
    avg_time = results_df['processing_time'].mean()
    avg_confidence = results_df['confidence_score'].mean()
    
    print(f"Average Accuracy: {avg_accuracy:.1%}")
    print(f"Average Processing Time: {avg_time:.3f}s")
    print(f"Average Confidence: {avg_confidence:.1%}")
    
    # Category performance
    print("\n📈 Performance by Category:")
    category_performance = results_df.groupby('category')['accuracy'].mean().sort_values(ascending=False)
    for category, accuracy in category_performance.items():
        print(f"   {category:15}: {accuracy:.1%}")
    
    # Save results
    results_df.to_csv("benchmark_results.csv", index=False)
    benchmark.save_benchmark_report("benchmark_report.json")
    
    print(f"\n💾 Results saved:")
    print(f"   📄 CSV: benchmark_results.csv")
    print(f"   📋 Report: benchmark_report.json")

# Run the benchmark
asyncio.run(run_benchmark())
```

### Step 5: Advanced Configuration and Optimization

```python
# advanced_optimization.py
import asyncio
from src.config import FrameworkConfig, SpacyYakeConfig, LoggingConfig, LogLevel
from src.core.extractors import SpacyYakeExtractor
from src.analysis import PerformanceAnalyzer

async def optimize_for_domain():
    print("🔬 Advanced Domain Optimization")
    print("=" * 40)
    
    # Create domain-specific configurations
    configs = {
        "social_media": SpacyYakeConfig(
            entity_weight=0.9,  # High weight for hashtags, mentions
            chunk_weight=0.4,   # Lower weight for noun chunks
            yake_n=2,          # Focus on bigrams
            max_keywords=25
        ),
        
        "technical": SpacyYakeConfig(
            entity_weight=0.6,  # Moderate entity weight
            chunk_weight=0.8,   # High weight for technical terms
            yake_n=3,          # Include trigrams for technical phrases
            max_keywords=35
        ),
        
        "business": SpacyYakeConfig(
            entity_weight=0.7,  # Balanced approach
            chunk_weight=0.6,
            yake_n=2,
            max_keywords=30
        )
    }
    
    # Test texts for each domain
    test_texts = {
        "social_media": """
        Breaking: #OpenAI just released #GPT4Turbo with incredible performance improvements! 
        🚀 Faster processing, lower costs, and better accuracy. The AI revolution continues! 
        @developers are going to love this. #ArtificialIntelligence #MachineLearning #Tech
        """,
        
        "technical": """
        Our distributed system architecture implements event-driven microservices using 
        Apache Kafka for message streaming. Container orchestration via Kubernetes ensures 
        high availability and auto-scaling capabilities across multi-cloud environments.
        """,
        
        "business": """
        Q4 revenue growth exceeded projections by 15%, driven by strategic partnerships 
        in emerging markets. Digital transformation initiatives and subscription model 
        expansion contributed to improved customer lifetime value and retention rates.
        """
    }
    
    # Test each configuration
    results = {}
    for domain, config in configs.items():
        print(f"\n🎯 Testing {domain.title()} Configuration:")
        
        extractor = SpacyYakeExtractor(config.__dict__)
        result = await extractor.extract(test_texts[domain])
        results[domain] = result
        
        print(f"   Keywords: {len(result.keywords)}")
        print(f"   Time: {result.processing_time:.3f}s")
        print(f"   Confidence: {result.confidence_score:.1%}")
        print(f"   Top 5: {', '.join([kw['keyword'] for kw in result.keywords[:5]])}")
    
    # Performance comparison
    print(f"\n📊 OPTIMIZATION COMPARISON")
    print("=" * 50)
    for domain, result in results.items():
        print(f"{domain:15} | Time: {result.processing_time:.3f}s | "
              f"Keywords: {len(result.keywords):2d} | "
              f"Confidence: {result.confidence_score:.1%}")

asyncio.run(optimize_for_domain())
```

### Step 6: Production Deployment Script

```python
# production_deploy.py
import asyncio
import logging
from pathlib import Path
from src.config import get_config, get_config_manager
from src.core.extractors import SpacyYakeExtractor
from src.core.utils import setup_logging, LogContext

class ProductionKeywordExtractor:
    """Production-ready keyword extraction service"""
    
    def __init__(self, config_path: str = None):
        # Setup logging for production
        self.logger = setup_logging(__name__)
        
        # Load configuration
        if config_path:
            self.config_manager = get_config_manager(config_path)
        else:
            self.config_manager = get_config_manager()
        
        self.config = self.config_manager.load_config()
        
        # Initialize extractor
        extractor_config = self.config.spacy_yake.__dict__
        self.extractor = SpacyYakeExtractor(extractor_config)
        
        # Performance tracking
        self.request_count = 0
        self.total_processing_time = 0.0
        
        self.logger.info("🚀 Production KeywordExtractor initialized")
    
    async def extract_keywords(self, text: str, request_id: str = None) -> dict:
        """Extract keywords with production logging and monitoring"""
        
        self.request_count += 1
        request_id = request_id or f"req_{self.request_count}"
        
        with LogContext(self.logger, f"keyword extraction [{request_id}]"):
            try:
                # Validate input
                if not text or not text.strip():
                    raise ValueError("Empty text provided")
                
                if len(text) > self.config.max_text_length:
                    self.logger.warning(f"Text length {len(text)} exceeds limit")
                    text = text[:self.config.max_text_length]
                
                # Extract keywords
                result = await self.extractor.extract(text)
                
                # Update metrics
                self.total_processing_time += result.processing_time
                
                # Log performance metrics
                self.logger.info(
                    f"Extraction completed: "
                    f"keywords={len(result.keywords)}, "
                    f"time={result.processing_time:.3f}s, "
                    f"confidence={result.confidence_score:.3f}"
                )
                
                # Return production-ready response
                return {
                    "status": "success",
                    "request_id": request_id,
                    "keywords": result.keywords,
                    "metadata": {
                        "processing_time": result.processing_time,
                        "confidence_score": result.confidence_score,
                        "keywords_count": len(result.keywords),
                        "method": result.method_name
                    }
                }
                
            except Exception as e:
                self.logger.error(f"Extraction failed: {str(e)}")
                return {
                    "status": "error",
                    "request_id": request_id,
                    "error": str(e),
                    "keywords": []
                }
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        avg_time = (self.total_processing_time / self.request_count 
                   if self.request_count > 0 else 0)
        
        return {
            "total_requests": self.request_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_time,
            "requests_per_second": (1.0 / avg_time) if avg_time > 0 else 0
        }

# Production usage example
async def production_demo():
    print("🏭 Production Deployment Demo")
    print("=" * 40)
    
    # Initialize production service
    service = ProductionKeywordExtractor("config.yaml")
    
    # Sample production requests
    sample_requests = [
        {
            "id": "social_001",
            "text": "Excited to announce our new #AI product launch! 🚀 #MachineLearning #Innovation"
        },
        {
            "id": "business_001", 
            "text": "Quarterly revenue increased by 25% due to strategic market expansion."
        },
        {
            "id": "tech_001",
            "text": "Implementing microservices architecture with Docker and Kubernetes orchestration."
        }
    ]
    
    # Process requests
    print("🔄 Processing production requests...\n")
    
    for request in sample_requests:
        response = await service.extract_keywords(
            request["text"], 
            request["id"]
        )
        
        print(f"📋 Request {response['request_id']}:")
        if response["status"] == "success":
            print(f"   ✅ Status: {response['status']}")
            print(f"   ⏱️  Time: {response['metadata']['processing_time']:.3f}s")
            print(f"   🎯 Confidence: {response['metadata']['confidence_score']:.1%}")
            print(f"   📝 Keywords: {len(response['keywords'])}")
            print(f"   🔑 Top 3: {', '.join([kw['keyword'] for kw in response['keywords'][:3]])}")
        else:
            print(f"   ❌ Error: {response['error']}")
        print()
    
    # Display performance statistics
    stats = service.get_performance_stats()
    print("📊 Performance Statistics:")
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Average time: {stats['average_processing_time']:.3f}s")
    print(f"   Throughput: {stats['requests_per_second']:.1f} requests/second")

# Run production demo
asyncio.run(production_demo())
```

---

## 🛠️ Command Line Usage

### All Available Commands

| Command | Purpose | Result |
|---------|---------|--------|
| `python scripts/demo.py` | Quick algorithm demo | Show extraction results |
| `python scripts/test_simple.py` | Basic functionality test | Check framework works |
| `python scripts/run_experiments.py` | **Run comprehensive experiments** | Generate data + charts |
| `python scripts/main.py` | Main entry point | Same as run_experiments.py |
| `python -m src.experiments.run_all` | Run module directly | Same as main.py |
| `python scripts/generate_charts.py` | Generate charts only | Create visualizations from existing data |

### Quick Commands

```bash
# Quickest demo
python scripts/demo.py

# Basic test
python scripts/test_simple.py

# Run comprehensive experiments (Recommended)
python scripts/run_experiments.py

# Generate charts from existing data
python scripts/generate_charts.py
```

### Custom Scripts

```bash
# Create custom analysis script
cat > my_analysis.py << 'EOF'
import asyncio
from src.core.extractors import SpacyYakeExtractor

async def main():
    extractor = SpacyYakeExtractor()
    result = await extractor.extract("Your text here")
    print(f"Keywords: {[kw['keyword'] for kw in result.keywords[:5]]}")

asyncio.run(main())
EOF

# Run script
python my_analysis.py
```

---

## 📊 Performance Benchmarks

### Domain-Specific Performance

| Domain | spaCy+YAKE Accuracy | Processing Time | Confidence |
|---------|-------------------|-----------------|------------|
| **Social Media** | **47.23%** | 9.91ms | 97.41% |
| **Short Text** | **49.60%** | 3.20ms | 99.22% |
| **Technical** | **44.03%** | 18.91ms | 94.22% |
| **Business** | **37.40%** | 19.30ms | 95.48% |
| **Challenging** | **35.01%** | 29.66ms | 100.0% |
| **Vietnamese** | **15.96%** | 13.38ms | 98.01% |

---

## 🔧 Configuration Reference

### YAML Configuration Example

```yaml
# config.yaml - Complete configuration example
spacy_yake:
  spacy_model: "en_core_web_sm"
  yake_language: "en"
  yake_n: 2                    # N-gram size (1=unigrams, 2=bigrams, 3=trigrams)
  yake_dedup_lim: 0.8         # Deduplication threshold
  yake_max_keywords: 30       # Maximum YAKE keywords
  entity_weight: 0.7          # Weight for named entities
  chunk_weight: 0.5           # Weight for noun chunks
  max_keywords: 30            # Final keyword limit
  timeout: 30.0               # Processing timeout (seconds)

benchmark:
  max_timeout: 30.0           # Benchmark timeout per method
  iterations: 1               # Number of iterations per test
  save_results: true          # Save results to files
  output_directory: "./results" # Output directory
  enable_memory_monitoring: true # Monitor memory usage
  enable_visualization: true   # Generate charts

logging:
  level: "INFO"               # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file_enabled: true          # Enable file logging
  file_path: "keyword_extraction.log" # Log file path
  console_enabled: true       # Enable console logging

# Framework settings
max_text_length: 10000        # Maximum text length to process
enable_caching: true          # Enable result caching
cache_size: 1000             # Cache size limit
output_format: "json"        # Output format: json, csv, yaml
include_metadata: true       # Include processing metadata
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. **spaCy Model Not Found**
```bash
# Error: Can't find model 'en_core_web_sm'
# Solution:
python -m spacy download en_core_web_sm

# For other languages:
python -m spacy download en_core_web_lg  # Large model
python -m spacy download xx_ent_wiki_sm  # Multilingual
```

#### 2. **Import Errors**
```python
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Run from project root directory
# ✅ Fixed in new scripts

# If still getting error, add to script beginning:
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
```

#### 3. **NLTK Data Missing**
```bash
# Error: NLTK data not found
# Solution:
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

#### 4. **Memory Issues**
```python
# Error: Out of memory during processing
# Solution: Reduce batch size and text length
config = SpacyYakeConfig(
    max_keywords=20,  # Reduce from 30
    yake_max_keywords=20,  # Reduce YAKE keywords
)

# Or process text in chunks:
def chunk_text(text, chunk_size=1000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i+chunk_size])
```

#### 5. **Slow Performance**
```python
# Solution: Optimize configuration for speed
speed_config = SpacyYakeConfig(
    max_keywords=15,      # Fewer keywords
    entity_weight=0.8,    # Higher entity weight
    chunk_weight=0.3,     # Lower chunk weight
    yake_n=2,            # Only bigrams
)
```

#### 6. **Low Accuracy**
```python
# Solution: Tune parameters for better accuracy
accuracy_config = SpacyYakeConfig(
    max_keywords=50,      # More keywords
    yake_n=3,            # Include trigrams
    entity_weight=0.6,    # Balanced weights
    chunk_weight=0.7,
    yake_dedup_lim=0.7,  # Less aggressive deduplication
)
```

#### 7. **Scripts not working**
```bash
# Check running order:
1. python scripts/test_simple.py  # Basic test
2. python scripts/demo.py         # Quick demo
3. python scripts/run_experiments.py  # Comprehensive experiments
```

### Debugging Tips

```python
# Enable debug logging
from src.core.utils import setup_logging
logger = setup_logging(__name__)
logger.setLevel(logging.DEBUG)

# Check extraction details
result = await extractor.extract(text)
print(f"Processing time: {result.processing_time:.3f}s")
print(f"Memory usage: {result.memory_usage:.2f}MB")
print(f"Success: {result.success}")
if result.error_message:
    print(f"Error: {result.error_message}")

# Inspect keyword types
for kw in result.keywords:
    print(f"{kw['keyword']} ({kw['type']}) - {kw['score']:.3f}")
```

### Performance Optimization

```python
# Monitor performance
import time
import psutil

def monitor_performance(func):
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        result = await func(*args, **kwargs)
        
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        print(f"⏱️  Time: {end_time - start_time:.3f}s")
        print(f"💾 Memory: {end_memory - start_memory:.2f}MB")
        
        return result
    return wrapper

@monitor_performance
async def extract_keywords(text):
    return await extractor.extract(text)
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
