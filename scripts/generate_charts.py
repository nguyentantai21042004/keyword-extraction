#!/usr/bin/env python3
"""
Generate charts from existing experiment data
"""

import sys
from pathlib import Path

# Add the project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import json
import pandas as pd
from src.visualization.charts import BenchmarkVisualizer

def generate_charts_from_existing_data():
    """Generate charts from existing experiment data"""
    
    print("📊 Generating charts from existing experiment data...")
    
    # Check if data exists
    results_file = REPO_ROOT / "experiment_results" / "comprehensive_analysis.json"
    
    if not results_file.exists():
        print("❌ No existing experiment data found!")
        print("   Please run experiments first using: python scripts/run_experiments.py")
        return
    
    try:
        # Load data
        print("📋 Loading experiment data...")
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        results_df = pd.DataFrame(data)
        print(f"✅ Loaded {len(results_df)} results")
        
        # Create visualizations directory
        vis_dir = REPO_ROOT / "experiment_visualizations"
        vis_dir.mkdir(exist_ok=True)
        
        # Generate charts
        print("📈 Generating charts...")
        visualizer = BenchmarkVisualizer()
        visualizer.create_comprehensive_charts(results_df, str(vis_dir))
        
        print(f"✅ Charts generated successfully in {vis_dir}")
        
        # List generated files
        print("\n📁 Generated files:")
        for file in vis_dir.glob("*.png"):
            print(f"   📊 {file.name}")
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_charts_from_existing_data()
