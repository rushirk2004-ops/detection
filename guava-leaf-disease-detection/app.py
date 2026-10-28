"""
Master Application Entry Point: Guava Leaf & Fruit Disease Detection System
Supports role-based routing between Farmer / User Panel and Secure Admin Panel.
"""
import streamlit as st
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from components.farmer_ui import render_farmer_ui
from components.admin_ui import render_admin_ui

st.set_page_config(
    page_title="Guava Disease Detection System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Inject PWA & Mobile Web App meta tags
    st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="theme-color" content="#1b4332">
        <link rel="manifest" href="/static/manifest.json">
        <link rel="apple-touch-icon" href="https://img.icons8.com/color/192/guava.png">
    </head>
    """, unsafe_allow_html=True)

    # Role Selection in Sidebar
    st.sidebar.markdown("## 🌿 Guava Agri-AI System")
    portal_choice = st.sidebar.radio(
        "Select Portal / पोर्टल निवडा",
        ["🌿 Farmer / User Portal", "🛡️ Admin Sign In", "📝 Admin Sign Up"],
        index=0
    )
    st.sidebar.markdown("---")

    if "Farmer" in portal_choice:
        render_farmer_ui()
    elif "Sign Up" in portal_choice:
        render_admin_ui(default_tab="signup")
    else:
        render_admin_ui(default_tab="login")

if __name__ == "__main__":
    main()
