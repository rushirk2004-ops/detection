"""
Farmer Dashboard Component: Guava Agri-AI Platform
Personalized dashboard for authenticated farmers. Provides:
1. Welcome header and personal metrics (Total diagnoses, healthy, diseased, last date)
2. AI Disease Detection with automatic association to farmer_id
3. "My Diagnosis History" with filters (Target, Disease) and safe record deletion
4. Profile viewer & updater, password changer, and secure session logout.
"""
import streamlit as st
import pandas as pd
from PIL import Image
from typing import Dict, Any, Optional

from core.inference import run_disease_inference
from services.disease_service import get_disease_info
from services.database import (
    record_farmer_diagnosis, get_farmer_diagnoses,
    get_farmer_diagnosis_stats, delete_farmer_diagnosis,
    update_farmer_profile, get_farmer_by_id
)
from services.authentication import change_farmer_password
from services.configuration_service import load_settings
from components.translations import t
from components.ui_styles import (
    render_hero, render_metric_cards, render_expert_disclaimer, render_agri_footer
)

def render_farmer_dashboard(farmer_session: Dict[str, Any], is_mr: bool = False):
    """Renders the comprehensive personalized dashboard for an authenticated farmer."""
    farmer_id = farmer_session["farmer_id"]
    
    # Reload fresh profile from database
    farmer_data = get_farmer_by_id(farmer_id) or farmer_session.get("data", {})
    full_name = farmer_data.get("full_name", farmer_session.get("full_name", "Farmer"))
    username = farmer_data.get("username", farmer_session.get("username", ""))

    settings = load_settings()
    uncertainty_threshold = settings.get("inference", {}).get("uncertainty_threshold", 0.60)
    default_model = settings.get("inference", {}).get("default_model", "EfficientNet-B3")

    # ----------------- SIDEBAR FARMER PROFILE WIDGET -----------------
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-card" style="border-left: 4px solid #D8F36A;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #D8F36A; text-transform: uppercase; letter-spacing: 0.5px;">
                👤 {'शेतकरी खाते' if is_mr else 'Authenticated Farmer'}
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-top: 4px;">
                {full_name}
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">
                🆔 <code style="color: #38BDF8; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px;">{farmer_id}</code>
            </div>
            <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 4px;">
                📍 {farmer_data.get('village', '')}, {farmer_data.get('district', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Logout button in sidebar
        if st.button("🚪 " + t("logout_btn", is_mr), key="f_sidebar_logout_btn", use_container_width=True):
            st.session_state.farmer_session = None
            st.success("✅ " + ("लॉगआउट यशस्वी." if is_mr else "Logged out successfully."))
            st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(33, 163, 102, 0.25); margin: 14px 0;'>", unsafe_allow_html=True)

    # ----------------- HERO & METRICS -----------------
    render_hero(farmer_name=full_name, is_mr=is_mr)

    # Fetch personalized stats from database
    p_stats = get_farmer_diagnosis_stats(farmer_id)
    render_metric_cards(
        total_analyses=p_stats["total_diagnoses"],
        healthy_count=p_stats["healthy_samples"],
        diseased_count=p_stats["disease_cases"],
        last_date=p_stats["last_diagnosis_date"],
        is_mr=is_mr
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- DASHBOARD TABS -----------------
    tab_diag, tab_hist, tab_prof = st.tabs([
        f"🔬 {t('nav_diagnosis', is_mr)}",
        f"📜 {t('nav_my_history', is_mr)} ({p_stats['total_diagnoses']})",
        f"👤 {t('nav_profile', is_mr)}"
    ])

    # ==================== TAB 1: AI DISEASE DETECTION ====================
    with tab_diag:
        render_detection_workspace(farmer_id, default_model, uncertainty_threshold, is_mr)

    # ==================== TAB 2: MY DIAGNOSIS HISTORY ====================
    with tab_hist:
        render_farmer_history_view(farmer_id, is_mr)

    # ==================== TAB 3: PROFILE & SECURITY ====================
    with tab_prof:
        render_farmer_profile_view(farmer_data, is_mr)

    render_agri_footer(is_mr=is_mr)

# ----------------------------------------------------------------------------------
# SUB-VIEW: DETECTION WORKSPACE
# ----------------------------------------------------------------------------------
def render_detection_workspace(farmer_id: str, model_name: str, uncertainty_threshold: float, is_mr: bool):
    """Renders the AI disease detection section."""
    col_target, col_info = st.columns([1, 2])
    with col_target:
        target_choice = st.radio(
            "काय तपासणार आहात? / Target" if is_mr else "Analysis Target",
            ["🍃 पान (Leaf Disease)", "🍎 फळ (Fruit Disease)"],
            horizontal=True,
            key="farmer_target_choice_radio"
        )
        target_type = "Leaf" if ("Leaf" in target_choice or "पान" in target_choice) else "Fruit"

    if target_type == "Fruit":
        st.markdown(f"""
        <div class="glass-card" style="border-left: 8px solid #FFC857; background: rgba(40, 20, 15, 0.75);">
            <div style="font-size: 1.25rem; font-weight: 800; color: #FFC857; margin-bottom: 6px;">
                🍎 {'पेरू फळ रोग निदान मॉडेल सध्या संकलनाधीन आहे' if is_mr else 'Guava Fruit Pathology Module is Under Active Dataset Collection'}
            </div>
            <div style="font-size: 0.98rem; color: #CBD5E1; line-height: 1.6;">
                {'सध्या पेरूच्या पानांवरील रोगांचे मॉडेल (खैऱ्या, ठिपके, तांबेरा, ममीफिकेशन) १००% कार्यरत आहे. कृपया वरील <b>🍃 पान (Leaf Disease)</b> निवडून पानाचा फोटो तपासा.'
                if is_mr else
                'The guava foliage pathology neural network is 100% active and trained on 4,598 images. Please switch to <b>Leaf Disease</b> above to analyze leaf foliage.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-card-title">
                <span>📸</span> {'पानाचा फोटो द्या' if is_mr else 'Provide Guava Leaf Image'}
            </div>
            <p style="color: #94A3B8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 14px;">
                {'स्पष्ट, जवळून काढलेला फोटो अपलोड करा किंवा थेट कॅमेऱ्याने काढा.' if is_mr else 'Upload from phone/PC gallery or capture directly using camera.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        input_mode = st.radio(
            "Input Mode",
            [f"📁 {t('upload_option', is_mr)}", f"📸 {t('camera_option', is_mr)}"],
            horizontal=True,
            key="auth_farmer_input_mode"
        )

        uploaded_file = None
        if "Camera" in input_mode or "कॅमेरा" in input_mode:
            uploaded_file = st.camera_input("कॅमेऱ्याने फोटो काढा" if is_mr else "Capture Leaf Photo", key="auth_camera_in")
        else:
            uploaded_file = st.file_uploader(
                "गॅलरीतून फोटो निवडा..." if is_mr else "Choose leaf image...",
                type=["jpg", "jpeg", "png"],
                key="auth_file_uploader",
                help="Supported file extensions: .jpg, .jpeg, .png"
            )

        pil_img = None
        file_valid = False
        if uploaded_file is not None:
            try:
                pil_img = Image.open(uploaded_file)
                file_valid = True
                w, h = pil_img.size
                st.markdown(f"""
                <div style="background: rgba(18, 61, 43, 0.5); border: 1px solid rgba(33, 163, 102, 0.4); border-radius: 12px; padding: 10px 16px; margin: 10px 0; display: flex; justify-content: space-between; font-size: 0.85rem; color: #CBD5E1;">
                    <span>🖼️ <strong>{'नमुना' if is_mr else 'File'}:</strong> {getattr(uploaded_file, 'name', 'camera.jpg')}</span>
                    <span>📐 <strong>{'रिझोल्यूशन' if is_mr else 'Size'}:</strong> {w} × {h} px</span>
                </div>
                """, unsafe_allow_html=True)
                st.image(pil_img, caption="निवडलेला नमुना" if is_mr else "Selected Leaf Sample", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")

        analyze_clicked = False
        if file_valid and pil_img is not None:
            analyze_clicked = st.button(t("analyze_btn", is_mr), use_container_width=True, type="primary", key="auth_analyze_btn")

    with col_result:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-card-title">
                <span>📋</span> {'निदान आणि कृषी अहवाल' if is_mr else 'AI Diagnosis & Remedial Report'}
            </div>
            <p style="color: #94A3B8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 14px;">
                {'खोल न्यूरल नेटवर्क विश्लेषण आणि अचूक उपाययोजना' if is_mr else 'Deep Learning Foliage Pathology & Grad-CAM Heatmap'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        current_file_id = getattr(uploaded_file, 'name', None) or (f"cam_{uploaded_file.size}" if uploaded_file else None)

        if uploaded_file is None or pil_img is None:
            guide_title = "👈 अचूक निदानासाठी मार्गदर्शक सूचना" if is_mr else "👈 Guidelines for Best Diagnosis"
            g1 = "पेरूच्या झाडावरील रोगट किंवा संशयास्पद पानाचा जवळून स्वच्छ फोटो काढा." if is_mr else "Capture a clear close-up of the suspected diseased leaf."
            g2 = "चांगल्या सूर्यप्रकाशात फोटो काढा, सावली किंवा जास्त चमक टाळा." if is_mr else "Photograph under natural daylight; avoid blur and harsh glares."
            g3 = "फोटो निवडल्यानंतर हिरव्या 'Analyze Foliage Now' बटनावर क्लिक करा." if is_mr else "Click the green 'Analyze Foliage Now' button to run AI classification."
            st.markdown(f"""
            <div class="glass-card" style="border: 1px dashed rgba(33, 163, 102, 0.5); padding: 22px;">
                <div style="font-size: 1.12rem; font-weight: 700; color: #D8F36A; margin-bottom: 10px;">{guide_title}</div>
                <div style="margin-bottom: 8px; color: #CBD5E1; font-size: 0.92rem;">• {g1}</div>
                <div style="margin-bottom: 8px; color: #CBD5E1; font-size: 0.92rem;">• {g2}</div>
                <div style="margin-bottom: 8px; color: #CBD5E1; font-size: 0.92rem;">• {g3}</div>
                <div style="margin-top: 16px; padding: 10px 14px; background: rgba(33, 163, 102, 0.15); border-radius: 8px; font-size: 0.85rem; color: #D8F36A;">
                    🌿 <strong>{'कार्यरत मॉडेल' if is_mr else 'Active Model'}:</strong> {model_name} (ResNet-50 / EfficientNet-B3 Engine)
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

        should_run = analyze_clicked or (
            st.session_state.get(f"cached_fid_{farmer_id}") == current_file_id and f"cached_res_{farmer_id}" in st.session_state
        )

        if not should_run:
            st.info("👉 " + ("फोटो तयार आहे. निदानासाठी डाव्या बाजूला <b>'पानाचे विश्लेषण करा'</b> वर क्लिक करा." if is_mr else "Photo ready. Click the green <b>'Analyze Foliage Now'</b> button on the left to start AI diagnosis."))
            return

        if analyze_clicked or (st.session_state.get(f"cached_fid_{farmer_id}") != current_file_id):
            with st.spinner("🧠 AI मॉडेल पानाचे सखोल विश्लेषण करत आहे..." if is_mr else "🧠 Deep Neural Network analyzing leaf pathology..."):
                inference_result = run_disease_inference(
                    image_source=pil_img,
                    target_type="Leaf",
                    model_name=model_name,
                    uncertainty_threshold=uncertainty_threshold,
                    generate_gradcam=True
                )
                st.session_state[f"cached_res_{farmer_id}"] = inference_result
                st.session_state[f"cached_fid_{farmer_id}"] = current_file_id

                # Save diagnosis to database associated with this farmer!
                if inference_result.get("success", False):
                    try:
                        raw_bytes = uploaded_file.getvalue()
                        fname = getattr(uploaded_file, "name", "leaf_scan.jpg")
                        p_class = inference_result["predicted_class"]
                        conf_val = inference_result["confidence"]
                        lat_val = inference_result.get("latency_ms", 0.0)
                        is_unc = inference_result.get("is_uncertain", False)
                        
                        d_info = get_disease_info(p_class)
                        summary_treat = d_info.get("causes_en", "") + " | " + "; ".join(d_info.get("chemical_control_en", [])[:2])

                        record_farmer_diagnosis(
                            farmer_id=farmer_id,
                            target_type="Leaf",
                            predicted_disease=p_class,
                            confidence_score=conf_val,
                            model_name=model_name,
                            latency_ms=lat_val,
                            is_uncertain=is_unc,
                            treatment_recommendations=summary_treat,
                            image_bytes=raw_bytes,
                            filename=fname
                        )
                    except Exception as save_err:
                        pass
        else:
            inference_result = st.session_state[f"cached_res_{farmer_id}"]

        if not inference_result.get("success", False):
            msg = inference_result.get("message_mr") if (is_mr and inference_result.get("message_mr")) else inference_result.get("message", "Analysis failed")
            st.error(f"❌ {msg}")
            return

        pred_class = inference_result["predicted_class"]
        confidence_pct = inference_result["confidence_pct"]
        is_uncertain = inference_result["is_uncertain"]
        probabilities = inference_result["probabilities"]
        gradcam_vis = inference_result.get("gradcam_vis")
        latency = inference_result.get("latency_ms", 0.0)

        info = get_disease_info(pred_class)
        disease_name = info["name_mr"] if is_mr else info["name_en"]
        is_healthy = (pred_class == "Healthy")

        card_class = "result-card-healthy" if is_healthy else "result-card-disease"
        status_color = "#D8F36A" if is_healthy else ("#FFA500" if is_uncertain else "#EF4444")
        status_title = "निरोगी पान (Healthy)" if is_healthy else ("रोग आढळला (Disease Detected)" if is_mr else "Disease Detected")

        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #D8F36A; text-transform: uppercase; letter-spacing: 0.5px;">
                        {'रोग निदान निष्कर्ष' if is_mr else 'AI Pathology Classification'}
                    </div>
                    <div class="result-title">
                        {info['icon']} {disease_name}
                    </div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.45); border: 1px solid {status_color}; border-radius: 30px; padding: 6px 16px; font-weight: 700; color: {status_color}; font-size: 0.95rem;">
                    ● {status_title}
                </div>
            </div>
            
            <div style="margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #CBD5E1; margin-bottom: 4px;">
                    <span>{'विश्वासार्हता (Confidence Score)' if is_mr else 'Confidence Score'}</span>
                    <strong style="color: #38BDF8;">{confidence_pct:.2f}%</strong>
                </div>
                <div style="width: 100%; height: 10px; background: rgba(0,0,0,0.5); border-radius: 5px; overflow: hidden;">
                    <div style="width: {confidence_pct}%; height: 100%; background: linear-gradient(90deg, #21A366 0%, #D8F36A 70%, #FFC857 100%);"></div>
                </div>
            </div>

            <div style="margin-top: 12px; display: flex; flex-wrap: wrap;">
                <span class="result-meta-chip">🤖 {model_name}</span>
                <span class="result-meta-chip">⚡ {latency:.1f} ms</span>
                <span class="result-meta-chip">🎯 {'तीव्रता' if is_mr else 'Severity'}: {info.get('severity', 'Moderate')}</span>
                <span class="result-meta-chip">💾 {'इतिहासात जतन केले' if is_mr else 'Saved to Profile History'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_uncertain:
            st.warning(
                f"⚠️ **{'कमी आत्मविश्वास / अस्पष्ट फोटो' if is_mr else 'Low Confidence Warning'} ({confidence_pct:.1f}%)**\n\n"
                f"{'मॉडेलचा विश्वास ' + str(int(uncertainty_threshold*100)) + '% पेक्षा कमी आहे. कृपया चांगल्या सूर्यप्रकाशात पानाचा स्पष्ट व जवळून फोटो काढून पुन्हा तपासा.' if is_mr else 'Confidence is below the safety threshold. Please capture a clearer close-up under natural light.'}"
            )

        if gradcam_vis is not None:
            st.markdown(f"""
            <div class="glass-card">
                <div class="glass-card-title">
                    <span>🔬</span> {'AI उष्णता नकाशा (Grad-CAM Explainability)' if is_mr else 'AI Explainability Heatmap (Grad-CAM)'}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.image(gradcam_vis, caption="Grad-CAM Layer Activation Map", use_container_width=True)

        with st.expander("📊 " + ("सर्व रोगांची संभाव्यता (Probability Breakdown)" if is_mr else "All Class Probabilities")):
            for c_name, prob in probabilities.items():
                c_info = get_disease_info(c_name)
                display_c = c_info["name_mr"] if is_mr else c_name
                st.write(f"**{display_c}**: {prob*100:.2f}%")
                st.progress(min(max(float(prob), 0.0), 1.0))

        # Treatments
        st.markdown(f"""
        <div class="glass-card" style="margin-top: 20px;">
            <div class="glass-card-title">
                <span>🌾</span> {'तज्ज्ञ कृषी सल्ला व उपाययोजना' if is_mr else 'Expert Agricultural Advisory & Treatment Guide'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        t_sym, t_chem, t_org, t_prev = st.tabs([
            "🔍 लक्षणे (Symptoms)" if is_mr else "🔍 Symptoms",
            "💊 रासायनिक फवारणी (Chemical)" if is_mr else "💊 Chemical Spray",
            "🌿 सेंद्रिय/जैविक (Organic)" if is_mr else "🌿 Organic / Bio",
            "🛡️ प्रतिबंधात्मक काळजी (Prevention)" if is_mr else "🛡️ Prevention"
        ])

        with t_sym:
            symptoms = info["symptoms_mr"] if is_mr else info["symptoms_en"]
            cause = info["causes_mr"] if is_mr else info["causes_en"]
            st.markdown(f"""
            <div style="background: rgba(18, 61, 43, 0.7); border: 1px solid rgba(33, 163, 102, 0.4); padding: 12px 16px; border-radius: 10px; margin-bottom: 12px;">
                <span style="color: #94A3B8;">{'रोगकारक बुरशी/जीवाणू' if is_mr else 'Causal Organism'}:</span>
                <span style="color: #D8F36A; font-weight: 700; margin-left: 6px;">{cause}</span>
            </div>
            """, unsafe_allow_html=True)
            for s in symptoms:
                st.markdown(f"""<div class="treatment-item" style="border-left: 5px solid #38BDF8;"><span style="color: #F8FAFC; font-weight: 600;">🔍 {s}</span></div>""", unsafe_allow_html=True)

        with t_chem:
            for step in (info["chemical_control_mr"] if is_mr else info["chemical_control_en"]):
                st.markdown(f"""<div class="treatment-item" style="border-left: 5px solid #EF4444;"><span style="color: #F8FAFC; font-weight: 600;">💊 {step}</span></div>""", unsafe_allow_html=True)

        with t_org:
            for step in (info["organic_remedies_mr"] if is_mr else info["organic_remedies_en"]):
                st.markdown(f"""<div class="treatment-item" style="border-left: 5px solid #21A366;"><span style="color: #F8FAFC; font-weight: 600;">🌿 {step}</span></div>""", unsafe_allow_html=True)

        with t_prev:
            for step in (info["prevention_mr"] if is_mr else info["prevention_en"]):
                st.markdown(f"""<div class="treatment-item" style="border-left: 5px solid #FFC857;"><span style="color: #F8FAFC; font-weight: 600;">🛡️ {step}</span></div>""", unsafe_allow_html=True)

        render_expert_disclaimer(is_mr=is_mr)

# ----------------------------------------------------------------------------------
# SUB-VIEW: MY DIAGNOSIS HISTORY
# ----------------------------------------------------------------------------------
def render_farmer_history_view(farmer_id: str, is_mr: bool):
    """Renders private diagnosis records with filters and deletion."""
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-card-title">
            <span>📜</span> {t('history_title', is_mr)}
        </div>
        <p style="color: #94A3B8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 0px;">
            {t('history_subtitle', is_mr)}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
    with f_col1:
        target_f = st.selectbox(
            t("filter_target", is_mr),
            ["All", "Leaf", "Fruit"] if not is_mr else ["सर्व (All)", "Leaf (पान)", "Fruit (फळ)"],
            key="hist_filter_target"
        )
        clean_target = "all" if "all" in target_f.lower() or "सर्व" in target_f else ("Leaf" if "leaf" in target_f.lower() or "पान" in target_f else "Fruit")

    with f_col2:
        disease_options = ["All", "Canker", "Dot", "Healthy", "Mummification", "Rust"] if not is_mr else ["सर्व (All)", "Canker", "Dot", "Healthy", "Mummification", "Rust"]
        disease_f = st.selectbox(t("filter_disease", is_mr), disease_options, key="hist_filter_disease")
        clean_disease = "all" if "all" in disease_f.lower() or "सर्व" in disease_f else disease_f

    records = get_farmer_diagnoses(
        farmer_id=farmer_id,
        target_filter=clean_target,
        disease_filter=clean_disease,
        limit=50
    )

    if not records:
        st.info("ℹ️ " + ("या निकषांसाठी कोणतीही तपासणी नोंद आढळली नाही." if is_mr else "No diagnosis records found matching your filters."))
        return

    st.markdown(f"**{'एकूण नोंदी' if is_mr else 'Found Records'}:** `{len(records)}`")

    for rec in records:
        diag_id = rec["diagnosis_id"]
        d_name = rec["predicted_disease"]
        conf = rec["confidence_score"] * 100.0
        d_date = rec["diagnosis_date"]
        t_type = rec["target_type"]
        img_p = rec.get("image_path")

        d_info = get_disease_info(d_name)
        display_name = d_info["name_mr"] if is_mr else d_info["name_en"]
        badge_c = "#D8F36A" if d_name == "Healthy" else "#FFC857"

        with st.expander(f"🌿 {d_date} — {display_name} ({conf:.1f}%)", expanded=False):
            exp_col1, exp_col2 = st.columns([1, 2])
            with exp_col1:
                if img_p and os.path.exists(img_p):
                    try:
                        st.image(img_p, caption=f"Scan #{diag_id}", use_container_width=True)
                    except Exception:
                        st.caption("Image file")
                else:
                    st.caption("🔒 Stored in-memory only")
            with exp_col2:
                st.write(f"- **Target:** {t_type}")
                st.write(f"- **AI Model:** {rec.get('model_name', 'ResNet-50')}")
                st.write(f"- **Confidence:** {conf:.2f}%")
                st.write(f"- **Diagnosis Date:** {d_date}")
                if rec.get("treatment_recommendations"):
                    st.info(f"🌾 **Advisory Summary:** {rec['treatment_recommendations']}")

                if st.button(f"🗑️ {t('delete_record_btn', is_mr)}", key=f"del_rec_{diag_id}"):
                    if delete_farmer_diagnosis(diag_id, farmer_id):
                        st.success(t("record_deleted", is_mr))
                        st.rerun()
                    else:
                        st.error("Failed to delete record.")

# ----------------------------------------------------------------------------------
# SUB-VIEW: PROFILE & SECURITY
# ----------------------------------------------------------------------------------
def render_farmer_profile_view(farmer_data: Dict[str, Any], is_mr: bool):
    """Renders profile inspection, profile editing, and password update forms."""
    farmer_id = farmer_data.get("farmer_id", "")
    
    col_p1, col_p2 = st.columns([1, 1], gap="large")

    with col_p1:
        st.markdown(f"#### 👤 {t('profile_header', is_mr)}")
        with st.form("edit_profile_form"):
            fn = st.text_input(t("full_name", is_mr), value=farmer_data.get("full_name", ""), key="ep_fn")
            mob = st.text_input(t("mobile_number", is_mr), value=farmer_data.get("mobile_number", ""), key="ep_mob")
            em = st.text_input(t("email_optional", is_mr), value=farmer_data.get("email") or "", key="ep_em")
            vil = st.text_input(t("village", is_mr), value=farmer_data.get("village", ""), key="ep_vil")
            tal = st.text_input(t("taluka", is_mr), value=farmer_data.get("taluka", ""), key="ep_tal")
            dist = st.text_input(t("district", is_mr), value=farmer_data.get("district", ""), key="ep_dist")
            st_val = st.text_input(t("state", is_mr), value=farmer_data.get("state", "Maharashtra"), key="ep_st")

            save_btn = st.form_submit_button(t("update_profile_btn", is_mr), use_container_width=True, type="primary")
            if save_btn:
                ok, msg = update_farmer_profile(farmer_id, fn, mob, em, vil, tal, dist, st_val)
                if ok:
                    st.success("✅ " + ("प्रोफाइल माहिती यशस्वीरित्या अद्ययावत केली!" if is_mr else "Profile updated successfully!"))
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    with col_p2:
        st.markdown(f"#### 🔒 {t('change_password_header', is_mr)}")
        with st.form("change_pwd_form"):
            curr_p = st.text_input(t("current_password", is_mr), type="password", key="cp_curr")
            new_p = st.text_input(t("new_password", is_mr), type="password", key="cp_new")
            conf_p = st.text_input(t("confirm_new_password", is_mr), type="password", key="cp_conf")

            pwd_btn = st.form_submit_button(t("update_password_btn", is_mr), use_container_width=True)
            if pwd_btn:
                ok, msg = change_farmer_password(farmer_id, curr_p, new_p, conf_p)
                if ok:
                    st.success("✅ " + ("पासवर्ड यशस्वीरित्या बदलला!" if is_mr else "Password changed successfully!"))
                else:
                    st.error(f"❌ {msg}")

        # Account Details summary card
        st.markdown(f"""
        <div style="background: rgba(18, 61, 43, 0.4); border: 1px solid rgba(33, 163, 102, 0.3); border-radius: 12px; padding: 14px 18px; margin-top: 18px; font-size: 0.88rem; color: #CBD5E1;">
            <div><strong>Farmer ID:</strong> <span style="color: #D8F36A;">{farmer_id}</span></div>
            <div><strong>Username:</strong> {farmer_data.get('username')}</div>
            <div><strong>Registered On:</strong> {farmer_data.get('created_at')}</div>
            <div><strong>Account Status:</strong> <span style="color: #21A366; font-weight: 700;">Active</span></div>
        </div>
        """, unsafe_allow_html=True)
