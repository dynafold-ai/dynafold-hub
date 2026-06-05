"""HuggingFace Spaces entry point.

This file is the entry point that HF Spaces auto-runs.
It simply imports the main Streamlit app from dynafold_hub.
"""

import sys
from pathlib import Path

# Add src to path so we can import dynafold_hub
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

# Import and run the main app
exec(open(ROOT / "src" / "dynafold_hub" / "ui" / "app.py").read())
