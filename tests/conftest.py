"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

# Ensure src/ is on the path for editable-style imports without pip install
sys.path.insert(0, str(Path(__file__).parent / "src"))
