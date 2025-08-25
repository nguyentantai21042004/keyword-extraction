# 🚀 Standalone Keyword Extraction Algorithms

Bộ thuật toán trích xuất từ khóa độc lập, có thể sử dụng trực tiếp trong bất kỳ dự án Python nào.

## 📋 Tổng Quan

Dự án này cung cấp **2 thuật toán chính** được tối ưu hóa cho việc trích xuất từ khóa:

### 1. **spaCy + YAKE** (`spacy_yake_standalone.py`)
- **Độ chính xác cao nhất** (67% trong nghiên cứu)
- Kết hợp NLP (spaCy) + Statistical (YAKE)
- Named Entity Recognition + Noun chunk extraction
- Phù hợp cho: tài liệu kỹ thuật, nội dung kinh doanh, tin tức

### 2. **Hybrid Ensemble** (`hybrid_ensemble_standalone.py`)
- **Kết hợp thông minh** nhiều phương pháp
- Chạy song song để tối ưu hiệu suất
- Weighted voting system cho kết quả chính xác
- Phù hợp cho: yêu cầu độ chính xác cao, môi trường production

## 🛠️ Cài Đặt

### Bước 1: Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv keyword_env
source keyword_env/bin/activate  # Linux/Mac
# hoặc
keyword_env\Scripts\activate     # Windows
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements_standalone.txt
```

### Bước 3: Tải spaCy model
```bash
python -m spacy download en_core_web_sm
```

## 🚀 Sử Dụng Nhanh

### spaCy + YAKE Algorithm

```python
import asyncio
from spacy_yake_standalone import SpacyYakeExtractor

async def main():
    # Khởi tạo extractor
    extractor = SpacyYakeExtractor()
    
    # Văn bản cần trích xuất từ khóa
    text = """
    Artificial Intelligence (AI) and Machine Learning (ML) are transforming 
    the technology industry. Companies like Google, Microsoft, and OpenAI 
    are leading innovation in natural language processing.
    """
    
    # Trích xuất từ khóa
    result = await extractor.extract(text)
    
    # Hiển thị kết quả
    print(f"Confidence: {result.confidence_score:.3f}")
    print(f"Keywords found: {len(result.keywords)}")
    
    for kw in result.keywords[:10]:
        print(f"{kw.rank}. {kw.keyword} [{kw.type}] Score: {kw.score:.3f}")

# Chạy
asyncio.run(main())
```

### Hybrid Ensemble Algorithm

```python
import asyncio
from hybrid_ensemble_standalone import HybridEnsembleExtractor

async def main():
    # Cấu hình ensemble
    config = {
        'method_weights': {
            'spacy_yake': 0.4,  # Trọng số cao nhất
            'rake': 0.3,        # Trọng số trung bình
            'tfidf': 0.3        # Trọng số trung bình
        },
        'timeout': 15.0,        # Timeout cho mỗi method
        'max_keywords': 30      # Số từ khóa tối đa
    }
    
    # Khởi tạo ensemble extractor
    extractor = HybridEnsembleExtractor(config)
    
    # Văn bản cần trích xuất
    text = "Your text here..."
    
    # Trích xuất sử dụng ensemble
    result = await extractor.extract(text)
    
    # Hiển thị kết quả
    print(f"Ensemble Confidence: {result.confidence_score:.3f}")
    print(f"Methods used: {result.metadata['methods_used']}")
    
    for kw in result.keywords[:15]:
        methods = ', '.join(kw.methods_used) if kw.methods_used else 'unknown'
        print(f"{kw.rank}. {kw.keyword} | Methods: {methods}")

# Chạy
asyncio.run(main())
```

## ⚙️ Cấu Hình Nâng Cao

### spaCy + YAKE Configuration

```python
config = {
    'model_size': 'sm',        # 'sm', 'md', 'lg' (default: 'sm')
    'yake_top': 30,            # Số từ khóa YAKE tối đa
    'entity_weight': 0.7,      # Trọng số cho named entities
    'chunk_weight': 0.5        # Trọng số cho noun chunks
}

extractor = SpacyYakeExtractor(config)
```

### Hybrid Ensemble Configuration

```python
config = {
    'method_weights': {
        'spacy_yake': 0.4,     # Trọng số cao nhất - độ chính xác tốt nhất
        'rake': 0.2,           # Trọng số trung bình - tốc độ tốt
        'tfidf': 0.2,          # Trọng số trung bình - baseline đáng tin cậy
    },
    'timeout': 10.0,           # Timeout cho mỗi method (giây)
    'max_keywords': 25         # Số từ khóa cuối cùng tối đa
}

extractor = HybridEnsembleExtractor(config)
```

## 📊 So Sánh Hiệu Suất

| Thuật toán | Tốc độ | Độ chính xác | Bộ nhớ | Độ tin cậy |
|------------|--------|---------------|---------|------------|
| **spaCy+YAKE** | 🥈 2nd | 🥇 1st (67%) | 🥉 3rd | 🥇 1st (85.3%) |
| **Hybrid Ensemble** | 🥉 4th | 🥇 1st | 🥉 5th | 🥇 1st |

## 🔍 Cấu Trúc Kết Quả

### ExtractionResult
```python
@dataclass
class ExtractionResult:
    keywords: List[KeywordResult]      # Danh sách từ khóa
    metadata: Dict                     # Thông tin bổ sung
    performance_metrics: Dict          # Metrics hiệu suất
    method_name: str                   # Tên method
    processing_time: float             # Thời gian xử lý
    memory_usage: float                # Bộ nhớ sử dụng
    confidence_score: float            # Độ tin cậy (0-1)
