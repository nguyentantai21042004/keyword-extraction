"""
Create visualizations for keyword extraction benchmark results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict

class BenchmarkVisualizer:
    """Create visualizations for thesis report"""
    
    def __init__(self):
        # Set style for better looking plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_method_performance_comparison(self, results_df: pd.DataFrame):
        """Create comprehensive performance comparison charts"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Processing Time Comparison
        sns.boxplot(data=results_df, x='method', y='processing_time', ax=axes[0,0])
        axes[0,0].set_title('Processing Time by Method', fontsize=14, fontweight='bold')
        axes[0,0].set_xlabel('Extraction Method')
        axes[0,0].set_ylabel('Processing Time (seconds)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Memory Usage Comparison  
        sns.boxplot(data=results_df, x='method', y='memory_usage', ax=axes[0,1])
        axes[0,1].set_title('Memory Usage by Method', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('Extraction Method')
        axes[0,1].set_ylabel('Memory Usage (MB)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Confidence Score Distribution
        sns.boxplot(data=results_df, x='method', y='confidence_score', ax=axes[1,0])
        axes[1,0].set_title('Confidence Score by Method', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Extraction Method')
        axes[1,0].set_ylabel('Confidence Score')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Success Rate
        success_rates = results_df.groupby('method')['success'].mean()
        success_rates.plot(kind='bar', ax=axes[1,1], color='skyblue', edgecolor='black')
        axes[1,1].set_title('Success Rate by Method', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('Extraction Method')
        axes[1,1].set_ylabel('Success Rate')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].set_ylim(0, 1)
        
        # Add value labels on success rate bars
        for i, v in enumerate(success_rates):
            axes[1,1].text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('method_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_enhanced_accuracy_analysis(self, results_df: pd.DataFrame):
        """Create enhanced accuracy analysis visualization"""
        
        # Filter out None accuracy values
        accuracy_data = results_df[results_df['accuracy'].notna()]
        
        if len(accuracy_data) > 0:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # Accuracy by method
            sns.boxplot(data=accuracy_data, x='method', y='accuracy', ax=axes[0])
            axes[0].set_title('Accuracy Distribution by Method', fontsize=14, fontweight='bold')
            axes[0].set_xlabel('Extraction Method')
            axes[0].set_ylabel('Accuracy Score (F1)')
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].set_ylim(0, 1)
            
            # Accuracy by category
            sns.boxplot(data=accuracy_data, x='category', y='accuracy', ax=axes[1])
            axes[1].set_title('Accuracy by Text Category', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Text Category')
            axes[1].set_ylabel('Accuracy Score (F1)')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].set_ylim(0, 1)
            
            plt.tight_layout()
            plt.savefig('enhanced_accuracy_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print("No accuracy data available for visualization")
    
    def create_domain_performance_analysis(self, results_df: pd.DataFrame):
        """Create domain-specific performance analysis"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Performance by category
        category_performance = results_df.groupby('category').agg({
            'accuracy': 'mean',
            'processing_time': 'mean',
            'memory_usage': 'mean'
        })
        
        # Accuracy by category
        category_performance['accuracy'].plot(kind='bar', ax=axes[0,0], color='lightcoral')
        axes[0,0].set_title('Accuracy by Domain', fontsize=12, fontweight='bold')
        axes[0,0].set_ylabel('Accuracy')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Processing time by category
        category_performance['processing_time'].plot(kind='bar', ax=axes[0,1], color='lightblue')
        axes[0,0].set_title('Processing Time by Domain', fontsize=12, fontweight='bold')
        axes[0,1].set_ylabel('Processing Time (s)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Language performance
        language_performance = results_df.groupby('language').agg({
            'accuracy': 'mean',
            'success': 'mean'
        })
        
        # Accuracy by language
        language_performance['accuracy'].plot(kind='bar', ax=axes[1,0], color='lightgreen')
        axes[1,0].set_title('Accuracy by Language', fontsize=12, fontweight='bold')
        axes[1,0].set_ylabel('Accuracy')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Success rate by language
        language_performance['success'].plot(kind='bar', ax=axes[1,1], color='lightyellow')
        axes[1,1].set_title('Success Rate by Language', fontsize=12, fontweight='bold')
        axes[1,1].set_ylabel('Success Rate')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('domain_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_language_performance_analysis(self, results_df: pd.DataFrame):
        """Create language-specific performance analysis"""
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Filter by language
        en_data = results_df[results_df['language'] == 'en']
        vi_data = results_df[results_df['language'] == 'vi']
        
        if not en_data.empty and not vi_data.empty:
            # Accuracy comparison
            methods = results_df['method'].unique()
            en_accuracies = [en_data[en_data['method'] == method]['accuracy'].mean() for method in methods]
            vi_accuracies = [vi_data[vi_data['method'] == method]['accuracy'].mean() for method in methods]
            
            x = range(len(methods))
            width = 0.35
            
            axes[0].bar([i - width/2 for i in x], en_accuracies, width, label='English', color='skyblue')
            axes[0].bar([i + width/2 for i in x], vi_accuracies, width, label='Vietnamese', color='lightcoral')
            axes[0].set_xlabel('Method')
            axes[0].set_ylabel('Accuracy')
            axes[0].set_title('Accuracy by Language and Method')
            axes[0].set_xticks(x)
            axes[0].set_xticklabels(methods, rotation=45)
            axes[0].legend()
            axes[0].set_ylim(0, 1)
            
            # Processing time comparison
            en_times = [en_data[en_data['method'] == method]['processing_time'].mean() for method in methods]
            vi_times = [vi_data[vi_data['method'] == method]['processing_time'].mean() for method in methods]
            
            axes[1].bar([i - width/2 for i in x], en_times, width, label='English', color='skyblue')
            axes[1].bar([i + width/2 for i in x], vi_times, width, label='Vietnamese', color='lightcoral')
            axes[1].set_xlabel('Method')
            axes[1].set_ylabel('Processing Time (s)')
            axes[1].set_title('Processing Time by Language and Method')
            axes[1].set_xticks(x)
            axes[1].set_xticklabels(methods, rotation=45)
            axes[1].legend()
        
        plt.tight_layout()
        plt.savefig('language_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_complexity_performance_analysis(self, results_df: pd.DataFrame):
        """Create complexity-based performance analysis"""
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Accuracy by complexity
        complexity_order = ['low', 'medium', 'high', 'very_high']
        sns.boxplot(data=results_df, x='complexity', y='accuracy', order=complexity_order, ax=axes[0])
        axes[0].set_title('Accuracy by Text Complexity', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Complexity Level')
        axes[0].set_ylabel('Accuracy')
        axes[0].set_ylim(0, 1)
        
        # Processing time by complexity
        sns.boxplot(data=results_df, x='complexity', y='processing_time', order=complexity_order, ax=axes[1])
        axes[1].set_title('Processing Time by Text Complexity', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Complexity Level')
        axes[1].set_ylabel('Processing Time (s)')
        
        plt.tight_layout()
        plt.savefig('complexity_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_method_comparison_heatmap(self, results_df: pd.DataFrame):
        """Create heatmap comparing all methods across different metrics"""
        
        # Prepare data for heatmap
        method_metrics = results_df.groupby('method').agg({
            'processing_time': 'mean',
            'memory_usage': 'mean',
            'confidence_score': 'mean',
            'keywords_count': 'mean',
            'success': 'mean'
        }).round(4)
        
        # Normalize metrics for better visualization
        normalized_metrics = method_metrics.copy()
        normalized_metrics['processing_time'] = 1 - (normalized_metrics['processing_time'] / normalized_metrics['processing_time'].max())
        normalized_metrics['memory_usage'] = 1 - (normalized_metrics['memory_usage'] / normalized_metrics['memory_usage'].max())
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(normalized_metrics.T, annot=True, cmap='RdYlGn', center=0.5, 
                   fmt='.3f', cbar_kws={'label': 'Normalized Score'})
        plt.title('Method Performance Heatmap', fontsize=16, fontweight='bold')
        plt.xlabel('Extraction Method')
        plt.ylabel('Performance Metric')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('method_comparison_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
