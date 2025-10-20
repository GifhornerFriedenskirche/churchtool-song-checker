import sys
from pathlib import Path

# Add repository root to sys.path so tests can import top-level modules
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
