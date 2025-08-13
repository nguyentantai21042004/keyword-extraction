"""
Charts and visualizations for experiment results.
Reads from 'experiment_results/' and writes to 'experiment_visualizations/' at repo root.
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
        # style
        plt.style.use('seaborn-v0_8')

    def load_data(self):
        try:
            with open('experiment_results/comprehensive_analysis.json', 'r') as f:
                self.comprehensive_data = json.load(f)
            print("✅ Loaded comprehensive analysis data")
        except FileNotFoundError:
            print("❌ comprehensive_analysis.json not found in 'experiment_results/'")
            return
        try:
            with open('experiment_results/detailed_analysis.json', 'r') as f:
                self.detailed_data = json.load(f)
            print("✅ Loaded detailed analysis data")
        except FileNotFoundError:
            print("❌ detailed_analysis.json not found")

    def create_performance_comparison_chart(self):
        if not self.comprehensive_data:
            return
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        accuracies = []
        for method in methods:
            if method == 'spacy_yake':
                accuracies.append(self.comprehensive_data['spacy_yake_overall_performance'].get('accuracy', {}).get('mean', 0))
            else:
                accuracies.append(self.comprehensive_data['baseline_overall_performance'].get(method, {}).get('accuracy', {}).get('mean', 0))
        processing_times = []
        for method in methods:
            if method == 'spacy_yake':
                processing_times.append(self.comprehensive_data['spacy_yake_overall_performance'].get('processing_time', {}).get('mean', 0))
            else:
                processing_times.append(self.comprehensive_data['baseline_overall_performance'].get(method, {}).get('processing_time', {}).get('mean', 0))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        colors = ['#FF6B6B' if method == 'spacy_yake' else '#4ECDC4' for method in methods]
        labels = [m.replace('_', ' ').title() for m in methods]
        bars1 = ax1.bar(labels, accuracies, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_title('Accuracy Comparison: All Methods', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1)')
        ax1.set_ylim(0, max(accuracies) * 1.2 if accuracies else 1)
        ax1.tick_params(axis='x', rotation=45)
        for bar, acc in zip(bars1, accuracies):
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., h + 0.01, f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        bars2 = ax2.bar(labels, processing_times, color=colors, alpha=0.8, edgecolor='black')
        ax2.set_title('Processing Time Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Processing Time (s)')
        ax2.tick_params(axis='x', rotation=45)
        for bar, t in zip(bars2, processing_times):
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., h + 0.0001, f'{t:.4f}s', ha='center', va='bottom', fontweight='bold')
        os.makedirs('experiment_visualizations', exist_ok=True)
        plt.tight_layout()
        plt.savefig('experiment_visualizations/performance_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Created performance comparison chart")

    def create_radar_chart(self):
        if not self.comprehensive_data:
            return
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        categories = ['Accuracy', 'Speed', 'Confidence', 'Keywords']
        num_vars = len(categories)
        angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        for i, method in enumerate(methods):
            values = []
            acc = self.comprehensive_data['spacy_yake_overall_performance']['accuracy']['mean'] if method == 'spacy_yake' else self.comprehensive_data['baseline_overall_performance'][method]['accuracy']['mean']
            values.append(acc)
            speed = 1 / ((self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'] if method == 'spacy_yake' else self.comprehensive_data['baseline_overall_performance'][method]['processing_time']['mean']) + 0.001)
            max_speed = max([1/(self.comprehensive_data['spacy_yake_overall_performance']['processing_time']['mean'] + 0.001)] + [1/(self.comprehensive_data['baseline_overall_performance'][m]['processing_time']['mean'] + 0.001) for m in methods if m != 'spacy_yake'])
            values.append(speed / max_speed)
            conf = self.comprehensive_data['spacy_yake_overall_performance']['confidence_score']['mean'] if method == 'spacy_yake' else self.comprehensive_data['baseline_overall_performance'][method]['confidence_score']['mean']
            values.append(conf)
            kw = self.comprehensive_data['spacy_yake_overall_performance']['keywords_count']['mean'] if method == 'spacy_yake' else self.comprehensive_data['baseline_overall_performance'][method]['keywords_count']['mean']
            max_kw = max([self.comprehensive_data['spacy_yake_overall_performance']['keywords_count']['mean']] + [self.comprehensive_data['baseline_overall_performance'][m]['keywords_count']['mean'] for m in methods if m != 'spacy_yake'])
            values.append(kw / max_kw)
            values += values[:1]
            label = method.replace('_', ' ').title()
            ax.plot(angles, values, 'o-', linewidth=2, label=label, color=colors[i % len(colors)])
            ax.fill(angles, values, alpha=0.1, color=colors[i % len(colors)])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title('Method Performance Radar Chart', size=16, y=1.1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        os.makedirs('experiment_visualizations', exist_ok=True)
        plt.tight_layout()
        plt.savefig('experiment_visualizations/radar_chart.png', dpi=300, bbox_inches='tight')
        print("✅ Created radar chart")

    def create_domain_performance_chart(self):
        if not self.comprehensive_data or 'domain_specific_analysis' not in self.comprehensive_data:
            return
        domain_data = self.comprehensive_data['domain_specific_analysis']
        domains = list(domain_data.keys())
        accuracies = [domain_data[domain]['avg_accuracy'] for domain in domains]
        confidences = [domain_data[domain]['avg_confidence'] for domain in domains]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        labels = [d.replace('_', ' ').title() for d in domains]
        bars1 = ax1.bar(labels, accuracies, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
        ax1.set_title('spaCy + YAKE Accuracy by Domain', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Accuracy (F1)')
        ax1.set_ylim(0, max(accuracies) * 1.2)
        ax1.tick_params(axis='x', rotation=45)
        for bar, acc in zip(bars1, accuracies):
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., h + 0.01, f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        bars2 = ax2.bar(labels, confidences, color=colors[:len(domains)], alpha=0.8, edgecolor='black')
        ax2.set_title('spaCy + YAKE Confidence by Domain', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Confidence')
        ax2.set_ylim(0, 1)
        ax2.tick_params(axis='x', rotation=45)
        for bar, conf in zip(bars2, confidences):
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., h + 0.01, f'{conf:.3f}', ha='center', va='bottom', fontweight='bold')
        os.makedirs('experiment_visualizations', exist_ok=True)
        plt.tight_layout()
        plt.savefig('experiment_visualizations/domain_performance.png', dpi=300, bbox_inches='tight')
        print("✅ Created domain performance chart")

    def create_processing_time_analysis(self):
        if not self.comprehensive_data:
            return
        methods = ['spacy_yake']
        if 'baseline_overall_performance' in self.comprehensive_data:
            methods.extend(list(self.comprehensive_data['baseline_overall_performance'].keys()))
        times = []
        stds = []
        for m in methods:
            if m == 'spacy_yake':
                times.append(self.comprehensive_data['spacy_yake_overall_performance'].get('processing_time', {}).get('mean', 0))
                stds.append(self.comprehensive_data['spacy_yake_overall_performance'].get('processing_time', {}).get('std', 0))
            else:
                times.append(self.comprehensive_data['baseline_overall_performance'].get(m, {}).get('processing_time', {}).get('mean', 0))
                stds.append(self.comprehensive_data['baseline_overall_performance'].get(m, {}).get('processing_time', {}).get('std', 0))
        fig, ax = plt.subplots(figsize=(12, 6))
        labels = [m.replace('_', ' ').title() for m in methods]
        colors = ['#FF6B6B' if m == 'spacy_yake' else '#4ECDC4' for m in methods]
        bars = ax.bar(labels, times, yerr=stds, color=colors, alpha=0.8, edgecolor='black', capsize=5)
        ax.set_title('Processing Time Analysis with Standard Deviation', fontsize=14, fontweight='bold')
        ax.set_ylabel('Processing Time (s)')
        ax.tick_params(axis='x', rotation=45)
        for bar, t, s in zip(bars, times, stds):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + s + 0.0001, f'{t:.4f}s\n±{s:.4f}s', ha='center', va='bottom', fontweight='bold')
        os.makedirs('experiment_visualizations', exist_ok=True)
        plt.tight_layout()
        plt.savefig('experiment_visualizations/processing_time_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Created processing time analysis chart")

    def create_all_charts(self):
        print("🎨 Creating all visualizations...")
        os.makedirs('experiment_visualizations', exist_ok=True)
        self.create_performance_comparison_chart()
        self.create_radar_chart()
        self.create_domain_performance_chart()
        self.create_processing_time_analysis()
        print("🎉 All charts created successfully!")
        print("📁 Check 'experiment_visualizations/' directory for PNG files")
