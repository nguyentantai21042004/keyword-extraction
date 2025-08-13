#!/usr/bin/env python3
"""
Simple demo script for the keyword extraction framework
"""

import asyncio
from src.core import SpacyYakeExtractor, RakeExtractor
from src.core.ensemble import HybridEnsembleExtractor

async def demo():
    """Run a simple demonstration"""
    
    print("🎯 Keyword Extraction Framework Demo")
    print("=" * 50)
    
    # Sample text
    text = "Machine learning algorithms for natural language processing applications in social media sentiment analysis."
    
    print(f"📝 Sample text: {text}")
    print()
    
    # Test individual extractors
    extractors = {
        "SpaCy + YAKE": SpacyYakeExtractor(),
        "RAKE": RakeExtractor(),
        "Hybrid Ensemble": HybridEnsembleExtractor()
    }
    
    for name, extractor in extractors.items():
        try:
            print(f"🔍 Testing {name}...")
            result = await extractor.extract(text)
            
            if result.keywords:
                print(f"   ✅ Extracted {len(result.keywords)} keywords:")
                for i, kw in enumerate(result.keywords[:5], 1):  # Show top 5
                    print(f"      {i}. {kw['keyword']} (score: {kw['score']:.3f})")
            else:
                print(f"   ❌ No keywords extracted")
            
            print(f"   ⏱️  Processing time: {result.processing_time:.3f}s")
            print(f"   💾 Memory usage: {result.memory_usage:.1f}MB")
            print(f"   🎯 Confidence: {result.confidence_score:.3f}")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("🎉 Demo completed!")

if __name__ == "__main__":
    asyncio.run(demo())
