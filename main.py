#!/usr/bin/env python3
"""
🎓 Multi-Method Keyword Extraction Research Framework
Comparative Analysis Framework for Đồ Án

This framework implements and benchmarks multiple keyword extraction methods:
1. spaCy + YAKE (Primary method)
2. RAKE + NLTK (Fast baseline)
3. TextRank (Graph-based)
4. TF-IDF (Statistical)
5. KeyBERT (Semantic)
6. Hybrid Ensemble (Intelligent combination)

Author: Research Team
Purpose: Comprehensive comparison and optimization analysis
"""

import asyncio
import sys
import os
from typing import Dict, List
import pandas as pd

# Import our modules
from multi_method_extractor import (
    ExtractionMethod, SpacyYakeExtractor, RakeExtractor, 
    TextRankExtractor, TfIdfExtractor, KeyBertExtractor
)
from hybrid_ensemble import HybridEnsembleExtractor
from benchmark_framework import ExtractionBenchmark, create_research_test_dataset
from visualization import BenchmarkVisualizer
from optimization_analyzer import OptimizationAnalyzer

class ResearchFramework:
    """Main orchestrator for the research framework"""
    
    def __init__(self):
        self.benchmark = None
        self.results_df = None
        self.performance_report = None
        self.optimization_report = None
        
    async def run_complete_research(self, custom_test_cases: List[Dict] = None):
        """Run the complete research pipeline"""
        
        print("🚀 Starting Multi-Method Keyword Extraction Research Framework")
        print("=" * 70)
        
        # Step 1: Initialize benchmark
        print("\n📊 Step 1: Initializing Benchmark Framework...")
        self.benchmark = ExtractionBenchmark()
        
        # Step 2: Add test cases
        print("\n📝 Step 2: Setting up Test Dataset...")
        if custom_test_cases:
            for case in custom_test_cases:
                self.benchmark.add_test_case(
                    case['text'], 
                    case.get('expected_keywords', []), 
                    case.get('category', 'custom')
                )
        else:
            # Use default research dataset
            test_cases = create_research_test_dataset()
            for case in test_cases:
                self.benchmark.add_test_case(
                    case['text'], 
                    case['expected_keywords'], 
                    case['category']
                )
        
        print(f"   ✓ Added {len(self.benchmark.test_cases)} test cases")
        
        # Step 3: Run comprehensive benchmark
        print("\n⚡ Step 3: Running Comprehensive Benchmark...")
        print("   This may take a few minutes depending on text complexity...")
        
        try:
            self.results_df = await self.benchmark.run_comprehensive_benchmark()
            print(f"   ✓ Benchmark completed successfully!")
            print(f"   ✓ Generated {len(self.results_df)} data points")
            
        except Exception as e:
            print(f"   ❌ Benchmark failed: {e}")
            return False
        
        # Step 4: Generate performance report
        print("\n📈 Step 4: Generating Performance Analysis...")
        try:
            self.performance_report = self.benchmark.generate_performance_report(self.results_df)
            print("   ✓ Performance report generated")
            
        except Exception as e:
            print(f"   ❌ Performance report generation failed: {e}")
            return False
        
        # Step 5: Create visualizations
        print("\n🎨 Step 5: Creating Visualizations...")
        try:
            visualizer = BenchmarkVisualizer(self.results_df)
            visualizer.create_all_visualizations()
            print("   ✓ All visualizations created and saved")
            
        except Exception as e:
            print(f"   ❌ Visualization creation failed: {e}")
        
        # Step 6: Run optimization analysis
        print("\n🎯 Step 6: Running Optimization Analysis...")
        try:
            analyzer = OptimizationAnalyzer(self.results_df)
            self.optimization_report = analyzer.generate_optimization_report()
            print("   ✓ Optimization analysis completed")
            
            # Create optimization visualizations
            analyzer.create_optimization_visualization()
            print("   ✓ Optimization visualizations created")
            
        except Exception as e:
            print(f"   ❌ Optimization analysis failed: {e}")
        
        # Step 7: Save results
        print("\n💾 Step 7: Saving Research Results...")
        try:
            self._save_research_results()
            print("   ✓ All results saved successfully")
            
        except Exception as e:
            print(f"   ❌ Results saving failed: {e}")
        
        print("\n🎉 Research Framework Execution Completed Successfully!")
        return True
    
    def _save_research_results(self):
        """Save all research results to files"""
        
        # Save benchmark results
        if self.results_df is not None:
            self.results_df.to_csv('research_benchmark_results.csv', index=False)
            print("     - Benchmark results saved to 'research_benchmark_results.csv'")
        
        # Save performance report
        if self.performance_report:
            with open('research_performance_report.txt', 'w', encoding='utf-8') as f:
                f.write("MULTI-METHOD KEYWORD EXTRACTION PERFORMANCE REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("OVERALL PERFORMANCE BY METHOD:\n")
                f.write(str(self.performance_report['overall_performance']))
                f.write("\n\n")
                
                f.write("SUMMARY STATISTICS:\n")
                for key, value in self.performance_report['summary_stats'].items():
                    f.write(f"{key}: {value}\n")
            
            print("     - Performance report saved to 'research_performance_report.txt'")
        
        # Save optimization report
        if self.optimization_report:
            with open('research_optimization_report.txt', 'w', encoding='utf-8') as f:
                f.write("OPTIMIZATION ANALYSIS REPORT\n")
                f.write("=" * 30 + "\n\n")
                
                f.write(f"OPTIMAL METHOD: {self.optimization_report['optimal_method']}\n\n")
                
                f.write("JUSTIFICATION:\n")
                f.write(self.optimization_report['justification'])
                f.write("\n\n")
                
                f.write("COMPARISON TABLE:\n")
                f.write(str(self.optimization_report['comparison_table']))
                f.write("\n\n")
                
                f.write("RECOMMENDATIONS:\n")
                f.write(f"Primary: {self.optimization_report['recommendations']['primary_recommendation']}\n\n")
                
                if self.optimization_report['recommendations']['performance_insights']:
                    f.write("Performance Insights:\n")
                    for insight in self.optimization_report['recommendations']['performance_insights']:
                        f.write(f"- {insight}\n")
                    f.write("\n")
                
                if self.optimization_report['recommendations']['optimization_suggestions']:
                    f.write("Optimization Suggestions:\n")
                    for suggestion in self.optimization_report['recommendations']['optimization_suggestions']:
                        f.write(f"- {suggestion}\n")
                    f.write("\n")
                
                f.write("Use Case Recommendations:\n")
                for use_case, method in self.optimization_report['recommendations']['use_case_recommendations'].items():
                    f.write(f"- {use_case}: {method}\n")
            
            print("     - Optimization report saved to 'research_optimization_report.txt'")
    
    def print_summary(self):
        """Print a summary of the research results"""
        
        if not self.results_df is not None:
            print("❌ No results available. Run the research framework first.")
            return
        
        print("\n" + "=" * 70)
        print("📊 RESEARCH FRAMEWORK SUMMARY")
        print("=" * 70)
        
        # Benchmark summary
        print(f"\n🔬 Benchmark Results:")
        print(f"   - Test Cases: {len(self.benchmark.test_cases)}")
        print(f"   - Methods Tested: {len(self.benchmark.extractors)}")
        print(f"   - Total Data Points: {len(self.results_df)}")
        
        # Performance summary
        if self.performance_report:
            print(f"\n⚡ Performance Summary:")
            summary = self.performance_report['summary_stats']
            print(f"   - Success Rates:")
            for method, rate in summary['success_rate_by_method'].items():
                print(f"     • {method}: {rate*100:.1f}%")
            
            print(f"   - Average Processing Times:")
            for method, time in summary['avg_processing_time_by_method'].items():
                print(f"     • {method}: {time:.3f}s")
        
        # Optimization summary
        if self.optimization_report:
            print(f"\n🎯 Optimization Results:")
            print(f"   - Optimal Method: {self.optimization_report['optimal_method']}")
            
            # Show top 3 methods
            top_methods = self.optimization_report['comparison_table'].head(3)
            print(f"   - Top 3 Methods:")
            for _, row in top_methods.iterrows():
                print(f"     • {row['Method']}: {row['Weighted Score']:.3f}")
        
        print(f"\n💾 Results saved to:")
        print(f"   - research_benchmark_results.csv")
        print(f"   - research_performance_report.txt")
        print(f"   - research_optimization_report.txt")
        print(f"   - Various visualization PNG files")
        
        print("\n" + "=" * 70)

def create_custom_test_cases():
    """Create custom test cases for specific research needs"""
    
    custom_cases = [
        # Add your custom test cases here
        {
            'text': "Your custom text here for testing specific scenarios",
            'expected_keywords': ['keyword1', 'keyword2'],
            'category': 'custom'
        }
    ]
    
    return custom_cases

async def main():
    """Main entry point for the research framework"""
    
    print("🎓 Multi-Method Keyword Extraction Research Framework")
    print("For Đồ Án - Comprehensive Method Comparison and Optimization")
    print("=" * 70)
    
    # Initialize framework
    framework = ResearchFramework()
    
    # Check if user wants to use custom test cases
    use_custom = input("\n🤔 Do you want to use custom test cases? (y/n): ").lower().strip()
    
    if use_custom == 'y':
        print("\n📝 Please provide your custom test cases in the create_custom_test_cases() function")
        print("   Then run the framework again.")
        return
    
    # Run the complete research
    success = await framework.run_complete_research()
    
    if success:
        # Print summary
        framework.print_summary()
        
        # Ask if user wants to see detailed results
        show_details = input("\n🔍 Do you want to see detailed results? (y/n): ").lower().strip()
        
        if show_details == 'y':
            print("\n📊 Detailed Results:")
            if framework.results_df is not None:
                print("\nBenchmark Results Preview:")
                print(framework.results_df.head(10))
            
            if framework.optimization_report:
                print(f"\n🎯 Optimization Justification:")
                print(framework.optimization_report['justification'])
    
    print("\n✨ Research Framework execution completed!")
    print("   Check the generated files for detailed analysis.")

if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("Please check your dependencies and try again.")
