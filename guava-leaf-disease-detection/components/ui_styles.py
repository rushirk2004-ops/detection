"""
UI Styling and Design System Component: Guava Agri-AI Multi-Farmer Platform
Provides the requested agricultural color tokens:
- Forest green: #123D2B
- Emerald green: #21A366
- Lime green: #D8F36A
- Golden yellow: #FFC857
- Mint background: #E8F7EE
- Dark slate: #1C2430
With glassmorphism cards, modern typography, responsive layout rules,
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
            --forest-green: #123D2B;
            --emerald-green: #21A366;
            --lime-green: #D8F36A;
            --golden-yellow: #FFC857;
            --mint-bg: #E8F7EE;
            --dark-slate: #1C2430;
            --card-glass: rgba(18, 61, 43, 0.75);
            --card-border: rgba(33, 163, 102, 0.35);
            --text-light: #F0FDF4;
            --text-muted: #94A3B8;
        }

        /* Full App Background */
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgba(33, 163, 102, 0.15) 0%, transparent 40%),
                        radial-gradient(circle at 90% 80%, rgba(216, 243, 106, 0.1) 0%, transparent 40%),
                        linear-gradient(145deg, #0D281C 0%, #123D2B 45%, #1C2430 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Plus Jakarta Sans', 'Inter', 'Mukta', sans-serif !important;
            color: #F1F5F9 !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A2217 0%, #123D2B 60%, #1C2430 100%) !important;
            border-right: 1px solid rgba(33, 163, 102, 0.3) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.45) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h1,
        section[data-testid="stSidebar"] .stMarkdown h2,
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #D8F36A !important;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Sidebar Cards */
        .sidebar-card {
            background: rgba(18, 61, 43, 0.65);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(33, 163, 102, 0.35);
            border-radius: 14px;
            padding: 14px 16px;
            margin-bottom: 14px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
            transition: all 0.25s ease;
        }
        .sidebar-card:hover {
            border-color: #D8F36A;
            box-shadow: 0 6px 20px rgba(33, 163, 102, 0.3);
        }

        /* Hero Banner Component */
        .hero-banner {
            position: relative;
            background: linear-gradient(135deg, rgba(18, 61, 43, 0.95) 0%, rgba(33, 163, 102, 0.85) 60%, rgba(28, 36, 48, 0.95) 100%);
            border: 1px solid rgba(216, 243, 106, 0.35);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 14px 38px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(16px);
            overflow: hidden;
        }
        .hero-banner::after {
            content: '';
            position: absolute;
            top: -40%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(216, 243, 106, 0.2) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #FFFFFF 0%, #D8F36A 50%, #FFC857 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            font-size: 1.12rem;
            color: #E2E8F0;
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
            background: rgba(18, 61, 43, 0.6);
            border: 1px solid #21A366;
            color: #D8F36A;
            padding: 5px 14px;
            border-radius: 30px;
            font-size: 0.88rem;
            font-weight: 600;
            backdrop-filter: blur(6px);
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(28, 36, 48, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(33, 163, 102, 0.35);
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.25s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: #D8F36A;
            box-shadow: 0 10px 25px rgba(33, 163, 102, 0.3);
        }
        .metric-card-icon {
            font-size: 1.8rem;
            margin-bottom: 8px;
            display: inline-block;
        }
        .metric-card-title {
            color: #94A3B8;
            font-size: 0.88rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .metric-card-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: #F8FAFC;
            line-height: 1.2;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .metric-card-subtitle {
            font-size: 0.82rem;
            color: #21A366;
            margin-top: 4px;
            font-weight: 500;
        }

        /* Glassmorphism Section Cards */
        .glass-card {
            background: rgba(28, 36, 48, 0.82);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(33, 163, 102, 0.28);
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 22px;
            box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35);
        }
        .glass-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #D8F36A;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
        }

        /* Upload Area */
        div[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #21A366 !important;
            border-radius: 18px !important;
            background: rgba(18, 61, 43, 0.35) !important;
            padding: 24px 18px !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stFileUploaderDropzone"]:hover {
            border-color: #D8F36A !important;
            background: rgba(18, 61, 43, 0.55) !important;
            box-shadow: 0 0 25px rgba(33, 163, 102, 0.4) !important;
        }

        /* Prominent Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #123D2B 0%, #21A366 60%, #16804F 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            border: 1px solid rgba(216, 243, 106, 0.35) !important;
            border-radius: 14px !important;
            padding: 12px 26px !important;
            box-shadow: 0 6px 20px rgba(33, 163, 102, 0.4) !important;
            transition: all 0.25s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(33, 163, 102, 0.6) !important;
            border-color: #D8F36A !important;
            color: #D8F36A !important;
        }

        /* High-contrast tabs */
        div[data-testid="stTabs"] button {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #94A3B8 !important;
            padding: 10px 18px !important;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #D8F36A !important;
            border-bottom: 3px solid #21A366 !important;
        }

        /* Result Highlighting Cards */
        .result-card-healthy {
            background: linear-gradient(135deg, rgba(18, 61, 43, 0.9) 0%, rgba(33, 163, 102, 0.85) 100%);
            border: 2px solid #21A366;
            border-left: 10px solid #D8F36A;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            box-shadow: 0 8px 30px rgba(33, 163, 102, 0.35);
        }
        .result-card-disease {
            background: linear-gradient(135deg, rgba(40, 20, 15, 0.92) 0%, rgba(28, 36, 48, 0.95) 100%);
            border: 2px solid #EA580C;
            border-left: 10px solid #EF4444;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.3);
        }
        .result-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #FFFFFF;
            font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
            margin-bottom: 8px;
        }
        .result-meta-chip {
            display: inline-flex;
            align-items: center;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 0.88rem;
            font-weight: 600;
            color: #E2E8F0;
            margin-right: 8px;
            margin-top: 6px;
        }

        .treatment-item {
            background: rgba(28, 36, 48, 0.8);
            border: 1px solid rgba(51, 65, 85, 0.7);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
        }
        .treatment-item:hover {
            border-color: #21A366;
            transform: translateX(3px);
        }

        .disclaimer-box {
            background: rgba(28, 36, 48, 0.75);
            border: 1px solid #475569;
            border-left: 5px solid #FFC857;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 24px;
            margin-bottom: 20px;
            color: #CBD5E1;
            font-size: 0.92rem;
            line-height: 1.6;
        }

        .modern-footer {
            text-align: center;
            padding: 30px 20px;
            margin-top: 40px;
            border-top: 1px solid rgba(33, 163, 102, 0.25);
            color: #94A3B8;
            font-size: 0.9rem;
            background: rgba(18, 61, 43, 0.55);
            border-radius: 16px;
        }

        @media (max-width: 768px) {
            .hero-banner {
                padding: 18px 20px !important;
            }
            .hero-title {
                font-size: 1.55rem !important;
            }
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero(farmer_name: Optional[str] = None, is_mr: bool = True):
    """Renders the visually rich hero section."""
    if farmer_name:
        greeting = f"🌱 नमस्कार, {farmer_name}!" if is_mr else f"🌱 Welcome back, {farmer_name}!"
        title = f"{greeting} — पेरू रोग निदान प्रणाली" if is_mr else f"{greeting} — Guava Diagnostic Studio"
        subtitle = (
            "आपल्या वैयक्तिक शेतकरी खात्यात आपले स्वागत आहे. पेरू पिकाचे फोटो तपासा, "
            "इतिहास पहा आणि अचूक कृषी उपचार मिळवा."
            if is_mr else
            "Access your private diagnostic history, submit leaf scans for AI analysis, and receive certified agricultural remedies."
        )
    else:
        title = "🌿 पेरू ॲग्री-एआय रोग निदान प्रणाली" if is_mr else "🌿 Guava Agri-AI Smart Diagnostic Studio"
        subtitle = (
            "खोल न्यूरल नेटवर्क (Deep Learning), स्पष्टीकरणात्मक एआय (Grad-CAM), "
            "आणि अचूक कृषी उपायांसह पेरूच्या बागांचे स्मार्ट संरक्षण."
            if is_mr else
            "Enterprise-grade Foliage & Fruit Pathology Diagnostic Suite powered by ResNet-50 & EfficientNet-B3 with Grad-CAM Explainable AI."
        )

    badge1 = "🎯 96.26% AI Accuracy" if not is_mr else "🎯 ९६.२६% अचूकता"
    badge2 = "🔬 Grad-CAM Heatmap" if not is_mr else "🔬 उष्णता नकाशा (XAI)"
    badge3 = "👥 Multi-Farmer Secure" if not is_mr else "👥 बहु-शेतकरी सुरक्षित खाते"
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
    last_date: Optional[str] = None,
    is_mr: bool = True
):
    """Renders 4 glowing agricultural metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    t1 = "माझ्या एकूण तपासण्या" if is_mr else "Total Diagnoses"
    s1 = "वैयक्तिक नोंदी" if is_mr else "Personal Scans"

    t2 = "निरोगी नमुने" if is_mr else "Healthy Leaves"
    s2 = "रोगमुक्त झाडे" if is_mr else "Disease-Free"

    t3 = "रोग निदान प्रकरणे" if is_mr else "Pathologies Found"
    s3 = "उपचार आवश्यक" if is_mr else "Treatments Required"

    t4 = "शेवटची तपासणी" if is_mr else "Last Diagnosis"
    disp_date = last_date.split()[0] if last_date else ("--" if not is_mr else "--")
    s4 = "नोंद तारीख" if is_mr else "Date of Activity"

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
            <div class="metric-card-value" style="color: #D8F36A;">{healthy_count}</div>
            <div class="metric-card-subtitle" style="color: #21A366;">{s2}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">⚠️</span>
            <div class="metric-card-title">{t3}</div>
            <div class="metric-card-value" style="color: #FFC857;">{diseased_count}</div>
            <div class="metric-card-subtitle" style="color: #FFA500;">{s3}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-card-icon">📅</span>
            <div class="metric-card-title">{t4}</div>
            <div class="metric-card-value" style="font-size: 1.35rem; color: #38BDF8;">{disp_date}</div>
            <div class="metric-card-subtitle" style="color: #94A3B8;">{s4}</div>
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
        <strong style="color: #FFC857; font-size: 1.02rem;">{disc_title}</strong><br>
        <span style="display: block; margin-top: 6px;">{disc_text}</span>
    </div>
    """, unsafe_allow_html=True)

def render_agri_footer(is_mr: bool = True):
    """Renders the clean agricultural AI footer."""
    line1 = "पेरू ॲग्री-एआय बहु-शेतकरी स्मार्ट रोग निदान व्यासपीठ" if is_mr else "Guava Agri-AI Multi-Farmer Smart Diagnostic Platform"
    line2 = (
        "अंतिम वर्ष अभियांत्रिकी शैक्षणिक प्रकल्प (२०२६–२०२७) | विकसित: Deep Learning, PyTorch आणि Streamlit"
        if is_mr else
        "Final Year Engineering Academic Capstone Project (2026–2027) | Powered by Deep Learning, PyTorch & Streamlit"
    )
    st.markdown(f"""
    <div class="modern-footer">
        <div style="font-weight: 700; color: #D8F36A; font-size: 1.05rem; margin-bottom: 4px;">🌿 {line1}</div>
        <div style="font-size: 0.88rem; color: #94A3B8;">{line2}</div>
        <div style="font-size: 0.82rem; color: #64748B; margin-top: 6px;">
            © 2026–2027 Guava Disease Detection System | Multi-User Secure SQLite Authentication
        </div>
    </div>
    """, unsafe_allow_html=True)
