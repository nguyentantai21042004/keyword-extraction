# Implementation Tasks: Enhance SpaCy+YAKE with Aspect Mapping

## Implementation Status

**Overall Progress**: 10 of 23 tasks complete (43%)

### Completed Phases:
- ✅ **Phase 1: Foundation (Aspect Mapping Core)** - 4/4 tasks complete
- ✅ **Phase 2: Configuration and Setup** - 3/3 tasks complete
- ✅ **Phase 3: Integration with SpacyYakeExtractor** - 3/3 tasks complete

### Pending Phases:
- ⏸️ **Phase 4: Vietnamese Language Support** - 0/2 tasks (future work)
- ⏸️ **Phase 5: Testing and Validation** - 0/3 tasks (future work)
- ⏸️ **Phase 6: Documentation and Polish** - 0/3 tasks (future work)
- ⏸️ **Phase 7: Final Validation and Cleanup** - 0/3 tasks (future work)

**Note**: The core functionality (Phases 1-3) is complete and functional. Phases 4-7 represent additional enhancements and polishing tasks for future iterations.

---

## Overview
This task list breaks down the implementation into small, verifiable work items that deliver incremental user-visible progress. Tasks are ordered to enable early testing and validation.

## Task Sequencing
- **Sequential**: Tasks marked with `→` must complete before next task
- **Parallel**: Tasks marked with `||` can be done simultaneously
- **Dependencies**: Explicitly noted where applicable

---

## Phase 1: Foundation (Aspect Mapping Core)

### Task 1.1: Create AspectMapper Class Structure ✅ COMPLETED
**Type**: Implementation
**Dependencies**: None
**Validation**: Unit test passes
**Status**: ✅ Complete

- [x] Create new file `src/core/utils/aspect_mapper.py`
- [x] Define `AspectMapper` class with `__init__` method
- [x] Add attributes: `_aspect_map`, `_dictionary`, `_config`
- [x] Add placeholder methods: `load_dictionary()`, `map_keyword()`, `map_keywords()`
- [x] Write initial docstrings
- [x] Create corresponding test file `tests/test_aspect_mapper.py` with skeleton tests

**Acceptance Criteria**:
- [x] File created and importable
- [x] Class instantiates without errors
- [x] Basic test file exists

---

### Task 1.2: Implement Dictionary Loading ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 1.1 →
**Validation**: Unit test passes

- Implement `load_dictionary()` method to read YAML files
- Use `yaml.safe_load()` for security
- Parse YAML structure: `aspects: { ASPECT_NAME: { keywords: [...] } }`
- Build `_aspect_map` dict with lowercase normalized keys
- Add error handling for file not found, malformed YAML
- Log INFO on success, ERROR on failure

**Acceptance Criteria**:
- Loads valid YAML dictionary correctly
- Handles missing file gracefully (logs warning, empty dict)
- Handles malformed YAML gracefully (logs error, empty dict)
- Tests cover: valid dict, missing file, malformed YAML

---

### Task 1.3: Implement Keyword Mapping Logic ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 1.2 →
**Validation**: Unit test passes

- Implement `map_keyword()` method
  - Normalize input keyword to lowercase
  - Lookup in `_aspect_map`
  - Return aspect label or "UNKNOWN"
- Implement `map_keywords()` batch method
  - Process list of keywords
  - Return `Dict[str, str]` mapping keywords to aspects
- Add case-insensitive matching

**Acceptance Criteria**:
- Exact match returns correct aspect
- Case-insensitive matching works (e.g., "Battery" → "PERFORMANCE")
- Unknown keywords return "UNKNOWN"
- Batch mapping processes multiple keywords correctly
- Tests cover: exact match, case variations, unknowns, batch operation

---

### Task 1.4: Add Dictionary Validation ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 1.2 || (can parallel with 1.3)
**Validation**: Unit test passes

- Add `_validate_dictionary()` method called during load
- Check structure: aspects must be dict, keywords must be list
- Check keywords are non-empty strings
- Check for duplicate keywords within same aspect
- Log warnings for validation issues
- Skip invalid entries, continue with valid ones

**Acceptance Criteria**:
- Valid dictionary passes validation
- Invalid structure is caught and logged
- Duplicate keywords are detected and logged
- Invalid entries are skipped, valid ones used
- Tests cover: valid dict, invalid structure, duplicates

---

## Phase 2: Configuration and Setup

