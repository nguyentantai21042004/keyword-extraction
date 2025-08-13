#!/usr/bin/env python3
"""
Entry point for the Enhanced Keyword Extraction Framework.
"""

import sys
from pathlib import Path

# Ensure repo root is on sys.path for package imports
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.experiments.run_all import run_complete

if __name__ == "__main__":
    # One-liner to generate all reports and charts
    try:
        run_complete()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
