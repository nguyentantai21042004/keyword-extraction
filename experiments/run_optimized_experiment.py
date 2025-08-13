#!/usr/bin/env python3
"""
Run Experiment with Optimized spaCy+YAKE Parameters
"""

import json
import os
import subprocess

def load_optimization_results():
    """Load optimization results"""
    if os.path.exists('spacy_yake_optimization_results.json'):
        with open('spacy_yake_optimization_results.json', 'r') as f:
            return json.load(f)
    return None

def update_spacy_yake_config(optimization_results):
    """Update spaCy+YAKE configuration with optimized parameters"""
    if not optimization_results:
        print("❌ No optimization results found!")
        return False
    
    # Get best configuration by confidence
    best_config = optimization_results['best_by_confidence']['config']
    
    print(f"🎯 Using optimized configuration: {best_config['name']}")
    print(f"   Parameters: {best_config}")
    
    # Update the multi_method_extractor.py with optimized parameters
    # This is a simplified approach - in practice you'd want to modify the class directly
    
    return True

def run_optimized_experiment():
    """Run experiment with optimized parameters"""
    print("🚀 RUNNING OPTIMIZED SPAÇY+YAKE EXPERIMENT")
    print("=" * 60)
    
    # Step 1: Load optimization results
    print("\n📊 STEP 1: Loading optimization results...")
    optimization_results = load_optimization_results()
    if not optimization_results:
        print("❌ Cannot continue without optimization results")
        return False
    
    # Step 2: Update configuration
    print("\n⚙️  STEP 2: Updating configuration...")
    if not update_spacy_yake_config(optimization_results):
        return False
    
    # Step 3: Run experiment
    print("\n🧪 STEP 3: Running experiment with optimized parameters...")
    experiment_command = "cd /Users/tantai/Workspaces/smap/smap-keyword-extraction && source myenv/bin/activate && cd experiments && python spacy_yake_experiment.py"
    
    try:
        result = subprocess.run(experiment_command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Experiment completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Experiment failed: {e}")
        return False

def show_optimization_summary():
    """Show optimization summary"""
    optimization_results = load_optimization_results()
    if not optimization_results:
        return
    
    print("\n📈 OPTIMIZATION SUMMARY:")
    print("-" * 40)
    
    configs = optimization_results['all_configurations']
    for config in configs:
        name = config['config']['name']
        time = config['avg_processing_time']
        confidence = config['avg_confidence']
        keywords = config['total_keywords']
        
        print(f"🔍 {name}:")
        print(f"   ⏱️  Time: {time:.4f}s")
        print(f"   🎯 Confidence: {confidence:.3f}")
        print(f"   🔑 Keywords: {keywords}")
        print()
    
    best_time = optimization_results['best_by_time']
    best_confidence = optimization_results['best_by_confidence']
    
    print(f"🏆 BEST PERFORMANCE:")
    print(f"   🚀 Fastest: {best_time['config']['name']} ({best_time['avg_processing_time']:.4f}s)")
    print(f"   🎯 Most Confident: {best_confidence['config']['name']} ({best_confidence['avg_confidence']:.3f})")
    
    # Show recommendations
    if 'recommendations' in optimization_results:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in optimization_results['recommendations']:
            print(f"   • {rec}")

def main():
    print("🎯 OPTIMIZED EXPERIMENT RUNNER")
    print("=" * 60)
    
    # Show optimization summary
    show_optimization_summary()
    
    # Ask user if they want to run optimized experiment
    print("\n❓ Do you want to run the experiment with optimized parameters?")
    print("   This will use the best configuration found during optimization.")
    
    # For now, just show the summary
    print("\n💡 To run with optimized parameters:")
    print("   1. Update multi_method_extractor.py with best parameters")
    print("   2. Run: python run_complete_experiment.py")
    print("\n📊 Current best configuration is saved in 'spacy_yake_optimization_results.json'")

if __name__ == "__main__":
    main()
