# Proposal: Enhance SpaCy+YAKE with Aspect Mapping

**Change ID**: `enhance-spacy-yake-aspects`
**Status**: Proposed
**Date**: 2025-11-29
**Author**: AI Assistant

## Overview

This proposal enhances the existing SpaCy+YAKE keyword extraction method with automatic aspect/domain labeling capabilities and improved Vietnamese language support. The enhancement addresses current limitations where statistical algorithms return high-frequency but meaningless keywords, and adds semantic categorization to extracted keywords.

## Problem Statement

The current SpaCy+YAKE implementation has several limitations:

1. **No Semantic Context**: Keywords are extracted without domain/topic labels, making it difficult to understand their semantic category (e.g., PERFORMANCE, DESIGN, PRICE)
2. **Limited Vietnamese Support**: While YAKE supports Vietnamese, the current configuration and grammar filtering are optimized for English
3. **Missing Aspect Classification**: Downstream tasks like sentiment analysis would benefit from knowing which domain/aspect each keyword relates to
4. **Inflexible Grammar Filtering**: Current POS filtering is basic and doesn't leverage configurable stopword lists

## Proposed Solution

Enhance the `SpacyYakeExtractor` to include:

1. **Aspect Dictionary System**: Configurable domain dictionaries that map keywords to semantic categories
2. **Vietnamese Language Profile**: Dedicated configuration and spaCy model support for Vietnamese text
3. **Enhanced Grammar Filtering**: Improved POS-based filtering with configurable stopword lists
4. **Enriched Result Schema**: Extended `ExtractionResult` to include aspect labels for each keyword

## Goals

1. Add configurable aspect/domain mapping with dictionary-based classification
2. Support Vietnamese text with appropriate spaCy models and YAKE configuration
3. Enrich keyword results with aspect labels while maintaining backward compatibility
4. Maintain extraction performance under 500ms per text
5. Preserve existing test coverage and add tests for new capabilities

## Non-Goals

1. Machine learning-based aspect classification (future enhancement)
2. Multi-language aspect dictionaries in this change (can be added separately)
3. Changes to other extractor methods beyond SpaCy+YAKE
4. UI/API changes for consuming applications

## Scope

### In Scope
- Aspect dictionary configuration and loading
- Aspect mapping logic integrated into SpaCy+YAKE pipeline
- Vietnamese language support configuration
- Enhanced keyword result schema with aspect field
- Unit tests for aspect mapping
- Documentation updates

### Out of Scope
- Custom aspect dictionary UI/editor
- Automatic aspect dictionary generation
- Multi-language aspect dictionaries (handled via configuration)
- Changes to BaseExtractor interface

## Success Criteria

1. Keywords include aspect labels (e.g., "PERFORMANCE", "DESIGN", "UNKNOWN")
2. Vietnamese text extraction works with appropriate spaCy model
3. Aspect mapping accuracy >= 80% for keywords in dictionary
4. Extraction time remains < 500ms for typical texts (< 1000 words)
5. All existing tests pass with backward compatibility maintained
6. New tests cover aspect mapping and Vietnamese support

## Impact Assessment

### Benefits
- **Better Downstream Analysis**: Aspect-labeled keywords enable more precise sentiment analysis and topic modeling
- **Domain Flexibility**: Configurable dictionaries allow customization for different domains (e-commerce, reviews, support tickets)
- **Vietnamese Support**: Opens usage to Vietnamese text applications
- **Richer Metadata**: Enhanced results provide more context for consumers

### Risks
- **Dictionary Maintenance**: Aspect dictionaries need domain expertise to maintain
- **Memory Overhead**: Loading aspect dictionaries increases memory usage (minimal impact)
- **Configuration Complexity**: More configuration options may confuse users

### Mitigation Strategies
- Provide sensible default aspect dictionaries
- Document aspect dictionary format clearly
- Make aspect mapping optional via configuration flag
- Include example dictionaries for common domains

## Dependencies

- Existing SpaCy+YAKE implementation (`src/core/extractors/spacy_yake.py`)
- Configuration system (`src/config/`)
- Vietnamese spaCy model: `vi_core_news_lg` or `vi_core_news_sm`

## Timeline Estimate

- Implementation: 2-3 development sessions
- Testing: 1 session
- Documentation: 1 session

## Open Questions

1. **Dictionary Format**: Should we use YAML, JSON, or Python dict for aspect dictionaries?
   - *Recommendation*: YAML for readability and consistency with existing config

2. **Multi-word Matching**: How should aspect mapping handle partial matches for multi-word keywords?
   - *Recommendation*: Use exact match first, then substring match with longest match wins

3. **Unknown Aspects**: What label should keywords without aspect mapping receive?
   - *Recommendation*: "UNKNOWN" or configurable default

4. **Dictionary Priority**: If a keyword matches multiple aspects, which takes precedence?
   - *Recommendation*: First match in ordered dictionary, or highest priority if priorities are configured

## Related Changes

None (initial enhancement)

## Alternatives Considered

1. **ML-based Aspect Classification**: Using a trained classifier
   - *Rejected*: Adds complexity and model training overhead; dictionary-based is simpler and transparent

2. **External Aspect Service**: Call external API for aspect labeling
   - *Rejected*: Adds latency and external dependency; local dictionary is faster

3. **Post-processing Module**: Separate aspect mapper after extraction
   - *Rejected*: Integrated approach is more efficient and cohesive

## References

- Term.md proposal document: `/Users/tantai/Workspaces/smap/keyword-extraction/term.md`
- Existing implementation: `src/core/extractors/spacy_yake.py`
- Project conventions: `openspec/project.md`
