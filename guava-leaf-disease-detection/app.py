"""
Master Application Entry Point: Guava Leaf & Fruit Disease Detection System
Supports role-based routing between Farmer / User Panel and Secure Admin Panel
with rich agricultural styling, glassmorphism components, and bilingual support.
"""
import streamlit as st
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from components.ui_styles import inject_custom_css
from components.farmer_ui import render_farmer_ui
from components.admin_ui import render_admin_ui

st.set_page_config(
    page_title="Guava Agri-AI | Smart Disease Detection Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Inject Global Custom CSS Theme & Fonts
    inject_custom_css()

    # Inject PWA & Mobile Web App meta tags
    st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="theme-color" content="#062b1e">
        <link rel="manifest" href="/static/manifest.json">
        <link rel="apple-touch-icon" href="https://img.icons8.com/color/192/guava.png">
    </head>
    """, unsafe_allow_html=True)

    # Sidebar Header Branding
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 12px 6px 18px 6px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 68px; height: 68px; background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(2, 44, 34, 0.8) 100%); border: 2px solid #10b981; border-radius: 50%; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); margin-bottom: 10px;">
                <span style="font-size: 2.2rem;">🌿</span>
            </div>
            <div style="font-size: 1.45rem; font-weight: 800; background: linear-gradient(90deg, #ecfdf5 0%, #a7f3d0 50%, #fef08a 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; font-family: 'Plus Jakarta Sans', sans-serif;">
                GUAVA AGRI-AI
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; font-weight: 500; margin-top: 2px;">
                Smart Foliage Health & Pathology
            </div>
            <div style="display: inline-block; margin-top: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; color: #6ee7b7; font-weight: 700;">
                v2.4 PRO CAPSTONE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size: 0.85rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
            🎯 Navigation / दालन निवडा
        </div>
        """, unsafe_allow_html=True)

        portal_choice = st.radio(
            "Navigation Menu",
            ["🌿 Farmer / User Portal", "🛡️ Admin Sign In", "📝 Admin Sign Up"],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 12px; padding: 8px 12px; background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; border-radius: 6px; font-size: 0.78rem; color: #cbd5e1;">
            ⚡ <strong>Engine Status:</strong> <span style="color: #4ade80;">Active</span> (PyTorch & CUDA/CPU)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(16, 185, 129, 0.2); margin: 12px 0 16px 0;'>", unsafe_allow_html=True)

    # Portal Router
    if "Farmer" in portal_choice:
        render_farmer_ui()
    elif "Sign Up" in portal_choice:
        render_admin_ui(default_tab="signup")
    else:
        render_admin_ui(default_tab="login")

if __name__ == "__main__":
    main()
