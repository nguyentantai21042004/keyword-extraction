# Capability: Vietnamese Language Support

## Overview

Vietnamese language support enables the SpaCy+YAKE extractor to process Vietnamese text effectively using appropriate spaCy models and YAKE configurations optimized for Vietnamese linguistic characteristics.

## ADDED Requirements

### Requirement: Vietnamese spaCy Model Support

The system SHALL support Vietnamese spaCy models for text processing.

**Priority**: High
**Rationale**: Vietnamese has different linguistic structures requiring dedicated models

#### Scenario: Load Vietnamese spaCy model

- **GIVEN** configuration specifying Vietnamese language `language: "vi"`
- **AND** spaCy model `vi_core_news_lg` or `vi_core_news_sm` is available
- **WHEN** SpacyYakeExtractor is initialized
- **THEN** the Vietnamese spaCy model SHALL be loaded
- **AND** the extractor SHALL be ready to process Vietnamese text

#### Scenario: Fallback when Vietnamese model unavailable

- **GIVEN** configuration specifying Vietnamese language
- **AND** Vietnamese spaCy model is not installed
- **WHEN** SpacyYakeExtractor is initialized
- **THEN** the system SHALL log a warning about missing model
- **AND** SHALL attempt to download the model automatically or provide clear installation instructions
- **AND** SHALL fail gracefully with informative error if download fails

### Requirement: Vietnamese YAKE Configuration

The system SHALL configure YAKE parameters optimized for Vietnamese text.

**Priority**: High
**Rationale**: Vietnamese characteristics (monosyllabic, tonal) require different parameters

#### Scenario: Vietnamese YAKE parameters

- **GIVEN** configuration with `language: "vi"`
- **WHEN** YAKE is initialized for Vietnamese
- **THEN** YAKE SHALL be configured with `lan: "vi"` for Vietnamese language
- **AND** SHALL use `n: 3` for max N-gram size to capture Vietnamese multi-word terms
- **AND** SHALL use `dedupLim: 0.9` for deduplication threshold
- **AND** SHALL use `windowsSize: 1` for context window

#### Scenario: Vietnamese stopword handling

- **GIVEN** Vietnamese text processing is enabled
- **WHEN** YAKE extracts candidates
- **THEN** Vietnamese stopwords SHALL be filtered appropriately
- **AND** meaningful Vietnamese keywords SHALL be preserved

### Requirement: Vietnamese POS Filtering

The system SHALL apply Vietnamese-appropriate part-of-speech filtering.

**Priority**: Medium
**Rationale**: Vietnamese grammar patterns differ from English

#### Scenario: Vietnamese noun phrase extraction

- **GIVEN** Vietnamese text "điện thoại thông minh" (smartphone)
- **WHEN** spaCy processes the text
- **THEN** noun phrases SHALL be extracted according to Vietnamese grammar rules
- **AND** SHALL include appropriate multi-word terms

#### Scenario: Vietnamese entity recognition

- **GIVEN** Vietnamese text with named entities like "VinFast", "Hà Nội"
- **WHEN** entity extraction is performed
- **THEN** Vietnamese proper nouns SHALL be correctly identified
- **AND** SHALL be included in keyword results with entity type labels

### Requirement: Bilingual Dictionary Support

Aspect dictionaries SHALL support both Vietnamese and English keywords.

**Priority**: Medium
**Rationale**: Many Vietnamese texts contain English loanwords and technical terms

#### Scenario: Mixed language aspect dictionary

- **GIVEN** an aspect dictionary containing both Vietnamese and English keywords for the same aspect
- **AND** Vietnamese text containing both "pin" and "battery"
- **WHEN** keywords are extracted
- **THEN** both "pin" and "battery" SHALL map to the same aspect "PERFORMANCE"
- **AND** aspect labeling SHALL work correctly for both languages

### Requirement: Vietnamese Text Normalization

The system SHALL normalize Vietnamese text for consistent processing.

**Priority**: Medium
**Rationale**: Vietnamese diacritics and encoding variations need handling

#### Scenario: Diacritic normalization

- **GIVEN** Vietnamese text with various diacritic representations
- **WHEN** text is preprocessed
- **THEN** diacritics SHALL be normalized to composed form (NFC)
- **AND** keyword matching SHALL be consistent regardless of encoding

#### Scenario: Vietnamese number and punctuation handling

- **GIVEN** Vietnamese text with numbers and Vietnamese punctuation
- **WHEN** text is processed
- **THEN** Vietnamese-specific number formats SHALL be handled correctly
- **AND** Vietnamese punctuation SHALL not interfere with keyword extraction
