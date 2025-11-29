# Design: Enhance SpaCy+YAKE with Aspect Mapping

## Interface Definition

### IKeywordExtractor Interface

All keyword extractors SHALL implement a common interface to ensure consistency and enable polymorphic usage. This aligns with the term.md specification.

**Location**: `src/core/base_extractor.py` (extends existing)

**Interface Contract**:
```python
from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel

class KeywordResult(BaseModel):
    """Standard keyword result format"""
    keyword: str
    weight: float      # 0-1, higher means more important
    score: float       # Algorithm-specific score (YAKE: lower is better)
    aspect: str        # Domain/topic label (e.g., "PERFORMANCE", "DESIGN")
    method: str        # Extraction method name (e.g., "HYBRID", "YAKE")

class IKeywordExtractor(ABC):
    """
    Interface for keyword extraction methods.

    Instance Lifecycle:
    - Instances MUST be initialized once at service startup
    - Instances MUST NOT be re-initialized per request
    - Instances MUST be thread-safe for concurrent requests
    """

    @abstractmethod
    def extract(self, text: str, top_n: int = 10) -> List[KeywordResult]:
        """
        Extract and label keywords from text.

        Args:
            text: Input text (Vietnamese or English)
            top_n: Maximum number of keywords to return (default: 10)

        Returns:
            List of KeywordResult objects, sorted by weight (descending)

        Raises:
            ValueError: If text is empty or invalid
            RuntimeError: If models are not initialized
        """
        pass
```

**Return Format Specification**:
```python
# Example return value
[
    {
        "keyword": "pin",
        "weight": 0.85,        # Normalized importance (0-1, higher is better)
        "score": 0.15,         # YAKE raw score (lower is better)
        "aspect": "PERFORMANCE",
        "method": "HYBRID"     # SpaCy + YAKE + Aspect Mapping
    },
    {
        "keyword": "thiết kế",
        "weight": 0.72,
        "score": 0.28,
        "aspect": "DESIGN",
        "method": "HYBRID"
    },
    # ... up to top_n results
]
```

### HybridKeywordExtractor Implementation

**Location**: `src/core/extractors/hybrid_extractor.py` (rename from `spacy_yake.py` or create new)

**Class Definition**:
```python
class HybridKeywordExtractor(IKeywordExtractor):
    """
    Hybrid keyword extractor combining:
    1. YAKE: Statistical keyword ranking
    2. SpaCy: Grammar filtering (POS tags, noun phrases)
    3. Aspect Mapping: Domain/topic labeling
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize extractor with models and configuration.

        IMPORTANT: This should be called ONCE at service startup,
        not on every request.

        Args:
            config: Configuration dict with keys:
                - spacy_model: "en_core_web_sm" or "vi_core_news_lg"
                - yake_language: "en" or "vi"
                - enable_aspect_mapping: bool
                - aspect_dictionary_path: str
        """
        self.config = config or {}
        self.nlp = None              # spaCy model
        self.yake_extractor = None   # YAKE instance
        self.aspect_mapper = None    # AspectMapper instance

        # Load models once during initialization
        self._initialize_models()
        self._initialize_aspect_mapper()

    def extract(self, text: str, top_n: int = 10) -> List[KeywordResult]:
        """
        Extract keywords using hybrid pipeline.

        Pipeline:
        1. YAKE extracts candidate keywords
        2. SpaCy filters by POS tags (NOUN/PROPN only)
        3. AspectMapper assigns domain labels
        4. Results sorted by weight, limited to top_n
        """
        # Implementation details in Component Design section
        pass
```

**Instance Lifecycle Management**:
```python
# Service initialization (once at startup)
class KeywordService:
    def __init__(self):
        # Initialize extractor ONCE
        self.extractor = HybridKeywordExtractor(config={
            'spacy_model': 'vi_core_news_lg',
            'yake_language': 'vi',
            'enable_aspect_mapping': True,
            'aspect_dictionary_path': 'config/aspect_dictionaries/vietnamese.yaml'
        })

    def extract_keywords(self, text: str, top_n: int = 10):
        # Use the same instance for all requests
        return self.extractor.extract(text, top_n)

# FastAPI example
@app.on_event("startup")
async def startup_event():
    app.state.keyword_extractor = HybridKeywordExtractor(config=load_config())

@app.post("/extract")
async def extract_keywords(request: Request, text: str, top_n: int = 10):
    # Reuse the initialized instance
    results = request.app.state.keyword_extractor.extract(text, top_n)
    return {"keywords": results}
```

