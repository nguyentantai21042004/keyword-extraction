#!/usr/bin/env python3
"""
🚀 Enhanced Keyword Extraction Experiment Runner
Improved framework with Vietnamese support and balanced scoring
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command and show progress"""
    print(f"\n🔄 {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout[:200]}...")
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
    print("🚀 ENHANCED KEYWORD EXTRACTION EXPERIMENT RUNNER")
    print("=" * 70)
    print("✨ Enhanced Features:")
    print("   • 25+ test cases including Vietnamese content")
    print("   • Balanced scoring system for fair comparison")
    print("   • Enhanced accuracy metrics with partial matching")
    print("   • Comprehensive performance analysis")
    print("   • Multilingual support (English + Vietnamese)")
    print("=" * 70)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"\n📁 Working directory: {os.getcwd()}")
    
    # Step 1: Clean old results
    print("\n🧹 STEP 1: Cleaning old results...")
    for dir_name in ['experiment_results', 'experiment_visualizations']:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"✅ Removed old {dir_name}")
    
    # Step 2: Activate virtual environment and run enhanced experiment
    print("\n🧪 STEP 2: Running enhanced experiment...")
    
    # Check if virtual environment exists
    venv_path = project_root / "myenv"
    if venv_path.exists():
        activate_cmd = f"source {venv_path}/bin/activate"
        experiment_cmd = f"{activate_cmd} && python main.py"
    else:
        print("⚠️ Virtual environment not found, running without activation")
        experiment_cmd = "python main.py"
    
    if not run_command(experiment_cmd, "Running enhanced experiment"):
        print("❌ Enhanced experiment failed! Cannot continue.")
        return
    
    # Step 3: Check if results were generated
    print("\n📊 STEP 3: Checking results...")
    
    expected_files = [
        "enhanced_benchmark_results.csv",
        "enhanced_benchmark_report.json", 
        "enhanced_optimization_report.txt",
        "enhanced_analysis_results.json"
    ]
    
    generated_files = []
    for file_name in expected_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            generated_files.append((file_name, size))
            print(f"✅ {file_name} ({size:,} bytes)")
        else:
            print(f"❌ {file_name} - NOT FOUND")
    
    # Step 4: Show experiment summary
    print("\n📈 STEP 4: Experiment summary...")
    
    if os.path.exists("enhanced_analysis_results.json"):
        try:
            with open("enhanced_analysis_results.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'summary' in data:
                summary = data['summary']
                print(f"📊 Test Cases: {summary.get('total_test_cases', 'N/A')}")
                print(f"🔄 Total Methods: {summary.get('total_methods', 'N/A')}")
                print(f"📋 Results Generated: {summary.get('total_results', 'N/A')}")
                print(f"✅ Success Rate: {summary.get('success_rate', 'N/A'):.1%}")
                print(f"🌍 Languages: {', '.join(summary.get('languages_covered', []))}")
                print(f"📂 Categories: {', '.join(summary.get('categories_covered', []))}")
            
            if 'best_method' in data:
                print(f"🏆 Best Method: {data['best_method']}")
                print(f"📊 Best Score: {data['best_score']:.3f}")
                
        except Exception as e:
            print(f"⚠️ Could not read analysis results: {e}")
    
    # Step 5: Show method rankings
    print("\n🏆 STEP 5: Method rankings...")
    
    if os.path.exists("enhanced_analysis_results.json"):
        try:
            with open("enhanced_analysis_results.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'method_rankings' in data:
                print("Method Rankings (Enhanced Scoring):")
                for i, (method, score) in enumerate(data['method_rankings'][:5], 1):
                    print(f"   {i}. {method}: {score:.3f}")
                    
        except Exception as e:
            print(f"⚠️ Could not read method rankings: {e}")
    
    # Step 6: Show generated files summary
    print("\n📁 STEP 6: Generated files summary...")
    
    if generated_files:
        print("📂 Enhanced Results Files:")
        for file_name, size in generated_files:
            print(f"   📄 {file_name} ({size:,} bytes)")
    
    # Step 7: Show next steps
    print("\n💡 STEP 7: Next steps...")
    print("✅ Enhanced experiment completed successfully!")
    print("=" * 70)
    print("🎯 What was accomplished:")
    print("   • Expanded from 10 to 25+ test cases")
    print("   • Added Vietnamese content support")
    print("   • Implemented balanced scoring system")
    print("   • Enhanced accuracy metrics")
    print("   • Comprehensive performance analysis")
    print("")
    print("📚 How to use the results:")
    print("   • Check 'enhanced_analysis_results.json' for detailed analysis")
    print("   • Review 'enhanced_optimization_report.txt' for recommendations")
    print("   • Use 'enhanced_benchmark_results.csv' for further analysis")
    print("   • Compare all 6 algorithms with fair scoring")
    print("")
    print("🔬 Research improvements:")
    print("   • Larger sample size (25+ vs 10 test cases)")
    print("   • Multilingual evaluation (English + Vietnamese)")
    print("   • Balanced scoring prevents baseline methods from scoring 0")
    print("   • Enhanced accuracy with partial matching")
    print("   • Comprehensive domain and complexity coverage")
    print("")
    print("🚀 Ready for thesis integration!")

if __name__ == "__main__":
    main()
