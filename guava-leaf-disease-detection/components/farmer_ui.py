"""
Farmer UI Router Component: Guava Agri-AI Multi-Farmer Platform
Routes between Farmer Authentication (Sign In / Sign Up) and the authenticated
Farmer Dashboard (AI Disease Detection, Personal History, and Profile Settings).
"""
import streamlit as st

from services.authentication import is_farmer_session_valid
from components.farmer_auth_ui import render_farmer_auth_portal
from components.farmer_dashboard import render_farmer_dashboard

def render_farmer_ui():
    """Renders the appropriate farmer view based on authentication session state."""
    # Read interface language
    lang = st.session_state.get("global_app_lang", "मराठी (Marathi)")
    is_mr = "मराठी" in lang

    # Initialize farmer session container if not present
    if "farmer_session" not in st.session_state:
        st.session_state.farmer_session = None

    # Check if a farmer is securely authenticated
    if is_farmer_session_valid(st.session_state.farmer_session):
        render_farmer_dashboard(st.session_state.farmer_session, is_mr=is_mr)
    else:
        auth_mode = st.session_state.get("farmer_auth_initial_tab", "signin")
        render_farmer_auth_portal(default_mode=auth_mode, is_mr=is_mr)
