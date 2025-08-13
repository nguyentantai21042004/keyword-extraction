"""
Unified experiment runner that cleans, runs the original experiment workflow, and generates charts.
Outputs are preserved in the same locations/names as before under experiments/experiment_results and experiments/experiment_visualizations.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiment_results"
VIS_DIR = REPO_ROOT / "experiment_visualizations"


def run_cmd(cmd: str, desc: str) -> None:
    print(f"\n🔄 {desc}...")
    print(f"   Command: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def clean_outputs() -> None:
    print("\n🧹 Cleaning old results...")
    if RESULTS_DIR.exists():
        import shutil
        shutil.rmtree(RESULTS_DIR)
        print("✅ Removed old experiment results")
    if VIS_DIR.exists():
        import shutil
        shutil.rmtree(VIS_DIR)
        print("✅ Removed old visualizations")


def run_complete() -> None:
    """Run the end-to-end experiment and chart generation."""
    # Ensure we are at repo root
    os.chdir(REPO_ROOT)

    clean_outputs()

    # Run experiment to produce experiment_results/*.json using the current interpreter
    run_cmd(f"{sys.executable} -m src.experiments.spacy_yake_experiment", "Running experiment")

    # Generate charts to experiment_visualizations/ at repo root
    # Use migrated charts module to write at root
    from .charts import ExperimentVisualizer
    viz = ExperimentVisualizer()
    viz.create_all_charts()

    print("\n🎉 All reports generated successfully!")
    print("📁 Results: experiments/experiment_results/")
    print("🖼️  Charts: experiments/experiment_visualizations/")


if __name__ == "__main__":
    try:
        run_complete()
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)
