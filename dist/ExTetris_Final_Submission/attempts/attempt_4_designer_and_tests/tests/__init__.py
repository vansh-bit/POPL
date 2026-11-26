import sys
from pathlib import Path

ATTEMPT4_DIR = str(Path(__file__).resolve().parent.parent)
if ATTEMPT4_DIR not in sys.path:
    sys.path.insert(0, ATTEMPT4_DIR)
