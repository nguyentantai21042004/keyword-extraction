#!/usr/bin/env python3
"""
📊 Visualization Generator for spaCy + YAKE Experiment Results
Tạo charts và graphs từ kết quả thí nghiệm để sử dụng trong đồ án
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Dict, List

class ExperimentVisualizer:
    """Generate comprehensive visualizations from experiment results"""
    
    def __init__(self, results_dir: str = 'experiment_results'):
        self.results_dir = results_dir
        self.comprehensive_analysis = None
        self.detailed_analysis = None
        
        # Load results
        self._load_experiment_results()
        
        # Set plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def _load_experiment_results(self):
        """Load experiment results from files"""
        
        # Load comprehensive analysis
        comp_analysis_path = os.path.join(self.results_dir, 'comprehensive_analysis.json')
        if os.path.exists(comp_analysis_path):
            with open(comp_analysis_path, 'r', encoding='utf-8') as f:
                self.comprehensive_analysis = json.load(f)
            print(f"✓ Loaded comprehensive analysis from {comp_analysis_path}")
        else:
            print(f"❌ Comprehensive analysis not found at {comp_analysis_path}")
            return
        
        # Load detailed analysis
        detailed_analysis_path = os.path.join(self.results_dir, 'detailed_analysis.json')
        if os.path.exists(detailed_analysis_path):
            with open(detailed_analysis_path, 'r', encoding='utf-8') as f:
                self.detailed_analysis = json.load(f)
            print(f"✓ Loaded detailed analysis from {detailed_analysis_path}")
        else:
            print(f"❌ Detailed analysis not found at {detailed_analysis_path}")
    
    def create_all_visualizations(self):
        """Create all visualizations for the experiment results"""
        
        if not self.comprehensive_analysis:
            print("❌ No experiment results loaded. Run the experiment first.")
            return
        
        print("🎨 Creating comprehensive visualizations...")
        
        # Create output directory
        os.makedirs('experiment_visualizations', exist_ok=True)
        
        # Generate all visualizations
        self.create_performance_comparison_chart()
        self.create_accuracy_by_domain_chart()
        self.create_processing_time_analysis()
        self.create_confidence_score_distribution()
        self.create_method_ranking_chart()
        self.create_domain_performance_heatmap()
        self.create_statistical_significance_chart()
        self.create_keywords_count_comparison()
        
        print("✅ All visualizations created and saved to 'experiment_visualizations/' directory")
    
    def create_performance_comparison_chart(self):
        """Create comprehensive performance comparison chart"""
        
        if not self.comprehensive_analysis:
            return
        
        # Extract data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_analysis:
            methods.extend(list(self.comprehensive_analysis['baseline_overall_performance'].keys()))
        
        # Get accuracy data
        accuracies = []
        for method in methods:
            if method == 'spacy_yake':
                if 'accuracy' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    accuracies.append(self.comprehensive_analysis['spacy_yake_overall_performance']['accuracy']['mean'])
                else:
                    accuracies.append(0)
            else:
                if method in self.comprehensive_analysis['baseline_overall_performance']:
                    if 'accuracy' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        accuracies.append(self.comprehensive_analysis['baseline_overall_performance'][method]['accuracy'])
                    else:
                        accuracies.append(0)
                else:
                    accuracies.append(0)
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Accuracy comparison
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        bars1 = ax1.bar(methods, accuracies, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_title('Accuracy Comparison: spaCy + YAKE vs Baselines', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax1.set_ylim(0, 1)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, acc in zip(bars1, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Processing time comparison
        processing_times = []
        for method in methods:
            if method == 'spacy_yake':
                if 'processing_time' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    processing_times.append(self.comprehensive_analysis['spacy_yake_overall_performance']['processing_time']['mean'])
                else:
                    processing_times.append(0)
            else:
                if method in self.comprehensive_analysis['baseline_overall_performance']:
                    if 'processing_time' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        processing_times.append(self.comprehensive_analysis['baseline_overall_performance'][method]['processing_time'])
                    else:
                        processing_times.append(0)
                else:
                    processing_times.append(0)
        
        bars2 = ax2.bar(methods, processing_times, color=colors, alpha=0.8, edgecolor='black')
        ax2.set_title('Processing Time Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Processing Time (seconds)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, time_val in zip(bars2, processing_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{time_val:.3f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_accuracy_by_domain_chart(self):
        """Create accuracy analysis by domain"""
        
        if not self.comprehensive_analysis or 'domain_specific_analysis' not in self.comprehensive_analysis:
            return
        
        domain_data = self.comprehensive_analysis['domain_specific_analysis']
        
        domains = list(domain_data.keys())
        accuracies = [domain_data[domain]['avg_accuracy'] for domain in domains]
        confidences = [domain_data[domain]['avg_confidence'] for domain in domains]
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Accuracy by domain
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars1 = ax1.bar(domains, accuracies, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
        ax1.set_title('spaCy + YAKE Accuracy by Domain', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax1.set_ylim(0, 1)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, acc in zip(bars1, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Confidence by domain
        bars2 = ax2.bar(domains, confidences, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
        ax2.set_title('spaCy + YAKE Confidence by Domain', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Confidence Score', fontsize=12)
        ax2.set_ylim(0, 1)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, conf in zip(bars2, confidences):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{conf:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/accuracy_by_domain.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_processing_time_analysis(self):
        """Create detailed processing time analysis"""
        
        if not self.comprehensive_analysis:
            return
        
        # Extract processing time data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_analysis:
            methods.extend(list(self.comprehensive_analysis['baseline_overall_performance'].keys()))
        
        processing_times = []
        memory_usage = []
        
        for method in methods:
            if method == 'spacy_yake':
                if 'processing_time' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    processing_times.append(self.comprehensive_analysis['spacy_yake_overall_performance']['processing_time']['mean'])
                else:
                    processing_times.append(0)
                
                if 'memory_usage' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    memory_usage.append(self.comprehensive_analysis['spacy_yake_overall_performance']['memory_usage']['mean'])
                else:
                    memory_usage.append(0)
            else:
                if method in self.comprehensive_analysis['baseline_overall_performance']:
                    if 'processing_time' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        processing_times.append(self.comprehensive_analysis['baseline_overall_performance'][method]['processing_time'])
                    else:
                        processing_times.append(0)
                    
                    if 'memory_usage' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        memory_usage.append(self.comprehensive_analysis['baseline_overall_performance'][method]['memory_usage'])
                    else:
                        memory_usage.append(0)
                else:
                    processing_times.append(0)
                    memory_usage.append(0)
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Processing time
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        bars1 = ax1.bar(methods, processing_times, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_title('Processing Time Analysis', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Processing Time (seconds)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, time_val in zip(bars1, processing_times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{time_val:.3f}s', ha='center', va='bottom', fontweight='bold')
        
        # Memory usage
        bars2 = ax2.bar(methods, memory_usage, color=colors, alpha=0.8, edgecolor='black')
        ax2.set_title('Memory Usage Analysis', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Memory Usage (MB)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, mem_val in zip(bars2, memory_usage):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{mem_val:.1f}MB', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/processing_time_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_confidence_score_distribution(self):
        """Create confidence score distribution chart"""
        
        if not self.comprehensive_analysis:
            return
        
        # Extract confidence data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_analysis:
            methods.extend(list(self.comprehensive_analysis['baseline_overall_performance'].keys()))
        
        confidence_scores = []
        for method in methods:
            if method == 'spacy_yake':
                if 'confidence_score' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    confidence_scores.append(self.comprehensive_analysis['spacy_yake_overall_performance']['confidence_score']['mean'])
                else:
                    confidence_scores.append(0)
            else:
                if method in self.comprehensive_analysis['baseline_overall_performance']:
                    if 'confidence_score' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        confidence_scores.append(self.comprehensive_analysis['baseline_overall_performance'][method]['confidence_score'])
                    else:
                        confidence_scores.append(0)
                else:
                    confidence_scores.append(0)
        
        # Create chart
        plt.figure(figsize=(12, 6))
        
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        bars = plt.bar(methods, confidence_scores, color=colors, alpha=0.8, edgecolor='black')
        
        plt.title('Confidence Score Distribution Across Methods', fontsize=16, fontweight='bold')
        plt.ylabel('Confidence Score', fontsize=12)
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, conf in zip(bars, confidence_scores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{conf:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/confidence_score_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_method_ranking_chart(self):
        """Create method ranking chart"""
        
        if not self.comprehensive_analysis or 'performance_ranking' not in self.comprehensive_analysis:
            return
        
        ranking_data = self.comprehensive_analysis['performance_ranking']
        
        if 'ranking' not in ranking_data:
            return
        
        methods = [item[0] for item in ranking_data['ranking']]
        scores = [item[1] for item in ranking_data['ranking']]
        
        # Create chart
        plt.figure(figsize=(12, 6))
        
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        bars = plt.bar(methods, scores, color=colors, alpha=0.8, edgecolor='black')
        
        plt.title('Method Performance Ranking (Composite Score)', fontsize=16, fontweight='bold')
        plt.ylabel('Composite Performance Score', fontsize=12)
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Highlight best method
        best_method = ranking_data.get('best_method', '')
        if best_method:
            plt.text(0.02, 0.98, f'🏆 Best Method: {best_method}', 
                    transform=plt.gca().transAxes, fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/method_ranking.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_domain_performance_heatmap(self):
        """Create domain performance heatmap"""
        
        if not self.comprehensive_analysis or 'domain_specific_analysis' not in self.comprehensive_analysis:
            return
        
        domain_data = self.comprehensive_analysis['domain_specific_analysis']
        
        # Prepare data for heatmap
        domains = list(domain_data.keys())
        metrics = ['avg_accuracy', 'avg_confidence', 'avg_processing_time']
        
        heatmap_data = []
        for domain in domains:
            row = []
            for metric in metrics:
                if metric in domain_data[domain]:
                    row.append(domain_data[domain][metric])
                else:
                    row.append(0)
            heatmap_data.append(row)
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        
        # Normalize processing time (lower is better)
        normalized_data = np.array(heatmap_data)
        normalized_data[:, 2] = 1 - np.clip(normalized_data[:, 2] / 2.0, 0, 1)  # Normalize to 0-1
        
        sns.heatmap(normalized_data, 
                   annot=True, 
                   fmt='.3f',
                   xticklabels=['Accuracy', 'Confidence', 'Processing Time (Normalized)'],
                   yticklabels=[d.replace('_', ' ').title() for d in domains],
                   cmap='RdYlGn',
                   center=0.5,
                   cbar_kws={'label': 'Normalized Score (0-1)'})
        
        plt.title('Domain Performance Heatmap\n(Higher = Better Performance)', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Performance Metrics', fontsize=12)
        plt.ylabel('Text Domains', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/domain_performance_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_statistical_significance_chart(self):
        """Create statistical significance analysis chart"""
        
        if not self.detailed_analysis:
            return
        
        # Extract statistical data
        test_cases = list(self.detailed_analysis.keys())
        accuracies = []
        processing_times = []
        complexities = []
        
        for test_case in test_cases:
            if 'spacy_yake_stats' in self.detailed_analysis[test_case]:
                stats = self.detailed_analysis[test_case]['spacy_yake_stats']
                if stats and 'accuracy' in stats and 'mean' in stats['accuracy']:
                    accuracies.append(stats['accuracy']['mean'])
                    processing_times.append(stats['processing_time']['mean'])
                    complexities.append(self.detailed_analysis[test_case]['test_case_info']['complexity'])
        
        if not accuracies:
            return
        
        # Convert complexity to numeric
        complexity_map = {'low': 1, 'medium': 2, 'high': 3, 'very_high': 4}
        numeric_complexities = [complexity_map.get(c, 2) for c in complexities]
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Accuracy vs Complexity
        ax1.scatter(numeric_complexities, accuracies, s=100, alpha=0.7, color='#FF6B6B')
        ax1.set_title('Accuracy vs Text Complexity', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Complexity Level (1=Low, 4=Very High)', fontsize=12)
        ax1.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax1.set_ylim(0, 1)
        ax1.set_xticks([1, 2, 3, 4])
        ax1.set_xticklabels(['Low', 'Medium', 'High', 'Very High'])
        
        # Add trend line
        if len(accuracies) > 1:
            z = np.polyfit(numeric_complexities, accuracies, 1)
            p = np.poly1d(z)
            ax1.plot(numeric_complexities, p(numeric_complexities), "r--", alpha=0.8)
        
        # Processing Time vs Accuracy
        ax2.scatter(processing_times, accuracies, s=100, alpha=0.7, color='#4ECDC4')
        ax2.set_title('Processing Time vs Accuracy', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Processing Time (seconds)', fontsize=12)
        ax2.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax2.set_ylim(0, 1)
        
        # Add trend line
        if len(accuracies) > 1:
            z = np.polyfit(processing_times, accuracies, 1)
            p = np.poly1d(z)
            ax2.plot(processing_times, p(processing_times), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/statistical_significance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_keywords_count_comparison(self):
        """Create keywords count comparison chart"""
        
        if not self.comprehensive_analysis:
            return
        
        # Extract keywords count data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_analysis:
            methods.extend(list(self.comprehensive_analysis['baseline_overall_performance'].keys()))
        
        keywords_counts = []
        for method in methods:
            if method == 'spacy_yake':
                if 'keywords_count' in self.comprehensive_analysis['spacy_yake_overall_performance']:
                    keywords_counts.append(self.comprehensive_analysis['spacy_yake_overall_performance']['keywords_count']['mean'])
                else:
                    keywords_counts.append(0)
            else:
                if method in self.comprehensive_analysis['baseline_overall_performance']:
                    if 'keywords_count' in self.comprehensive_analysis['baseline_overall_performance'][method]:
                        keywords_counts.append(self.comprehensive_analysis['baseline_overall_performance'][method]['keywords_count'])
                    else:
                        keywords_counts.append(0)
                else:
                    keywords_counts.append(0)
        
        # Create chart
        plt.figure(figsize=(12, 6))
        
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        bars = plt.bar(methods, keywords_counts, color=colors, alpha=0.8, edgecolor='black')
        
        plt.title('Average Keywords Count by Method', fontsize=16, fontweight='bold')
        plt.ylabel('Average Keywords Count', fontsize=12)
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, count in zip(bars, keywords_counts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/keywords_count_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main function to create all visualizations"""
    
    print("📊 Experiment Visualization Generator")
    print("=" * 50)
    
    # Check if results exist
    if not os.path.exists('experiment_results'):
        print("❌ No experiment results found!")
        print("Please run the experiment first:")
        print("   python spacy_yake_experiment.py")
        return
    
    # Create visualizations
    visualizer = ExperimentVisualizer()
    visualizer.create_all_visualizations()
    
    print("\n🎉 All visualizations created successfully!")
    print("📁 Check the 'experiment_visualizations/' directory for all charts")
    print("\n📋 Generated charts:")
    print("   • performance_comparison.png - Overall performance comparison")
    print("   • accuracy_by_domain.png - Domain-specific accuracy analysis")
    print("   • processing_time_analysis.png - Time and memory analysis")
    print("   • confidence_score_distribution.png - Confidence score comparison")
    print("   • method_ranking.png - Method performance ranking")
    print("   • domain_performance_heatmap.png - Domain performance heatmap")
    print("   • statistical_significance.png - Statistical analysis")
    print("   • keywords_count_comparison.png - Keywords count comparison")

if __name__ == "__main__":
    main()
