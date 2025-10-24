import os
import sys

# Ensure project root is on PYTHONPATH when launching debugger
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
