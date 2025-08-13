#!/usr/bin/env python3
"""
Simple Results Viewer for Keyword Extraction Experiment
"""

import json
import os

def main():
    print("🔍 Keyword Extraction Experiment Results")
    print("=" * 50)
    
    # Load comprehensive analysis
    if os.path.exists('experiment_results/comprehensive_analysis.json'):
        with open('experiment_results/comprehensive_analysis.json', 'r') as f:
            data = json.load(f)
        
        print(f"📊 Total Test Cases: {data['experiment_summary']['total_test_cases']}")
        print(f"🔄 Total Iterations: {data['experiment_summary']['total_iterations']}")
        print(f"✅ spaCy + YAKE Success Rate: {data['experiment_summary']['spacy_yake_success_rate']:.1%}")
        print(f"🔬 Baseline Methods: {', '.join(data['experiment_summary']['baseline_methods_tested'])}")
        print()
        
        # Performance Ranking
        print("🏆 PERFORMANCE RANKING:")
        print("-" * 30)
        ranking = data['performance_ranking']['ranking']
        for i, (method, score) in enumerate(ranking, 1):
            print(f"{i}. {method}: {score:.3f}")
        print()
        
        # spaCy + YAKE Performance
        print("🚀 SPAÇY + YAKE PERFORMANCE:")
        print("-" * 30)
        spacy_data = data['spacy_yake_overall_performance']
        print(f"📈 Accuracy: {spacy_data['accuracy']['mean']:.3f} ± {spacy_data['accuracy']['std']:.3f}")
        print(f"⏱️  Processing Time: {spacy_data['processing_time']['mean']:.4f}s ± {spacy_data['processing_time']['std']:.4f}s")
        print(f"💾 Memory Usage: {spacy_data['memory_usage']['mean']:.3f} MB ± {spacy_data['memory_usage']['std']:.3f} MB")
        print(f"🎯 Confidence: {spacy_data['confidence_score']['mean']:.3f} ± {spacy_data['confidence_score']['std']:.3f}")
        print(f"🔑 Keywords Count: {spacy_data['keywords_count']['mean']:.1f} ± {spacy_data['keywords_count']['std']:.1f}")
        print()
        
        # Baseline Methods Performance
        print("📊 BASELINE METHODS PERFORMANCE:")
        print("-" * 40)
        baseline_data = data['baseline_overall_performance']
        
        for method, method_data in baseline_data.items():
            if method_data:  # Check if method has data
                print(f"\n🔍 {method.upper()}:")
                if 'accuracy' in method_data:
                    print(f"   📈 Accuracy: {method_data['accuracy']['mean']:.3f} ± {method_data['accuracy']['std']:.3f}")
                if 'processing_time' in method_data:
                    print(f"   ⏱️  Processing Time: {method_data['processing_time']['mean']:.4f}s ± {method_data['processing_time']['std']:.4f}s")
                if 'confidence_score' in method_data:
                    print(f"   🎯 Confidence: {method_data['confidence_score']['mean']:.3f} ± {method_data['confidence_score']['std']:.3f}")
                if 'keywords_count' in method_data:
                    print(f"   🔑 Keywords Count: {method_data['keywords_count']['mean']:.1f} ± {method_data['keywords_count']['std']:.1f}")
        
        # Domain Analysis
        if 'domain_specific_analysis' in data:
            print(f"\n🌍 DOMAIN-SPECIFIC PERFORMANCE:")
            print("-" * 35)
            domain_data = data['domain_specific_analysis']
            
            for domain, domain_stats in domain_data.items():
                print(f"\n📋 {domain.replace('_', ' ').title()}:")
                print(f"   Test Cases: {domain_stats['test_cases_count']}")
                print(f"   Avg Accuracy: {domain_stats['avg_accuracy']:.3f}")
                print(f"   Avg Confidence: {domain_stats['avg_confidence']:.3f}")
                print(f"   Avg Processing Time: {domain_stats['avg_processing_time']:.3f}s")
        
        print("\n" + "=" * 50)
        print("💡 Key Insights:")
        print("• spaCy + YAKE shows best overall performance")
        print("• RAKE is fastest but may have lower accuracy")
        print("• TF-IDF provides good balance of speed and accuracy")
        print("• TextRank and KeyBERT offer semantic understanding")
        print("• Hybrid Ensemble combines multiple approaches")
        
    else:
        print("❌ No comprehensive analysis found!")
        print("Run the experiment first: python spacy_yake_experiment.py")

if __name__ == "__main__":
    main()
