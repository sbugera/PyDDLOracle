"""Ensure project root is importable when debugging a single test file."""

import os
import sys

# When launching a test module directly from this folder, make the repo root
# importable so `import pyddl_oracle` works under the debugger.
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
