#!/usr/bin/env python3
"""
Create Charts and Visualizations for Keyword Extraction Experiment
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os

class ExperimentVisualizer:
    def __init__(self):
        self.comprehensive_data = None
        self.detailed_data = None
        self.load_data()
        
    def load_data(self):
        """Load experiment data"""
        try:
            with open('experiment_results/comprehensive_analysis.json', 'r') as f:
                self.comprehensive_data = json.load(f)
            print("✅ Loaded comprehensive analysis data")
        except FileNotFoundError:
            print("❌ comprehensive_analysis.json not found")
            return
            
        try:
            with open('experiment_results/detailed_analysis.json', 'r') as f:
                self.detailed_data = json.load(f)
            print("✅ Loaded detailed analysis data")
        except FileNotFoundError:
            print("❌ detailed_analysis.json not found")
    
    def create_performance_comparison_chart(self):
        """Create performance comparison chart"""
        if not self.comprehensive_data:
            return
            
        # Extract data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        
        # Get accuracy data
        accuracies = []
        for method in methods:
            if method == 'spacy_yake':
                if 'accuracy' in self.comprehensive_data['spacy_yake_overall_performance']:
                    accuracies.append(self.comprehensive_data['spacy_yake_overall_performance']['accuracy']['mean'])
                else:
                    accuracies.append(0)
            else:
                if method in self.comprehensive_data['baseline_overall_performance']:
                    if 'accuracy' in self.comprehensive_data['baseline_overall_performance'][method]:
                        accuracies.append(self.comprehensive_data['baseline_overall_performance'][method]['accuracy']['mean'])
                    else:
                        accuracies.append(0)
                else:
                    accuracies.append(0)
        
        # Get processing time data
        processing_times = []
        for method in methods:
            if method == 'spacy_yake':
                if 'processing_time' in self.comprehensive_data['spacy_yake_overall_performance']:
                    processing_times.append(self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'])
                else:
                    processing_times.append(0)
            else:
                if method in self.comprehensive_data['baseline_overall_performance']:
                    if 'processing_time' in self.comprehensive_data['baseline_overall_performance'][method]:
                        processing_times.append(self.comprehensive_data['baseline_overall_performance'][method]['processing_time']['mean'])
                    else:
                        processing_times.append(0)
                else:
                    processing_times.append(0)
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Accuracy comparison
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        method_labels = [method.replace('_', ' ').title() for method in methods]
        
        bars1 = ax1.bar(method_labels, accuracies, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_title('Accuracy Comparison: All Methods', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax1.set_ylim(0, max(accuracies) * 1.2)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, acc in zip(bars1, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Processing time comparison
        bars2 = ax2.bar(method_labels, processing_times, color=colors, alpha=0.8, edgecolor='black')
        ax2.set_title('Processing Time Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Processing Time (seconds)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, time_val in zip(bars2, processing_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                    f'{time_val:.4f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/performance_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Created performance comparison chart")
        plt.show()
    
    def create_radar_chart(self):
        """Create radar chart for method comparison"""
        if not self.comprehensive_data:
            return
            
        # Extract methods
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        
        # Prepare data for radar chart
        categories = ['Accuracy', 'Speed', 'Confidence', 'Keywords']
        num_vars = len(categories)
        
        # Calculate angles for each axis
        angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
        angles += angles[:1]  # Complete the circle
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot each method
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, method in enumerate(methods):
            values = []
            
            # Accuracy (normalize to 0-1)
            if method == 'spacy_yake':
                acc = self.comprehensive_data['spacy_yake_overall_performance']['accuracy']['mean']
            else:
                acc = self.comprehensive_data['baseline_overall_performance'][method]['accuracy']['mean']
            values.append(acc)
            
            # Speed (inverse of processing time, normalize)
            if method == 'spacy_yake':
                speed = 1 / (self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'] + 0.001)
            else:
                speed = 1 / (self.comprehensive_data['baseline_overall_performance'][method]['processing_time']['mean'] + 0.001)
            # Normalize speed to 0-1
            max_speed = max([1/(self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'] + 0.001)] + 
                           [1/(self.comprehensive_data['baseline_overall_performance'][m]['processing_time']['mean'] + 0.001) 
                            for m in methods if m != 'spacy_yake'])
            speed = speed / max_speed
            values.append(speed)
            
            # Confidence
            if method == 'spacy_yake':
                conf = self.comprehensive_data['spacy_yake_overall_performance']['confidence_score']['mean']
            else:
                conf = self.comprehensive_data['baseline_overall_performance'][method]['confidence_score']['mean']
            values.append(conf)
            
            # Keywords (normalize to 0-1)
            if method == 'spacy_yake':
                kw = self.comprehensive_data['spacy_yake_overall_performance']['keywords_count']['mean']
            else:
                kw = self.comprehensive_data['baseline_overall_performance'][method]['keywords_count']['mean']
            # Normalize keywords to 0-1
            max_kw = max([self.comprehensive_data['spacy_yake_overall_performance']['keywords_count']['mean']] + 
                        [self.comprehensive_data['baseline_overall_performance'][m]['keywords_count']['mean'] 
                         for m in methods if m != 'spacy_yake'])
            kw = kw / max_kw
            values.append(kw)
            
            values += values[:1]  # Complete the circle
            
            # Plot
            method_label = method.replace('_', ' ').title()
            ax.plot(angles, values, 'o-', linewidth=2, label=method_label, color=colors[i % len(colors)])
            ax.fill(angles, values, alpha=0.1, color=colors[i % len(colors)])
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title('Method Performance Radar Chart', size=16, y=1.1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/radar_chart.png', dpi=300, bbox_inches='tight')
        print("✅ Created radar chart")
        plt.show()
    
    def create_domain_performance_chart(self):
        """Create domain performance chart"""
        if not self.comprehensive_data or 'domain_specific_analysis' not in self.comprehensive_data:
            return
            
        domain_data = self.comprehensive_data['domain_specific_analysis']
        
        domains = list(domain_data.keys())
        accuracies = [domain_data[domain]['avg_accuracy'] for domain in domains]
        confidences = [domain_data[domain]['avg_confidence'] for domain in domains]
        processing_times = [domain_data[domain]['avg_processing_time'] for domain in domains]
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Accuracy by domain
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        domain_labels = [domain.replace('_', ' ').title() for domain in domains]
        
        bars1 = ax1.bar(domain_labels, accuracies, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
        ax1.set_title('spaCy + YAKE Accuracy by Domain', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1 Score)', fontsize=12)
        ax1.set_ylim(0, max(accuracies) * 1.2)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, acc in zip(bars1, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Confidence by domain
        bars2 = ax2.bar(domain_labels, confidences, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
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
        plt.savefig('experiment_visualizations/domain_performance.png', dpi=300, bbox_inches='tight')
        print("✅ Created domain performance chart")
        plt.show()
    
    def create_processing_time_analysis(self):
        """Create processing time analysis chart"""
        if not self.comprehensive_data:
            return
            
        # Extract data
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        
        # Get processing time data with error bars
        processing_times = []
        processing_stds = []
        
        for method in methods:
            if method == 'spacy_yake':
                if 'processing_time' in self.comprehensive_data['spacy_yake_overall_performance']:
                    processing_times.append(self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'])
                    processing_stds.append(self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['std'])
                else:
                    processing_times.append(0)
                    processing_stds.append(0)
            else:
                if method in self.comprehensive_data['baseline_overall_performance']:
                    if 'processing_time' in self.comprehensive_data['baseline_overall_performance'][method]:
                        processing_times.append(self.comprehensive_data['baseline_overall_performance'][method]['processing_time']['mean'])
                        processing_stds.append(self.comprehensive_data['baseline_overall_performance'][method]['processing_time']['std'])
                    else:
                        processing_times.append(0)
                        processing_stds.append(0)
                else:
                    processing_times.append(0)
                    processing_stds.append(0)
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        method_labels = [method.replace('_', ' ').title() for method in methods]
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        
        bars = ax.bar(method_labels, processing_times, yerr=processing_stds, 
                      color=colors, alpha=0.8, edgecolor='black', capsize=5)
        
        ax.set_title('Processing Time Analysis with Standard Deviation', fontsize=14, fontweight='bold')
        ax.set_ylabel('Processing Time (seconds)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, time_val, std_val in zip(bars, processing_times, processing_stds):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std_val + 0.0001,
                    f'{time_val:.4f}s\n±{std_val:.4f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('experiment_visualizations/processing_time_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Created processing time analysis chart")
        plt.show()
    
    def create_all_charts(self):
        """Create all charts"""
        print("🎨 Creating all visualizations...")
        
        # Create directory if it doesn't exist
        os.makedirs('experiment_visualizations', exist_ok=True)
        
        # Create charts
        self.create_performance_comparison_chart()
        self.create_radar_chart()
        self.create_domain_performance_chart()
        self.create_processing_time_analysis()
        
        print("🎉 All charts created successfully!")
        print("📁 Check 'experiment_visualizations/' directory for PNG files")

def main():
    print("📊 Experiment Visualization Generator")
    print("=" * 50)
    
    visualizer = ExperimentVisualizer()
    visualizer.create_all_charts()

if __name__ == "__main__":
    main()
