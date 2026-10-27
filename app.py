"""
Agri Gram AI - Production Application Entry Point
Supports running via:
  - python app.py
  - gunicorn app:app (Render, Railway, Linux containers)
  - waitress-serve --port=5000 app:app (Windows production)
Author: Abinaya K
"""
import os
import sys
import importlib.util

# Ensure UTF-8 output encoding on Windows console to avoid charmap codec errors
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure backend directory is in python module path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Load the backend Flask application module directly
_backend_app_path = os.path.join(BACKEND_DIR, "app.py")
_spec = importlib.util.spec_from_file_location("backend_app", _backend_app_path)
_backend_app = importlib.util.module_from_spec(_spec)
sys.modules["backend_app"] = _backend_app
_spec.loader.exec_module(_backend_app)

app = _backend_app.app
database = _backend_app.database

# Ensure database tables exist and are properly initialized
try:
    if hasattr(database, "init_db"):
        database.init_db()
    elif hasattr(database, "local_db") and hasattr(database.local_db, "init_db"):
        database.local_db.init_db()
except Exception as e:
    print(f"  [DB] Initialization notice: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 60)
    print("🌾 Agri Gram AI - Smart Farming Assistant")
    print(f"🚀 Server is running on: http://127.0.0.1:{port}")
    print(f"📱 Access the Web App at: http://127.0.0.1:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)