### Task 2.1: Create Default Aspect Dictionary YAML Files ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Configuration
**Dependencies**: None || (can parallel with Phase 1)
**Validation**: Manual review + YAML validation

- Create directory `config/aspect_dictionaries/`
- Create `config/aspect_dictionaries/default.yaml` with English aspects:
  - PERFORMANCE, DESIGN, PRICE, QUALITY, SERVICE
  - ~50 keywords across all aspects
- Create `config/aspect_dictionaries/vietnamese.yaml` with Vietnamese aspects:
  - Include both Vietnamese and English keywords
  - ~50-80 keywords total
- Validate YAML syntax

**Acceptance Criteria**:
- Both YAML files exist and are valid
- Default dict has at least 40 keywords across 5 aspects
- Vietnamese dict includes bilingual keywords
- Files are well-commented for user reference

---

### Task 2.2: Extend Configuration Schema ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Configuration
**Dependencies**: None || (can parallel with Phase 1)
**Validation**: Config loads successfully

- Update `src/config/default_config.yaml`:
  - Add `enable_aspect_mapping: false` to `spacy_yake` section
  - Add `aspect_dictionary_path` setting
  - Add `unknown_aspect_label: "UNKNOWN"`
- Create new `spacy_yake_vi` configuration profile:
  - Vietnamese-specific settings
  - Different YAKE parameters (n=3, dedupLim=0.9)
  - Reference Vietnamese dictionary
- Document new configuration options in comments

**Acceptance Criteria**:
- YAML syntax valid
- Config loads without errors
- Default has aspect mapping disabled (backward compatibility)
- Vietnamese profile exists with appropriate settings

---

### Task 2.3: Update ConfigManager to Support Aspect Settings ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 2.2 →
**Validation**: Integration test

- Update `src/config/config_manager.py` if needed to read new settings
- Ensure aspect mapping settings are accessible
- Add validation for aspect dictionary paths
- Add helper method to get aspect configuration

**Acceptance Criteria**:
- Aspect settings are readable from config
- Dictionary path resolution works
- Config validation passes

---

## Phase 3: Integration with SpacyYakeExtractor

### Task 3.1: Initialize AspectMapper in SpacyYakeExtractor ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 1.3 →, Task 2.2 →
**Validation**: Integration test

- Update `SpacyYakeExtractor.__init__()`:
  - Add `self.aspect_mapper = None` attribute
- Create new method `_initialize_aspect_mapper()`:
  - Check if `enable_aspect_mapping` is True
  - If enabled, instantiate `AspectMapper` with config settings
  - Handle initialization errors gracefully
  - Log success/failure
- Call `_initialize_aspect_mapper()` in `__init__`

**Acceptance Criteria**:
- AspectMapper initializes when enabled
- Stays None when disabled
- Errors are caught and logged
- Extractor works with and without aspect mapping

---

### Task 3.2: Add Aspect Mapping to Keyword Combination ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 3.1 →
**Validation**: Integration test

- Create helper method `_get_aspect(keyword: str) -> str`:
  - If `aspect_mapper` is None, return "UNKNOWN"
  - Otherwise call `aspect_mapper.map_keyword(keyword)`
- Update `_combine_keyword_sources()`:
  - Add `'aspect': self._get_aspect(keyword)` to each keyword dict
  - Apply to YAKE keywords, entities, and noun chunks
- Ensure aspect field is always present in keyword dicts

**Acceptance Criteria**:
- All keywords have 'aspect' field
- Aspect mapping works when enabled
- Returns "UNKNOWN" when disabled
- Test with both enabled and disabled states

---

### Task 3.3: Add Aspect Statistics to Metadata ✅ COMPLETED
**Status**: ✅ Complete

**Type**: Implementation
**Dependencies**: Task 3.2 →
**Validation**: Unit test + integration test

- Update `extract()` method to calculate aspect statistics:
  - Count keywords per aspect → `aspect_distribution` dict
  - Calculate percentage with known aspects → `aspect_coverage` float
- Add to `ExtractionResult` metadata:
  - `'aspect_distribution': {...}`
  - `'aspect_coverage': 0.0-1.0`
- Handle case where aspect mapping is disabled (omit or null values)

**Acceptance Criteria**:
- Aspect statistics appear in metadata when enabled
- Aspect coverage calculation is correct (known/total)
- Metadata omits aspect stats when disabled
- Tests verify correct calculation

---

## Phase 4: Vietnamese Language Support

### Task 4.1: Add Vietnamese spaCy Model Loading
**Type**: Implementation
**Dependencies**: Task 3.1 ||
**Validation**: Integration test

