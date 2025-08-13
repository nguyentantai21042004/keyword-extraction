# 🕸️ TextRank Algorithm Documentation

## 🎯 Overview

**TextRank** là một thuật toán dựa trên graph theory, được phát triển bởi Mihalcea và Tarau (2004), lấy cảm hứng từ thuật toán PageRank của Google. Trong framework này, TextRank được sử dụng như một **graph-based baseline** để so sánh với các phương pháp khác về khả năng hiểu mối quan hệ ngữ nghĩa.

## 🧮 Methodology

### Core Algorithm

TextRank xây dựng một đồ thị từ văn bản và sử dụng thuật toán ranking để xác định tầm quan trọng:

1. **Graph Construction**: Tạo đồ thị với từ là nodes, mối quan hệ là edges
2. **Edge Weighting**: Trọng số dựa trên co-occurrence trong window
3. **PageRank Algorithm**: Tính toán importance scores
4. **Keyword Ranking**: Sắp xếp theo scores và extract top keywords

### Mathematical Foundation

**TextRank Score Formula:**
```
TR(Vi) = (1-d) + d × Σ(wji × TR(Vj) / Σ(wjk))
```

Trong đó:
- `TR(Vi)`: TextRank score của vertex i
- `d`: damping factor (thường = 0.85)
- `wji`: trọng số edge từ vertex j đến i
- `Vj`: các vertex kết nối với Vi

### Implementation Strategy

```python
class TextRankExtractor(BaseExtractor):
    """Graph-based method using TextRank algorithm"""
    
    async def extract(self, text: str) -> ExtractionResult:
        # 1. Initialize TextRank4Keyword
        tr4w = TextRank4Keyword()
        
        # 2. Analyze text with configuration
        tr4w.analyze(
            text,
            lower=True,     # Convert to lowercase
            window=4        # Co-occurrence window size
        )
        
        # 3. Extract ranked keywords
        keywords = tr4w.get_keywords(
            num=20,         # Top 20 keywords
            word_min_len=2  # Minimum word length
        )
        
        # 4. Format results
        return formatted_results
```

## ⚙️ Configuration

### Key Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `window_size` | 4 | Co-occurrence window for graph construction |
| `lower` | True | Convert text to lowercase |
| `word_min_len` | 2 | Minimum word length filter |
| `num_keywords` | 20 | Maximum keywords returned |
| `damping_factor` | 0.85 | PageRank damping parameter |

### Dependencies

```python
from textrank4zh import TextRank4Keyword
import numpy as np
```

**Note**: Framework sử dụng `textrank4zh` library, chủ yếu được tối ưu cho tiếng Trung nhưng cũng hỗ trợ tiếng Anh.

## 📈 Performance Characteristics

### Strengths

✅ **Semantic Relationships**: Hiểu được mối quan hệ giữa các từ
✅ **Unsupervised**: Không cần training data
✅ **Language Independent**: Hoạt động với nhiều ngôn ngữ
✅ **Contextual**: Xem xét context xung quanh từ
✅ **Mathematical Foundation**: Dựa trên graph theory vững chắc

### Limitations

❌ **Language Optimization**: textrank4zh tối ưu cho tiếng Trung
❌ **Inconsistent Results**: Có thể trả về 0 keywords với English text
❌ **Computational Complexity**: Chậm hơn statistical methods
❌ **Dependency Issues**: Requires specific Chinese NLP libraries
❌ **Limited English Support**: Suboptimal for English text analysis

## 📊 Experimental Results

### Performance Metrics (Average)

| Metric | Value | Ranking |
|--------|-------|---------|
| Processing Time | 0.25s | 🥉 3rd |
| Memory Usage | 15MB | 🥉 3rd |
| Confidence Score | 0.000 | ❌ Last |
| Keywords Count | 0-5 | ❌ Last |
| Accuracy (F1) | 0.05 | ❌ Last |

### Domain Performance

| Domain | Accuracy | Issues |
|--------|----------|--------|
| Technical | 0.05 | Poor English support |
| Business | 0.03 | Language mismatch |
| Social Media | 0.01 | Limited keyword extraction |
| Short Text | 0.00 | No keywords extracted |

**⚠️ Warning**: Current implementation shows poor performance with English text due to using Chinese-optimized library.

## 🔧 Usage Examples

### Basic Usage

```python
from multi_method_extractor import TextRankExtractor

# Initialize extractor
textrank = TextRankExtractor()

# Extract keywords
text = "Machine learning algorithms for data analysis"
result = await textrank.extract(text)

print(f"Keywords: {result.keywords[:5]}")
print(f"Confidence: {result.confidence_score}")
```

