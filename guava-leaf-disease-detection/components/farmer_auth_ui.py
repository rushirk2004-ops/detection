"""
Farmer Authentication UI Component: Guava Agri-AI Platform
Renders beautiful, accessible Farmer Sign In and Farmer Registration forms
with client-side & server-side validation, password visibility toggle,
and Marathi / English localization.
"""
import streamlit as st
from typing import Dict, Any, Optional

from services.authentication import register_farmer_account, authenticate_farmer, create_farmer_session
from components.translations import t
from components.ui_styles import render_agri_footer

def render_farmer_auth_portal(default_mode: str = "signin", is_mr: bool = False):
    """Renders the combined Farmer Authentication Portal (Sign In / Sign Up)."""
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown(f"""
        <div style="background: rgba(18, 61, 43, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(33, 163, 102, 0.4); border-radius: 20px; padding: 26px 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); text-align: center; margin-top: 10px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background: rgba(33, 163, 102, 0.25); border: 2px solid #21A366; border-radius: 50%; box-shadow: 0 0 20px rgba(33, 163, 102, 0.4); margin-bottom: 12px;">
                <span style="font-size: 2rem;">🌱</span>
            </div>
            <h2 style="color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin-bottom: 4px; font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;">
                {'शेतकरी प्रवेश दालन' if is_mr else 'Farmer Access Portal'}
            </h2>
            <p style="color: #D8F36A; font-size: 0.95rem; margin-bottom: 0px;">
                {'वैयक्तिक पेरू रोग निदान व कृषी मार्गदर्शन' if is_mr else 'Personalized Foliage Disease Diagnosis & Crop Protection'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # High-contrast tabs for instant switching between Sign In and Sign Up
        auth_mode = st.radio(
            "Select Farmer Portal Action",
            [
                f"🔑 {t('nav_sign_in', is_mr)}",
                f"📝 {t('nav_sign_up', is_mr)}"
            ],
            index=1 if default_mode == "signup" else 0,
            horizontal=True,
            key="farmer_auth_choice_radio",
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if "Sign Up" in auth_mode or "नोंदणी" in auth_mode:
            render_farmer_signup_form(is_mr=is_mr)
        else:
            render_farmer_login_form(is_mr=is_mr)

    render_agri_footer(is_mr=is_mr)

def render_farmer_login_form(is_mr: bool = False):
    """Renders the secure login form for farmers."""
    with st.form("farmer_login_form"):
        st.markdown(f"#### 🔐 {t('login_title', is_mr)}")
        st.caption(t('login_subtitle', is_mr))

        username = st.text_input(
            t('username', is_mr),
            placeholder="e.g. rushi_patil" if not is_mr else "उदा. rushi_patil",
            key="f_login_user"
        )

        show_pwd = st.checkbox("👁️ " + ("पासवर्ड दाखवा" if is_mr else "Show Password"), key="f_login_show_pwd")
        password = st.text_input(
            t('password', is_mr),
            type="default" if show_pwd else "password",
            placeholder="••••••••",
            key="f_login_pass"
        )

        submit = st.form_submit_button(t('login_submit_btn', is_mr), use_container_width=True, type="primary")

        if submit:
            if not username or not password:
                st.error("⚠️ " + ("कृपया युझरनेम आणि पासवर्ड दोन्ही भरा." if is_mr else "Please enter both username and password."))
            else:
                success, msg, farmer_data = authenticate_farmer(username, password)
                if success and farmer_data:
                    st.session_state.farmer_session = create_farmer_session(farmer_data)
                    st.success("✅ " + ("लॉगिन यशस्वी! आपले स्वागत आहे..." if is_mr else "Login successful! Welcome..."))
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    st.info("💡 " + t('dont_have_account', is_mr))

def render_farmer_signup_form(is_mr: bool = False):
    """Renders the comprehensive registration form for new farmers."""
    with st.form("farmer_signup_form"):
        st.markdown(f"#### 📝 {t('reg_title', is_mr)}")
        st.caption(t('reg_subtitle', is_mr))

        col_a, col_b = st.columns(2)
        with col_a:
            full_name = st.text_input(
                f"{t('full_name', is_mr)} *",
                placeholder="e.g. Rushi Patil" if not is_mr else "उदा. ऋषी पाटील",
                key="reg_fn"
            )
            username = st.text_input(
                f"{t('username', is_mr)} *",
                placeholder="e.g. rushi_patil" if not is_mr else "उदा. rushi_patil",
                help="Unique username (letters, numbers, underscore only)",
                key="reg_un"
            )
            mobile = st.text_input(
                f"{t('mobile_number', is_mr)} *",
                placeholder="e.g. 9876543210",
                key="reg_mob"
            )
            email = st.text_input(
                t('email_optional', is_mr),
                placeholder="e.g. farmer@example.com",
                key="reg_em"
            )

        with col_b:
            village = st.text_input(
                f"{t('village', is_mr)} *",
                placeholder="e.g. Baramati" if not is_mr else "उदा. बारामती",
                key="reg_vil"
            )
            taluka = st.text_input(
                f"{t('taluka', is_mr)} *",
                placeholder="e.g. Baramati" if not is_mr else "उदा. बारामती",
                key="reg_tal"
            )
            district = st.text_input(
                f"{t('district', is_mr)} *",
                placeholder="e.g. Pune" if not is_mr else "उदा. पुणे",
                key="reg_dist"
            )
            state = st.text_input(
                f"{t('state', is_mr)} *",
                value="Maharashtra",
                key="reg_st"
            )

        st.markdown("---")
        show_reg_pwd = st.checkbox("👁️ " + ("पासवर्ड दाखवा" if is_mr else "Show Passwords"), key="f_reg_show_pwd")
        p_type = "default" if show_reg_pwd else "password"
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            password = st.text_input(f"{t('password', is_mr)} *", type=p_type, placeholder="Min 6 characters", key="reg_p1")
        with col_p2:
            confirm = st.text_input(f"{t('confirm_password', is_mr)} *", type=p_type, placeholder="Re-enter password", key="reg_p2")

        signup_btn = st.form_submit_button(t('register_submit_btn', is_mr), use_container_width=True, type="primary")

        if signup_btn:
            ok, msg, f_id = register_farmer_account(
                full_name=full_name,
                username=username,
                mobile_number=mobile,
                email=email,
                village=village,
                taluka=taluka,
                district=district,
                state=state,
                password=password,
                confirm_password=confirm
            )
            if ok:
                st.success(f"🎉 {'नोंदणी यशस्वी!' if is_mr else 'Registration Successful!'} " + 
                           (f"तुमचा शेतकरी आयडी: **{f_id}**." if is_mr else f"Your Farmer ID is: **{f_id}**."))
                st.info("👉 " + ("आता वर 'शेतकरी लॉगिन' पर्याय निवडून आपल्या खात्यात प्रवेश करा." if is_mr else "Please switch to 'Farmer Sign In' above to log into your new account."))
            else:
                st.error(f"❌ {msg}")

    st.caption("ℹ️ " + t('already_have_account', is_mr))
