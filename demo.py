#!/usr/bin/env python3
"""
Demo script for testing individual components of the research framework
"""

import asyncio
from multi_method_extractor import SpacyYakeExtractor, RakeExtractor
from hybrid_ensemble import HybridEnsembleExtractor

async def test_individual_methods():
    """Test individual extraction methods"""
    
    print("🧪 Testing Individual Extraction Methods")
    print("=" * 50)
    
    # Test text
    test_text = "Machine learning algorithms for natural language processing applications in social media sentiment analysis"
    
    print(f"Test Text: {test_text}")
    print()
    
    # Test spaCy + YAKE
    print("1. Testing spaCy + YAKE Method...")
    try:
        spacy_yake = SpacyYakeExtractor()
        result = await spacy_yake.extract(test_text)
        print(f"   ✓ Success! Extracted {len(result.keywords)} keywords")
        print(f"   ✓ Processing time: {result.processing_time:.3f}s")
        print(f"   ✓ Memory usage: {result.memory_usage:.1f}MB")
        print(f"   ✓ Confidence: {result.confidence_score:.3f}")
        print(f"   ✓ Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print()
    
    # Test RAKE
    print("2. Testing RAKE Method...")
    try:
        rake = RakeExtractor()
        result = await rake.extract(test_text)
        print(f"   ✓ Success! Extracted {len(result.keywords)} keywords")
        print(f"   ✓ Processing time: {result.processing_time:.3f}s")
        print(f"   ✓ Memory usage: {result.memory_usage:.1f}MB")
        print(f"   ✓ Confidence: {result.confidence_score:.3f}")
        print(f"   ✓ Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print()
    
    # Test Hybrid Ensemble
    print("3. Testing Hybrid Ensemble Method...")
    try:
        ensemble = HybridEnsembleExtractor()
        result = await ensemble.extract(test_text)
        print(f"   ✓ Success! Extracted {len(result.keywords)} keywords")
        print(f"   ✓ Processing time: {result.processing_time:.3f}s")
        print(f"   ✓ Memory usage: {result.memory_usage:.1f}MB")
        print(f"   ✓ Confidence: {result.confidence_score:.3f}")
        print(f"   ✓ Methods used: {result.metadata.get('methods_used', [])}")
        print(f"   ✓ Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_imports():
    """Test if all modules can be imported"""
    
    print("📦 Testing Module Imports")
    print("=" * 30)
    
    modules = [
        ("multi_method_extractor", "Core extraction methods"),
        ("hybrid_ensemble", "Hybrid ensemble method"),
        ("benchmark_framework", "Benchmarking framework"),
        ("visualization", "Visualization module"),
        ("optimization_analyzer", "Optimization analyzer")
    ]
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"   ✓ {module_name} - {description}")
        except ImportError as e:
            print(f"   ❌ {module_name} - {description}: {e}")
    
    print()

async def main():
    """Main demo function"""
    
    print("🎓 Multi-Method Keyword Extraction Research Framework - DEMO")
    print("=" * 70)
    
    # Test imports first
    test_imports()
    
    # Test individual methods
    await test_individual_methods()
    
    print("\n✨ Demo completed!")
    print("\nTo run the full research framework:")
    print("   python main.py")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        print("Please check your dependencies and try again.")
