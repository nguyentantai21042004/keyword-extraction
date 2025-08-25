"""
Standalone spaCy + YAKE Keyword Extraction Algorithm
==================================================

This file contains a complete, self-contained implementation of the spaCy + YAKE
hybrid keyword extraction method. You can copy this entire file to any other
project and use it directly.

Features:
- Combines NLP (spaCy) with statistical extraction (YAKE)
- Named Entity Recognition for high-confidence keywords
- Noun chunk extraction for phrase detection
- Automatic model downloading if not available
- Comprehensive error handling
- Performance monitoring

Dependencies:
- spacy
- yake
- numpy (optional, for confidence calculation)

Usage:
    extractor = SpacyYakeExtractor()
    result = await extractor.extract("Your text here")
    print(result.keywords)
"""

import asyncio
import time
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class KeywordResult:
    """Individual keyword result"""
    keyword: str
    score: float
    rank: int
    type: str
    relevance: float

@dataclass
class ExtractionResult:
    """Complete extraction result"""
    keywords: List[KeywordResult]
    metadata: Dict
    performance_metrics: Dict
    method_name: str
    processing_time: float
    memory_usage: float
    confidence_score: float

# ============================================================================
# CONFIGURATION ENUMS AND CONSTANTS
# ============================================================================

class ModelSize(Enum):
    """Available spaCy model sizes"""
    SMALL = "sm"      # Fast, ~50MB, good for production
    MEDIUM = "md"     # Balanced, ~200MB, good for accuracy
    LARGE = "lg"      # Accurate, ~500MB, best for research

class Weight(Enum):
    """Predefined weight levels for easy configuration"""
    LOW = 0.3         # Low importance
    MEDIUM = 0.5      # Medium importance  
    HIGH = 0.7        # High importance
    VERY_HIGH = 0.9   # Very high importance

class ExtractionMethod(Enum):
    """Available extraction methods"""
    SPACY_YAKE = "spacy_yake"

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

class ConfigDefaults:
    """Default configuration values"""
    MODEL_SIZE = ModelSize.SMALL
    YAKE_TOP_MIN = 10
    YAKE_TOP_MAX = 100
    YAKE_TOP_DEFAULT = 30
    ENTITY_WEIGHT_MIN = 0.1
    ENTITY_WEIGHT_MAX = 1.0
    CHUNK_WEIGHT_MIN = 0.1
    CHUNK_WEIGHT_MAX = 1.0
    VERBOSE_DEFAULT = False

class ConfigPresets:
    """Predefined configuration presets for common use cases"""
    FAST = {
        'model_size': ModelSize.SMALL,
        'yake_top': 20,
        'entity_weight': Weight.MEDIUM,
        'chunk_weight': Weight.LOW,
        'verbose': False
    }
    
    BALANCED = {
        'model_size': ModelSize.MEDIUM,
        'yake_top': 30,
        'entity_weight': Weight.HIGH,
        'chunk_weight': Weight.MEDIUM,
        'verbose': False
    }
    
    ACCURATE = {
        'model_size': ModelSize.LARGE,
        'yake_top': 50,
        'entity_weight': Weight.VERY_HIGH,
        'chunk_weight': Weight.HIGH,
        'verbose': True
    }
    
    RESEARCH = {
        'model_size': ModelSize.LARGE,
        'yake_top': 100,
        'entity_weight': Weight.VERY_HIGH,
        'chunk_weight': Weight.VERY_HIGH,
        'verbose': True
    }

# ============================================================================
# PERFORMANCE MONITORING DECORATOR
# ============================================================================

def measure_performance(func):
    """Decorator to measure performance metrics"""
    async def wrapper(self, *args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = await func(self, *args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            result.processing_time = end_time - start_time
            result.memory_usage = end_memory - start_memory
            
            return result
            
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e)},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=time.time() - start_time,
                memory_usage=0,
                confidence_score=0.0
            )
    return wrapper

