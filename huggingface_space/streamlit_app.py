"""HuggingFace Spaces entry point — DYNAFOLD Hub."""

import sys
from pathlib import Path

# Add src to path so dynafold_hub imports work
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

# Execute the main landing page
# Streamlit will auto-discover pages/ at root level
app_file = ROOT / "src" / "dynafold_hub" / "ui" / "app.py"
exec(compile(app_file.read_text(), str(app_file), "exec"))
