"""
UI Styling and Design System Component: Guava Agri-AI System
Provides rich agricultural green, emerald, lime, and golden-yellow palette,
glassmorphism card styles, modern typography, responsive layout rules,
and reusable UI widgets (hero banner, metric cards, disclaimers, footer).
"""
import streamlit as st
from typing import Dict, Any, List, Optional

def inject_custom_css():
    """Injects high-performance agricultural AI theme and glassmorphism styling."""
    st.markdown("""
    <style>
        /* Import Modern Google Fonts: Inter, Plus Jakarta Sans, Mukta (Marathi/Devanagari) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

        /* Color Tokens & Global Variables */
        :root {
            --primary-emerald: #10b981;
            --primary-green: #059669;
            --dark-forest: #022c22;
            --deep-slate: #0b1512;
            --lime-accent: #84cc16;
            --golden-yellow: #f59e0b;
            --card-glass: rgba(15, 28, 24, 0.78);
            --card-border: rgba(16, 185, 129, 0.22);
            --card-hover-border: rgba(132, 204, 22, 0.55);
            --text-light: #f0fdf4;
            --text-muted: #94a3b8;
        }

        /* Full App Background: Lush Botanical Gradient with Radial Glow */
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgba(5, 150, 105, 0.12) 0%, transparent 40%),
                        radial-gradient(circle at 90% 80%, rgba(132, 204, 22, 0.08) 0%, transparent 40%),
                        linear-gradient(145deg, #021a13 0%, #062b1e 45%, #031e16 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Plus Jakarta Sans', 'Inter', 'Mukta', sans-serif !important;
            color: #f1f5f9 !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #031b14 0%, #06251c 60%, #02140e 100%) !important;
            border-right: 1px solid rgba(16, 185, 129, 0.2) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h1,
        section[data-testid="stSidebar"] .stMarkdown h2,
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #d1fae5 !important;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Sidebar Cards */
        .sidebar-card {
            background: rgba(6, 43, 30, 0.55);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 14px;
            padding: 14px 16px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            transition: all 0.25s ease;
        }
        .sidebar-card:hover {
            border-color: rgba(132, 204, 22, 0.5);
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.2);
        }

        /* Hero Banner Component */
        .hero-banner {
            position: relative;
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.92) 0%, rgba(4, 47, 46, 0.95) 50%, rgba(2, 44, 34, 0.98) 100%);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            overflow: hidden;
        }
        .hero-banner::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(132, 204, 22, 0.18) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ecfdf5 0%, #a7f3d0 40%, #fef08a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            font-size: 1.12rem;
            color: #cbd5e1;
            font-weight: 500;
            margin-bottom: 18px;
            line-height: 1.5;
            font-family: 'Mukta', 'Inter', sans-serif;
        }
        .hero-badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.16);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #d1fae5;
            padding: 5px 14px;
            border-radius: 30px;
            font-size: 0.88rem;
            font-weight: 600;
            backdrop-filter: blur(6px);
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(15, 32, 26, 0.82);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(16, 185, 129, 0.28);
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
            transition: all 0.25s ease-in-out;
            position: relative;
            overflow: hidden;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(132, 204, 22, 0.6);
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
        }
        .metric-card-icon {
            font-size: 1.8rem;
            margin-bottom: 8px;
            display: inline-block;
        }
        .metric-card-title {
            color: #94a3b8;
            font-size: 0.88rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .metric-card-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1.2;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .metric-card-subtitle {
            font-size: 0.82rem;
            color: #10b981;
            margin-top: 4px;
            font-weight: 500;
        }

        /* Glassmorphism Section Cards */
        .glass-card {
            background: rgba(13, 30, 24, 0.82);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(16, 185, 129, 0.22);
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 22px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        .glass-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #a7f3d0;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
        }

        /* Large Drag and Drop Upload Area Customization */
        div[data-testid="stFileUploader"] {
            background: transparent !important;
        }
        div[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #10b981 !important;
            border-radius: 18px !important;
            background: rgba(6, 78, 59, 0.22) !important;
            padding: 24px 18px !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stFileUploaderDropzone"]:hover {
            border-color: #84cc16 !important;
            background: rgba(6, 78, 59, 0.42) !important;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.35) !important;
            transform: scale(1.005);
        }

        /* Prominent Animated-Looking Green Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #059669 0%, #10b981 50%, #16a34a 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.08rem !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 14px !important;
            padding: 12px 28px !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            letter-spacing: 0.3px !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(16, 185, 129, 0.6) !important;
            border-color: #a3e635 !important;
            color: #ffffff !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Result Highlighting Cards */
        .result-card-healthy {
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(4, 47, 46, 0.9) 100%);
            border: 2px solid #10b981;
            border-left: 10px solid #10b981;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            box-shadow: 0 8px 30px rgba(16, 185, 129, 0.3);
        }
        .result-card-disease {
            background: linear-gradient(135deg, rgba(69, 26, 3, 0.88) 0%, rgba(30, 15, 10, 0.95) 100%);
            border: 2px solid #ea580c;
            border-left: 10px solid #ef4444;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.3);
        }
        .result-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
            margin-bottom: 8px;
        }
        .result-meta-chip {
            display: inline-flex;
            align-items: center;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 0.88rem;
            font-weight: 600;
            color: #e2e8f0;
            margin-right: 8px;
            margin-top: 6px;
        }

        /* Treatment Box Item */
        .treatment-item {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(51, 65, 85, 0.6);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
        }
        .treatment-item:hover {
            border-color: rgba(16, 185, 129, 0.4);
            transform: translateX(3px);
        }

        /* Disclaimer Card */
        .disclaimer-box {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid #475569;
            border-left: 5px solid #f59e0b;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 24px;
            margin-bottom: 20px;
            color: #cbd5e1;
            font-size: 0.92rem;
            line-height: 1.6;
        }

        /* Clean Modern Footer */
        .modern-footer {
            text-align: center;
            padding: 30px 20px;
            margin-top: 40px;
            border-top: 1px solid rgba(16, 185, 129, 0.2);
            color: #94a3b8;
            font-size: 0.9rem;
            background: rgba(2, 26, 19, 0.6);
            border-radius: 16px;
        }
        .footer-highlight {
            color: #10b981;
            font-weight: 700;
        }

        /* Responsive Mobile Layout Adjustments */
        @media (max-width: 768px) {
            .hero-banner {
                padding: 18px 20px !important;
                border-radius: 14px !important;
            }
            .hero-title {
                font-size: 1.55rem !important;
            }
            .hero-subtitle {
                font-size: 0.95rem !important;
            }
            .metric-card {
                margin-bottom: 12px !important;
            }
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero(is_mr: bool = True):
    """Renders the visually rich hero section."""
    title = "🌿 पेरू ॲग्री-एआय रोग निदान प्रणाली" if is_mr else "🌿 Guava Agri-AI Smart Diagnostic Studio"
    subtitle = (
        "खोल न्यूरल नेटवर्क (Deep Learning), स्पष्टीकरणात्मक एआय (Grad-CAM), "
        "आणि अचूक कृषी उपायांसह पेरूच्या बागांचे स्मार्ट संरक्षण."
        if is_mr else
        "Enterprise-grade Foliage & Fruit Pathology Diagnostic Suite powered by ResNet-50 & EfficientNet-B3 with Grad-CAM Explainable AI."
    )
    badge1 = "🎯 96.26% AI Accuracy" if not is_mr else "🎯 ९६.२६% अचूकता"
    badge2 = "🔬 Grad-CAM Heatmap" if not is_mr else "🔬 उष्णता नकाशा (XAI)"
    badge3 = "⚡ Sub-50ms Latency" if not is_mr else "⚡ अतिजलद विश्लेषण"
    badge4 = "🌐 Bilingual (मराठी / English)" if not is_mr else "🌐 द्विभाषिक सल्ला"

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
        <div class="hero-badge-container">
            <span class="hero-badge">{badge1}</span>
            <span class="hero-badge">{badge2}</span>
            <span class="hero-badge">{badge3}</span>
            <span class="hero-badge">{badge4}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_cards(
    total_analyses: int,
    healthy_count: int,
    diseased_count: int,
    accuracy_pct: float = 96.26,
    is_mr: bool = True
):
    """Renders 4 glowing agricultural metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    t1 = "एकूण तपासण्या" if is_mr else "Total Diagnoses"
    s1 = "स्थानिक नोंदी" if is_mr else "Verified Samples"

    t2 = "निरोगी नमुने" if is_mr else "Healthy Leaves"
    s2 = "चांगली पाने" if is_mr else "Disease-Free"

    t3 = "रोग निदान प्रकरणे" if is_mr else "Pathologies Found"
    s3 = "सक्रिय उपचार आवश्यक" if is_mr else "Action Required"

    t4 = "मॉडेल अचूकता" if is_mr else "Model Accuracy"
    s4 = "EfficientNet-B3 चाचणी" if is_mr else "Test Benchmark"

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">🔬</span>
            <div class="metric-card-title">{t1}</div>
            <div class="metric-card-value">{total_analyses}</div>
            <div class="metric-card-subtitle">{s1}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">🌿</span>
            <div class="metric-card-title">{t2}</div>
            <div class="metric-card-value" style="color: #4ade80;">{healthy_count}</div>
            <div class="metric-card-subtitle" style="color: #86efac;">{s2}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">⚠️</span>
            <div class="metric-card-title">{t3}</div>
            <div class="metric-card-value" style="color: #fb923c;">{diseased_count}</div>
            <div class="metric-card-subtitle" style="color: #fdba74;">{s3}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">🎯</span>
            <div class="metric-card-title">{t4}</div>
            <div class="metric-card-value" style="color: #38bdf8;">{accuracy_pct:.1f}%</div>
            <div class="metric-card-subtitle" style="color: #7dd3fc;">{s4}</div>
        </div>
        """, unsafe_allow_html=True)

def render_expert_disclaimer(is_mr: bool = True):
    """Renders the official agricultural advisory disclaimer."""
    disc_title = "⚠️ महत्त्वपूर्ण कृषी सल्ला व सूचना" if is_mr else "⚠️ Official Agricultural Expert Disclaimer"
    disc_text = (
        "सदर एआय प्रणाली शेतकरी बांधवांना आणि कृषी संशोधकांना प्राथमिक निदानासाठी मार्गदर्शनपर मदत करते. "
        "रासायनिक फवारणी किंवा व्यापक उपाययोजना करण्यापूर्वी कृपया स्थानिक कृषी विज्ञान केंद्र (KVK), "
        "कृषी विद्यापीठ किंवा अधिकृत कृषी अधिकाऱ्यांचा सल्ला अवश्य घ्यावा."
        if is_mr else
        "This AI diagnostic suite is intended for assistive field guidance and academic research. "
        "Before administering chemical treatments or major field interventions, always verify recommendations "
        "with an authorized agricultural extension officer or your local Krishi Vigyan Kendra (KVK)."
    )
    st.markdown(f"""
    <div class="disclaimer-box">
        <strong style="color: #fbbf24; font-size: 1.02rem;">{disc_title}</strong><br>
        <span style="display: block; margin-top: 6px;">{disc_text}</span>
    </div>
    """, unsafe_allow_html=True)

def render_agri_footer(is_mr: bool = True):
    """Renders the clean agricultural AI footer."""
    line1 = "पेरू ॲग्री-एआय स्मार्ट रोग निदान प्रणाली" if is_mr else "Guava Agri-AI Smart Diagnostic System"
    line2 = (
        "अंतिम वर्ष अभियांत्रिकी शैक्षणिक प्रकल्प (२०२६–२०२७) | विकसित: Deep Learning, PyTorch आणि Streamlit"
        if is_mr else
        "Final Year Engineering Academic Capstone Project (2026–2027) | Powered by Deep Learning, PyTorch & Streamlit"
    )
    st.markdown(f"""
    <div class="modern-footer">
        <div style="font-weight: 700; color: #ecfdf5; font-size: 1.05rem; margin-bottom: 4px;">🌿 {line1}</div>
        <div style="font-size: 0.88rem; color: #94a3b8;">{line2}</div>
        <div style="font-size: 0.82rem; color: #64748b; margin-top: 6px;">
            © 2026–2027 Guava Disease Detection System | Strictly In-Memory Data Privacy Enabled
        </div>
    </div>
    """, unsafe_allow_html=True)