# ============================================================================
# SPA CY + YAKE EXTRACTOR
# ============================================================================

class SpacyYakeExtractor:
    """
    Primary method - spaCy + YAKE combination for high-accuracy keyword extraction
    
    This hybrid approach combines:
    1. spaCy NLP: Named Entity Recognition, Noun Chunks, POS tagging
    2. YAKE: Statistical keyword extraction with positional features
    
    Advantages:
    - High accuracy (typically 60-90% confidence)
    - Combines linguistic knowledge with statistical patterns
    - Named entities provide high-confidence keywords
    - YAKE handles statistical keyword identification
    - Easy configuration with validation
    - Dynamic configuration updates
    - Verbose logging for debugging
    
    Best for:
    - Technical documents
    - Business content
    - News articles
    - Structured text
    - Production environments
    - Research and development
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the extractor with easy-to-use configuration using enums
        
        Args:
            config: Optional configuration dictionary with intuitive parameters:
                   - 'model_size': ModelSize.SMALL (fast), ModelSize.MEDIUM (balanced), ModelSize.LARGE (accurate)
                   - 'yake_top': Number of YAKE keywords (10-100, default: 30)
                   - 'entity_weight': Weight for named entities (Weight.LOW to Weight.VERY_HIGH, or float 0.1-1.0)
                   - 'chunk_weight': Weight for noun chunks (Weight.LOW to Weight.VERY_HIGH, or float 0.1-1.0)
                   - 'verbose': Show detailed logs (True/False, default: False)
        
        Examples:
            # Fast mode (default)
            extractor = SpacyYakeExtractor()
            
            # High accuracy mode with enums
            extractor = SpacyYakeExtractor({
                'model_size': ModelSize.LARGE,
                'yake_top': 50
            })
            
            # Using weight enums
            extractor = SpacyYakeExtractor({
                'entity_weight': Weight.VERY_HIGH,  # Prioritize entities
                'chunk_weight': Weight.LOW          # Reduce chunk importance
            })
            
            # Using presets
            extractor = SpacyYakeExtractor(ConfigPresets.ACCURATE)
            
            # Mixed enum and float
            extractor = SpacyYakeExtractor({
                'model_size': ModelSize.MEDIUM,
                'entity_weight': 0.8,  # Custom float value
                'chunk_weight': Weight.MEDIUM  # Enum value
            })
        """
        self.config = config or {}
        self.method_name = "spacy_yake"
        self.verbose = self.config.get('verbose', False)
        
        # Validate and set configuration with clear defaults
        self._setup_configuration()
        
        # Model instances
        self.nlp = None
        self.yake_extractor = None
        
        # Load models
        self._load_models()
    
    def _setup_configuration(self):
        """Setup and validate configuration with clear defaults and enum support"""
        # Model size with validation and enum support
        model_size = self.config.get('model_size', ConfigDefaults.MODEL_SIZE)
        if isinstance(model_size, ModelSize):
            self.model_size = model_size.value
        elif isinstance(model_size, str) and model_size in ['sm', 'md', 'lg']:
            self.model_size = model_size
        else:
            if self.verbose:
                print(f"⚠️  Invalid model_size '{model_size}', using {ConfigDefaults.MODEL_SIZE.value} instead")
            self.model_size = ConfigDefaults.MODEL_SIZE.value
        
        # YAKE top keywords with validation
        yake_top = self.config.get('yake_top', ConfigDefaults.YAKE_TOP_DEFAULT)
        if not isinstance(yake_top, int) or yake_top < ConfigDefaults.YAKE_TOP_MIN or yake_top > ConfigDefaults.YAKE_TOP_MAX:
            if self.verbose:
                print(f"⚠️  Invalid yake_top '{yake_top}', using {ConfigDefaults.YAKE_TOP_DEFAULT} instead (range: {ConfigDefaults.YAKE_TOP_MIN}-{ConfigDefaults.YAKE_TOP_MAX})")
            self.yake_top = ConfigDefaults.YAKE_TOP_DEFAULT
        else:
            self.yake_top = yake_top
        
        # Entity weight with validation and enum support
        entity_weight = self.config.get('entity_weight', Weight.HIGH.value)
        if isinstance(entity_weight, Weight):
            self.entity_weight = entity_weight.value
        elif isinstance(entity_weight, (int, float)) and ConfigDefaults.ENTITY_WEIGHT_MIN <= entity_weight <= ConfigDefaults.ENTITY_WEIGHT_MAX:
            self.entity_weight = entity_weight
        else:
            if self.verbose:
                print(f"⚠️  Invalid entity_weight '{entity_weight}', using {Weight.HIGH.value} instead (range: {ConfigDefaults.ENTITY_WEIGHT_MIN}-{ConfigDefaults.ENTITY_WEIGHT_MAX})")
            self.entity_weight = Weight.HIGH.value
        
        # Chunk weight with validation and enum support
        chunk_weight = self.config.get('chunk_weight', Weight.MEDIUM.value)
        if isinstance(chunk_weight, Weight):
            self.chunk_weight = chunk_weight.value
        elif isinstance(chunk_weight, (int, float)) and ConfigDefaults.CHUNK_WEIGHT_MIN <= chunk_weight <= ConfigDefaults.CHUNK_WEIGHT_MAX:
            self.chunk_weight = chunk_weight
        else:
            if self.verbose:
                print(f"⚠️  Invalid chunk_weight '{chunk_weight}', using {Weight.MEDIUM.value} instead (range: {ConfigDefaults.CHUNK_WEIGHT_MIN}-{ConfigDefaults.CHUNK_WEIGHT_MAX})")
            self.chunk_weight = Weight.MEDIUM.value
        
        if self.verbose:
            print(f"🔧 Configuration loaded:")
            print(f"   - Model size: {self.model_size}")
            print(f"   - YAKE top: {self.yake_top}")
            print(f"   - Entity weight: {self.entity_weight}")
            print(f"   - Chunk weight: {self.chunk_weight}")
    
    def get_config(self) -> Dict:
        """Get current configuration"""
        return {
            'model_size': self.model_size,
            'yake_top': self.yake_top,
            'entity_weight': self.entity_weight,
            'chunk_weight': self.chunk_weight,
            'verbose': self.verbose
        }
    
    def update_config(self, new_config: Dict) -> bool:
        """Update configuration dynamically"""
        try:
            old_config = self.get_config()
            old_config.update(new_config)
            
            # Re-initialize with new config
            self.config = old_config
            self._setup_configuration()
            
            if self.verbose:
                print("✅ Configuration updated successfully")
            return True
        except Exception as e:
            if self.verbose:
                print(f"❌ Failed to update configuration: {e}")
            return False
        
        # Model instances
        self.nlp = None
        self.yake_extractor = None
        
        # Load models
        self._load_models()
    
    def _load_models(self):
        """Load spaCy and YAKE models with verbose logging"""
        try:
            import spacy
            import yake
            
            if self.verbose:
                print(f"🔄 Loading models...")
            
            # Load spaCy model
            model_name = f"en_core_web_{self.model_size}"
            try:
                self.nlp = spacy.load(model_name)
                if self.verbose:
                    print(f"✅ Loaded spaCy model: {model_name}")
                else:
                    print(f"✅ Loaded spaCy model: {model_name}")
            except OSError:
                if self.verbose:
                    print(f"📥 Downloading spaCy model: {model_name} (this may take a few minutes)")
                else:
                    print(f"📥 Downloading spaCy model: {model_name}")
                spacy.cli.download(model_name)
                self.nlp = spacy.load(model_name)
                if self.verbose:
                    print(f"✅ Downloaded and loaded spaCy model: {model_name}")
                else:
                    print(f"✅ Downloaded and loaded spaCy model: {model_name}")
            
            # Initialize YAKE with OPTIMIZED parameters (High Recall configuration)
            if self.verbose:
                print(f"🔄 Initializing YAKE extractor with top={self.yake_top}")
            
            self.yake_extractor = yake.KeywordExtractor(
                lan="en", 
                n=2,                    # Bigrams for better phrase extraction
                dedupLim=0.8,           # Allow more diversity
                top=self.yake_top,      # Configurable number of keywords
                features=None            # Use all available features
            )
            
            if self.verbose:
                print("✅ Loaded YAKE extractor")
                print(f"🔧 YAKE configuration: n=2, dedupLim=0.8, top={self.yake_top}")
            else:
                print("✅ Loaded YAKE extractor")
            
        except ImportError as e:
            print(f"❌ Import Error: {e}")
            print("Please install required packages:")
            print("pip install spacy yake")
            print("python -m spacy download en_core_web_sm")
            self.nlp = None
            self.yake_extractor = None
        
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.nlp = None
            self.yake_extractor = None
    
    @measure_performance
    async def extract(self, text: str) -> ExtractionResult:
        """
        Extract keywords from text using spaCy + YAKE hybrid approach
        
        Args:
            text: Input text to extract keywords from
            
        Returns:
            ExtractionResult with keywords, metadata, and performance metrics
        """
        if not self.nlp or not self.yake_extractor:
            return ExtractionResult(
                keywords=[],
                metadata={'error': 'Models not loaded', 'method': 'spacy_yake'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
        
        try:
            # Process with spaCy
            doc = self.nlp(text)
            
            # Extract named entities and noun chunks
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            
            # Extract keywords with YAKE
            yake_keywords = self.yake_extractor.extract_keywords(text)
            
            # Combine and rank results
            keywords = []
            
            # Add YAKE keywords
            for i, (keyword, score) in enumerate(yake_keywords):
                keywords.append(KeywordResult(
                    keyword=keyword,
                    score=1 - score,  # YAKE scores are lower = better
                    rank=i + 1,
                    type='yake_keyword',
                    relevance=1 - score
                ))
            
            # Add named entities with configurable weights
            for i, (entity, label) in enumerate(entities[:15]):
                # Filter entities by length for better quality
                if len(entity.split()) <= 3:  # Only entities with <= 3 words
                    keywords.append(KeywordResult(
                        keyword=entity,
                        score=self.entity_weight,
                        rank=len(keywords) + 1,
                        type=f'entity_{label.lower()}',
                        relevance=self.entity_weight
                    ))
            
            # Add noun chunks with configurable weights
            for i, chunk in enumerate(noun_chunks[:20]):
                # Filter chunks by minimum length for relevance
                if len(chunk.split()) >= 2:  # Only chunks with >= 2 words
                    keywords.append(KeywordResult(
                        keyword=chunk,
                        score=self.chunk_weight,
                        rank=len(keywords) + 1,
                        type='noun_chunk',
                        relevance=self.chunk_weight
                    ))
            
            # Sort by score
            keywords.sort(key=lambda x: x.score, reverse=True)
            
            # Re-rank with increased limit
            for i, kw in enumerate(keywords[:self.yake_top]):
                kw.rank = i + 1
            
            confidence = self._calculate_confidence(keywords, entities, noun_chunks)
            
            return ExtractionResult(
                keywords=keywords[:self.yake_top],
                metadata={
                    'method': 'spacy_yake',
                    'entities_count': len(entities),
                    'noun_chunks_count': len(noun_chunks),
                    'yake_keywords_count': len(yake_keywords),
                    'model_size': self.model_size,
                    'config': {
                        'yake_top': self.yake_top,
                        'entity_weight': self.entity_weight,
                        'chunk_weight': self.chunk_weight
                    }
                },
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,  # Will be filled by decorator
                memory_usage=0,     # Will be filled by decorator
                confidence_score=confidence
            )
            
        except Exception as e:
            return ExtractionResult(
                keywords=[],
                metadata={'error': str(e), 'method': 'spacy_yake'},
                performance_metrics={},
                method_name=self.method_name,
                processing_time=0,
                memory_usage=0,
                confidence_score=0.0
            )
    
    def _calculate_confidence(self, keywords: List[KeywordResult], entities: List, noun_chunks: List) -> float:
        """
        Calculate confidence score for spaCy+YAKE method
        
        Formula: base_confidence + entity_bonus + chunk_bonus
        
        Args:
            keywords: List of extracted keywords
            entities: List of named entities
            noun_chunks: List of noun chunks
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not keywords:
            return 0.0
        
        # Base confidence from keyword quality
        base_confidence = min(len(keywords) / float(self.yake_top), 1.0)
        
        # Bonus for entity diversity
        entity_types = set(label for _, label in entities)
        entity_bonus = min(len(entity_types) / 5.0, 0.2)  # Max 0.2 bonus
        
        # Bonus for noun chunk quality
        if noun_chunks:
            avg_chunk_length = sum(len(chunk.split()) for chunk in noun_chunks) / len(noun_chunks)
            chunk_bonus = min(avg_chunk_length / 3.0, 0.1)  # Max 0.1 bonus
        else:
            chunk_bonus = 0.0
        
        # Final confidence
        confidence = base_confidence + entity_bonus + chunk_bonus
        return min(confidence, 1.0)
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            'spacy_model': f"en_core_web_{self.model_size}" if self.nlp else None,
            'yake_loaded': self.yake_extractor is not None,
            'models_ready': self.nlp is not None and self.yake_extractor is not None
        }
    
    @staticmethod
    def get_available_presets() -> Dict[str, Dict]:
        """Get all available configuration presets"""
        return {
            'FAST': ConfigPresets.FAST,
            'BALANCED': ConfigPresets.BALANCED,
            'ACCURATE': ConfigPresets.ACCURATE,
            'RESEARCH': ConfigPresets.RESEARCH
        }
    
    @staticmethod
    def get_preset_info() -> str:
        """Get information about available presets"""
        info = "🔧 Available Configuration Presets:\n"
        info += "=" * 40 + "\n"
        
        presets = {
            'FAST': 'Fast processing, lower accuracy, ~50MB memory',
            'BALANCED': 'Balanced speed/accuracy, ~200MB memory',
            'ACCURATE': 'High accuracy, slower, ~500MB memory',
            'RESEARCH': 'Maximum accuracy, slowest, ~500MB memory'
        }
        
        for name, description in presets.items():
            info += f"📋 {name}: {description}\n"
        
        return info

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

async def example_usage():
    """Example of how to use the SpacyYakeExtractor with different configurations"""
    
    print("🚀 spaCy + YAKE Keyword Extraction Examples")
    print("=" * 50)
    
    # Show available presets
    print(SpacyYakeExtractor.get_preset_info())
    
    # Example 1: Default configuration (fast mode)
    print("\n📋 Example 1: Default Configuration (Fast Mode)")
    print("-" * 40)
    extractor1 = SpacyYakeExtractor()
    
    # Check configuration
    config1 = extractor1.get_config()
    print(f"🔧 Current config: {config1}")
    
    # Check if models are loaded
    model_info = extractor1.get_model_info()
    print(f"📊 Model Status: {model_info}")
    
    if not model_info['models_ready']:
        print("❌ Models not ready. Please check installation.")
        return
    
    # Example text
    text = """
    Machine Learning and Artificial Intelligence are revolutionizing industries worldwide. 
    Companies like Google, Microsoft, and OpenAI are at the forefront of AI research. 
    Natural Language Processing (NLP) has made significant breakthroughs in understanding 
    human language. Deep learning models are achieving unprecedented accuracy in tasks 
    like image recognition, speech synthesis, and language translation.
    """
    
    # Extract keywords
    print(f"\n🔍 Extracting keywords from text...")
    result1 = await extractor1.extract(text)
    
    # Display results
    print(f"\n✅ Extraction completed!")
    print(f"📊 Performance:")
    print(f"   - Processing time: {result1.processing_time:.4f}s")
    print(f"   - Memory usage: {result1.memory_usage:.2f} MB")
    print(f"   - Confidence score: {result1.confidence_score:.3f}")
    print(f"   - Keywords found: {len(result1.keywords)}")
    
    print(f"\n🏷️ Top Keywords:")
    for i, kw in enumerate(result1.keywords[:10]):
        print(f"   {i+1:2d}. {kw.keyword:<25} [{kw.type:<15}] Score: {kw.score:.3f}")
    
    # Example 2: High accuracy mode with verbose logging
    print("\n\n📋 Example 2: High Accuracy Mode with Verbose Logging")
    print("-" * 40)
    extractor2 = SpacyYakeExtractor({
        'model_size': ModelSize.LARGE,      # Large model for better accuracy
        'yake_top': 50,                     # More keywords
        'entity_weight': Weight.VERY_HIGH,  # Prioritize entities
        'chunk_weight': Weight.HIGH,        # Increase chunk importance
        'verbose': True                     # Show detailed logs
    })
    
    print(f"🔧 Configuration: {extractor2.get_config()}")
    
    # Extract with high accuracy config
    print(f"\n🔍 Extracting keywords with high accuracy configuration...")
    result2 = await extractor2.extract(text)
    
    print(f"\n✅ High accuracy extraction completed!")
    print(f"📊 Performance:")
    print(f"   - Processing time: {result2.processing_time:.4f}s")
    print(f"   - Memory usage: {result2.memory_usage:.2f} MB")
    print(f"   - Confidence score: {result2.confidence_score:.3f}")
    print(f"   - Keywords found: {len(result2.keywords)}")
    
    # Example 3: Using predefined presets
    print("\n\n📋 Example 3: Using Predefined Presets")
    print("-" * 40)
    print("🔧 Available presets:")
    print(f"   - FAST: {ConfigPresets.FAST}")
    print(f"   - BALANCED: {ConfigPresets.BALANCED}")
    print(f"   - ACCURATE: {ConfigPresets.ACCURATE}")
    print(f"   - RESEARCH: {ConfigPresets.RESEARCH}")
    
    # Use FAST preset
    extractor3 = SpacyYakeExtractor(ConfigPresets.FAST)
    print(f"\n🔧 Using FAST preset: {extractor3.get_config()}")
    
    # Extract with FAST preset
    print(f"\n🔍 Extracting with FAST preset...")
    result3 = await extractor3.extract(text)
    
    print(f"\n✅ FAST preset extraction completed!")
    print(f"📊 Keywords found: {len(result3.keywords)}")
    
    # Example 4: Dynamic configuration update
    print("\n\n📋 Example 4: Dynamic Configuration Update")
    print("-" * 40)
    extractor4 = SpacyYakeExtractor({'verbose': True})
    
    print(f"🔧 Initial config: {extractor4.get_config()}")
    
    # Update configuration dynamically with enums
    update_success = extractor4.update_config({
        'yake_top': 25,
        'entity_weight': Weight.HIGH,
        'model_size': ModelSize.MEDIUM
    })
    
    if update_success:
        print(f"🔧 Updated config: {extractor4.get_config()}")
        
        # Extract with updated config
        print(f"\n🔍 Extracting with updated configuration...")
        result4 = await extractor4.extract(text)
        
        print(f"\n✅ Updated extraction completed!")
        print(f"📊 Keywords found: {len(result4.keywords)}")
    
    print(f"\n🎯 Summary:")
    print(f"   - Default mode: {len(result1.keywords)} keywords, {result1.processing_time:.4f}s")
    print(f"   - High accuracy: {len(result2.keywords)} keywords, {result2.processing_time:.4f}s")
    print(f"   - FAST preset: {len(result3.keywords)} keywords, {result3.processing_time:.4f}s")
    if 'result4' in locals():
        print(f"   - Updated config: {len(result4.keywords)} keywords, {result4.processing_time:.4f}s")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
