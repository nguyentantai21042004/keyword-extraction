"""
Aspect Mapper for keyword domain/topic labeling.

This module provides functionality to map extracted keywords to semantic
aspect categories (e.g., PERFORMANCE, DESIGN, PRICE) using configurable
dictionaries.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class AspectMapper:
    """
    Maps keywords to aspect/domain labels using dictionary-based matching.

    Attributes:
        _aspect_map: Flattened dict mapping keywords to aspects (lowercase keys)
        _dictionary: Original aspect dictionary structure
        _config: Configuration settings
        logger: Logger instance

    Example:
        >>> mapper = AspectMapper(dictionary_path="config/aspects.yaml")
        >>> aspect = mapper.map_keyword("battery")
        >>> print(aspect)  # "PERFORMANCE"
    """

    def __init__(
        self,
        dictionary_path: Optional[str] = None,
        dictionary_data: Optional[Dict] = None,
        config: Optional[Dict] = None
    ):
        """
        Initialize AspectMapper with dictionary source.

        Args:
            dictionary_path: Path to YAML dictionary file
            dictionary_data: Pre-loaded dictionary data
            config: Additional configuration options

        Note:
            Either dictionary_path or dictionary_data should be provided.
            If both are provided, dictionary_data takes precedence.
        """
        self._aspect_map: Dict[str, str] = {}
        self._dictionary: Dict[str, List[str]] = {}
        self._config = config or {}
        self.logger = logging.getLogger(__name__)

        # Load dictionary if provided
        if dictionary_data:
            self._load_from_data(dictionary_data)
        elif dictionary_path:
            self.load_dictionary(dictionary_path)

    def load_dictionary(self, path: str) -> None:
        """
        Load aspect dictionary from YAML file.

        Args:
            path: Path to YAML dictionary file

        Raises:
            FileNotFoundError: If dictionary file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                self.logger.warning(f"Dictionary file not found: {path}. Using empty dictionary.")
                self._aspect_map = {}
                self._dictionary = {}
                return

            # Load YAML file using safe_load for security
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                self.logger.warning(f"Empty dictionary file: {path}")
                self._aspect_map = {}
                self._dictionary = {}
                return

            # Load from parsed data
            self._load_from_data(data)
            self.logger.info(
                f"Loaded aspect dictionary from {path}: "
                f"{len(self._dictionary)} aspects, {len(self._aspect_map)} keywords"
            )

        except yaml.YAMLError as e:
            self.logger.error(f"Malformed YAML in {path}: {e}. Using empty dictionary.")
            self._aspect_map = {}
            self._dictionary = {}

        except Exception as e:
            self.logger.error(f"Failed to load dictionary from {path}: {e}. Using empty dictionary.")
            self._aspect_map = {}
            self._dictionary = {}

    def _load_from_data(self, data: Dict) -> None:
        """
        Load aspect dictionary from pre-loaded data.

        Expected format:
            {
                "aspects": {
                    "PERFORMANCE": {"keywords": ["battery", "speed", ...]},
                    "DESIGN": {"keywords": ["color", "style", ...]},
                    ...
                }
            }

        Args:
            data: Dictionary data structure
        """
        try:
            if not isinstance(data, dict):
                self.logger.error(f"Invalid dictionary format: expected dict, got {type(data)}")
                self._aspect_map = {}
                self._dictionary = {}
                return

            # Extract aspects section
            aspects = data.get('aspects', {})
            if not aspects:
                self.logger.warning("No 'aspects' key found in dictionary data")
                self._aspect_map = {}
                self._dictionary = {}
                return

            # Validate dictionary structure
            is_valid = self._validate_dictionary(aspects)
            if not is_valid:
                self.logger.error("Dictionary validation failed. Using empty dictionary.")
                self._aspect_map = {}
                self._dictionary = {}
                return

            # Build both the original dictionary and the flattened aspect map
            self._dictionary = {}
            self._aspect_map = {}

            for aspect_name, aspect_data in aspects.items():
                # Validate aspect data
                if not isinstance(aspect_data, dict):
                    self.logger.warning(f"Invalid data for aspect '{aspect_name}': expected dict")
                    continue

                keywords = aspect_data.get('keywords', [])
                if not isinstance(keywords, list):
                    self.logger.warning(f"Invalid keywords for aspect '{aspect_name}': expected list")
                    continue

                # Store in original dictionary
                self._dictionary[aspect_name] = keywords

                # Build flattened map with lowercase keys for case-insensitive matching
                for keyword in keywords:
                    if not isinstance(keyword, str) or not keyword.strip():
                        self.logger.warning(f"Skipping invalid keyword in aspect '{aspect_name}': {keyword}")
                        continue

                    keyword_normalized = keyword.strip().lower()
                    if keyword_normalized in self._aspect_map:
                        self.logger.warning(
                            f"Duplicate keyword '{keyword}' found. "
                            f"Previously mapped to '{self._aspect_map[keyword_normalized]}', "
                            f"now mapping to '{aspect_name}'"
                        )
                    self._aspect_map[keyword_normalized] = aspect_name

        except Exception as e:
            self.logger.error(f"Error loading dictionary data: {e}")
            self._aspect_map = {}
            self._dictionary = {}

    def _validate_dictionary(self, aspects: Dict) -> bool:
        """
        Validate aspect dictionary structure.

        Checks:
        - Aspects must be a dictionary
        - Each aspect must have a 'keywords' list
        - Keywords must be non-empty strings
        - Detects duplicate keywords within same aspect

        Args:
            aspects: Dictionary of aspects to validate

        Returns:
            True if dictionary is valid (or has minor issues that can be skipped),
            False if dictionary has fatal errors
        """
        if not isinstance(aspects, dict):
            self.logger.error(f"Aspects must be a dictionary, got {type(aspects)}")
            return False

        if not aspects:
            self.logger.warning("Empty aspects dictionary")
            return True  # Empty is valid, just not useful

        has_valid_aspect = False

        for aspect_name, aspect_data in aspects.items():
            # Check aspect data is a dict
            if not isinstance(aspect_data, dict):
                self.logger.warning(f"Aspect '{aspect_name}' data must be dict, got {type(aspect_data)}")
                continue

            # Check keywords exist
            if 'keywords' not in aspect_data:
                self.logger.warning(f"Aspect '{aspect_name}' missing 'keywords' key")
                continue

            keywords = aspect_data['keywords']

            # Check keywords is a list
            if not isinstance(keywords, list):
                self.logger.warning(f"Aspect '{aspect_name}' keywords must be list, got {type(keywords)}")
                continue

            # Check for empty keywords list
            if not keywords:
                self.logger.warning(f"Aspect '{aspect_name}' has empty keywords list")
                continue

            # Validate individual keywords
            valid_keywords = []
            seen_keywords = set()

            for keyword in keywords:
                # Check keyword is string
                if not isinstance(keyword, str):
                    self.logger.warning(
                        f"Aspect '{aspect_name}': Invalid keyword type {type(keyword)}, expected string"
                    )
                    continue

                # Check keyword is non-empty
                keyword_stripped = keyword.strip()
                if not keyword_stripped:
                    self.logger.warning(f"Aspect '{aspect_name}': Empty or whitespace-only keyword")
                    continue

                # Check for duplicates within same aspect
                keyword_normalized = keyword_stripped.lower()
                if keyword_normalized in seen_keywords:
                    self.logger.warning(
                        f"Aspect '{aspect_name}': Duplicate keyword '{keyword}'"
                    )
                    continue

                seen_keywords.add(keyword_normalized)
                valid_keywords.append(keyword)

            # If this aspect has at least one valid keyword, mark as having valid aspect
            if valid_keywords:
                has_valid_aspect = True

        if not has_valid_aspect:
            self.logger.error("No valid aspects found in dictionary")
            return False

        return True

    def map_keyword(self, keyword: str) -> str:
        """
        Map a single keyword to its aspect label.

        Args:
            keyword: Keyword to map

        Returns:
            Aspect label (e.g., "PERFORMANCE") or "UNKNOWN"

        Example:
            >>> mapper.map_keyword("battery")
            "PERFORMANCE"
            >>> mapper.map_keyword("unknown_word")
            "UNKNOWN"
        """
        if not keyword or not isinstance(keyword, str):
            return self._config.get('unknown_aspect_label', 'UNKNOWN')

        # Normalize to lowercase for case-insensitive matching
        keyword_normalized = keyword.strip().lower()

        # Lookup in aspect map
        return self._aspect_map.get(
            keyword_normalized,
            self._config.get('unknown_aspect_label', 'UNKNOWN')
        )

    def map_keywords(self, keywords: List[str]) -> Dict[str, str]:
        """
        Map multiple keywords to their aspect labels (batch operation).

        Args:
            keywords: List of keywords to map

        Returns:
            Dictionary mapping each keyword to its aspect label

        Example:
            >>> mapper.map_keywords(["battery", "design", "price"])
            {"battery": "PERFORMANCE", "design": "DESIGN", "price": "PRICE"}
        """
        if not keywords:
            return {}

        result = {}
        for keyword in keywords:
            if isinstance(keyword, str) and keyword.strip():
                result[keyword] = self.map_keyword(keyword)

        return result

    def get_statistics(self) -> Dict:
        """
        Return statistics about the loaded dictionary.

        Returns:
            Dictionary with statistics (aspect count, keyword count, etc.)

        Example:
            >>> mapper.get_statistics()
            {
                "total_aspects": 5,
                "total_keywords": 42,
                "aspects": ["PERFORMANCE", "DESIGN", "PRICE", ...]
            }
        """
        return {
            "total_aspects": len(self._dictionary),
            "total_keywords": len(self._aspect_map),
            "aspects": list(self._dictionary.keys())
        }