## Architecture Overview

This enhancement integrates aspect mapping into the existing SpaCy+YAKE extraction pipeline without breaking existing functionality. The design follows the Single Responsibility Principle by introducing a dedicated `AspectMapper` component while keeping the core extraction logic in `HybridKeywordExtractor`.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  SpacyYakeExtractor                     │
│  ┌──────────────┐   ┌──────────────┐  ┌──────────────┐ │
│  │   spaCy      │   │    YAKE      │  │   Aspect     │ │
│  │  Processor   │───│  Extractor   │──│   Mapper     │ │
│  └──────────────┘   └──────────────┘  └──────────────┘ │
│         │                   │                 │         │
│         └───────────────────┴─────────────────┘         │
│                             ↓                           │
│                  Enhanced ExtractionResult              │
│               (with aspect-labeled keywords)            │
└─────────────────────────────────────────────────────────┘
                             ↑
                             │
                   ┌─────────┴─────────┐
                   │  Configuration    │
                   │  - aspect_dict    │
                   │  - language       │
                   │  - enable_aspects │
                   └───────────────────┘
```

## Component Design

### 1. AspectMapper Class

**Location**: `src/core/utils/aspect_mapper.py` (new file)

**Responsibilities**:
- Load aspect dictionaries from YAML files
- Map keywords to aspect labels
- Validate dictionary structure
- Provide case-insensitive matching

**Interface**:
```python
class AspectMapper:
    def __init__(self, dictionary_path: Optional[str] = None,
                 dictionary_data: Optional[Dict] = None):
        """Initialize with either file path or dict data"""

    def load_dictionary(self, path: str) -> None:
        """Load aspect dictionary from YAML file"""

    def map_keyword(self, keyword: str) -> str:
        """Map a single keyword to aspect label"""

    def map_keywords(self, keywords: List[str]) -> Dict[str, str]:
        """Batch map keywords to aspects"""

    def get_statistics(self) -> Dict:
        """Return dictionary statistics"""
```

**Internal Data Structure**:
```python
# Optimized for fast lookup
self._aspect_map: Dict[str, str] = {
    'pin': 'PERFORMANCE',
    'battery': 'PERFORMANCE',
    'sạc': 'PERFORMANCE',
    'thiết kế': 'DESIGN',
    'design': 'DESIGN',
    # ... normalized lowercase keys
}

# Original dictionary for reference
self._dictionary: Dict[str, List[str]] = {
    'PERFORMANCE': ['pin', 'battery', 'sạc', ...],
    'DESIGN': ['thiết kế', 'design', ...],
    # ...
}
```

### 2. Enhanced SpacyYakeExtractor

**Modifications to** `src/core/extractors/spacy_yake.py`:

**New Attributes**:
```python
class SpacyYakeExtractor(BaseExtractor):
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config)
        self.method_name = "spacy_yake"
        self.nlp = None
        self.yake_extractor = None
        self.aspect_mapper = None  # NEW
        self._initialize_models()
        self._initialize_aspect_mapper()  # NEW
```

**New Method** `_initialize_aspect_mapper()`:
```python
def _initialize_aspect_mapper(self):
    """Initialize aspect mapper if enabled"""
    if not self.config.get('enable_aspect_mapping', False):
        self.logger.info("Aspect mapping disabled")
        return

    dict_path = self.config.get('aspect_dictionary_path')
    dict_data = self.config.get('aspect_dictionary_data')

    try:
        self.aspect_mapper = AspectMapper(
            dictionary_path=dict_path,
            dictionary_data=dict_data
        )
        self.logger.info(f"Aspect mapper initialized with {len(self.aspect_mapper._aspect_map)} mappings")
    except Exception as e:
        self.logger.error(f"Failed to initialize aspect mapper: {e}")
        self.aspect_mapper = None
