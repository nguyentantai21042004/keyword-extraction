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

    def create_comprehensive_charts(self, results_df: pd.DataFrame, output_dir: str = "./"):
        """Create all comprehensive visualization charts"""
        
        print("📊 Creating comprehensive visualization charts...")
        
        # Set output directory
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Change to output directory for saving files
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        try:
            # 1. Method Performance Comparison
            print("   📈 Creating method performance comparison...")
            self.create_method_performance_comparison(results_df)
            plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. Domain Performance Analysis
            print("   🌐 Creating domain performance analysis...")
            self.create_domain_performance_analysis(results_df)
            plt.savefig('domain_performance.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 3. Processing Time Analysis
            print("   ⏱️  Creating processing time analysis...")
            self.create_processing_time_analysis(results_df)
            plt.savefig('processing_time_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 4. Radar Chart
            print("   📊 Creating radar chart...")
            self.create_radar_chart(results_df)
            plt.savefig('radar_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 5. Enhanced Accuracy Analysis
            print("   🎯 Creating enhanced accuracy analysis...")
            self.create_enhanced_accuracy_analysis(results_df)
            plt.savefig('enhanced_accuracy_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 6. Language Performance Analysis
            print("   🌍 Creating language performance analysis...")
            self.create_language_performance_analysis(results_df)
            plt.savefig('language_performance_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 7. Complexity Performance Analysis
            print("   📚 Creating complexity performance analysis...")
            self.create_complexity_performance_analysis(results_df)
            plt.savefig('complexity_performance_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 8. Method Comparison Heatmap
            print("   🔥 Creating method comparison heatmap...")
            self.create_method_comparison_heatmap(results_df)
            plt.savefig('method_comparison_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ All charts created successfully in {output_dir}")
            
        finally:
            # Return to original directory
            os.chdir(original_dir)

    def create_processing_time_analysis(self, results_df: pd.DataFrame):
        """Create detailed processing time analysis"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Processing time distribution by method
        sns.boxplot(data=results_df, x='method', y='processing_time', ax=axes[0,0])
        axes[0,0].set_title('Processing Time Distribution by Method', fontsize=12, fontweight='bold')
        axes[0,0].set_xlabel('Method')
        axes[0,0].set_ylabel('Processing Time (seconds)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Processing time vs accuracy scatter
        sns.scatterplot(data=results_df, x='processing_time', y='accuracy', hue='method', ax=axes[0,1])
        axes[0,1].set_title('Processing Time vs Accuracy', fontsize=12, fontweight='bold')
        axes[0,1].set_xlabel('Processing Time (seconds)')
        axes[0,1].set_ylabel('Accuracy')
        
        # Processing time by category
        sns.boxplot(data=results_df, x='category', y='processing_time', ax=axes[1,0])
        axes[1,0].set_title('Processing Time by Category', fontsize=12, fontweight='bold')
        axes[1,0].set_xlabel('Category')
        axes[1,0].set_ylabel('Processing Time (seconds)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Processing time statistics
        time_stats = results_df.groupby('method')['processing_time'].agg(['mean', 'std', 'min', 'max']).round(4)
        time_stats.plot(kind='bar', ax=axes[1,1])
        axes[1,1].set_title('Processing Time Statistics by Method', fontsize=12, fontweight='bold')
        axes[1,1].set_xlabel('Method')
        axes[1,1].set_ylabel('Time (seconds)')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].legend()
        
        plt.tight_layout()

    def create_radar_chart(self, results_df: pd.DataFrame):
        """Create radar chart comparing methods across multiple metrics"""
        
        # Calculate average metrics for each method
        method_metrics = results_df.groupby('method').agg({
            'accuracy': 'mean',
            'confidence_score': 'mean',
            'success': 'mean',
            'keywords_count': 'mean'
        }).fillna(0)
        
        # Normalize metrics to 0-1 scale
        normalized_metrics = method_metrics.copy()
        for col in normalized_metrics.columns:
            if normalized_metrics[col].max() > 0:
                normalized_metrics[col] = normalized_metrics[col] / normalized_metrics[col].max()
        
        # Prepare data for radar chart
        categories = list(normalized_metrics.columns)
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
        angles += angles[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot each method
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        for i, method in enumerate(normalized_metrics.index):
            values = normalized_metrics.loc[method].values.flatten().tolist()
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, label=method, color=colors[i % len(colors)])
            ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        
        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.title('Method Performance Radar Chart', size=16, y=1.1)
        plt.tight_layout()

    def create_all_charts(self):
        """Create all charts from existing data"""
        
        # Load existing results
        import json
        from pathlib import Path
        
        results_file = Path("experiment_results/comprehensive_analysis.json")
        if results_file.exists():
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame
            import pandas as pd
            results_df = pd.DataFrame(data)
            
            # Create charts
            self.create_comprehensive_charts(results_df, "experiment_visualizations/")
        else:
            print("❌ No existing results found. Please run experiments first.")
