"""
Optimization analysis for keyword extraction methods
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from ..config import OPTIMIZATION_WEIGHTS

class OptimizationAnalyzer:
    """Analyze and optimize keyword extraction performance"""
    
    def __init__(self):
        self.optimization_weights = OPTIMIZATION_WEIGHTS
    
    def analyze_performance(self, results_df: pd.DataFrame) -> Dict:
        """Analyze performance and provide optimization recommendations"""
        
        if results_df.empty:
            return {'error': 'No results to analyze'}
        
        analysis = {
            'method_rankings': self._rank_methods(results_df),
            'performance_analysis': self._analyze_performance_metrics(results_df),
            'optimization_recommendations': self._generate_recommendations(results_df),
            'best_method': self._find_best_method(results_df),
            'performance_gaps': self._identify_performance_gaps(results_df)
        }
        
        return analysis
    
    def _rank_methods(self, results_df: pd.DataFrame) -> List[Tuple[str, float]]:
        """Rank methods by overall performance score"""
        
        # Calculate weighted scores for each method
        method_scores = {}
        
        for method in results_df['method'].unique():
            method_data = results_df[results_df['method'] == method]
            
            # Calculate normalized scores
            accuracy_score = method_data['accuracy'].mean()
            time_score = 1 - (method_data['processing_time'].mean() / results_df['processing_time'].max())
            memory_score = 1 - (method_data['memory_usage'].mean() / results_df['memory_usage'].max())
            confidence_score = method_data['confidence_score'].mean()
            success_score = method_data['success'].mean()
            
            # Apply weights
            weighted_score = (
                OPTIMIZATION_WEIGHTS['balanced']['accuracy'] * accuracy_score +
                OPTIMIZATION_WEIGHTS['balanced']['processing_time'] * time_score +
                OPTIMIZATION_WEIGHTS['balanced']['memory_usage'] * memory_score +
                OPTIMIZATION_WEIGHTS['balanced']['confidence_score'] * confidence_score +
                OPTIMIZATION_WEIGHTS['balanced']['success_rate'] * success_score
            )
            
            method_scores[method] = weighted_score
        
        # Sort by score
        ranked_methods = sorted(method_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_methods
    
    def _analyze_performance_metrics(self, results_df: pd.DataFrame) -> Dict:
        """Analyze performance metrics across methods"""
        
        analysis = {}
        
        # Method-wise analysis
        for method in results_df['method'].unique():
            method_data = results_df[results_df['method'] == method]
            
            analysis[method] = {
                'accuracy': {
                    'mean': method_data['accuracy'].mean(),
                    'std': method_data['accuracy'].std(),
                    'min': method_data['accuracy'].min(),
                    'max': method_data['accuracy'].max()
                },
                'processing_time': {
                    'mean': method_data['processing_time'].mean(),
                    'std': method_data['processing_time'].std()
                },
                'memory_usage': {
                    'mean': method_data['memory_usage'].mean(),
                    'std': method_data['memory_usage'].std()
                },
                'confidence_score': {
                    'mean': method_data['confidence_score'].mean(),
                    'std': method_data['confidence_score'].std()
                },
                'success_rate': method_data['success'].mean()
            }
        
        return analysis
    
    def _generate_recommendations(self, results_df: pd.DataFrame) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Analyze accuracy gaps
        accuracy_by_method = results_df.groupby('method')['accuracy'].mean()
        best_accuracy = accuracy_by_method.max()
        
        for method, accuracy in accuracy_by_method.items():
            if accuracy < best_accuracy * 0.8:  # 20% below best
                recommendations.append(f"Improve accuracy for {method}: currently {accuracy:.3f}, target {best_accuracy:.3f}")
        
        # Analyze processing time
        time_by_method = results_df.groupby('method')['processing_time'].mean()
        avg_time = time_by_method.mean()
        
        for method, time in time_by_method.items():
            if time > avg_time * 2:  # 2x slower than average
                recommendations.append(f"Optimize processing time for {method}: currently {time:.3f}s, target {avg_time:.3f}s")
        
        # Analyze memory usage
        memory_by_method = results_df.groupby('method')['memory_usage'].mean()
        avg_memory = memory_by_method.mean()
        
        for method, memory in memory_by_method.items():
            if memory > avg_memory * 1.5:  # 50% higher than average
                recommendations.append(f"Reduce memory usage for {method}: currently {memory:.1f}MB, target {avg_memory:.1f}MB")
        
        return recommendations
    
    def _find_best_method(self, results_df: pd.DataFrame) -> Tuple[str, float]:
        """Find the best performing method"""
        
        ranked_methods = self._rank_methods(results_df)
        if ranked_methods:
            return ranked_methods[0]
        return None, 0.0
    
    def _identify_performance_gaps(self, results_df: pd.DataFrame) -> Dict:
        """Identify performance gaps between methods"""
        
        gaps = {}
        
        # Calculate performance ranges
        accuracy_range = results_df['accuracy'].max() - results_df['accuracy'].min()
        time_range = results_df['processing_time'].max() - results_df['processing_time'].min()
        memory_range = results_df['memory_usage'].max() - results_df['memory_usage'].min()
        
        gaps['accuracy_gap'] = accuracy_range
        gaps['time_gap'] = time_range
        gaps['memory_gap'] = memory_range
        
        # Identify methods with largest gaps
        method_accuracy = results_df.groupby('method')['accuracy'].mean()
        method_time = results_df.groupby('method')['processing_time'].mean()
        method_memory = results_df.groupby('method')['memory_usage'].mean()
        
        gaps['accuracy_leader'] = method_accuracy.idxmax()
        gaps['time_leader'] = method_time.idxmin()
        gaps['memory_leader'] = method_memory.idxmin()
        
        return gaps
    
    def generate_optimization_report(self, analysis_results: Dict) -> str:
        """Generate human-readable optimization report"""
        
        report = []
        report.append("=" * 80)
        report.append("KEYWORD EXTRACTION OPTIMIZATION REPORT")
        report.append("=" * 80)
        
        # Method rankings
        if 'method_rankings' in analysis_results:
            report.append("\n🏆 METHOD RANKINGS:")
            for i, (method, score) in enumerate(analysis_results['method_rankings'], 1):
                report.append(f"   {i}. {method}: {score:.3f}")
        
        # Best method
        if 'best_method' in analysis_results and analysis_results['best_method'][0]:
            best_method, best_score = analysis_results['best_method']
            report.append(f"\n🥇 BEST METHOD: {best_method} (Score: {best_score:.3f})")
        
        # Performance gaps
        if 'performance_gaps' in analysis_results:
            gaps = analysis_results['performance_gaps']
            report.append(f"\n📊 PERFORMANCE GAPS:")
            report.append(f"   • Accuracy gap: {gaps.get('accuracy_gap', 0):.3f}")
            report.append(f"   • Processing time gap: {gaps.get('time_gap', 0):.3f}s")
            report.append(f"   • Memory usage gap: {gaps.get('memory_gap', 0):.1f}MB")
        
        # Recommendations
        if 'optimization_recommendations' in analysis_results:
            recommendations = analysis_results['optimization_recommendations']
            if recommendations:
                report.append(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
                for i, rec in enumerate(recommendations, 1):
                    report.append(f"   {i}. {rec}")
            else:
                report.append("\n✅ No optimization recommendations - all methods performing well!")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def save_analysis_results(self, analysis_results: Dict, filename: str):
        """Save analysis results to file"""
        
        import json
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"✅ Analysis results saved to {filename}")