```

**Modified Method** `_combine_keyword_sources()`:
```python
def _combine_keyword_sources(self, yake_keywords: List[tuple],
                           entities: List[tuple],
                           noun_chunks: List[str]) -> List[Dict]:
    """Combine keywords from different sources with aspect mapping"""
    keywords = []

    # Add YAKE keywords
    for i, (keyword, score) in enumerate(yake_keywords):
        aspect = self._get_aspect(keyword)  # NEW
        keywords.append({
            'keyword': keyword.strip(),
            'score': 1.0 - score,
            'rank': i + 1,
            'type': 'statistical',
            'relevance': 1.0 - score,
            'aspect': aspect  # NEW
        })

    # Add entities with aspects
    entity_score = self.config.get('entity_weight', 0.7)
    for entity, label in entities:
        aspect = self._get_aspect(entity)  # NEW
        keywords.append({
            'keyword': entity,
            'score': entity_score,
            'rank': len(keywords) + 1,
            'type': f'entity_{label.lower()}',
            'relevance': entity_score,
            'aspect': aspect  # NEW
        })

    # Similar for noun chunks...

    return keywords
```

**New Helper Method** `_get_aspect()`:
```python
def _get_aspect(self, keyword: str) -> str:
    """Get aspect label for keyword"""
    if not self.aspect_mapper:
        return "UNKNOWN"
    return self.aspect_mapper.map_keyword(keyword)
```

**Modified Method** `extract()` - Add aspect statistics to metadata:
```python
async def extract(self, text: str) -> ExtractionResult:
    # ... existing extraction logic ...

    # Calculate aspect distribution
    aspect_distribution = {}
    if self.aspect_mapper:
        for kw in final_keywords:
            aspect = kw.get('aspect', 'UNKNOWN')
            aspect_distribution[aspect] = aspect_distribution.get(aspect, 0) + 1

    # Calculate aspect coverage
    total = len(final_keywords)
    known = sum(1 for kw in final_keywords if kw.get('aspect') != 'UNKNOWN')
    aspect_coverage = known / total if total > 0 else 0

    return ExtractionResult(
        keywords=final_keywords,
        metadata={
            'method': self.method_name,
            # ... existing metadata ...
            'aspect_distribution': aspect_distribution,  # NEW
            'aspect_coverage': aspect_coverage  # NEW
        },
        # ...
    )
```

### 3. Configuration Extensions

**Update** `src/config/default_config.yaml`:
```yaml
spacy_yake:
  enabled: true
  spacy_model: "en_core_web_sm"
  yake_language: "en"
  yake_n: 2
  yake_dedup_lim: 0.8
  yake_max_keywords: 30
  entity_weight: 0.7
  chunk_weight: 0.5
  max_keywords: 30
  timeout: 30.0

  # NEW: Aspect mapping configuration
  enable_aspect_mapping: false  # Default disabled for backward compatibility
  aspect_dictionary_path: "config/aspect_dictionaries/default.yaml"
  unknown_aspect_label: "UNKNOWN"

# NEW: Vietnamese language profile
spacy_yake_vi:
  enabled: true
  spacy_model: "vi_core_news_lg"
  yake_language: "vi"
  yake_n: 3  # Vietnamese multi-word terms
  yake_dedup_lim: 0.9
  yake_max_keywords: 30
  entity_weight: 0.7
  chunk_weight: 0.5
  max_keywords: 30
  timeout: 30.0
  enable_aspect_mapping: true
  aspect_dictionary_path: "config/aspect_dictionaries/vietnamese.yaml"
