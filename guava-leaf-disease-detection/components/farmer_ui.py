"""
Farmer / User Panel Component
Agricultural-first UI with green/cream design, English & Marathi localization,
clear disease diagnosis, high-contrast treatment recommendations, and Grad-CAM visualization.
"""
import streamlit as st
from PIL import Image
from typing import Dict, Any

from core.inference import run_disease_inference
from services.disease_service import get_disease_info
from services.history_service import record_prediction
from services.configuration_service import load_settings

def render_farmer_ui():
    """Renders the Farmer / User disease detection interface."""
    settings = load_settings()
    uncertainty_threshold = settings.get("inference", {}).get("uncertainty_threshold", 0.60)
    
    # Custom Agricultural & High-Contrast CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        
        .agri-banner {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
            padding: 24px;
            border-radius: 14px;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 4px 15px rgba(27, 67, 50, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .agri-banner h1 {
            color: #d8f3dc !important;
            font-size: 2.2rem;
            margin-bottom: 6px;
            font-weight: 800;
            font-family: 'Mukta', 'Inter', sans-serif;
        }
        .agri-banner p {
            color: #b7e4c7 !important;
            font-size: 1.15rem;
            margin-bottom: 0px;
            font-weight: 500;
            font-family: 'Mukta', 'Inter', sans-serif;
        }
        
        /* High-Contrast Tab styling */
        div[data-testid="stTabs"] button {
            font-size: 1.08rem !important;
            font-weight: 700 !important;
            color: #94a3b8 !important;
            padding: 10px 16px !important;
            font-family: 'Mukta', 'Inter', sans-serif !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #22c55e !important;
            border-bottom: 3px solid #22c55e !important;
        }

        /* Mobile Responsive & Touch Target Enhancements */
        @media (max-width: 768px) {
            .agri-banner {
                padding: 16px !important;
                margin-bottom: 16px !important;
                border-radius: 10px !important;
            }
            .agri-banner h1 {
                font-size: 1.55rem !important;
            }
            .agri-banner p {
                font-size: 0.98rem !important;
            }
            /* Large comfortable touch targets for smartphones */
            button, input, select {
                min-height: 48px !important;
            }
            div[data-testid="stTabs"] button {
                font-size: 0.92rem !important;
                padding: 8px 10px !important;
            }
            /* Stack columns vertically on mobile screens */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                margin-bottom: 16px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Language and Control Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col2:
        lang = st.selectbox(
            "🌐 भाषा / Language",
            ["मराठी (Marathi)", "English"],
            index=0,
            key="farmer_lang"
        )
    is_mr = "मराठी" in lang

    # Banner
    title = "🌿 पेरू पान व फळ रोग निदान प्रणाली" if is_mr else "🌿 Guava Leaf & Fruit Disease Detection System"
    subtitle = "अद्ययावत कृत्रिम बुद्धिमत्ता (AI) आणि अचूक उपाययोजना" if is_mr else "Advanced Deep Learning & Agricultural Treatment Advisory"
    st.markdown(f"""
    <div class="agri-banner">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

    # Configuration Sidebar / Expander
    with st.sidebar:
        st.markdown("### ⚙️ " + ("तपासणी पर्याय" if is_mr else "Inspection Options"))
        target_choice = st.radio(
            "काय तपासणार आहात? / Target" if is_mr else "Analysis Target",
            ["🍃 पान (Leaf)", "🍎 फळ (Fruit)"],
            index=0
        )
        target_type = "Leaf" if "Leaf" in target_choice or "पान" in target_choice else "Fruit"

        model_name = st.selectbox(
            "मॉडेल निवडा / Model" if is_mr else "AI Architecture",
            ["ResNet-50", "EfficientNet-B3"],
            index=0
        )

        st.markdown("---")
        st.markdown("#### 🔒 " + ("गोपनीयता / Privacy" if is_mr else "Data Privacy"))
        opt_in_history = st.checkbox(
            "माझा फोटो इतिहासात जतन करा" if is_mr else "Opt-in: Save image to local history",
            value=False,
            help="Your photo stays strictly in memory during analysis. Check only if you wish to record it in local history."
        )

    # If Fruit target is selected, show informative notice
    if target_type == "Fruit":
        st.warning(
            "🍎 **पेरू फळ रोग निदान मॉडेल सध्या संकलनाधीन आहे!**\n\n"
            "सध्या पेरूच्या पानांच्या रोगांचे मॉडेल (खैऱ्या, ठिपके, तांबेरा, ममीफिकेशन) १००% प्रशिक्षित व कार्यरत आहे. "
            "कृपया पानाचा फोटो निवडा." if is_mr else
            "🍎 **Guava Fruit Disease Module is Under Dataset Collection!**\n\n"
            "The guava leaf disease detection model (Canker, Dot, Rust, Mummification, Healthy) is fully trained and operational. "
            "Please switch to **Leaf** target above to analyze foliage."
        )
        return

    # Main Interaction Area: Upload and Results
    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("### 📸 " + ("पानाचा फोटो द्या" if is_mr else "Provide Leaf Photo"))
        
        # Dual mobile input: File upload OR Live Mobile Camera
        input_method = st.radio(
            "फोटो घेण्याची पद्धत / Input Method" if is_mr else "Input Mode",
            ["📁 फोटो फाईल निवडा (Upload)", "📸 थेट कॅमेराने फोटो काढा (Camera)"] if is_mr else ["📁 Upload Image File", "📸 Use Device Camera"],
            horizontal=True,
            key="farmer_input_mode"
        )
        
        if "Camera" in input_method or "कॅमेरा" in input_method:
            uploaded_file = st.camera_input(
                "पेरूच्या पानाचा फोटो काढा" if is_mr else "Capture Guava Leaf Photo",
                key="farmer_camera_input"
            )
        else:
            uploaded_file = st.file_uploader(
                "गॅलरीतून फोटो निवडा (JPG, PNG)..." if is_mr else "Choose leaf image (JPG, PNG)...",
                type=["jpg", "jpeg", "png"],
                key="farmer_file_uploader"
            )

        if uploaded_file is not None:
            try:
                pil_img = Image.open(uploaded_file)
                st.image(pil_img, caption="निवडलेला फोटो" if is_mr else "Input Leaf Photo", width="stretch")
            except Exception as e:
                st.error(f"Image load error: {e}")

    with col_result:
        st.markdown("### 📋 " + ("निदान आणि अहवाल" if is_mr else "Diagnosis & Treatment"))

        if uploaded_file is None:
            st.info(
                "👈 डाव्या बाजूला पेरूच्या पानाचा फोटो अपलोड करा. काही सेकंदात AI द्वारे रोगाचे अचूक निदान व उपाय मिळतील."
                if is_mr else
                "👈 Upload a guava leaf photo on the left to obtain AI disease diagnosis and expert agricultural remedies."
            )
            return

        # Perform Unified Inference
        with st.spinner("फोटोचे विश्लेषण चालू आहे..." if is_mr else "AI model analyzing foliage..."):
            inference_result = run_disease_inference(
                image_source=pil_img,
                target_type="Leaf",
                model_name=model_name,
                uncertainty_threshold=uncertainty_threshold,
                generate_gradcam=True
            )

        if not inference_result.get("success", False):
            err_code = inference_result.get("error_code")
            msg = inference_result.get("message_mr") if (is_mr and inference_result.get("message_mr")) else inference_result.get("message", "Analysis failed")
            
            if err_code == "HUMAN_DETECTED":
                st.markdown(f"""
                <div style="background-color: #451a03 !important; border: 2px solid #f97316 !important; border-left: 8px solid #f97316 !important; padding: 20px !important; border-radius: 10px !important; margin-bottom: 16px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
                    <div style="font-size: 1.3rem !important; font-weight: 800 !important; color: #ffedd5 !important; font-family: 'Mukta', sans-serif !important;">
                        👤 {'मानवी चेहरा / व्यक्ती आढळली (Human Subject Detected)' if is_mr else 'Human Face / Person Detected'}
                    </div>
                    <div style="font-size: 1.05rem !important; color: #fed7aa !important; margin-top: 8px !important; line-height: 1.6 !important; font-family: 'Mukta', sans-serif !important;">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 " + ("कृपया कॅमेरा थेट पेरूच्या पानासमोर धरा आणि जवळून स्पष्ट फोटो काढा." if is_mr else "Please point the camera directly at a guava tree leaf under natural lighting."))
            elif err_code == "NON_PLANT_DETECTED":
                st.markdown(f"""
                <div style="background-color: #451a03 !important; border: 2px solid #f59e0b !important; border-left: 8px solid #f59e0b !important; padding: 20px !important; border-radius: 10px !important; margin-bottom: 16px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
                    <div style="font-size: 1.3rem !important; font-weight: 800 !important; color: #fef3c7 !important; font-family: 'Mukta', sans-serif !important;">
                        🍂 {'वनस्पतीचे पान आढळले नाही (No Plant Foliage Detected)' if is_mr else 'No Plant Foliage Detected'}
                    </div>
                    <div style="font-size: 1.05rem !important; color: #fde68a !important; margin-top: 8px !important; line-height: 1.6 !important; font-family: 'Mukta', sans-serif !important;">
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
        latency = inference_result.get("latency_ms", 0)

        # Get Agricultural Treatment Data
        info = get_disease_info(pred_class)
        disease_name = info["name_mr"] if is_mr else info["name_en"]
        status_label = "निरोगी (Healthy)" if pred_class == "Healthy" else ("रोग आढळला (Disease Detected)" if is_mr else "Disease Detected")

        # 1. Uncertainty Warning if confidence < threshold
        if is_uncertain:
            st.warning(
                f"⚠️ **कमी आत्मविश्वास / अस्पष्ट फोटो ({confidence_pct:.1f}%)**\n\n"
                f"मॉडेलचा विश्वास {uncertainty_threshold*100:.0f}% पेक्षा कमी आहे. कृपया चांगल्या सूर्यप्रकाशात पानाचा स्पष्ट व जवळून फोटो काढा."
                if is_mr else
                f"⚠️ **Low Confidence / Uncertainty Warning ({confidence_pct:.1f}%)**\n\n"
                f"Prediction confidence is below the safety threshold ({uncertainty_threshold*100:.0f}%). "
                f"Please ensure the image is in focus, well-lit, and shows clear leaf symptoms."
            )

        # 2. Main Disease Alert Card (Guaranteed High Contrast)
        badge_color = info["color"]
        st.markdown(f"""
        <div style="background-color: #0f172a !important; border: 2px solid {badge_color} !important; border-left: 8px solid {badge_color} !important; padding: 20px !important; border-radius: 10px !important; margin-bottom: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
            <div style="font-size: 1.45rem !important; font-weight: 800 !important; color: #ffffff !important; font-family: 'Mukta', 'Inter', sans-serif !important;">
                {info['icon']} {disease_name}
            </div>
            <div style="font-size: 1.05rem !important; color: #cbd5e1 !important; margin-top: 8px !important; font-weight: 500 !important; font-family: 'Mukta', 'Inter', sans-serif !important;">
                <span style="color: #94a3b8 !important;">{'स्थिती' if is_mr else 'Status'}:</span> <strong style="color: {badge_color} !important;">{status_label}</strong> &nbsp;|&nbsp; 
                <span style="color: #94a3b8 !important;">{'खात्री' if is_mr else 'Confidence'}:</span> <strong style="color: #38bdf8 !important;">{confidence_pct:.2f}%</strong> &nbsp;|&nbsp; 
                <span style="color: #94a3b8 !important;">{'वेळ' if is_mr else 'Latency'}:</span> <strong style="color: #a7f3d0 !important;">{latency:.1f} ms</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Probability Distribution Expander
        with st.expander("📊 " + ("सर्व रोगांची संभाव्यता (Probability Breakdown)" if is_mr else "All Class Probabilities")):
            for c_name, prob in probabilities.items():
                c_info = get_disease_info(c_name)
                display_c = c_info["name_mr"] if is_mr else c_name
                st.write(f"**{display_c}**: {prob*100:.2f}%")
                st.progress(min(max(float(prob), 0.0), 1.0))

        # 4. Grad-CAM Explainable AI Visualization
        if gradcam_vis is not None:
            st.markdown("#### 🔬 " + ("AI उष्णता नकाशा (Grad-CAM Explainability)" if is_mr else "AI Explainability Heatmap (Grad-CAM)"))
            st.caption(
                "हा नकाशा दर्शवितो की मॉडेलने पानातील कोणत्या रोगट भागावर लक्ष केंद्रित केले आहे."
                if is_mr else
                "Heatmap shows the exact pixel regions the neural network focused on to make this diagnosis."
            )
            st.image(gradcam_vis, caption="Grad-CAM Activation Map", width="stretch")

        # 5. Treatment and Remedial Tabs (High Contrast, Bold, Readable)
        st.markdown("---")
        st.markdown("### 🌾 " + ("तज्ज्ञ कृषी सल्ला व उपाय" if is_mr else "Recommended Agricultural Treatment"))
        
        tab_sym, tab_chem, tab_org, tab_prev = st.tabs([
            "🔍 लक्षणे (Symptoms)" if is_mr else "🔍 Symptoms",
            "💊 रासायनिक उपाय (Chemical)" if is_mr else "💊 Chemical Spray",
            "🌿 सेंद्रिय/जैविक (Organic)" if is_mr else "🌿 Organic / Bio",
            "🛡️ प्रतिबंधात्मक काळजी (Prevention)" if is_mr else "🛡️ Prevention"
        ])

        with tab_sym:
            symptoms = info["symptoms_mr"] if is_mr else info["symptoms_en"]
            cause = info["causes_mr"] if is_mr else info["causes_en"]
            st.markdown(f"""
            <div style="background-color: #0f172a !important; border: 1px solid #334155 !important; padding: 14px 18px !important; border-radius: 8px !important; margin-bottom: 14px !important;">
                <span style="color: #94a3b8 !important; font-size: 1.05rem !important; font-weight: 500 !important; font-family: 'Mukta', sans-serif !important;">{'कारणीभूत घटक' if is_mr else 'Causal Organism'}:</span>
                <span style="color: #4ade80 !important; font-size: 1.15rem !important; font-weight: 700 !important; margin-left: 6px !important; font-family: 'Mukta', sans-serif !important;">{cause}</span>
            </div>
            """, unsafe_allow_html=True)
            for s in symptoms:
                st.markdown(f"""
                <div style="background-color: #0f172a !important; border: 1px solid #334155 !important; border-left: 6px solid #38bdf8 !important; padding: 16px 20px !important; margin-bottom: 12px !important; border-radius: 8px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;">
                    <span style="color: #ffffff !important; font-size: 1.12rem !important; line-height: 1.7 !important; font-weight: 600 !important; font-family: 'Mukta', 'Noto Sans Devanagari', -apple-system, sans-serif !important;">
                        🔍 {s}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_chem:
            chemicals = info["chemical_control_mr"] if is_mr else info["chemical_control_en"]
            for step in chemicals:
                st.markdown(f"""
                <div style="background-color: #0f172a !important; border: 1px solid #334155 !important; border-left: 6px solid #ef4444 !important; padding: 16px 20px !important; margin-bottom: 12px !important; border-radius: 8px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;">
                    <span style="color: #ffffff !important; font-size: 1.12rem !important; line-height: 1.7 !important; font-weight: 600 !important; font-family: 'Mukta', 'Noto Sans Devanagari', -apple-system, sans-serif !important;">
                        💊 {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_org:
            organics = info["organic_remedies_mr"] if is_mr else info["organic_remedies_en"]
            for step in organics:
                st.markdown(f"""
                <div style="background-color: #0f172a !important; border: 1px solid #334155 !important; border-left: 6px solid #22c55e !important; padding: 16px 20px !important; margin-bottom: 12px !important; border-radius: 8px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;">
                    <span style="color: #ffffff !important; font-size: 1.12rem !important; line-height: 1.7 !important; font-weight: 600 !important; font-family: 'Mukta', 'Noto Sans Devanagari', -apple-system, sans-serif !important;">
                        🌿 {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with tab_prev:
            prevs = info["prevention_mr"] if is_mr else info["prevention_en"]
            for step in prevs:
                st.markdown(f"""
                <div style="background-color: #0f172a !important; border: 1px solid #334155 !important; border-left: 6px solid #f59e0b !important; padding: 16px 20px !important; margin-bottom: 12px !important; border-radius: 8px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;">
                    <span style="color: #ffffff !important; font-size: 1.12rem !important; line-height: 1.7 !important; font-weight: 600 !important; font-family: 'Mukta', 'Noto Sans Devanagari', -apple-system, sans-serif !important;">
                        🛡️ {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        # 6. Record to SQLite database
        try:
            raw_bytes = uploaded_file.getvalue() if opt_in_history else None
            record_prediction(
                predicted_class=pred_class,
                confidence=confidence_pct / 100.0,
                model_name=model_name,
                target_type="Leaf",
                image_name=uploaded_file.name,
                is_uncertain=is_uncertain,
                latency_ms=latency,
                image_bytes=raw_bytes,
                opt_in_storage=opt_in_history
            )
        except Exception:
            pass  # Ensure persistence issues never crash user inference

        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 " + ("दुसरे पान तपासा" if is_mr else "Analyze Another Leaf"), width="stretch"):
            st.rerun()
