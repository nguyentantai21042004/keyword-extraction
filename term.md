Proposal: Hybrid Keyword Extraction Adapter

Module: adapters/ai/keyword_client.py
Role: NLP Extraction Adapter – Hybrid Engine
Author: [Your Name]
Date: 2025-11-29

⸻

1. Overview

Currently, Vietnamese keyword extraction from text faces several issues:
	•	Many statistical algorithms (YAKE, TF-IDF) return meaningless keywords due to high frequency.
	•	Some linguistic algorithms are not strong enough to handle N-grams or multi-word phrases.
	•	Aspect (topic group) labeling is not yet automated.

Solution: Build a Hybrid Keyword Extractor that combines:
	1.	YAKE: Ranks keywords based on frequency, position, and N-grams.
	2.	SpaCy: Filters keywords by grammar (accepts only nouns and noun phrases).
	3.	Aspect Mapping: Uses a domain-specific dictionary to assign topic labels.

The result is a set of relevant and meaningful keywords, well-prepared for downstream tasks such as Sentiment Analysis.

⸻

2. Functional Requirements

Input:
	•	Vietnamese text (string)
	•	Optional: top_n (maximum number of keywords)

Output:

[
    {
        "keyword": str,
        "weight": float, # 0-1, higher means more important
        "score": float,  # YAKE score, lower is better
        "aspect": str,   # assigned DOMAIN or UNKNOWN
        "method": "HYBRID"
    },
    ...
]

Functional Rules:
	1.	Grammar Filtering (SpaCy)
	•	Accept only NOUN/PROPN
	•	Remove meaningless words or stopwords
	2.	Context Ranking (YAKE)
	•	N-gram max size = 3
	•	Weighting by position, frequency
	3.	Aspect Mapping
	•	Automatically assign label using dictionary (ASPECT_DICTIONARY)
	•	For example: "pin" → "PERFORMANCE", "thiết kế" → "DESIGN"

⸻

3. Technical Design

3.1. Interface

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

class KeywordResult(BaseModel):
    text: str
    score: float
    aspect: str

class IKeywordExtractor(ABC):
    @abstractmethod
    def extract(self, text: str, top_n: int = 10) -> List[KeywordResult]:
        """Extract and label keywords"""
        pass

3.2. Core Implementation: Hybrid Pipeline

Logic:
	1.	YAKE extracts candidate keywords
	2.	SpaCy validates candidates (POS & stopwords)
	3.	Map to Aspect dictionary
	4.	Normalize score (1 / (score + 1))
	5.	Return top N keywords

Pseudocode:

raw_candidates = yake_extractor.extract_keywords(text)
results = []

for kw, score in raw_candidates:
    if not _is_valid_candidate(kw):
        continue
    aspect = _map_aspect(kw)
    normalized_score = 1.0 / (score + 1.0)
    results.append(KeywordResult(text=kw, score=normalized_score, aspect=aspect))
    if len(results) >= top_n:
        break
return results

3.3. Aspect Dictionary

ASPECT_DICTIONARY = {
    "PERFORMANCE": ["pin", "sạc", "động cơ", "tốc độ", "quãng đường", "lỗi", "treo"],
    "DESIGN": ["thiết kế", "màu", "ngoại thất", "nội thất", "đẹp", "xấu", "nhựa"],
    "PRICE": ["giá", "tiền", "đắt", "rẻ", "lăn bánh", "cọc"],
    "SERVICE": ["bảo hành", "nhân viên", "showroom", "thái độ", "cứu hộ"]
}

⸻

4. YAKE Configuration

Library: yake (Vietnamese support)

Parameter	Value	Description
lan	"vi"	Vietnamese
n	2-3	Max N-gram size
dedupLim	0.9	Deduplication threshold
top	20	Top K candidates
windowsSize	1	Context window

Output Example:

[
    {"keyword": "thiết kế", "weight": 0.85, "score": 0.15, "method": "YAKE"},
    {"keyword": "pin", "weight": 0.72, "score": 0.28, "method": "YAKE"}
]

⸻

5. Performance & Edge Cases
	•	Extraction time: < 500ms per text
	•	Empty text → return empty list
	•	Text < 10 words → extract fewer keywords
	•	Stopwords → filtered via SpaCy + YAKE
	•	Duplicate keywords → deduplicate by highest weight

⸻

6. Integration Workflow

text = "VinFast VF8 car has a beautiful design, strong battery but the price is high"

# Step 1: Extract keywords
keywords = HybridKeywordAdapter().extract(text)

# Step 2: Analyze sentiment
sentiment = PhoBERTONNX("models/phobert_sentiment_cpu.onnx").predict(text)

# Step 3: Combine
result = {
    "text": text,
    "keywords": keywords,
    "sentiment": sentiment
}

⸻

7. Error Handling
	•	Model not found → raise clear error
	•	Invalid input → return default empty list
	•	Timeout → raise TimeoutError
	•	Memory overflow → degrade gracefully

⸻

9. Benefits
	•	Filters out irrelevant keywords (thanks to SpaCy grammar filter)
	•	Automatically assigns aspect labels
	•	Supports multi-word keywords, top N configurable
	•	Prepares high quality data for downstream NLP tasks

An instance must be initialized at the beginning of the service to load the model and config, and should not be re-initialized on every request.