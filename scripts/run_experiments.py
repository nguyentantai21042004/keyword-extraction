#!/usr/bin/env python3
"""
Complete experiment runner for SMAP Keyword Extraction Framework
Generates both experiment_results and experiment_visualizations
"""

import sys
from pathlib import Path

# Add the project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import asyncio
import json
import pandas as pd
from src.benchmark import ExtractionBenchmark
from src.benchmark.test_datasets import create_research_test_dataset
from src.visualization.charts import BenchmarkVisualizer

async def run_complete_experiments():
    """Run complete experiment pipeline"""
    
    print("🚀 Starting SMAP Keyword Extraction Experiments")
    print("=" * 60)
    
    # Create output directories
    results_dir = REPO_ROOT / "experiment_results"
    vis_dir = REPO_ROOT / "experiment_visualizations"
    
    results_dir.mkdir(exist_ok=True)
    vis_dir.mkdir(exist_ok=True)
    
    print(f"📁 Results directory: {results_dir}")
    print(f"📊 Visualizations directory: {vis_dir}")
    
    try:
        # Step 1: Initialize benchmark
        print("\n🔧 Initializing benchmark framework...")
        benchmark = ExtractionBenchmark()
        
        # Step 2: Load test dataset
        print("📋 Loading test dataset...")
        test_cases = create_research_test_dataset()
        
        for case in test_cases:
            benchmark.add_test_case(**case)
        
        print(f"✅ Loaded {len(test_cases)} test cases")
        
        # Step 3: Run comprehensive benchmark
        print("\n🧪 Running comprehensive benchmark...")
        print("   This may take several minutes...")
        
        results_df = await benchmark.run_comprehensive_benchmark()
        
        print(f"✅ Benchmark completed with {len(results_df)} results")
        
        # Step 4: Save results
        print("\n💾 Saving results...")
        
        # Save as CSV
        csv_file = results_dir / "comprehensive_analysis.csv"
        results_df.to_csv(csv_file, index=False)
        print(f"   📄 CSV: {csv_file}")
        
        # Save as JSON
        json_file = results_dir / "comprehensive_analysis.json"
        results_df.to_json(json_file, orient='records', indent=2)
        print(f"   📋 JSON: {json_file}")
        
        # Save detailed analysis
        detailed_file = results_dir / "detailed_analysis.json"
        detailed_results = []
        for _, row in results_df.iterrows():
            detailed_results.append({
                'method': row['method'],
                'category': row['category'],
                'language': row['language'],
                'text_id': row['text_id'],
                'accuracy': row['accuracy'],
                'processing_time': row['processing_time'],
                'memory_usage': row['memory_usage'],
                'confidence_score': row['confidence_score'],
                'keywords_count': row['keywords_count'],
                'success': row['success'],
                'extracted_keywords': row['extracted_keywords'],
                'expected_keywords': row['expected_keywords']
            })
        
        with open(detailed_file, 'w') as f:
            json.dump(detailed_results, f, indent=2, ensure_ascii=False)
        print(f"   📊 Detailed: {detailed_file}")
        
        # Step 5: Generate visualizations
        print("\n📈 Generating visualizations...")
        
        visualizer = BenchmarkVisualizer()
        visualizer.create_comprehensive_charts(results_df, str(vis_dir))
        
        # Step 6: Create summary report
        print("\n📝 Creating summary report...")
        
        summary_file = results_dir / "experiment_summary_report.txt"
        with open(summary_file, 'w') as f:
            f.write("SMAP Keyword Extraction Framework - Experiment Summary Report\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total Test Cases: {len(test_cases)}\n")
            f.write(f"Total Results: {len(results_df)}\n")
            f.write(f"Methods Tested: {len(results_df['method'].unique())}\n")
            f.write(f"Categories Tested: {len(results_df['category'].unique())}\n")
            f.write(f"Languages Tested: {len(results_df['language'].unique())}\n\n")
            
            # Method performance summary
            f.write("METHOD PERFORMANCE SUMMARY:\n")
            f.write("-" * 30 + "\n")
            method_summary = results_df.groupby('method').agg({
                'accuracy': 'mean',
                'processing_time': 'mean',
                'memory_usage': 'mean',
                'confidence_score': 'mean',
                'success': 'mean'
            }).round(4)
            
            for method, metrics in method_summary.iterrows():
                f.write(f"\n{method}:\n")
                f.write(f"  Accuracy: {metrics['accuracy']:.1%}\n")
                f.write(f"  Processing Time: {metrics['processing_time']:.3f}s\n")
                f.write(f"  Memory Usage: {metrics['memory_usage']:.2f}MB\n")
                f.write(f"  Confidence: {metrics['confidence_score']:.1%}\n")
                f.write(f"  Success Rate: {metrics['success']:.1%}\n")
            
            # Best method
            best_method, best_score = benchmark.get_best_method('accuracy')
            f.write(f"\n🏆 BEST METHOD: {best_method} (accuracy: {best_score:.1%})\n")
        
        print(f"   📄 Summary: {summary_file}")
        
        # Step 7: Display results
        print("\n📊 EXPERIMENT RESULTS SUMMARY:")
        print("=" * 50)
        
        # Method rankings
        method_performance = results_df.groupby('method').agg({
            'accuracy': 'mean',
            'processing_time': 'mean',
            'confidence_score': 'mean'
        }).round(4)
        
        method_performance = method_performance.sort_values('accuracy', ascending=False)
        
        print("🏆 Algorithm Rankings by Accuracy:")
        for i, (method, metrics) in enumerate(method_performance.iterrows(), 1):
            print(f"{i}. {method:20} | Accuracy: {metrics['accuracy']:.1%} | "
                  f"Time: {metrics['processing_time']:.3f}s | "
                  f"Confidence: {metrics['confidence_score']:.1%}")
        
        # Category performance
        print("\n📈 Performance by Category:")
        category_performance = results_df.groupby('category')['accuracy'].mean().sort_values(ascending=False)
        for category, accuracy in category_performance.items():
            print(f"   {category:15}: {accuracy:.1%}")
        
        print(f"\n🎉 All experiments completed successfully!")
        print(f"📁 Results: {results_dir}")
        print(f"🖼️  Charts: {vis_dir}")
        
    except Exception as e:
        print(f"❌ Error during experiments: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        asyncio.run(run_complete_experiments())
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)