### With Custom Configuration

```python
config = {
    'window_size': 6,     # Larger co-occurrence window
    'word_min_len': 3,    # Longer minimum words
}

textrank = TextRankExtractor(config)
result = await textrank.extract(text)
```

## ⚖️ Comparison with Other Methods

### vs. spaCy + YAKE
- **Semantic Understanding**: TextRank better in theory, worse in practice
- **Accuracy**: YAKE significantly better (0.828 vs 0.000 confidence)
- **Language Support**: YAKE better for English

### vs. TF-IDF
- **Approach**: TextRank graph-based vs TF-IDF statistical
- **Results**: TF-IDF performs better with current implementation
- **Complexity**: TextRank more complex

### vs. KeyBERT
- **Semantic Depth**: KeyBERT superior with modern embeddings
- **Performance**: KeyBERT more reliable for English text
- **Setup**: Both require external libraries

## 🛠️ Algorithm Details

### Graph Construction Process

1. **Tokenization**: Split text into words/phrases
2. **Filtering**: Remove stopwords and short words
3. **Co-occurrence Detection**: Find words appearing in same window
4. **Graph Building**: Create nodes (words) and edges (co-occurrences)
5. **Weight Calculation**: Assign edge weights based on frequency

### PageRank Application

1. **Initialization**: All nodes start with equal scores
2. **Iteration**: Apply PageRank formula repeatedly
3. **Convergence**: Stop when scores stabilize
4. **Ranking**: Sort nodes by final scores
5. **Selection**: Extract top-ranked keywords

### Confidence Calculation

```python
def _calculate_textrank_confidence(self, keywords: List) -> float:
    if not keywords:
        return 0.0
    scores = [kw['score'] for kw in keywords]
    return np.mean(scores) if scores else 0.0
```

## 🔬 Technical Analysis

### Algorithm Complexity

- **Time Complexity**: O(V² × I) where V=vertices, I=iterations
- **Space Complexity**: O(V + E) where E=edges
- **Convergence**: Typically 10-30 iterations

### Current Implementation Issues

1. **Library Mismatch**: textrank4zh optimized for Chinese
2. **Tokenization**: May not properly handle English text
3. **Stopwords**: Chinese stopword lists
4. **POS Tagging**: Chinese POS tags vs English requirements

### Potential Improvements

```python
# Ideal implementation with proper English support
class ImprovedTextRankExtractor(BaseExtractor):
    def __init__(self):
        # Use English-specific TextRank implementation
        # Proper English tokenization
        # English stopword lists
        # English POS tagging
```

## 🎯 Use Cases and Recommendations

### Current Status

❌ **Not Recommended** for production use with English text due to:
- Zero keyword extraction in most cases
- Language optimization mismatch
- Poor accuracy scores

### Potential Use Cases (with proper implementation)

1. **Document Summarization**: Extract key topics
2. **Semantic Analysis**: Understand word relationships
3. **Content Analysis**: Identify central themes
4. **Research Applications**: Graph-based NLP studies

### Recommended Alternatives

For English text analysis, consider:
1. **spaCy + YAKE**: Best accuracy and English support
2. **KeyBERT**: Semantic understanding with embeddings
3. **TF-IDF**: Fast statistical baseline

## 📚 References

### Academic Sources

1. Mihalcea, R., & Tarau, P. (2004). "TextRank: Bringing order into texts"
2. Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). "The PageRank citation ranking"
3. Wan, X., & Yang, J. (2008). "Multi-document summarization using cluster-based link analysis"

### Implementation References

- **textrank4zh Documentation**: Chinese TextRank implementation
- **Original TextRank Paper**: Algorithm foundation
- **Graph Theory**: Mathematical background

## 🔄 Status and Future Work

### Current Status

- **Implementation**: ✅ Functional but suboptimal
- **Performance**: ❌ Poor for English text
- **Role**: Research baseline for graph-based approaches

### Improvement Roadmap

- [ ] **English-Optimized Library**: Replace textrank4zh
- [ ] **Proper Tokenization**: English-specific text processing
- [ ] **POS Tag Integration**: Use English POS tags
- [ ] **Performance Optimization**: Improve extraction accuracy
- [ ] **Multi-language Support**: Proper language detection

### Alternative Implementations

```python
# Future implementation options:
# 1. NetworkX + NLTK for English TextRank
# 2. spaCy + custom graph construction
# 3. Transformer-based graph embeddings
```

---

**Status**: ⚠️ Experimental baseline (limited English support)
**Role**: Graph-based comparison method
**Recommendation**: Use spaCy+YAKE or KeyBERT for English text analysis
