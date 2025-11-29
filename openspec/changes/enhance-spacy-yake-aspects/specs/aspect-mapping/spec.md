# Capability: Aspect Mapping

## Overview

Aspect mapping automatically assigns semantic domain labels to extracted keywords based on configurable dictionaries. This enables downstream systems to understand the topical category of each keyword (e.g., PERFORMANCE, DESIGN, PRICE, SERVICE).

## ADDED Requirements

### Requirement: Aspect Dictionary Configuration

The system SHALL support loading aspect dictionaries from YAML configuration files.

**Priority**: High
**Rationale**: Dictionary-based approach provides transparency and easy customization for different domains

#### Scenario: Load aspect dictionary from YAML

- **GIVEN** a YAML configuration file at `config/aspect_dictionaries/default.yaml`
- **AND** the file contains aspect definitions with keywords
- **WHEN** the SpacyYakeExtractor is initialized
- **THEN** the aspect dictionary SHALL be loaded into memory
- **AND** the extractor SHALL be ready to map keywords to aspects

#### Scenario: Handle missing aspect dictionary

- **GIVEN** no aspect dictionary configuration is provided
- **WHEN** the SpacyYakeExtractor is initialized
- **THEN** the extractor SHALL use an empty default dictionary
- **AND** all keywords SHALL be assigned aspect "UNKNOWN"
- **AND** extraction SHALL continue without errors

### Requirement: Keyword to Aspect Mapping

The system SHALL map extracted keywords to aspect labels using the loaded dictionary.

**Priority**: High
**Rationale**: Core functionality that enriches keywords with semantic meaning

#### Scenario: Exact match mapping

- **GIVEN** an aspect dictionary with "pin" mapped to "PERFORMANCE"
- **AND** a text containing "pin tốt" (good battery)
- **WHEN** keywords are extracted including "pin"
- **THEN** the keyword "pin" SHALL have aspect label "PERFORMANCE"

#### Scenario: Multi-word keyword matching

- **GIVEN** an aspect dictionary with "thiết kế" mapped to "DESIGN"
- **AND** a text containing "thiết kế đẹp" (beautiful design)
- **WHEN** the multi-word keyword "thiết kế" is extracted
- **THEN** the keyword SHALL have aspect label "DESIGN"

#### Scenario: Case-insensitive matching

- **GIVEN** an aspect dictionary with "battery" mapped to "PERFORMANCE"
- **AND** a text containing "Battery life is excellent"
- **WHEN** the keyword "battery" is extracted (lowercase)
- **THEN** the keyword SHALL match the dictionary entry
- **AND** SHALL have aspect label "PERFORMANCE"

#### Scenario: Unknown keyword aspect

- **GIVEN** an aspect dictionary that does not contain "smartphone"
- **AND** a text from which "smartphone" is extracted as a keyword
- **WHEN** aspect mapping is performed
- **THEN** the keyword "smartphone" SHALL have aspect label "UNKNOWN"

### Requirement: Multiple Aspect Handling

The system SHALL handle cases where a keyword could match multiple aspects deterministically.

**Priority**: Medium
**Rationale**: Ensures predictable behavior when dictionary overlap occurs

#### Scenario: First match precedence

- **GIVEN** an aspect dictionary with overlapping keywords where "value" appears in both PERFORMANCE and PRICE
- **AND** a keyword "value" is extracted
- **WHEN** aspect mapping is performed
- **THEN** the keyword SHALL be assigned to the first matching aspect in dictionary order

### Requirement: Aspect Dictionary Validation

The system SHALL validate aspect dictionary structure on load.

**Priority**: Medium
**Rationale**: Prevents runtime errors from malformed dictionaries

#### Scenario: Validate dictionary structure

- **GIVEN** an aspect dictionary YAML file
- **WHEN** the dictionary is loaded
- **THEN** the system SHALL validate that each aspect has a list of keywords
- **AND** keywords are non-empty strings
- **AND** no duplicate keywords within same aspect
- **AND** SHALL log warnings for any validation issues
- **AND** SHALL skip invalid entries

#### Scenario: Handle malformed YAML

- **GIVEN** a malformed aspect dictionary YAML file
- **WHEN** the SpacyYakeExtractor attempts to load it
- **THEN** the system SHALL log an error
- **AND** SHALL fall back to empty dictionary
- **AND** SHALL continue operation with all aspects as "UNKNOWN"

### Requirement: Aspect Mapping Performance

Aspect mapping SHALL not significantly degrade extraction performance.

**Priority**: High
**Rationale**: Maintains system performance requirements

#### Scenario: Efficient dictionary lookup

- **GIVEN** an aspect dictionary with 100 keywords across 5 aspects
- **AND** text that yields 20 extracted keywords
- **WHEN** aspect mapping is performed
- **THEN** the mapping operation SHALL complete in under 10ms
- **AND** total extraction time SHALL remain under 500ms

### Requirement: Aspect Mapping Toggle

Aspect mapping SHALL be configurable via the main configuration file.

**Priority**: Medium
**Rationale**: Allows users to disable feature if not needed

#### Scenario: Disable aspect mapping

- **GIVEN** configuration with `enable_aspect_mapping: false`
- **WHEN** the SpacyYakeExtractor performs extraction
- **THEN** aspect mapping SHALL be skipped
- **AND** all keywords SHALL have aspect "UNKNOWN" or null

#### Scenario: Enable aspect mapping

- **GIVEN** configuration with `enable_aspect_mapping: true`
- **AND** a valid aspect dictionary path
- **WHEN** the SpacyYakeExtractor performs extraction
- **THEN** aspect mapping SHALL be performed
- **AND** keywords SHALL have appropriate aspect labels