```

### KeywordResult
```python
@dataclass
class KeywordResult:
    keyword: str                       # Từ khóa
    score: float                       # Điểm số
    rank: int                          # Thứ hạng
    type: str                          # Loại từ khóa
    relevance: float                   # Độ liên quan (0-1)
    methods_used: Optional[List[str]]  # Methods đã sử dụng (ensemble)
```

## 🎯 Các Loại Từ Khóa

### spaCy + YAKE
- `yake_keyword`: Từ khóa từ YAKE algorithm
- `entity_PERSON`: Named entity - người
- `entity_ORG`: Named entity - tổ chức
- `entity_GPE`: Named entity - địa điểm
- `noun_chunk`: Cụm danh từ

### Hybrid Ensemble
- `ensemble_yake_keyword`: Từ khóa YAKE trong ensemble
- `ensemble_rake_phrase`: Cụm từ RAKE trong ensemble
- `ensemble_tfidf_term`: Term TF-IDF trong ensemble

## 🚨 Xử Lý Lỗi

### Kiểm tra trạng thái models
```python
# spaCy + YAKE
extractor = SpacyYakeExtractor()
model_info = extractor.get_model_info()
print(f"Models ready: {model_info['models_ready']}")

# Hybrid Ensemble
extractor = HybridEnsembleExtractor()
method_status = extractor.get_method_status()
for method, status in method_status.items():
    print(f"{method}: {status}")
```

### Xử lý lỗi gracefully
```python
try:
    result = await extractor.extract(text)
    if result.keywords:
        print("Extraction successful!")
    else:
        print("No keywords extracted")
except Exception as e:
    print(f"Extraction failed: {e}")
```

## 📈 Tối Ưu Hóa Hiệu Suất

### 1. **Model Size Selection**
```python
# Fast processing, less memory
config = {'model_size': 'sm'}  # ~50MB

# Better accuracy, more memory
config = {'model_size': 'lg'}  # ~500MB
```

### 2. **Timeout Configuration**
```python
# For real-time applications
config = {'timeout': 5.0}

# For batch processing
config = {'timeout': 30.0}
```

### 3. **Method Weights Tuning**
```python
# High accuracy focus
config = {
    'method_weights': {
        'spacy_yake': 0.6,  # Higher weight
        'rake': 0.2,
        'tfidf': 0.2
    }
}

# Balanced approach
config = {
    'method_weights': {
        'spacy_yake': 0.4,
        'rake': 0.3,
        'tfidf': 0.3
    }
}
```

## 🔧 Troubleshooting

### Lỗi thường gặp

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **YAKE import error**
   ```bash
   pip install yake --upgrade
   ```

3. **RAKE import error**
   ```bash
   pip install rake-nltk
   python -c "import nltk; nltk.download('stopwords')"
   ```

4. **Memory issues**
   - Giảm `model_size` xuống 'sm'
   - Giảm `max_keywords`
   - Tăng `timeout` để tránh timeout

### Performance tips

- **First run**: Chậm hơn do model loading
- **Subsequent runs**: Nhanh hơn do model caching
- **Memory usage**: Tăng theo text length
- **CPU usage**: Ensemble method sử dụng nhiều CPU hơn

## 📚 Ví Dụ Thực Tế

### Social Media Content
```python
text = """
#AI #MachineLearning are revolutionizing #tech industry! 
Google, Microsoft, and OpenAI leading innovation in #NLP. 
The future of #technology is here! 🚀
"""

# Sử dụng spaCy + YAKE cho social media
extractor = SpacyYakeExtractor()
result = await extractor.extract(text)
```

### Technical Documentation
```python
text = """
The TensorFlow framework provides comprehensive tools for deep learning.
It supports both CPU and GPU acceleration, with automatic differentiation
and high-level APIs for neural network construction.
"""

# Sử dụng Ensemble cho technical docs
extractor = HybridEnsembleExtractor()
result = await extractor.extract(text)
```

### Business Content
```python
text = """
Digital transformation is reshaping traditional retail businesses.
Companies must adopt AI-powered solutions to remain competitive.
Customer experience optimization through machine learning algorithms.
"""

# Cả hai method đều phù hợp
spacy_result = await spacy_extractor.extract(text)
ensemble_result = await ensemble_extractor.extract(text)
```

## 🤝 Đóng Góp

Nếu bạn muốn cải thiện thuật toán:

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Các thuật toán này dựa trên research và open-source implementations. Vui lòng tôn trọng license của từng package được sử dụng.

## 📞 Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra [Troubleshooting](#-troubleshooting)
2. Xem [Requirements](#-cài-đặt)
3. Tạo issue với thông tin chi tiết
4. Liên hệ team development

---

**Happy Keyword Extraction! 🎉**
