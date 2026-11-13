import sys
from pathlib import Path

# Add root directory to sys.path so app and its modules are discovered
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import app

# Vercel serverless entrypoint
app.debug = False
