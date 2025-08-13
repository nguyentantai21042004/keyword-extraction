"""
Performance analysis for keyword extraction methods
"""

import pandas as pd
import numpy as np
from typing import Dict, List

class PerformanceAnalyzer:
    """Analyze performance characteristics of keyword extraction methods"""
    
    def __init__(self):
        pass
    
    def analyze_processing_time(self, results_df: pd.DataFrame) -> Dict:
        """Analyze processing time performance"""
        
        if results_df.empty:
            return {}
        
        analysis = {}
        
        # Overall statistics
        analysis['overall'] = {
            'mean': results_df['processing_time'].mean(),
            'median': results_df['processing_time'].median(),
            'std': results_df['processing_time'].std(),
            'min': results_df['processing_time'].min(),
            'max': results_df['processing_time'].max()
        }
        
        # By method
        method_time = results_df.groupby('method')['processing_time'].agg(['mean', 'std', 'min', 'max'])
        analysis['by_method'] = method_time.to_dict('index')
        
        # By category
        category_time = results_df.groupby('category')['processing_time'].agg(['mean', 'std'])
        analysis['by_category'] = category_time.to_dict('index')
        
        # By language
        language_time = results_df.groupby('language')['processing_time'].agg(['mean', 'std'])
        analysis['by_language'] = language_time.to_dict('index')
        
        return analysis
    
    def analyze_memory_usage(self, results_df: pd.DataFrame) -> Dict:
        """Analyze memory usage performance"""
        
        if results_df.empty:
            return {}
        
        analysis = {}
        
        # Overall statistics
        analysis['overall'] = {
            'mean': results_df['memory_usage'].mean(),
            'median': results_df['memory_usage'].median(),
            'std': results_df['memory_usage'].std(),
            'min': results_df['memory_usage'].min(),
            'max': results_df['memory_usage'].max()
        }
        
        # By method
        method_memory = results_df.groupby('method')['memory_usage'].agg(['mean', 'std', 'min', 'max'])
        analysis['by_method'] = method_memory.to_dict('index')
        
        # By category
        category_memory = results_df.groupby('category')['memory_usage'].agg(['mean', 'std'])
        analysis['by_category'] = category_memory.to_dict('index')
        
        return analysis
    
    def analyze_accuracy_distribution(self, results_df: pd.DataFrame) -> Dict:
        """Analyze accuracy distribution across different dimensions"""
        
        if results_df.empty:
            return {}
        
        analysis = {}
        
        # Overall accuracy
        analysis['overall'] = {
            'mean': results_df['accuracy'].mean(),
            'median': results_df['accuracy'].median(),
            'std': results_df['accuracy'].std(),
            'min': results_df['accuracy'].min(),
            'max': results_df['accuracy'].max()
        }
        
        # By method
        method_accuracy = results_df.groupby('method')['accuracy'].agg(['mean', 'std', 'min', 'max'])
        analysis['by_method'] = method_accuracy.to_dict('index')
        
        # By category
        category_accuracy = results_df.groupby('category')['accuracy'].agg(['mean', 'std'])
        analysis['by_category'] = category_accuracy.to_dict('index')
        
        # By language
        language_accuracy = results_df.groupby('language')['accuracy'].agg(['mean', 'std'])
        analysis['by_language'] = language_accuracy.to_dict('index')
        
        # By complexity
        complexity_accuracy = results_df.groupby('complexity')['accuracy'].agg(['mean', 'std'])
        analysis['by_complexity'] = complexity_accuracy.to_dict('index')
        
        return analysis
    
    def identify_bottlenecks(self, results_df: pd.DataFrame) -> List[str]:
        """Identify performance bottlenecks"""
        
        bottlenecks = []
        
        # Check for slow methods
        method_time = results_df.groupby('method')['processing_time'].mean()
        avg_time = method_time.mean()
        
        for method, time in method_time.items():
            if time > avg_time * 2:
                bottlenecks.append(f"{method} is {time/avg_time:.1f}x slower than average")
        
        # Check for memory-intensive methods
        method_memory = results_df.groupby('method')['memory_usage'].mean()
        avg_memory = method_memory.mean()
        
        for method, memory in method_memory.items():
            if memory > avg_memory * 2:
                bottlenecks.append(f"{method} uses {memory/avg_memory:.1f}x more memory than average")
        
        # Check for low accuracy methods
        method_accuracy = results_df.groupby('method')['accuracy'].mean()
        avg_accuracy = method_accuracy.mean()
        
        for method, accuracy in method_accuracy.items():
            if accuracy < avg_accuracy * 0.7:
                bottlenecks.append(f"{method} has {accuracy/avg_accuracy:.1f}x lower accuracy than average")
        
        return bottlenecks
    
    def generate_performance_summary(self, results_df: pd.DataFrame) -> str:
        """Generate performance summary report"""
        
        summary = []
        summary.append("=" * 80)
        summary.append("PERFORMANCE ANALYSIS SUMMARY")
        summary.append("=" * 80)
        
        # Overall performance
        if not results_df.empty:
            summary.append(f"\n📊 OVERALL PERFORMANCE:")
            summary.append(f"   • Total test cases: {len(results_df)}")
            summary.append(f"   • Methods tested: {results_df['method'].nunique()}")
            summary.append(f"   • Average accuracy: {results_df['accuracy'].mean():.3f}")
            summary.append(f"   • Average processing time: {results_df['processing_time'].mean():.3f}s")
            summary.append(f"   • Average memory usage: {results_df['memory_usage'].mean():.1f}MB")
        
        # Method performance
        method_performance = results_df.groupby('method').agg({
            'accuracy': 'mean',
            'processing_time': 'mean',
            'memory_usage': 'mean'
        }).round(4)
        
        summary.append(f"\n🏆 METHOD PERFORMANCE:")
        for method, metrics in method_performance.iterrows():
            summary.append(f"   • {method}:")
            summary.append(f"     - Accuracy: {metrics['accuracy']:.3f}")
            summary.append(f"     - Time: {metrics['processing_time']:.3f}s")
            summary.append(f"     - Memory: {metrics['memory_usage']:.1f}MB")
        
        # Bottlenecks
        bottlenecks = self.identify_bottlenecks(results_df)
        if bottlenecks:
            summary.append(f"\n⚠️ PERFORMANCE BOTTLENECKS:")
            for bottleneck in bottlenecks:
                summary.append(f"   • {bottleneck}")
        else:
            summary.append(f"\n✅ No significant performance bottlenecks detected")
        
        summary.append("\n" + "=" * 80)
        return "\n".join(summary)
