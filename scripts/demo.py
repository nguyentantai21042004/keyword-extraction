#!/usr/bin/env python3
"""
Simple demo script for the keyword extraction framework
"""

import sys
from pathlib import Path

# Add the project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import asyncio
from src.core.extractors import SpacyYakeExtractor

async def demo():
    """Run a simple demonstration"""
    
    print("🎯 Keyword Extraction Framework Demo")
    print("=" * 50)
    
    # Sample text
    text = "Machine learning algorithms for natural language processing applications in social media sentiment analysis."
    
    print(f"📝 Sample text: {text}")
    print()
    
    # Test SpacyYakeExtractor
    extractor = SpacyYakeExtractor()
    
    try:
        print(f"🔍 Testing SpaCy + YAKE...")
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
