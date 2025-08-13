import pandas as pd
import numpy as np
from typing import Dict

class OptimizationAnalyzer:
    """Analyze results to justify optimization decisions"""
    
    def __init__(self, benchmark_results: pd.DataFrame):
        self.results = benchmark_results
        
    def find_optimal_method(self, weights: Dict[str, float] = None) -> Dict:
        """Find optimal method based on weighted criteria"""
        
        if weights is None:
            weights = {
                'processing_time': 0.25,  # Lower is better
                'memory_usage': 0.15,     # Lower is better  
                'confidence_score': 0.25, # Higher is better
                'accuracy': 0.25,         # Higher is better
                'success_rate': 0.10      # Higher is better
            }
        
        method_scores = {}
        
        for method in self.results['method'].unique():
            method_data = self.results[self.results['method'] == method]
            
            # Normalize metrics (0-1 scale)
            metrics = {
                'processing_time': 1 - (method_data['processing_time'].mean() / self.results['processing_time'].max()),
                'memory_usage': 1 - (method_data['memory_usage'].mean() / self.results['memory_usage'].max()),
                'confidence_score': method_data['confidence_score'].mean(),
                'accuracy': method_data['accuracy'].mean() if method_data['accuracy'].notna().any() else 0.5,
                'success_rate': method_data['success'].mean()
            }
            
            # Calculate weighted score
            weighted_score = sum(
                metrics[metric] * weight 
                for metric, weight in weights.items()
            )
            
            method_scores[method] = {
                'weighted_score': weighted_score,
                'metrics': metrics,
                'raw_stats': {
                    'avg_processing_time': method_data['processing_time'].mean(),
                    'avg_memory_usage': method_data['memory_usage'].mean(),
                    'avg_confidence': method_data['confidence_score'].mean(),
                    'success_rate': method_data['success'].mean()
                }
            }
        
        # Find optimal method
        optimal_method = max(method_scores.keys(), key=lambda x: method_scores[x]['weighted_score'])
        
        return {
            'optimal_method': optimal_method,
            'scores': method_scores,
            'justification': self._generate_justification(optimal_method, method_scores)
        }
    
    def _generate_justification(self, optimal_method: str, scores: Dict) -> str:
        """Generate justification text for thesis"""
        
        optimal_score = scores[optimal_method]
        
        justification = f"""
        Phân tích tối ưu cho thấy '{optimal_method}' là phương pháp tối ưu với điểm số {optimal_score['weighted_score']:.3f}.
        
        Lý do lựa chọn:
        - Thời gian xử lý: {optimal_score['raw_stats']['avg_processing_time']:.2f}s (cân bằng tốt)
        - Sử dụng memory: {optimal_score['raw_stats']['avg_memory_usage']:.1f}MB (hiệu quả)
        - Độ tin cậy: {optimal_score['raw_stats']['avg_confidence']:.3f} (ổn định)
        - Tỉ lệ thành công: {optimal_score['raw_stats']['success_rate']*100:.1f}% (đáng tin cậy)
        
        Phương pháp này cung cấp sự cân bằng tối ưu giữa hiệu suất, độ chính xác và tài nguyên sử dụng,
        phù hợp cho hệ thống real-time social media analysis.
        """
        
        return justification.strip()
    
    def generate_optimization_report(self, weights: Dict[str, float] = None) -> Dict:
        """Generate comprehensive optimization report"""
        
        # Find optimal method
        optimization_result = self.find_optimal_method(weights)
        
        # Create detailed comparison table
        comparison_data = []
        for method, data in optimization_result['scores'].items():
            comparison_data.append({
                'Method': method,
                'Weighted Score': data['weighted_score'],
                'Processing Time Score': data['metrics']['processing_time'],
                'Memory Score': data['metrics']['memory_usage'],
                'Confidence Score': data['metrics']['confidence_score'],
                'Accuracy Score': data['metrics']['accuracy'],
                'Success Rate Score': data['metrics']['success_rate'],
                'Raw Processing Time (s)': data['raw_stats']['avg_processing_time'],
                'Raw Memory (MB)': data['raw_stats']['avg_memory_usage'],
                'Raw Confidence': data['raw_stats']['avg_confidence'],
                'Raw Success Rate': data['raw_stats']['success_rate']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Weighted Score', ascending=False)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(optimization_result, comparison_df)
        
        return {
            'optimal_method': optimization_result['optimal_method'],
            'justification': optimization_result['justification'],
            'comparison_table': comparison_df,
            'recommendations': recommendations,
            'weights_used': weights or {
                'processing_time': 0.25,
                'memory_usage': 0.15,
                'confidence_score': 0.25,
                'accuracy': 0.25,
                'success_rate': 0.10
            }
        }
    
    def _generate_recommendations(self, optimization_result: Dict, comparison_df: pd.DataFrame) -> Dict:
        """Generate actionable recommendations based on analysis"""
        
        recommendations = {
            'primary_recommendation': f"Sử dụng {optimization_result['optimal_method']} làm phương pháp chính",
            'performance_insights': [],
            'optimization_suggestions': [],
            'use_case_recommendations': {}
        }
        
        # Analyze performance insights
        top_methods = comparison_df.head(3)
        for _, method_data in top_methods.iterrows():
            method_name = method_data['Method']
            if method_name == optimization_result['optimal_method']:
                continue
                
            if method_data['Weighted Score'] > 0.7:  # High performing alternative
                recommendations['performance_insights'].append(
                    f"{method_name} cũng có hiệu suất cao ({method_data['Weighted Score']:.3f}) và có thể dùng làm backup"
                )
        
        # Generate optimization suggestions
        for _, method_data in comparison_df.iterrows():
            method_name = method_data['Method']
            
            if method_data['Raw Processing Time (s)'] > 1.0:
                recommendations['optimization_suggestions'].append(
                    f"{method_name}: Có thể tối ưu thời gian xử lý (hiện tại: {method_data['Raw Processing Time (s)']:.2f}s)"
                )
            
            if method_data['Raw Memory (MB)'] > 100:
                recommendations['optimization_suggestions'].append(
                    f"{method_name}: Có thể tối ưu memory usage (hiện tại: {method_data['Raw Memory (MB)']:.1f}MB)"
                )
        
        # Use case recommendations
        recommendations['use_case_recommendations'] = {
            'real_time_processing': optimization_result['optimal_method'],
            'high_accuracy_required': comparison_df.loc[comparison_df['Raw Confidence'].idxmax(), 'Method'],
            'resource_constrained': comparison_df.loc[comparison_df['Raw Memory (MB)'].idxmin(), 'Method'],
            'fast_processing': comparison_df.loc[comparison_df['Raw Processing Time (s)'].idxmin(), 'Method']
        }
        
        return recommendations
    
    def create_optimization_visualization(self, weights: Dict[str, float] = None):
        """Create visualization for optimization analysis"""
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Get optimization results
        optimization_result = self.find_optimal_method(weights)
        
        # Create radar chart for top 3 methods
        top_methods = list(optimization_result['scores'].keys())[:3]
        
        # Prepare data for radar chart
        categories = ['Processing Time', 'Memory Usage', 'Confidence', 'Accuracy', 'Success Rate']
        
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for method in top_methods:
            method_data = optimization_result['scores'][method]
            values = [
                method_data['metrics']['processing_time'],
                method_data['metrics']['memory_usage'],
                method_data['metrics']['confidence_score'],
                method_data['metrics']['accuracy'],
                method_data['metrics']['success_rate']
            ]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=method)
            ax.fill(angles, values, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title('Method Performance Comparison (Radar Chart)', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.tight_layout()
        plt.savefig('optimization_radar_chart.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create weighted score comparison
        plt.figure(figsize=(12, 6))
        methods = list(optimization_result['scores'].keys())
        scores = [optimization_result['scores'][method]['weighted_score'] for method in methods]
        
        bars = plt.bar(methods, scores, color=['#4CAF50' if method == optimization_result['optimal_method'] else '#2196F3' for method in methods])
        plt.title('Weighted Performance Scores by Method', fontsize=16, fontweight='bold')
        plt.xlabel('Extraction Method')
        plt.ylabel('Weighted Score')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                    f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('weighted_scores_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
