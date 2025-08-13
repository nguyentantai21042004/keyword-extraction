#!/usr/bin/env python3
"""
🧪 Test Script for All Algorithms
Kiểm tra xem tất cả các thuật toán có hoạt động không trước khi chạy thí nghiệm chính
"""

import asyncio
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_all_algorithms():
    """Test all algorithms to ensure they work properly"""
    
    print("🧪 Testing All Algorithms")
    print("=" * 50)
    
    # Test text
    test_text = "Machine learning algorithms for natural language processing applications in social media sentiment analysis"
    
    print(f"📝 Test Text: {test_text}")
    print()
    
    # Test 1: spaCy + YAKE
    print("1️⃣ Testing spaCy + YAKE...")
    try:
        from multi_method_extractor import SpacyYakeExtractor
        spacy_yake = SpacyYakeExtractor()
        result = await spacy_yake.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 Try: pip install spacy && python -m spacy download en_core_web_sm")
    
    print()
    
    # Test 2: RAKE
    print("2️⃣ Testing RAKE...")
    try:
        from multi_method_extractor import RakeExtractor
        rake = RakeExtractor()
        result = await rake.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 Try: pip install rake-nltk")
    
    print()
    
    # Test 3: TF-IDF
    print("3️⃣ Testing TF-IDF...")
    try:
        from multi_method_extractor import TfIdfExtractor
        tfidf = TfIdfExtractor()
        result = await tfidf.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 Try: pip install scikit-learn")
    
    print()
    
    # Test 4: Hybrid Ensemble
    print("4️⃣ Testing Hybrid Ensemble...")
    try:
        from hybrid_ensemble import HybridEnsembleExtractor
        ensemble = HybridEnsembleExtractor()
        result = await ensemble.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
        if 'methods_used' in result.metadata:
            print(f"   🔧 Methods used: {result.metadata['methods_used']}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 This depends on other methods working first")
    
    print()
    
    # Test 5: TextRank (if available)
    print("5️⃣ Testing TextRank...")
    try:
        from multi_method_extractor import TextRankExtractor
        textrank = TextRankExtractor()
        result = await textrank.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 Try: pip install textrank")
    
    print()
    
    # Test 6: KeyBERT (if available)
    print("6️⃣ Testing KeyBERT...")
    try:
        from multi_method_extractor import KeyBertExtractor
        keybert = KeyBertExtractor()
        result = await keybert.extract(test_text)
        print(f"   ✅ Success! Extracted {len(result.keywords)} keywords")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   🔑 Top keywords: {[kw['keyword'] for kw in result.keywords[:3]]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print(f"   💡 Try: pip install keybert sentence-transformers")
    
    print()
    print("=" * 50)
    print("🎯 Algorithm Test Summary")
    print("=" * 50)
    
    # Summary
    print("\n📋 Next Steps:")
    print("1. Fix any failed algorithms (see error messages above)")
    print("2. Run the full experiment: python spacy_yake_experiment.py")
    print("3. Create visualizations: python create_visualizations.py")
    
    print("\n💡 Tips:")
    print("- Install missing dependencies first")
    print("- Some algorithms may take time to download models")
    print("- Check internet connection for model downloads")

def check_dependencies():
    """Check if required packages are installed"""
    
    print("🔍 Checking Dependencies...")
    print("=" * 30)
    
    required_packages = [
        ('spacy', 'spaCy for NLP processing'),
        ('yake', 'YAKE for keyword extraction'),
        ('rake_nltk', 'RAKE algorithm'),
        ('sklearn', 'scikit-learn for TF-IDF'),
        ('pandas', 'pandas for data handling'),
        ('numpy', 'numpy for numerical operations'),
        ('matplotlib', 'matplotlib for plotting'),
        ('seaborn', 'seaborn for enhanced plots')
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            if package == 'spacy':
                import spacy
                print(f"   ✅ {package} - {description}")
            elif package == 'yake':
                import yake
                print(f"   ✅ {package} - {description}")
            elif package == 'rake_nltk':
                import rake_nltk
                print(f"   ✅ {package} - {description}")
            elif package == 'sklearn':
                import sklearn
                print(f"   ✅ {package} - {description}")
            elif package == 'pandas':
                import pandas
                print(f"   ✅ {package} - {description}")
            elif package == 'numpy':
                import numpy
                print(f"   ✅ {package} - {description}")
            elif package == 'matplotlib':
                import matplotlib
                print(f"   ✅ {package} - {description}")
            elif package == 'seaborn':
                import seaborn
                print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
    else:
        print("\n✅ All required packages are installed!")
    
    print()

async def main():
    """Main test function"""
    
    print("🧪 Algorithm Test Suite")
    print("=" * 50)
    
    # Check dependencies first
    check_dependencies()
    
    # Test all algorithms
    await test_all_algorithms()

if __name__ == "__main__":
    asyncio.run(main())