```

**New File**: `config/aspect_dictionaries/default.yaml`:
```yaml
# Default aspect dictionary for product reviews
aspects:
  PERFORMANCE:
    keywords:
      - "battery"
      - "speed"
      - "performance"
      - "lag"
      - "freeze"
      - "crash"
      - "slow"
      - "fast"

  DESIGN:
    keywords:
      - "design"
      - "appearance"
      - "color"
      - "look"
      - "style"
      - "beautiful"
      - "ugly"

  PRICE:
    keywords:
      - "price"
      - "cost"
      - "expensive"
      - "cheap"
      - "value"
      - "affordable"

  QUALITY:
    keywords:
      - "quality"
      - "build"
      - "material"
      - "durable"
      - "sturdy"

  SERVICE:
    keywords:
      - "service"
      - "support"
      - "warranty"
      - "staff"
      - "delivery"
```

**New File**: `config/aspect_dictionaries/vietnamese.yaml`:
```yaml
# Vietnamese aspect dictionary
aspects:
  PERFORMANCE:
    keywords:
      - "pin"
      - "battery"
      - "sạc"
      - "charging"
      - "động cơ"
      - "tốc độ"
      - "speed"
      - "quãng đường"
      - "lỗi"
      - "treo"
      - "lag"

  DESIGN:
    keywords:
      - "thiết kế"
      - "design"
      - "màu"
      - "color"
      - "ngoại thất"
      - "nội thất"
      - "đẹp"
      - "beautiful"
      - "xấu"
      - "ugly"
      - "nhựa"

  PRICE:
    keywords:
      - "giá"
      - "price"
      - "tiền"
      - "money"
      - "đắt"
      - "expensive"
      - "rẻ"
      - "cheap"
      - "lăn bánh"
      - "cọc"

  SERVICE:
    keywords:
      - "bảo hành"
      - "warranty"
      - "nhân viên"
      - "staff"
      - "showroom"
      - "thái độ"
      - "attitude"
      - "cứu hộ"
```

### 4. Language Detection Enhancement

**New Utility**: `src/core/utils/language_utils.py` (optional, low priority):
```python
def detect_language(text: str) -> str:
    """Simple heuristic language detection"""
    # Check for Vietnamese diacritics
    vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệ'
    vietnamese_count = sum(1 for c in text.lower() if c in vietnamese_chars)

    if vietnamese_count > len(text) * 0.05:  # 5% threshold
        return 'vi'
    return 'en'
```

## Data Flow

### Standard Extraction Flow with Aspect Mapping

```
1. Input Text
   ↓
2. SpacyYakeExtractor.extract()
   ↓
3. spaCy Processing (entities, chunks)
   ↓
4. YAKE Processing (statistical keywords)
   ↓
5. Combine Sources (_combine_keyword_sources)
   ├─→ For each keyword:
   │   ├─→ AspectMapper.map_keyword()
   │   │   ├─→ Normalize keyword (lowercase)
   │   │   ├─→ Lookup in aspect_map dict
   │   │   └─→ Return aspect label or "UNKNOWN"
   │   └─→ Add aspect to keyword dict
   ↓
6. Calculate Aspect Statistics
   ├─→ aspect_distribution
   └─→ aspect_coverage
   ↓
