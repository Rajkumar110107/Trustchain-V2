import os
import sys

# Ensure backend root directory is in sys.path
api_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(api_dir)
parent_dir = os.path.dirname(backend_dir)

for path in [api_dir, backend_dir, parent_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import the existing FastAPI app
try:
    from backend.main import app
except ImportError:
    from main import app
