"""
Compatibility wrapper for legacy path: app/streamlit_app.py
Redirects directly to the main modular app.
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import main

if __name__ == "__main__":
    main()