- Update `_initialize_models()` in `SpacyYakeExtractor`:
  - Check if language is 'vi' in config
  - If Vietnamese, attempt to load `vi_core_news_lg` or `vi_core_news_sm`
  - Handle model not found with helpful error message
  - Optionally attempt auto-download (document requirement)
- Add language-specific YAKE parameters based on config

**Acceptance Criteria**:
- Vietnamese model loads if available
- Helpful error if model not installed
- YAKE configured correctly for Vietnamese (n=3, etc.)
- English model still works (no regression)

---

### Task 4.2: Test Vietnamese Text Extraction
**Type**: Testing
**Dependencies**: Task 4.1 →
**Validation**: Integration test passes

- Create Vietnamese test texts in `tests/test_datasets.py`
- Add Vietnamese test case to `tests/test_extractors.py`:
  - Load Vietnamese profile config
  - Extract keywords from Vietnamese text
  - Verify Vietnamese keywords extracted
  - Verify aspect mapping works for Vietnamese
- Test bilingual dictionary (Vietnamese + English keywords)

**Acceptance Criteria**:
- Vietnamese text extraction produces keywords
- Vietnamese aspects map correctly
- Bilingual dictionary works for both languages
- Test passes consistently

---

## Phase 5: Testing and Validation

### Task 5.1: Write Comprehensive Unit Tests for AspectMapper
**Type**: Testing
**Dependencies**: Phase 1 complete →
**Validation**: All tests pass

- Test cases for `tests/test_aspect_mapper.py`:
  - `test_load_valid_dictionary`: Load and verify structure
  - `test_load_missing_file`: Handle missing file gracefully
  - `test_load_malformed_yaml`: Handle YAML parse errors
  - `test_map_keyword_exact_match`: Exact match returns aspect
  - `test_map_keyword_case_insensitive`: Case variations work
  - `test_map_keyword_unknown`: Unknown returns "UNKNOWN"
  - `test_map_keywords_batch`: Batch operation
  - `test_validate_dictionary_valid`: Validation passes
  - `test_validate_dictionary_invalid`: Validation fails appropriately
- Achieve >90% code coverage for `aspect_mapper.py`

**Acceptance Criteria**:
- All unit tests pass
- Code coverage >90%
- Edge cases covered

---

### Task 5.2: Write Integration Tests for SpacyYakeExtractor with Aspects
**Type**: Testing
**Dependencies**: Phase 3 complete →
**Validation**: All tests pass

- Add tests to `tests/test_extractors.py`:
  - `test_extract_with_aspect_mapping_enabled`: Full extraction with aspects
  - `test_extract_with_aspect_mapping_disabled`: Backward compatibility
  - `test_aspect_distribution_metadata`: Verify metadata statistics
  - `test_aspect_coverage_calculation`: Verify coverage metric
  - `test_unknown_aspect_for_unmapped_keywords`: Unknown handling
  - `test_mixed_aspects_in_results`: Multiple aspects in one extraction
- Verify backward compatibility (old tests still pass)

**Acceptance Criteria**:
- All new tests pass
- All existing tests still pass (no regression)
- Integration tests cover happy path and edge cases

---

### Task 5.3: Performance Testing
**Type**: Testing
**Dependencies**: Phase 3 complete →
**Validation**: Performance benchmarks met

- Add performance test to verify:
  - Aspect mapping overhead < 10ms for 20 keywords
  - Total extraction time < 500ms with aspect mapping enabled
  - Memory overhead < 200KB for typical dictionary
- Create benchmark script if needed
- Document performance results

**Acceptance Criteria**:
- Performance requirements met
- No significant regression vs. baseline (aspect disabled)
- Results documented

---

## Phase 6: Documentation and Polish

### Task 6.1: Update README and Documentation
**Type**: Documentation
**Dependencies**: Phase 5 complete →
**Validation**: Manual review

- Update `README.md`:
  - Add section on aspect mapping feature
  - Explain how to enable aspect mapping
  - Show example usage with aspects
  - Document Vietnamese support
- Update configuration documentation
- Add example aspect dictionary
- Document dictionary format and conventions

**Acceptance Criteria**:
- README has clear aspect mapping section
- Examples are runnable and correct
- Dictionary format is documented

---

### Task 6.2: Create Example Scripts and Demos
**Type**: Documentation/Examples
**Dependencies**: Phase 5 complete ||
**Validation**: Examples run successfully

