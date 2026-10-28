"""
Farmer / User Panel Component: Guava Agri-AI System
Modern, colorful, responsive agricultural AI dashboard with glassmorphism styling,
dual-language support (English & Marathi), ResNet-50 / EfficientNet-B3 inference,
Grad-CAM explainable AI visualizations, real database metrics, and expert treatment guides.
"""
import streamlit as st
import pandas as pd
from PIL import Image
from typing import Dict, Any, Optional

from core.inference import run_disease_inference
from services.disease_service import get_disease_info, DISEASE_KNOWLEDGE_BASE
from services.history_service import record_prediction, get_prediction_history, get_summary_statistics
from services.configuration_service import load_settings
from components.ui_styles import render_hero, render_metric_cards, render_expert_disclaimer, render_agri_footer

def render_farmer_ui():
    """Renders the comprehensive Farmer / User disease detection dashboard."""
    settings = load_settings()
    uncertainty_threshold = settings.get("inference", {}).get("uncertainty_threshold", 0.60)

    # ----------------- SIDEBAR CONTROLS -----------------
    with st.sidebar:
        # Language Selector Card
        st.markdown("""
        <div class="sidebar-card">
            <div style="font-size: 0.85rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                🌐 भाषा / Language
            </div>
        </div>
        """, unsafe_allow_html=True)
        lang = st.selectbox(
            "Select Interface Language",
            ["मराठी (Marathi)", "English"],
            index=0,
            key="farmer_lang",
            label_visibility="collapsed"
        )
        is_mr = "मराठी" in lang

        # Analysis Target Card
        target_label = "🎯 तपासणी प्रकार / Target" if is_mr else "🎯 Analysis Target"
        st.markdown(f"""
        <div class="sidebar-card" style="margin-top: 10px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                {target_label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        target_choice = st.radio(
            "Analysis Target Selection",
            ["🍃 पान (Leaf Disease)", "🍎 फळ (Fruit Disease)"],
            index=0,
            label_visibility="collapsed"
        )
        target_type = "Leaf" if ("Leaf" in target_choice or "पान" in target_choice) else "Fruit"

        # Automatic High-Performance AI Model Selection
        clean_model_name = settings.get("inference", {}).get("default_model", "EfficientNet-B3")

        # Data Privacy Card
        st.markdown(f"""
        <div class="sidebar-card" style="margin-top: 10px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                🔒 {'डेटा गोपनीयता' if is_mr else 'Data Privacy'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        opt_in_history = st.checkbox(
            "माझा फोटो इतिहासात जतन करा" if is_mr else "Opt-in: Save image to local history",
            value=False,
            help="Your photo is processed strictly in-memory by default. Check only if you wish to record it in local history."
        )

        # Quick Agri-Tip Card
        tip_text = (
            "🌾 <strong>शेती सल्ला:</strong> पानांवर सकाळी जास्त दव किंवा पाण्याचे थेंब असताना बुरशीनाशक फवारणी टाळावी. दुपारच्या उन्हात फवारणी करू नये."
            if is_mr else
            "🌾 <strong>Agri-Tip:</strong> Avoid foliar spraying during high midday heat or heavy leaf wetness to prevent chemical wash-off and leaf scorch."
        )
        st.markdown(f"""
        <div style="margin-top: 14px; padding: 12px 14px; background: rgba(245, 158, 11, 0.12); border-left: 3px solid #f59e0b; border-radius: 8px; font-size: 0.82rem; color: #fde68a; line-height: 1.5;">
            {tip_text}
        </div>
        """, unsafe_allow_html=True)

    # ----------------- MAIN DASHBOARD -----------------
    # 1. Hero Section
    render_hero(is_mr=is_mr)

    # 2. Live Metric Cards from Database
    stats = get_summary_statistics()
    total_q = stats.get("total_queries", 0)
    dist = stats.get("distribution", {})
    healthy_q = dist.get("Healthy", 0)
    diseased_q = total_q - healthy_q if total_q >= healthy_q else 0

    render_metric_cards(
        total_analyses=total_q,
        healthy_count=healthy_q,
        diseased_count=diseased_q,
        accuracy_pct=96.26 if clean_model_name == "EfficientNet-B3" else 90.95,
        is_mr=is_mr
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Fruit Target Warning (if chosen)
    if target_type == "Fruit":
        st.markdown(f"""
        <div class="glass-card" style="border-left: 8px solid #f59e0b; background: rgba(69, 26, 3, 0.7);">
            <div style="font-size: 1.3rem; font-weight: 800; color: #fde68a; margin-bottom: 8px;">
                🍎 {'पेरू फळ रोग निदान मॉडेल सध्या संकलनाधीन आहे' if is_mr else 'Guava Fruit Disease Module is Under Active Dataset Collection'}
            </div>
            <div style="font-size: 1.02rem; color: #fed7aa; line-height: 1.6;">
                {'सध्या पेरूच्या पानांवरील रोगांचे मॉडेल (खैऱ्या, ठिपके, तांबेरा, ममीफिकेशन) १००% प्रशिक्षित व कार्यरत आहे. कृपया डाव्या बाजूला <b>🍃 पान (Leaf Disease)</b> निवडा.'
                if is_mr else
                'The guava foliage pathology neural networks (Canker, Dot, Rust, Mummification, Healthy) are fully trained and active. Please select <b>Leaf Disease</b> in the sidebar to run analysis.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_agri_footer(is_mr=is_mr)
        return

    # ----------------- WORKSPACE: UPLOAD & DIAGNOSIS -----------------
    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-card-title">
                <span>📸</span> {'पानाचा फोटो अपलोड करा' if is_mr else 'Provide Guava Leaf Photo'}
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 16px;">
                {'स्पष्ट व जवळून काढलेला फोटो द्या (JPG, JPEG, PNG).' if is_mr else 'Upload or capture a sharp, close-up photo of the guava leaf.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Dual Input Selector: File or Camera
        input_mode = st.radio(
            "Input Mode Selection",
            ["📁 फाईल निवडा (Upload File)", "📸 थेट कॅमेरा वापरा (Live Camera)"] if is_mr else ["📁 Upload Image File", "📸 Use Device Camera"],
            horizontal=True,
            key="farmer_input_mode_radio"
        )

        uploaded_file = None
        if "Camera" in input_mode or "कॅमेरा" in input_mode:
            uploaded_file = st.camera_input(
                "कॅमेऱ्याने पानाचा फोटो काढा" if is_mr else "Capture Guava Leaf Photo",
                key="farmer_camera_input"
            )
        else:
            uploaded_file = st.file_uploader(
                "गॅलरीतून फोटो निवडा..." if is_mr else "Choose guava leaf image...",
                type=["jpg", "jpeg", "png"],
                key="farmer_file_uploader",
                help="Supported file extensions: .jpg, .jpeg, .png (under 25MB)"
            )

        pil_img: Optional[Image.Image] = None
        file_valid = False

        if uploaded_file is not None:
            try:
                pil_img = Image.open(uploaded_file)
                file_valid = True
                
                # Image Preview Card
                w, h = pil_img.size
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px 16px; margin: 12px 0 10px 0; display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #cbd5e1;">
                    <span>🖼️ <strong>{'नमुना नाव' if is_mr else 'File'}:</strong> {getattr(uploaded_file, 'name', 'camera_capture.jpg')}</span>
                    <span>📐 <strong>{'आकार' if is_mr else 'Resolution'}:</strong> {w} × {h} px</span>
                </div>
                """, unsafe_allow_html=True)
                st.image(pil_img, caption="निवडलेला नमुना" if is_mr else "Selected Leaf Sample", use_container_width=True)
            except Exception as e:
                st.error(f"❌ {'फोटो उघडताना त्रुटी आढळली:' if is_mr else 'Error reading image file:'} {e}")

        # Prominent Analyze Button
        btn_label = "🔍 पानाचे विश्लेषण करा (Analyze Image)" if is_mr else "🔍 Analyze Foliage Now"
        analyze_clicked = False
        if file_valid and pil_img is not None:
            analyze_clicked = st.button(btn_label, use_container_width=True, type="primary")

    with col_result:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-card-title">
                <span>📋</span> {'निदान आणि कृषी सल्ला अहवाल' if is_mr else 'AI Diagnosis & Field Advisory'}
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 16px;">
                {'खोल न्यूरल नेटवर्क विश्लेषण आणि अचूक उपचार मार्गदर्शक' if is_mr else 'Deep Learning Pathology Classification & Grad-CAM Heatmap'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # File tracking for seamless state persistence
        current_file_id = getattr(uploaded_file, 'name', None) or (f"cam_{uploaded_file.size}" if uploaded_file else None)
        
        if uploaded_file is None or pil_img is None:
            guide_title = "👈 सुरुवातीची मार्गदर्शक माहिती" if is_mr else "👈 How to Get Best Diagnostic Results"
            g1 = "पेरूच्या झाडावरील रोगट किंवा संशयास्पद पानाचा जवळून स्वच्छ फोटो काढा." if is_mr else "Capture a clear, in-focus close-up of the suspected guava leaf."
            g2 = "चांगल्या सूर्यप्रकाशात फोटो काढा जेणेकरून पानाचे रंग स्पष्ट दिसतील." if is_mr else "Ensure good natural illumination; avoid deep shadows or direct flash glare."
            g3 = "पानाचा फोटो अपलोड केल्यानंतर खालील 'Analyze Image' बटनावर क्लिक करा." if is_mr else "Once selected, click the prominent green 'Analyze Foliage Now' button."
            st.markdown(f"""
            <div class="glass-card" style="border: 1px dashed rgba(16, 185, 129, 0.4); text-align: left; padding: 24px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #a7f3d0; margin-bottom: 12px;">{guide_title}</div>
                <div style="margin-bottom: 8px; color: #cbd5e1; font-size: 0.95rem;">• {g1}</div>
                <div style="margin-bottom: 8px; color: #cbd5e1; font-size: 0.95rem;">• {g2}</div>
                <div style="margin-bottom: 8px; color: #cbd5e1; font-size: 0.95rem;">• {g3}</div>
                <div style="margin-top: 18px; padding: 10px 14px; background: rgba(16, 185, 129, 0.12); border-radius: 8px; font-size: 0.88rem; color: #6ee7b7;">
                    🌿 <strong>{'सध्या कार्यरत मॉडेल्स' if is_mr else 'Active Architectures'}:</strong> ResNet-50 & EfficientNet-B3 (5 Foliage Classes)
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

        # Check if we should run or display cached results
        should_run = analyze_clicked or (
            st.session_state.get("cached_file_id") == current_file_id and "cached_inference" in st.session_state
        )

        if not should_run:
            prompt_msg = (
                "👉 पानाचा फोटो निवडला गेला आहे. रोग निदानासाठी डाव्या बाजूला <b>'पानाचे विश्लेषण करा'</b> बटनावर क्लिक करा."
                if is_mr else
                "👉 Photo ready. Click the green <b>'Analyze Foliage Now'</b> button on the left to begin diagnosis."
            )
            st.info(prompt_msg)
            return

        # Run or retrieve inference
        if analyze_clicked or (st.session_state.get("cached_file_id") != current_file_id):
            with st.spinner("🧠 AI मॉडेल पानाचे सखोल विश्लेषण करत आहे..." if is_mr else "🧠 Deep Neural Network analyzing foliage pathology..."):
                inference_result = run_disease_inference(
                    image_source=pil_img,
                    target_type="Leaf",
                    model_name=clean_model_name,
                    uncertainty_threshold=uncertainty_threshold,
                    generate_gradcam=True
                )
                st.session_state["cached_inference"] = inference_result
                st.session_state["cached_file_id"] = current_file_id
        else:
            inference_result = st.session_state["cached_inference"]

        # Handle Inference Failure
        if not inference_result.get("success", False):
            err_code = inference_result.get("error_code")
            msg = inference_result.get("message_mr") if (is_mr and inference_result.get("message_mr")) else inference_result.get("message", "Analysis failed")
            
            if err_code == "HUMAN_DETECTED":
                st.markdown(f"""
                <div style="background: rgba(69, 26, 3, 0.9); border: 2px solid #f97316; border-left: 8px solid #f97316; padding: 20px; border-radius: 12px; margin-bottom: 16px;">
                    <div style="font-size: 1.3rem; font-weight: 800; color: #ffedd5;">
                        👤 {'मानवी चेहरा किंवा व्यक्ती आढळली' if is_mr else 'Human Face / Person Detected'}
                    </div>
                    <div style="font-size: 1.02rem; color: #fed7aa; margin-top: 8px; line-height: 1.6;">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 " + ("कृपया कॅमेरा थेट पेरूच्या पानासमोर धरा आणि जवळून स्पष्ट फोटो काढा." if is_mr else "Please point the camera directly at a guava tree leaf under natural lighting."))
            elif err_code == "NON_PLANT_DETECTED":
                st.markdown(f"""
                <div style="background: rgba(69, 26, 3, 0.9); border: 2px solid #f59e0b; border-left: 8px solid #f59e0b; padding: 20px; border-radius: 12px; margin-bottom: 16px;">
                    <div style="font-size: 1.3rem; font-weight: 800; color: #fef3c7;">
                        🍂 {'वनस्पतीचे पान आढळले नाही' if is_mr else 'No Plant Foliage Detected'}
                    </div>
                    <div style="font-size: 1.02rem; color: #fde68a; margin-top: 8px; line-height: 1.6;">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 " + ("पेरूच्या झाडाचे पान फ्रेममध्ये पूर्ण दिसेल असा जवळून फोटो काढा." if is_mr else "Ensure the guava leaf occupies the center of the camera frame."))
            else:
                st.error(f"❌ {msg}")
            return

        pred_class = inference_result["predicted_class"]
        confidence_pct = inference_result["confidence_pct"]
        is_uncertain = inference_result["is_uncertain"]
        probabilities = inference_result["probabilities"]
        gradcam_vis = inference_result.get("gradcam_vis")
        latency = inference_result.get("latency_ms", 0.0)

        # Knowledge Base Data
        info = get_disease_info(pred_class)
        disease_name = info["name_mr"] if is_mr else info["name_en"]
        is_healthy = (pred_class == "Healthy")

        # 1. Main Highlight Result Card
        card_class = "result-card-healthy" if is_healthy else "result-card-disease"
        status_color = "#10b981" if is_healthy else ("#ea580c" if not is_uncertain else "#f59e0b")
        status_title = "निरोगी पान (Healthy)" if is_healthy else ("रोग आढळला (Disease Detected)" if is_mr else "Disease Detected")

        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.5px;">
                        {'रोग निदान निष्कर्ष' if is_mr else 'AI Pathology Classification'}
                    </div>
                    <div class="result-title">
                        {info['icon']} {disease_name}
                    </div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.4); border: 1px solid {status_color}; border-radius: 30px; padding: 6px 16px; font-weight: 700; color: {status_color}; font-size: 0.95rem;">
                    ● {status_title}
                </div>
            </div>
            
            <div style="margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #cbd5e1; margin-bottom: 4px;">
                    <span>{'विश्वासार्हता (Confidence Score)' if is_mr else 'Confidence Score'}</span>
                    <strong style="color: #38bdf8;">{confidence_pct:.2f}%</strong>
                </div>
                <div style="width: 100%; height: 10px; background: rgba(0,0,0,0.5); border-radius: 5px; overflow: hidden;">
                    <div style="width: {confidence_pct}%; height: 100%; background: linear-gradient(90deg, #10b981 0%, #38bdf8 70%, #84cc16 100%);"></div>
                </div>
            </div>

            <div style="margin-top: 12px; display: flex; flex-wrap: wrap;">
                <span class="result-meta-chip">🤖 {clean_model_name}</span>
                <span class="result-meta-chip">⚡ {latency:.1f} ms</span>
                <span class="result-meta-chip">🎯 {'तीव्रता' if is_mr else 'Severity'}: {info.get('severity', 'Moderate')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Uncertainty Warning (if applicable)
        if is_uncertain:
            st.warning(
                f"⚠️ **{'कमी आत्मविश्वास / अस्पष्ट फोटो' if is_mr else 'Low Confidence Warning'} ({confidence_pct:.1f}%)**\n\n"
                f"{'मॉडेलचा विश्वास ' + str(int(uncertainty_threshold*100)) + '% पेक्षा कमी आहे. कृपया चांगल्या सूर्यप्रकाशात पानाचा स्पष्ट व जवळून फोटो काढून पुन्हा तपासा.' if is_mr else 'Prediction confidence is below the safety threshold (' + str(int(uncertainty_threshold*100)) + '%). Please capture a clearer, close-up photo under natural lighting.'}"
            )

        # 3. Grad-CAM Explainable AI Visualization
        if gradcam_vis is not None:
            st.markdown(f"""
            <div class="glass-card">
                <div class="glass-card-title">
                    <span>🔬</span> {'AI उष्णता नकाशा (Grad-CAM Explainability)' if is_mr else 'AI Explainability Heatmap (Grad-CAM)'}
                </div>
                <p style="color: #94a3b8; font-size: 0.88rem; margin-top: -6px; margin-bottom: 12px;">
                    {'हा उष्णता नकाशा दाखवतो की न्यूरल नेटवर्कने पानावरील कोणत्या रोगट भागावर लक्ष केंद्रित केले आहे.' if is_mr else 'This activation map reveals the specific leaf lesion patterns the neural network focused on.'}
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.image(gradcam_vis, caption="Grad-CAM Layer Activation Map", use_container_width=True)

        # 4. Multi-class Probability Breakdown Expander
        with st.expander("📊 " + ("सर्व रोगांची संभाव्यता (All Class Probabilities)" if is_mr else "All Class Probabilities")):
            for c_name, prob in probabilities.items():
                c_info = get_disease_info(c_name)
                display_c = c_info["name_mr"] if is_mr else c_name
                pct = prob * 100.0
                st.write(f"**{display_c}**: {pct:.2f}%")
                st.progress(min(max(float(prob), 0.0), 1.0))

        # 5. Agricultural Treatment and Guidance Tabs
        st.markdown(f"""
        <div class="glass-card" style="margin-top: 20px;">
            <div class="glass-card-title">
                <span>🌾</span> {'तज्ज्ञ कृषी सल्ला व उपाययोजना' if is_mr else 'Expert Agricultural Advisory & Treatment Guide'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_sym, tab_chem, tab_org, tab_prev = st.tabs([
            "🔍 लक्षणे (Symptoms)" if is_mr else "🔍 Symptoms",
            "💊 रासायनिक फवारणी (Chemical)" if is_mr else "💊 Chemical Spray",
            "🌿 सेंद्रिय/जैविक (Organic)" if is_mr else "🌿 Organic / Bio",
            "🛡️ प्रतिबंधात्मक काळजी (Prevention)" if is_mr else "🛡️ Prevention"
        ])

        with tab_sym:
            symptoms = info["symptoms_mr"] if is_mr else info["symptoms_en"]
            cause = info["causes_mr"] if is_mr else info["causes_en"]
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); padding: 14px 18px; border-radius: 10px; margin-bottom: 14px;">
                <span style="color: #94a3b8; font-size: 0.95rem;">{'कारणीभूत घटक / रोगकारक' if is_mr else 'Causal Organism'}:</span>
                <span style="color: #4ade80; font-size: 1.05rem; font-weight: 700; margin-left: 6px;">{cause}</span>
            </div>
            """, unsafe_allow_html=True)
            for s in symptoms:
                st.markdown(f"""
                <div class="treatment-item" style="border-left: 5px solid #38bdf8;">
                    <span style="color: #f8fafc; font-size: 1.02rem; line-height: 1.6; font-weight: 600;">
                        🔍 {s}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_chem:
            chemicals = info["chemical_control_mr"] if is_mr else info["chemical_control_en"]
            for step in chemicals:
                st.markdown(f"""
                <div class="treatment-item" style="border-left: 5px solid #ef4444;">
                    <span style="color: #f8fafc; font-size: 1.02rem; line-height: 1.6; font-weight: 600;">
                        💊 {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_org:
            organics = info["organic_remedies_mr"] if is_mr else info["organic_remedies_en"]
            for step in organics:
                st.markdown(f"""
                <div class="treatment-item" style="border-left: 5px solid #10b981;">
                    <span style="color: #f8fafc; font-size: 1.02rem; line-height: 1.6; font-weight: 600;">
                        🌿 {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_prev:
            prevs = info["prevention_mr"] if is_mr else info["prevention_en"]
            for step in prevs:
                st.markdown(f"""
                <div class="treatment-item" style="border-left: 5px solid #f59e0b;">
                    <span style="color: #f8fafc; font-size: 1.02rem; line-height: 1.6; font-weight: 600;">
                        🛡️ {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        # 6. Official Disclaimer Card
        render_expert_disclaimer(is_mr=is_mr)

        # 7. Record to SQLite database (Privacy Preserved)
        try:
            raw_bytes = uploaded_file.getvalue() if opt_in_history else None
            record_prediction(
                predicted_class=pred_class,
                confidence=confidence_pct / 100.0,
                model_name=clean_model_name,
                target_type="Leaf",
                image_name=getattr(uploaded_file, 'name', 'field_leaf_sample.jpg'),
                is_uncertain=is_uncertain,
                latency_ms=latency,
                image_bytes=raw_bytes,
                opt_in_storage=opt_in_history
            )
        except Exception:
            pass

        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 " + ("दुसरे पान तपासा (Analyze Another Leaf)" if is_mr else "Analyze Another Leaf"), use_container_width=True):
            if "cached_inference" in st.session_state:
                del st.session_state["cached_inference"]
            if "cached_file_id" in st.session_state:
                del st.session_state["cached_file_id"]
            st.rerun()

    # ----------------- RECENT DIAGNOSES & STATS SECTION -----------------
    st.markdown("<br><hr style='border: none; border-top: 1px solid rgba(16, 185, 129, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-card-title">
            <span>📊</span> {'शेतातील तपासण्यांचा इतिहास व सांख्यिकी' if is_mr else 'Field Diagnostics History & Distribution'}
        </div>
        <p style="color: #94a3b8; font-size: 0.92rem; margin-top: -6px; margin-bottom: 16px;">
            {'स्थानिक डेटाबेसमध्ये नोंदवलेली अलीकडील तपासणी प्रकरणे' if is_mr else 'Recent field diagnoses recorded in local SQLite audit storage'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    stat_col1, stat_col2 = st.columns([1, 1], gap="large")

    with stat_col1:
        st.markdown(f"##### 📜 {'अलीकडील तपासणी नोंदी' if is_mr else 'Recent Diagnostic Records'}")
        history = get_prediction_history(limit=6)
        if history:
            df_hist = pd.DataFrame(history)
            show_cols = ["timestamp", "predicted_class", "confidence", "model_name"]
            df_display = df_hist[[c for c in show_cols if c in df_hist.columns]].copy()
            df_display["confidence"] = df_display["confidence"].apply(lambda v: f"{v*100:.1f}%")
            df_display.rename(columns={
                "timestamp": "दिनांक / Time" if is_mr else "Timestamp",
                "predicted_class": "निदान / Disease" if is_mr else "Disease",
                "confidence": "खात्री / Confidence" if is_mr else "Confidence",
                "model_name": "मॉडेल / Model" if is_mr else "Model"
            }, inplace=True)
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("अद्याप कोणतीही नोंद आढळली नाही." if is_mr else "No recent diagnoses recorded yet.")

    with stat_col2:
        st.markdown(f"##### 📈 {'रोगांचे प्रमाण वितरण' if is_mr else 'Disease Distribution'} ({total_q} {'नमुने' if is_mr else 'Samples'})")
        if dist:
            df_chart = pd.DataFrame(list(dist.items()), columns=["Disease", "Count"]).set_index("Disease")
            st.bar_chart(df_chart, color="#10b981", height=220)
        else:
            st.info("सांख्यिकी उपलब्ध नाही." if is_mr else "Distribution data will populate as diagnoses are run.")

    # Seasonal Agricultural Guidelines
    st.markdown("<br>", unsafe_allow_html=True)
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.markdown(f"""
        <div class="glass-card" style="padding: 18px;">
            <div style="font-weight: 700; color: #4ade80; margin-bottom: 6px;">✂️ {'योग्य छाटणी (Pruning)' if is_mr else 'Canopy Pruning'}</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                {'झाडांच्या आतील सुकलेल्या व रोगट फांद्या वेळोवेळी कापून नष्ट करा. यामुळे झाडामध्ये हवा व सूर्यप्रकाश खेळता राहतो.' if is_mr else 'Prune dead, criss-crossing twigs after harvest to ensure sunlight reaches all internal foliage.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g_col2:
        st.markdown(f"""
        <div class="glass-card" style="padding: 18px;">
            <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">💧 {'पाणी व निचरा (Drainage)' if is_mr else 'Basin Drainage'}</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                {'झाडाच्या खोडापाशी पाणी साचू देऊ नका. जास्तीच्या पाण्याचा निचरा त्वरित करा जेणेकरून बुरशीचा प्रादुर्भाव रोखता येईल.' if is_mr else 'Prevent standing water around the root collar to inhibit fungal sporulation and collar rot.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g_col3:
        st.markdown(f"""
        <div class="glass-card" style="padding: 18px;">
            <div style="font-weight: 700; color: #fbbf24; margin-bottom: 6px;">🌿 {'जैविक संरक्षण (Bio-Defense)' if is_mr else 'Bio-Remedies'}</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                {'महिन्यातून एकदा ट्रायकोडर्मा किंवा कडुलिंबाच्या तेलाची (५ मिली/लिटर) प्रतिबंधात्मक फवारणी उपयुक्त ठरते.' if is_mr else 'Foliar application of Trichoderma viride or 5% Neem Oil serves as an eco-friendly prophylactic bio-shield.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------- FOOTER -----------------
    render_agri_footer(is_mr=is_mr)
