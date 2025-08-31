#!/usr/bin/env python3
"""
Simple test script to verify basic functionality
"""

import sys
from pathlib import Path

# Add the project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import asyncio
from src.core.extractors import SpacyYakeExtractor

async def test_basic_extraction():
    """Test basic keyword extraction"""
    
    print("🧪 Testing basic keyword extraction...")
    
    try:
        # Initialize extractor
        extractor = SpacyYakeExtractor()
        
        # Test text
        text = "Machine learning algorithms for natural language processing applications."
        
        print(f"📝 Test text: {text}")
        
        # Extract keywords
        result = await extractor.extract(text)
        
        # Display results
        print(f"✅ Extraction successful!")
        print(f"📊 Keywords found: {len(result.keywords)}")
        print(f"⏱️  Processing time: {result.processing_time:.3f}s")
        print(f"🎯 Confidence: {result.confidence_score:.1%}")
        
        print("\n🔑 Top keywords:")
        for i, kw in enumerate(result.keywords[:5], 1):
            print(f"   {i}. {kw['keyword']} (score: {kw['score']:.3f})")
        
        print("\n✅ Basic functionality test passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_basic_extraction())