7. Return ExtractionResult with aspect-enriched keywords
```

## Performance Considerations

### Memory Optimization
- **Aspect Map**: Use single flat dict for O(1) lookup instead of nested structure
- **Case Normalization**: Pre-normalize all dictionary keys to lowercase
- **Lazy Loading**: Only load aspect dictionaries when aspect mapping is enabled

### Speed Optimization
- **Batch Operations**: Map all keywords in single pass rather than individual calls
- **Early Exit**: If aspect mapping disabled, skip all aspect-related processing
- **Dictionary Size**: Limit to ~1000 keywords per aspect to keep memory footprint small

### Estimated Performance Impact
- **Aspect Mapping Overhead**: < 10ms for 20 keywords
- **Dictionary Load Time**: < 50ms for 500-entry dictionary
- **Memory Overhead**: ~100KB for typical aspect dictionary

## Error Handling Strategy

### Graceful Degradation
1. **Missing Dictionary File**: Fall back to empty dictionary, all aspects = "UNKNOWN"
2. **Malformed YAML**: Log error, use empty dictionary
3. **Invalid Dictionary Structure**: Skip invalid entries, use valid ones
4. **AspectMapper Initialization Failure**: Continue without aspect mapping

### Logging Strategy
- **INFO**: Dictionary loaded successfully, number of mappings
- **WARNING**: Dictionary file not found, using defaults
- **ERROR**: Failed to parse dictionary, malformed structure
- **DEBUG**: Individual keyword aspect assignments

## Testing Strategy

### Unit Tests
1. **AspectMapper Tests** (`tests/test_aspect_mapper.py`):
   - Load dictionary from YAML
   - Map keywords to aspects (exact match)
   - Handle case-insensitive matching
   - Handle unknown keywords
   - Validate dictionary structure
   - Handle malformed YAML

2. **SpacyYakeExtractor Tests** (`tests/test_extractors.py` additions):
   - Extract with aspect mapping enabled
   - Extract with aspect mapping disabled
   - Aspect distribution in metadata
   - Vietnamese text extraction
   - Backward compatibility (old result format)

### Integration Tests
1. **End-to-End Vietnamese**: Vietnamese text → Vietnamese model → aspect mapping
2. **Mixed Dictionary**: Text with both Vietnamese and English keywords
3. **Performance Test**: Verify extraction time < 500ms with aspect mapping

### Test Data
- English review text with known aspects
- Vietnamese review text with known aspects
- Mixed language text
- Edge cases: empty text, very long text, special characters

## Migration and Compatibility

### Backward Compatibility Guarantee
1. **Default Behavior**: Aspect mapping disabled by default
2. **Schema Extension**: New 'aspect' field added, old fields unchanged
3. **Null Handling**: Aspect field is null/None when disabled
4. **Metadata Extension**: New metadata fields added, existing fields unchanged

### Migration Path for Existing Users
1. **Phase 1**: Deploy with aspect mapping disabled (default)
2. **Phase 2**: Provide aspect dictionary templates
3. **Phase 3**: Users opt-in by enabling aspect mapping in config
4. **Phase 4**: Update documentation and examples

## Alternative Approaches Considered

### 1. ML-Based Aspect Classification
**Approach**: Train a classifier (BERT, etc.) to predict aspects
**Rejected Because**:
- Requires labeled training data
- Adds model training and deployment complexity
- Slower inference (100-200ms per text)
- Less transparent than dictionary-based

### 2. External Aspect Service
**Approach**: Call external API for aspect labeling
**Rejected Because**:
- Network latency (50-500ms)
- External dependency and availability risk
- Additional infrastructure cost
- Privacy concerns for sensitive text

### 3. Post-Processing Module
**Approach**: Separate aspect mapper that runs after extraction
**Rejected Because**:
- Two-pass approach is less efficient
- Requires passing data between modules
- Less cohesive design
- Duplicate configuration

### 4. LLM-Based Aspect Extraction
**Approach**: Use GPT/Claude to identify aspects
**Rejected Because**:
- Very high latency (1-5 seconds)
- API costs
- Requires internet connection
- Overkill for dictionary-based task

## Security Considerations

### YAML Injection
- Use `yaml.safe_load()` instead of `yaml.load()` to prevent code execution
- Validate dictionary structure before use

### Path Traversal
- Validate dictionary file paths
- Restrict to configuration directory only
- Reject paths with `..` or absolute paths outside config dir

### Resource Limits
- Limit dictionary size to prevent memory exhaustion
- Limit keyword length to prevent buffer issues
- Set timeout for dictionary loading

## Future Enhancements

1. **Multi-Level Aspects**: Hierarchical aspect taxonomy (e.g., DESIGN → EXTERIOR → COLOR)
2. **Aspect Synonyms**: Handle keyword synonyms within aspects
3. **Weighted Aspects**: Different keywords have different confidence weights
4. **Domain-Specific Dictionaries**: Pre-built dictionaries for common domains
5. **Aspect Auto-Discovery**: ML-based suggestion of new aspect-keyword mappings
6. **Aspect Sentiment**: Combine aspect with sentiment (e.g., DESIGN+POSITIVE)
