"""
Unified experiment runner for the keyword extraction framework.
Runs comprehensive benchmarks and generates visualizations.
"""

import asyncio
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiment_results"
VIS_DIR = REPO_ROOT / "experiment_visualizations"


def setup_directories() -> None:
    """Ensure output directories exist"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    VIS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Output directories ready")


def clean_outputs() -> None:
    """Clean old results"""
    print("\n🧹 Cleaning old results...")
    if RESULTS_DIR.exists():
        import shutil
        shutil.rmtree(RESULTS_DIR)
        print("✅ Removed old experiment results")
    if VIS_DIR.exists():
        import shutil
        shutil.rmtree(VIS_DIR)
        print("✅ Removed old visualizations")


async def run_complete() -> None:
    """Run the end-to-end experiment and chart generation."""
    # Ensure we are at repo root
    os.chdir(REPO_ROOT)
    
    print("🚀 Starting comprehensive keyword extraction benchmark...")
    
    clean_outputs()
    setup_directories()
    
    try:
        # Run comprehensive benchmark using the new framework
        from ..benchmark import ExtractionBenchmark
        from ..benchmark.test_datasets import create_research_test_dataset
        
        # Initialize benchmark
        benchmark = ExtractionBenchmark()
        
        # Load test cases
        test_cases = create_research_test_dataset()
        for case in test_cases:
            benchmark.add_test_case(**case)
        
        print(f"📋 Added {len(test_cases)} test cases")
        
        # Run benchmark
        results = await benchmark.run_comprehensive_benchmark()
        
        # Save results
        results_file = RESULTS_DIR / "comprehensive_analysis.csv"
        results.to_csv(results_file, index=False)
        print(f"💾 Results saved to {results_file}")
        
        # Save benchmark report
        benchmark.save_benchmark_report(RESULTS_DIR / "benchmark_report.json")
        
        # Generate visualizations
        from ..visualization.charts import BenchmarkVisualizer
        visualizer = BenchmarkVisualizer()
        visualizer.create_comprehensive_charts(results, str(VIS_DIR))
        
        print("\n🎉 All reports generated successfully!")
        print(f"📁 Results: {RESULTS_DIR}")
        print(f"🖼️  Charts: {VIS_DIR}")
        
    except Exception as e:
        print(f"❌ Error during experiment: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(run_complete())
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)