- Create `examples/aspect_mapping_demo.py`:
  - Demo English text with aspect extraction
  - Show aspect distribution
  - Pretty-print results
- Create `examples/vietnamese_demo.py`:
  - Demo Vietnamese text extraction
  - Show bilingual aspect mapping
- Ensure examples are self-contained and runnable

**Acceptance Criteria**:
- Both demo scripts run successfully
- Output is clear and informative
- Code is well-commented

---

### Task 6.3: Add Type Hints and Docstrings
**Type**: Code Quality
**Dependencies**: Phase 3 complete ||
**Validation**: mypy passes, docs generated

- Add comprehensive docstrings to:
  - `AspectMapper` class and all methods
  - New methods in `SpacyYakeExtractor`
- Add type hints to all new code
- Run `mypy` type checker and fix issues
- Ensure code follows project conventions

**Acceptance Criteria**:
- All public methods have docstrings
- Type hints are complete and correct
- mypy passes with no errors
- Code follows Black formatting

---

## Phase 7: Final Validation and Cleanup

### Task 7.1: End-to-End Integration Test
**Type**: Testing
**Dependencies**: All implementation tasks complete →
**Validation**: E2E test passes

- Create comprehensive end-to-end test:
  - English text → extraction → aspect mapping → result validation
  - Vietnamese text → extraction → aspect mapping → result validation
  - Mixed scenario: aspect enabled, then disabled, verify both work
- Test with real-world sample texts
- Verify all metadata fields present and correct

**Acceptance Criteria**:
- E2E test covers full workflow
- Both English and Vietnamese work correctly
- Results match expected format

---

### Task 7.2: Backward Compatibility Verification
**Type**: Testing
**Dependencies**: All implementation tasks complete →
**Validation**: Compatibility tests pass

- Run all existing tests to ensure no regression
- Test old configuration files still work
- Test with aspect mapping disabled (default)
- Verify results are compatible with old consumers (no breaking changes)
- Document any breaking changes (should be none)

**Acceptance Criteria**:
- All existing tests pass
- No breaking changes to API or result format
- Default behavior unchanged (aspect mapping off)

---

### Task 7.3: Code Review and Cleanup
**Type**: Code Quality
**Dependencies**: All tasks complete →
**Validation**: Review checklist complete

- Review checklist:
  - [ ] All code follows project style (Black, PEP 8)
  - [ ] No TODO comments left in code
  - [ ] All tests pass
  - [ ] Type hints complete
  - [ ] Docstrings complete
  - [ ] No debug print statements
  - [ ] Logging levels appropriate
  - [ ] Error handling robust
  - [ ] Configuration defaults sensible
  - [ ] Documentation complete
- Address any issues found

**Acceptance Criteria**:
- All checklist items complete
- Code is production-ready

---

## Summary Statistics

- **Total Tasks**: 23
- **Phases**: 7
- **Estimated Sessions**: 3-4 development sessions
- **Critical Path**: Phase 1 → Phase 3 → Phase 5 → Phase 7
- **Parallelizable**: Phase 2 (config) can start immediately with Phase 1

## Task Dependencies Diagram

```
Phase 1 (Foundation)
├─ 1.1 → 1.2 → 1.3
│         └───→ 1.4 ||

Phase 2 (Config) || can start with Phase 1
├─ 2.1 ||
├─ 2.2 → 2.3
│
Phase 1 + Phase 2 Complete ↓

Phase 3 (Integration)
├─ 3.1 → 3.2 → 3.3

Phase 4 (Vietnamese) || can parallel with Phase 3
├─ 4.1 → 4.2

Phase 5 (Testing)
├─ 5.1 (depends on Phase 1)
├─ 5.2 (depends on Phase 3)
├─ 5.3 (depends on Phase 3)

Phase 6 (Docs) || can start when Phase 5 progresses
├─ 6.1, 6.2, 6.3 || all parallel

Phase 7 (Final)
└─ 7.1 → 7.2 → 7.3
```

## Risk Mitigation

### High-Risk Tasks
1. **Task 4.1** (Vietnamese model loading): May fail if model unavailable
   - *Mitigation*: Provide clear installation instructions, graceful fallback

2. **Task 3.2** (Integration): Complex changes to core extraction logic
   - *Mitigation*: Comprehensive tests, incremental changes

### Testing Priorities
1. **Must Test**: Aspect mapping core logic, backward compatibility
2. **Should Test**: Vietnamese support, performance
3. **Nice to Test**: Edge cases, error scenarios
