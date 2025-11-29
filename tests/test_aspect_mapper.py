"""
Unit tests for AspectMapper class.
"""

import pytest
from src.core.utils.aspect_mapper import AspectMapper


class TestAspectMapperInitialization:
    """Test AspectMapper initialization"""

    def test_init_empty(self):
        """Test initialization without dictionary"""
        mapper = AspectMapper()
        assert mapper is not None
        assert mapper._aspect_map == {}
        assert mapper._dictionary == {}

    def test_init_with_data(self):
        """Test initialization with dictionary data"""
        # Placeholder - will be implemented in Task 1.2
        pass

    def test_init_with_path(self):
        """Test initialization with dictionary file path"""
        # Placeholder - will be implemented in Task 1.2
        pass


class TestDictionaryLoading:
    """Test dictionary loading functionality"""

    def test_load_valid_dictionary(self):
        """Test loading a valid YAML dictionary"""
        mapper = AspectMapper(dictionary_path="/tmp/test_aspect_dicts/valid_dict.yaml")

        # Check dictionary was loaded
        assert len(mapper._dictionary) == 3
        assert "PERFORMANCE" in mapper._dictionary
        assert "DESIGN" in mapper._dictionary
        assert "PRICE" in mapper._dictionary

        # Check aspect map was built correctly
        assert len(mapper._aspect_map) > 0
        assert mapper._aspect_map.get("battery") == "PERFORMANCE"
        assert mapper._aspect_map.get("design") == "DESIGN"
        assert mapper._aspect_map.get("price") == "PRICE"

    def test_load_missing_file(self):
        """Test handling of missing dictionary file"""
        mapper = AspectMapper(dictionary_path="/tmp/test_aspect_dicts/nonexistent.yaml")

        # Should create empty dictionaries
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_load_malformed_yaml(self):
        """Test handling of malformed YAML"""
        mapper = AspectMapper(dictionary_path="/tmp/test_aspect_dicts/malformed.yaml")

        # Should handle gracefully with empty dictionaries
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_load_from_data(self):
        """Test loading from dictionary data"""
        data = {
            "aspects": {
                "PERFORMANCE": {
                    "keywords": ["battery", "speed"]
                },
                "DESIGN": {
                    "keywords": ["color", "style"]
                }
            }
        }

        mapper = AspectMapper(dictionary_data=data)

        assert len(mapper._dictionary) == 2
        assert "PERFORMANCE" in mapper._dictionary
        assert mapper._aspect_map.get("battery") == "PERFORMANCE"
        assert mapper._aspect_map.get("color") == "DESIGN"


class TestKeywordMapping:
    """Test keyword to aspect mapping"""

    def test_map_keyword_exact_match(self):
        """Test exact keyword match"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery", "speed"]},
                "DESIGN": {"keywords": ["color", "style"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        assert mapper.map_keyword("battery") == "PERFORMANCE"
        assert mapper.map_keyword("speed") == "PERFORMANCE"
        assert mapper.map_keyword("color") == "DESIGN"

    def test_map_keyword_case_insensitive(self):
        """Test case-insensitive matching"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # All case variations should match
        assert mapper.map_keyword("battery") == "PERFORMANCE"
        assert mapper.map_keyword("Battery") == "PERFORMANCE"
        assert mapper.map_keyword("BATTERY") == "PERFORMANCE"
        assert mapper.map_keyword("BaTTeRy") == "PERFORMANCE"

    def test_map_keyword_unknown(self):
        """Test mapping of unknown keyword"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        assert mapper.map_keyword("unknown_word") == "UNKNOWN"
        assert mapper.map_keyword("xyz") == "UNKNOWN"

    def test_map_keyword_custom_unknown_label(self):
        """Test custom unknown aspect label"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery"]}
            }
        }
        mapper = AspectMapper(
            dictionary_data=data,
            config={"unknown_aspect_label": "NOT_FOUND"}
        )

        assert mapper.map_keyword("unknown_word") == "NOT_FOUND"

    def test_map_keywords_batch(self):
        """Test batch keyword mapping"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery", "speed"]},
                "DESIGN": {"keywords": ["color"]},
                "PRICE": {"keywords": ["cost"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        keywords = ["battery", "color", "cost", "unknown"]
        result = mapper.map_keywords(keywords)

        assert result["battery"] == "PERFORMANCE"
        assert result["color"] == "DESIGN"
        assert result["cost"] == "PRICE"
        assert result["unknown"] == "UNKNOWN"

    def test_map_keywords_empty_list(self):
        """Test batch mapping with empty list"""
        mapper = AspectMapper()
        result = mapper.map_keywords([])
        assert result == {}

    def test_map_keyword_whitespace_handling(self):
        """Test keyword with whitespace"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        assert mapper.map_keyword("  battery  ") == "PERFORMANCE"
        assert mapper.map_keyword(" Battery ") == "PERFORMANCE"


