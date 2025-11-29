# 🧠 spaCy + YAKE Algorithm: Detailed Analysis

## 📋 Overview

**spaCy + YAKE** là phương pháp hybrid kết hợp giữa **Natural Language Processing (NLP)** và **statistical keyword extraction**. Đây là method chính trong research framework, được thiết kế để tận dụng ưu điểm của cả hai approach.

## 🏗️ Architecture

```
Input Text → spaCy Processing → YAKE Extraction → Result Combination → Final Ranking
     ↓              ↓              ↓              ↓              ↓
   Raw Text    Entities + Chunks   Keywords    Merge Results   Top 20 Keywords
```

## 🔍 Detailed Algorithm Logic

### Phase 1: spaCy NLP Processing

#### 1.1 Text Preprocessing
```python
doc = self.nlp(text)
```
- **Tokenization**: Chia text thành individual tokens
- **Part-of-Speech (POS) Tagging**: Xác định từ loại (noun, verb, adjective...)
- **Dependency Parsing**: Phân tích cấu trúc câu
- **Named Entity Recognition (NER)**: Nhận diện entities (person, organization, location...)

#### 1.2 Entity Extraction
```python
entities = [(ent.text, ent.label_) for ent in doc.ents]
```
**Logic**: 
- Sử dụng pre-trained model để identify named entities
- Mỗi entity có confidence score và label
- **Types**: PERSON, ORG, GPE (location), DATE, MONEY, etc.

**Example**:
```
Text: "Apple CEO Tim Cook announced new iPhone"
Entities: [("Apple", "ORG"), ("Tim Cook", "PERSON"), ("iPhone", "PRODUCT")]
```

#### 1.3 Noun Chunk Extraction
```python
noun_chunks = [chunk.text for chunk in doc.noun_chunks]
```
**Logic**:
- Tìm các noun phrases (cụm danh từ)
- Sử dụng dependency parsing để identify boundaries
- **Pattern**: Determiner + Adjective + Noun

**Example**:
```
Text: "The sustainable fashion industry"
Noun Chunks: ["The sustainable fashion industry"]
```

### Phase 2: YAKE Keyword Extraction

#### 2.1 YAKE Algorithm Principles
**YAKE (Yet Another Keyword Extractor)** dựa trên **statistical properties** của text:

1. **Positional Features**: Vị trí của từ trong document
2. **Statistical Features**: TF-IDF, word frequency
3. **Contextual Features**: Surrounding words
4. **Semantic Features**: Word co-occurrence

#### 2.2 YAKE Configuration
```python
self.yake_extractor = yake.KeywordExtractor(
    lan="en",           # Language
    n=1,               # N-gram size (1 = unigram, 2 = bigram)
    dedupLim=0.9,      # Deduplication threshold
    top=20,            # Maximum keywords to extract
    features=None      # Use all available features
)
```

#### 2.3 YAKE Scoring Mechanism
**Formula**: `Score = f(w) × g(w) × h(w)`

- **f(w)**: Positional factor (words at beginning/end get higher scores)
- **g(w)**: Statistical factor (TF-IDF, frequency)
- **h(w)**: Contextual factor (co-occurrence patterns)

**Lower score = Better keyword** (YAKE convention)

### Phase 3: Result Combination & Ranking

#### 3.1 Score Normalization
```python
# YAKE scores are lower = better, so invert them
'score': 1 - score
```

#### 3.2 Entity Integration
```python
for i, (entity, label) in enumerate(entities[:10]):
    keywords.append({
        'keyword': entity,
        'score': 0.8,  # Fixed high confidence for entities
        'type': f'entity_{label.lower()}',
        'relevance': 0.8
    })
```

**Logic**:
- Named entities được assign fixed score 0.8
- Đây là high-confidence keywords từ NLP model
- Label được preserve để traceability

#### 3.3 Final Ranking
```python
# Sort by score (higher = better)
keywords.sort(key=lambda x: x['score'], reverse=True)

# Re-rank top 20
for i, kw in enumerate(keywords[:20]):
    kw['rank'] = i + 1
```

## 🎯 Confidence Calculation

### Formula
```python
confidence = base_confidence + entity_bonus + chunk_bonus
```

### Components

1. **Base Confidence** (50-70%):
   ```python
   yake_scores = [kw['score'] for kw in keywords if kw['type'] == 'yake_keyword']
   base_confidence = np.mean(yake_scores)
   ```

2. **Entity Bonus** (0-20%):
   ```python
   entity_bonus = min(len(entities) / 10, 0.2)
   ```

3. **Noun Chunk Bonus** (0-10%):
   ```python
   chunk_bonus = min(len(noun_chunks) / 20, 0.1)
   ```

## 💡 Advantages

### 1. **Hybrid Approach**
- Combines rule-based NLP với statistical extraction
- Leverages domain knowledge (entities) + data-driven patterns

### 2. **High Accuracy**
- Named entities có high precision
- YAKE handles statistical patterns well
- Multiple feature types reduce bias

### 3. **Interpretable Results**
- Clear source of each keyword (entity vs YAKE)
- Confidence scores explainable
- Entity labels provide context

## ⚠️ Limitations

### 1. **Computational Cost**
- spaCy model loading (memory)
- YAKE processing (time)
- Combined processing overhead

### 2. **Dependency on Models**
- Requires pre-trained spaCy model
- Model quality affects entity recognition
- Language-specific limitations

### 3. **Score Balancing**
- Fixed entity scores (0.8) may not reflect true relevance
- Manual weight balancing between methods

## 🔧 Optimization Opportunities

### 1. **Model Selection**
```python
# Use smaller model for speed
nlp = spacy.load("en_core_web_sm")  # vs en_core_web_lg
```

### 2. **Entity Thresholds**
```python
# Filter entities by confidence
entities = [ent for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE']]
```

### 3. **YAKE Parameter Tuning**
```python
# Adjust for specific domain
dedupLim=0.8,  # More aggressive deduplication
top=15,        # Fewer keywords for faster processing
```

## 📊 Performance Characteristics

| Metric | Typical Range | Notes |
|--------|---------------|-------|
| Processing Time | 0.5-2.0s | Depends on text length |
| Memory Usage | 50-150MB | spaCy model overhead |
| Confidence Score | 0.6-0.9 | High due to entity bonus |
| Keywords Count | 15-25 | Configurable via top parameter |

## 🎓 Research Implications

### 1. **Methodology Justification**
- "Hybrid approach combines linguistic knowledge với statistical patterns"
- "Named entity recognition provides high-confidence keywords"
- "YAKE handles statistical keyword identification"

### 2. **Performance Trade-offs**
- Higher accuracy vs higher computational cost
- Memory usage vs processing speed
- Entity precision vs statistical coverage

### 3. **Domain Adaptability**
- Works well for structured text (news, documents)
- May need tuning for informal text (social media)
- Entity recognition quality varies by domain

---

**Next**: [RAKE Algorithm Analysis](./rake_algorithm.md) | [Back to Index](../README.md)
