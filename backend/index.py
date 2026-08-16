import os
import sys
import types

# Ensure both backend directory and parent root directory are in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Ensure 'backend' module is available in sys.modules for standalone deployments
if "backend" not in sys.modules:
    mod = types.ModuleType("backend")
    mod.__path__ = [backend_dir]
    mod.__file__ = os.path.join(backend_dir, "__init__.py")
    sys.modules["backend"] = mod

# Load the existing FastAPI app as the source of truth
try:
    from backend.main import app
except ImportError:
    from main import app