class TestDictionaryValidation:
    """Test dictionary validation"""

    def test_validate_valid_dictionary(self):
        """Test validation of valid dictionary"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery", "speed"]},
                "DESIGN": {"keywords": ["color"]}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should load successfully
        assert len(mapper._dictionary) == 2
        assert len(mapper._aspect_map) == 3

    def test_validate_invalid_structure_not_dict(self):
        """Test validation catches non-dict aspects"""
        data = {
            "aspects": "not a dict"
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should fail validation and use empty dict
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_validate_missing_keywords_key(self):
        """Test aspect missing keywords key"""
        data = {
            "aspects": {
                "PERFORMANCE": {"something": "else"}  # Missing 'keywords'
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should skip invalid aspect
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_validate_keywords_not_list(self):
        """Test keywords value is not a list"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": "not a list"}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should skip invalid aspect
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_validate_duplicate_keywords(self):
        """Test detection of duplicate keywords within same aspect"""
        data = {
            "aspects": {
                "PERFORMANCE": {
                    "keywords": ["battery", "Battery", "BATTERY"]  # Duplicates
                }
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should load but deduplicate (only first occurrence)
        assert "PERFORMANCE" in mapper._dictionary
        # Only one "battery" in normalized map
        assert mapper._aspect_map.get("battery") == "PERFORMANCE"

    def test_validate_empty_keywords(self):
        """Test aspect with empty keywords list"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": []}
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should skip empty aspect
        assert mapper._dictionary == {}
        assert mapper._aspect_map == {}

    def test_validate_invalid_keyword_types(self):
        """Test keywords with invalid types"""
        data = {
            "aspects": {
                "PERFORMANCE": {
                    "keywords": ["battery", 123, None, "", "  ", "speed"]
                }
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should skip invalid keywords but keep valid ones
        assert "PERFORMANCE" in mapper._dictionary
        assert mapper._aspect_map.get("battery") == "PERFORMANCE"
        assert mapper._aspect_map.get("speed") == "PERFORMANCE"
        # Invalid ones should not be in map
        assert "123" not in mapper._aspect_map
        assert "" not in mapper._aspect_map

    def test_validate_mixed_valid_invalid_aspects(self):
        """Test dictionary with mix of valid and invalid aspects"""
        data = {
            "aspects": {
                "PERFORMANCE": {"keywords": ["battery"]},  # Valid
                "DESIGN": "not a dict",  # Invalid - skipped
                "PRICE": {"keywords": []},  # Empty - included but no keywords in map
                "QUALITY": {"keywords": ["durable"]}  # Valid
            }
        }
        mapper = AspectMapper(dictionary_data=data)

        # Should load valid aspects (PRICE is included even if empty)
        assert "PERFORMANCE" in mapper._dictionary
        assert "QUALITY" in mapper._dictionary
        assert "DESIGN" not in mapper._dictionary  # Invalid, skipped

        # Aspect map should only have keywords from valid non-empty aspects
        assert len(mapper._aspect_map) == 2  # battery + durable
        assert mapper._aspect_map.get("battery") == "PERFORMANCE"
        assert mapper._aspect_map.get("durable") == "QUALITY"


class TestStatistics:
    """Test statistics functionality"""

    def test_get_statistics_empty(self):
        """Test statistics for empty dictionary"""
        mapper = AspectMapper()
        stats = mapper.get_statistics()
        assert stats["total_aspects"] == 0
        assert stats["total_keywords"] == 0
        assert stats["aspects"] == []

    def test_get_statistics_with_data(self):
        """Test statistics with loaded dictionary"""
        # Placeholder - will be implemented in Task 1.2
        pass
