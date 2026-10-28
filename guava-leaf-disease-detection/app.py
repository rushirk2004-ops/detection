"""
Master Application Entry Point: Guava Agri-AI Multi-Farmer Platform
Supports role-based routing between Multi-Farmer Portal (Sign Up, Sign In,
Personal Dashboard, History, Profile) and Secure Admin Center.
"""
import streamlit as st
import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from components.ui_styles import inject_custom_css
from components.translations import t
from components.farmer_ui import render_farmer_ui
from components.admin_ui import render_admin_ui
from services.authentication import is_farmer_session_valid, is_session_valid

st.set_page_config(
    page_title="Guava Agri-AI | Multi-Farmer Smart Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Inject Custom Color Tokens & Glassmorphism Styling
    inject_custom_css()

    # Meta tags for Mobile Web App & PWA
    st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="theme-color" content="#123D2B">
        <link rel="manifest" href="/static/manifest.json">
        <link rel="apple-touch-icon" href="https://img.icons8.com/color/192/guava.png">
    </head>
    """, unsafe_allow_html=True)

    # Initialize Session States
    if "farmer_session" not in st.session_state:
        st.session_state.farmer_session = None
    if "admin_session" not in st.session_state:
        st.session_state.admin_session = None
    if "global_app_lang" not in st.session_state:
        st.session_state.global_app_lang = "मराठी (Marathi)"

    # Sidebar Header & Branding
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 4px 16px 4px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 68px; height: 68px; background: radial-gradient(circle, rgba(33, 163, 102, 0.3) 0%, rgba(18, 61, 43, 0.9) 100%); border: 2px solid #21A366; border-radius: 50%; box-shadow: 0 0 20px rgba(33, 163, 102, 0.4); margin-bottom: 8px;">
                <span style="font-size: 2.2rem;">🌿</span>
            </div>
            <div style="font-size: 1.45rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF 0%, #D8F36A 50%, #FFC857 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; font-family: 'Plus Jakarta Sans', sans-serif;">
                GUAVA AGRI-AI
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; font-weight: 500; margin-top: 2px;">
                Multi-Farmer Pathology & Crop Advisory
            </div>
            <div style="display: inline-block; margin-top: 6px; background: rgba(33, 163, 102, 0.2); border: 1px solid rgba(216, 243, 106, 0.4); border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; color: #D8F36A; font-weight: 700;">
                v2.5 MULTI-USER PRO
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Global Language Selector Card
        st.markdown("""
        <div class="sidebar-card">
            <div style="font-size: 0.82rem; font-weight: 700; color: #D8F36A; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
                🌐 भाषा / Language
            </div>
        </div>
        """, unsafe_allow_html=True)
        selected_lang = st.selectbox(
            "Select Interface Language",
            ["मराठी (Marathi)", "English"],
            index=0 if "मराठी" in st.session_state.global_app_lang else 1,
            key="sb_language_select",
            label_visibility="collapsed"
        )
        st.session_state.global_app_lang = selected_lang
        is_mr = "मराठी" in selected_lang

        # Navigation Options
        st.markdown(f"""
        <div style="font-size: 0.82rem; font-weight: 700; color: #D8F36A; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 12px; margin-bottom: 6px;">
            🎯 {'दालन निवडा / Navigation' if is_mr else 'Navigation Menu'}
        </div>
        """, unsafe_allow_html=True)

        farmer_active = is_farmer_session_valid(st.session_state.farmer_session)
        
        if farmer_active:
            f_name = st.session_state.farmer_session.get("full_name", "Farmer")
            portal_options = [
                f"🌱 {t('nav_farmer_portal', is_mr)} ({f_name})",
                f"🛡️ {t('nav_admin_portal', is_mr)}"
            ]
        else:
            portal_options = [
                f"🌿 {t('nav_farmer_portal', is_mr)} (लॉगिन / नोंदणी)" if is_mr else f"🌿 {t('nav_farmer_portal', is_mr)} (Sign In / Register)",
                f"🛡️ {t('nav_admin_portal', is_mr)}"
            ]

        portal_choice = st.radio(
            "Navigation Portal",
            portal_options,
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("""
        <div style="margin-top: 12px; margin-bottom: 12px; padding: 8px 12px; background: rgba(33, 163, 102, 0.15); border-left: 3px solid #21A366; border-radius: 6px; font-size: 0.78rem; color: #CBD5E1;">
            ⚡ <strong>Engine:</strong> <span style="color: #D8F36A;">Active</span> (ResNet-50 & EfficientNet-B3)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(33, 163, 102, 0.25); margin: 10px 0;'>", unsafe_allow_html=True)

    # Portal Router
    if "Admin" in portal_choice or "प्रशासकीय" in portal_choice:
        render_admin_ui(default_tab="login")
    else:
        render_farmer_ui()

if __name__ == "__main__":
    main()
