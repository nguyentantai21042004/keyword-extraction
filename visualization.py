import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict

class BenchmarkVisualizer:
    """Create visualizations for thesis report"""
    
    def __init__(self, results_df: pd.DataFrame):
        self.results_df = results_df
        # Set style for better looking plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_performance_comparison(self):
        """Create comprehensive performance comparison charts"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Processing Time Comparison
        sns.boxplot(data=self.results_df, x='method', y='processing_time', ax=axes[0,0])
        axes[0,0].set_title('Processing Time by Method', fontsize=14, fontweight='bold')
        axes[0,0].set_xlabel('Extraction Method')
        axes[0,0].set_ylabel('Processing Time (seconds)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Memory Usage Comparison  
        sns.boxplot(data=self.results_df, x='method', y='memory_usage', ax=axes[0,1])
        axes[0,1].set_title('Memory Usage by Method', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('Extraction Method')
        axes[0,1].set_ylabel('Memory Usage (MB)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Confidence Score Distribution
        sns.boxplot(data=self.results_df, x='method', y='confidence_score', ax=axes[1,0])
        axes[1,0].set_title('Confidence Score by Method', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Extraction Method')
        axes[1,0].set_ylabel('Confidence Score')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Success Rate
        success_rates = self.results_df.groupby('method')['success'].mean()
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
    
    def create_accuracy_analysis(self):
        """Create accuracy analysis visualization"""
        
        # Filter out None accuracy values
        accuracy_data = self.results_df[self.results_df['accuracy'].notna()]
        
        if len(accuracy_data) > 0:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # Accuracy by method
            sns.boxplot(data=accuracy_data, x='method', y='accuracy', ax=axes[0])
            axes[0].set_title('Accuracy Distribution by Method', fontsize=14, fontweight='bold')
            axes[0].set_xlabel('Extraction Method')
            axes[0].set_ylabel('Accuracy Score (F1)')
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].set_ylim(0, 1)
            
            # Accuracy by text category
            sns.boxplot(data=accuracy_data, x='text_category', y='accuracy', ax=axes[1])
            axes[1].set_title('Accuracy by Text Category', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Text Category')
            axes[1].set_ylabel('Accuracy Score (F1)')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].set_ylim(0, 1)
            
            plt.tight_layout()
            plt.savefig('accuracy_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print("No accuracy data available for visualization")
    
    def create_method_comparison_heatmap(self):
        """Create heatmap comparing all methods across different metrics"""
        
        # Prepare data for heatmap
        method_metrics = self.results_df.groupby('method').agg({
            'processing_time': 'mean',
            'memory_usage': 'mean',
            'confidence_score': 'mean',
            'keywords_count': 'mean',
            'success': 'mean'
        }).round(4)
        
        # Normalize metrics for better comparison (0-1 scale)
        normalized_metrics = method_metrics.copy()
        
        # For processing time and memory, lower is better (invert)
        normalized_metrics['processing_time'] = 1 - (method_metrics['processing_time'] / method_metrics['processing_time'].max())
        normalized_metrics['memory_usage'] = 1 - (method_metrics['memory_usage'] / method_metrics['memory_usage'].max())
        
        # For other metrics, higher is better
        normalized_metrics['confidence_score'] = method_metrics['confidence_score'] / method_metrics['confidence_score'].max()
        normalized_metrics['keywords_count'] = method_metrics['keywords_count'] / method_metrics['keywords_count'].max()
        normalized_metrics['success'] = method_metrics['success']  # Already 0-1
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            normalized_metrics.T, 
            annot=True, 
            cmap='RdYlGn', 
            center=0.5,
            fmt='.3f',
            cbar_kws={'label': 'Normalized Score (0-1)'}
        )
        plt.title('Method Performance Comparison Heatmap\n(Higher = Better Performance)', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Extraction Method')
        plt.ylabel('Performance Metric')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('method_comparison_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_social_media_analysis(self):
        """Create analysis specifically for social media performance"""
        
        # Filter social media cases
        social_data = self.results_df[self.results_df['has_social_elements'] == True]
        
        if len(social_data) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Social media processing time
            sns.boxplot(data=social_data, x='method', y='processing_time', ax=axes[0,0])
            axes[0,0].set_title('Social Media: Processing Time', fontsize=12, fontweight='bold')
            axes[0,0].tick_params(axis='x', rotation=45)
            
            # Social media confidence
            sns.boxplot(data=social_data, x='method', y='confidence_score', ax=axes[0,1])
            axes[0,1].set_title('Social Media: Confidence Score', fontsize=12, fontweight='bold')
            axes[0,1].tick_params(axis='x', rotation=45)
            
            # Social media accuracy
            social_accuracy = social_data[social_data['accuracy'].notna()]
            if len(social_accuracy) > 0:
                sns.boxplot(data=social_accuracy, x='method', y='accuracy', ax=axes[1,0])
                axes[1,0].set_title('Social Media: Accuracy', fontsize=12, fontweight='bold')
                axes[1,0].tick_params(axis='x', rotation=45)
                axes[1,0].set_ylim(0, 1)
            
            # Keywords count comparison
            sns.boxplot(data=social_data, x='method', y='keywords_count', ax=axes[1,1])
            axes[1,1].set_title('Social Media: Keywords Count', fontsize=12, fontweight='bold')
            axes[1,1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('social_media_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print("No social media data available for analysis")
    
    def create_summary_statistics(self):
        """Create summary statistics visualization"""
        
        # Calculate summary stats
        summary_stats = self.results_df.groupby('method').agg({
            'processing_time': ['mean', 'std'],
            'memory_usage': ['mean', 'std'],
            'confidence_score': ['mean', 'std'],
            'keywords_count': ['mean', 'std'],
            'success': 'mean'
        }).round(4)
        
        # Create a comprehensive summary table
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare table data
        table_data = []
        for method in summary_stats.index:
            row = [
                method,
                f"{summary_stats.loc[method, ('processing_time', 'mean')]:.4f} ± {summary_stats.loc[method, ('processing_time', 'std')]:.4f}",
                f"{summary_stats.loc[method, ('memory_usage', 'mean')]:.2f} ± {summary_stats.loc[method, ('memory_usage', 'std')]:.2f}",
                f"{summary_stats.loc[method, ('confidence_score', 'mean')]:.3f} ± {summary_stats.loc[method, ('confidence_score', 'std')]:.3f}",
                f"{summary_stats.loc[method, ('keywords_count', 'mean')]:.1f} ± {summary_stats.loc[method, ('keywords_count', 'std')]:.1f}",
                f"{summary_stats.loc[method, ('success', 'mean')]:.3f}"
            ]
            table_data.append(row)
        
        # Create table
        table = ax.table(
            cellText=table_data,
            colLabels=['Method', 'Processing Time (s)', 'Memory (MB)', 'Confidence', 'Keywords Count', 'Success Rate'],
            cellLoc='center',
            loc='center',
            colWidths=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        # Color header row
        for i in range(len(table_data[0])):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.title('Comprehensive Method Performance Summary', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('summary_statistics.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_all_visualizations(self):
        """Create all visualizations for the thesis"""
        print("Creating comprehensive performance comparison...")
        self.create_performance_comparison()
        
        print("Creating accuracy analysis...")
        self.create_accuracy_analysis()
        
        print("Creating method comparison heatmap...")
        self.create_method_comparison_heatmap()
        
        print("Creating social media analysis...")
        self.create_social_media_analysis()
        
        print("Creating summary statistics...")
        self.create_summary_statistics()
        
        print("All visualizations created and saved!")
