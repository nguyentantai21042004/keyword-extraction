#!/usr/bin/env python3
"""
Complete Experiment Runner: Clean, Run, and Visualize
"""

import os
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and show progress"""
    print(f"\n🔄 {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def main():
    print("🚀 COMPLETE KEYWORD EXTRACTION EXPERIMENT RUNNER")
    print("=" * 60)
    
    # Step 1: Clean old results
    print("\n🧹 STEP 1: Cleaning old results...")
    if os.path.exists('experiment_results'):
        import shutil
        shutil.rmtree('experiment_results')
        print("✅ Removed old experiment results")
    
    if os.path.exists('experiment_visualizations'):
        import shutil
        shutil.rmtree('experiment_visualizations')
        print("✅ Removed old visualizations")
    
    # Step 2: Run experiment
    print("\n🧪 STEP 2: Running complete experiment...")
    experiment_command = "cd /Users/tantai/Workspaces/smap/smap-keyword-extraction && source myenv/bin/activate && cd experiments && python spacy_yake_experiment.py"
    
    if not run_command(experiment_command, "Running experiment"):
        print("❌ Experiment failed! Cannot continue.")
        return
    
    # Step 3: Create visualizations
    print("\n🎨 STEP 3: Creating visualizations...")
    if not run_command("python create_charts.py", "Creating charts"):
        print("❌ Chart creation failed!")
        return
    
    # Step 4: Show results summary
    print("\n📊 STEP 4: Results summary...")
    if os.path.exists('experiment_results/comprehensive_analysis.json'):
        print("✅ Experiment data saved to 'experiment_results/'")
        print("✅ Charts saved to 'experiment_visualizations/'")
        
        # Show file sizes
        import json
        with open('experiment_results/comprehensive_analysis.json', 'r') as f:
            data = json.load(f)
            test_cases = data.get('experiment_summary', {}).get('total_test_cases', 0)
            iterations = data.get('experiment_summary', {}).get('total_iterations', 0)
            print(f"📈 Test Cases: {test_cases}")
            print(f"🔄 Total Iterations: {iterations}")
            print(f"🏆 Best Method: {data.get('performance_ranking', {}).get('best_method', 'N/A')}")
            print(f"📊 Best Score: {data.get('performance_ranking', {}).get('best_score', 'N/A')}")
    
    # Step 5: List generated files
    print("\n📁 STEP 5: Generated files...")
    if os.path.exists('experiment_results'):
        print("📂 experiment_results/")
        for file in os.listdir('experiment_results'):
            size = os.path.getsize(f'experiment_results/{file}')
            print(f"   📄 {file} ({size:,} bytes)")
    
    if os.path.exists('experiment_visualizations'):
        print("📂 experiment_visualizations/")
        for file in os.listdir('experiment_visualizations'):
            size = os.path.getsize(f'experiment_visualizations/{file}')
            print(f"   🖼️  {file} ({size:,} bytes)")
    
    print("\n🎉 EXPERIMENT COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("💡 Next steps:")
    print("   • Check 'experiment_results/' for detailed data")
    print("   • View 'experiment_visualizations/' for charts")
    print("   • Use data to write your report")
    print("   • Compare all 6 algorithms: spaCy+YAKE, RAKE, TF-IDF, TextRank, KeyBERT, Hybrid")

if __name__ == "__main__":
    main()
