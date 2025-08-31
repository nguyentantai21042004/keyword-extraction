"""
Configuration management for the keyword extraction framework
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json
import yaml
from enum import Enum


class ConfigError(Exception):
    """Configuration related errors"""
    pass


class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class ExtractorConfig:
    """Configuration for individual extractors"""
    enabled: bool = True
    timeout: float = 30.0
    max_keywords: int = 30
    min_confidence: float = 0.1
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpacyYakeConfig(ExtractorConfig):
    """Configuration for SpaCy + YAKE extractor"""
    spacy_model: str = "en_core_web_sm"
    yake_language: str = "en"
    yake_n: int = 2
    yake_dedup_lim: float = 0.8
    yake_max_keywords: int = 30
    entity_weight: float = 0.7
    chunk_weight: float = 0.5


@dataclass
class BenchmarkConfig:
    """Benchmarking configuration"""
    max_timeout: float = 30.0
    iterations: int = 1
    save_results: bool = True
    output_directory: str = "./results"
    enable_memory_monitoring: bool = True
    enable_visualization: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    file_path: str = "keyword_extraction.log"
    console_enabled: bool = True


@dataclass
class FrameworkConfig:
    """Main framework configuration"""
    # Extractor configurations
    spacy_yake: SpacyYakeConfig = field(default_factory=SpacyYakeConfig)
    extractors: Dict[str, ExtractorConfig] = field(default_factory=dict)
    
    # Framework settings
    benchmark: BenchmarkConfig = field(default_factory=BenchmarkConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Performance settings
    max_text_length: int = 10000
    enable_caching: bool = True
    cache_size: int = 1000
    
    # Output settings
    output_format: str = "json"  # json, csv, yaml
    include_metadata: bool = True


class ConfigManager:
    """Manages configuration loading and validation"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.config_path = Path(config_path) if config_path else self._get_default_config_path()
        self._config: Optional[FrameworkConfig] = None
        
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path"""
        # Look for config file in various locations
        possible_paths = [
            Path("config.yaml"),
            Path("config.json"),
            Path("src/config/default_config.yaml"),
            Path.home() / ".keyword_extraction" / "config.yaml"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        # Return default path for creation
        return Path("config.yaml")
    
    def load_config(self) -> FrameworkConfig:
        """Load configuration from file or create default"""
        if self._config:
            return self._config
            
        if self.config_path.exists():
            try:
                self._config = self._load_from_file(self.config_path)
            except Exception as e:
                raise ConfigError(f"Failed to load config from {self.config_path}: {e}")
        else:
            # Create default configuration
            self._config = FrameworkConfig()
            self.save_config()  # Save default config for future use
            
        return self._config
    
    def _load_from_file(self, path: Path) -> FrameworkConfig:
        """Load configuration from file"""
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix.lower() == '.json':
                data = json.load(f)
            elif path.suffix.lower() in ['.yml', '.yaml']:
                data = yaml.safe_load(f)
            else:
                raise ConfigError(f"Unsupported config file format: {path.suffix}")
        
        return self._dict_to_config(data)
    
    def _dict_to_config(self, data: Dict) -> FrameworkConfig:
        """Convert dictionary to configuration object"""
        # This is a simplified conversion - in practice you'd want more robust handling
        config = FrameworkConfig()
        
        # Update spacy_yake config
        if 'spacy_yake' in data:
            spacy_config = data['spacy_yake']
            config.spacy_yake = SpacyYakeConfig(**spacy_config)
        
        # Update benchmark config
        if 'benchmark' in data:
            config.benchmark = BenchmarkConfig(**data['benchmark'])
        
        # Update logging config
        if 'logging' in data:
            logging_data = data['logging']
            if 'level' in logging_data:
                logging_data['level'] = LogLevel(logging_data['level'])
            config.logging = LoggingConfig(**logging_data)
        
        # Update other fields
        for field_name in ['max_text_length', 'enable_caching', 'cache_size', 
                          'output_format', 'include_metadata']:
            if field_name in data:
                setattr(config, field_name, data[field_name])
        
        return config
    
    def save_config(self, config: Optional[FrameworkConfig] = None):
        """Save configuration to file"""
        config_to_save = config or self._config
        if not config_to_save:
            raise ConfigError("No configuration to save")
        
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dictionary
        config_dict = self._config_to_dict(config_to_save)
        
        # Save based on file extension
        with open(self.config_path, 'w', encoding='utf-8') as f:
            if self.config_path.suffix.lower() == '.json':
                json.dump(config_dict, f, indent=2, default=str)
            else:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
    
    def _config_to_dict(self, config: FrameworkConfig) -> Dict:
        """Convert configuration object to dictionary"""
        return {
            'spacy_yake': {
                'enabled': config.spacy_yake.enabled,
                'spacy_model': config.spacy_yake.spacy_model,
                'yake_language': config.spacy_yake.yake_language,
                'yake_n': config.spacy_yake.yake_n,
                'yake_dedup_lim': config.spacy_yake.yake_dedup_lim,
                'yake_max_keywords': config.spacy_yake.yake_max_keywords,
                'entity_weight': config.spacy_yake.entity_weight,
                'chunk_weight': config.spacy_yake.chunk_weight,
                'max_keywords': config.spacy_yake.max_keywords,
                'timeout': config.spacy_yake.timeout
            },
            'benchmark': {
                'max_timeout': config.benchmark.max_timeout,
                'iterations': config.benchmark.iterations,
                'save_results': config.benchmark.save_results,
                'output_directory': config.benchmark.output_directory,
                'enable_memory_monitoring': config.benchmark.enable_memory_monitoring,
                'enable_visualization': config.benchmark.enable_visualization
            },
            'logging': {
                'level': config.logging.level.value,
                'format': config.logging.format,
                'file_enabled': config.logging.file_enabled,
                'file_path': config.logging.file_path,
                'console_enabled': config.logging.console_enabled
            },
            'max_text_length': config.max_text_length,
            'enable_caching': config.enable_caching,
            'cache_size': config.cache_size,
            'output_format': config.output_format,
            'include_metadata': config.include_metadata
        }
    
    def get_extractor_config(self, extractor_name: str) -> ExtractorConfig:
        """Get configuration for specific extractor"""
        config = self.load_config()
        
        if extractor_name == 'spacy_yake':
            return config.spacy_yake
        elif extractor_name in config.extractors:
            return config.extractors[extractor_name]
        else:
            # Return default configuration
            return ExtractorConfig()
    
    def update_config(self, **kwargs):
        """Update configuration with new values"""
        config = self.load_config()
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        self.save_config(config)


# Global configuration instance
_config_manager = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None or config_path:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_config() -> FrameworkConfig:
    """Get current configuration"""
    return get_config_manager().load_config()


def get_extractor_config(extractor_name: str) -> ExtractorConfig:
    """Get configuration for specific extractor"""
    return get_config_manager().get_extractor_config(extractor_name)