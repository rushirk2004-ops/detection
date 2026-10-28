"""
Bilingual Translation Dictionary: Guava Agri-AI Multi-Farmer Platform
Provides comprehensive translations in Marathi (मराठी) and English (en)
for registration, authentication, personal dashboard, diagnosis, history, and admin features.
"""

TRANSLATIONS = {
    # Navigation and General
    "app_title": {
        "en": "Guava Agri-AI | Smart Multi-Farmer Diagnostic Platform",
        "mr": "पेरू ॲग्री-एआय | स्मार्ट शेतकरी रोग निदान व्यासपीठ"
    },
    "tagline": {
        "en": "Deep Learning Agricultural Pathology & Farm Advisory",
        "mr": "खोल न्यूरल नेटवर्क व आधुनिक शेती सल्लागार"
    },
    "nav_farmer_portal": {
        "en": "🌿 Farmer Portal",
        "mr": "🌿 शेतकरी दालन"
    },
    "nav_admin_portal": {
        "en": "🛡️ Admin Portal",
        "mr": "🛡️ प्रशासकीय दालन"
    },
    "nav_sign_in": {
        "en": "🔑 Farmer Sign In",
        "mr": "🔑 शेतकरी लॉगिन"
    },
    "nav_sign_up": {
        "en": "📝 Farmer Registration",
        "mr": "📝 नवीन शेतकरी नोंदणी"
    },
    "nav_diagnosis": {
        "en": "🔬 AI Disease Detection",
        "mr": "🔬 AI रोग निदान"
    },
    "nav_my_history": {
        "en": "📜 My Diagnosis History",
        "mr": "📜 माझा तपासणी इतिहास"
    },
    "nav_profile": {
        "en": "👤 My Farmer Profile",
        "mr": "👤 माझे प्रोफाइल"
    },
    "logout_btn": {
        "en": "🚪 Log Out",
        "mr": "🚪 बाहेर पडा (लॉगआउट)"
    },

    # Registration Form
    "reg_title": {
        "en": "📝 Register New Farmer Account",
        "mr": "📝 नवीन शेतकरी खाते नोंदणी करा"
    },
    "reg_subtitle": {
        "en": "Create your private account to analyze guava crops, track diagnoses, and access expert treatment.",
        "mr": "पेरू पिकाचे रोग निदान, अहवाल आणि तज्ज्ञ कृषी सल्ल्यासाठी आपले वैयक्तिक खाते तयार करा."
    },
    "full_name": {
        "en": "Full Name",
        "mr": "पूर्ण नाव"
    },
    "username": {
        "en": "Username (unique ID)",
        "mr": "वापरकर्ता नाव (युझरनेम)"
    },
    "mobile_number": {
        "en": "Mobile Number (10 Digits)",
        "mr": "मोबाईल नंबर (१० अंकी)"
    },
    "email_optional": {
        "en": "Email Address (Optional)",
        "mr": "ईमेल पत्ता (ऐच्छिक)"
    },
    "village": {
        "en": "Village / गाव",
        "mr": "गाव"
    },
    "taluka": {
        "en": "Taluka / तालुका",
        "mr": "तालुका"
    },
    "district": {
        "en": "District / जिल्हा",
        "mr": "जिल्हा"
    },
    "state": {
        "en": "State / राज्य",
        "mr": "राज्य"
    },
    "password": {
        "en": "Password (min 6 characters)",
        "mr": "पासवर्ड (किमान ६ अक्षरे)"
    },
    "confirm_password": {
        "en": "Confirm Password",
        "mr": "पासवर्डची पुष्टी करा"
    },
    "register_submit_btn": {
        "en": "🚀 Register Farmer Account",
        "mr": "🚀 शेतकरी खाते तयार करा"
    },
    "already_have_account": {
        "en": "Already have an account? Switch to 'Farmer Sign In' above.",
        "mr": "आधीच खाते आहे का? वरील 'शेतकरी लॉगिन' पर्याय निवडा."
    },

    # Login Form
    "login_title": {
        "en": "🔐 Farmer Account Sign In",
        "mr": "🔐 शेतकरी खाते लॉगिन"
    },
    "login_subtitle": {
        "en": "Enter your username and password to access your personalized farming dashboard.",
        "mr": "आपल्या शेती अहवालांमध्ये प्रवेश करण्यासाठी युझरनेम आणि पासवर्ड टाका."
    },
    "login_submit_btn": {
        "en": "🔓 Sign In & Access Dashboard",
        "mr": "🔓 लॉगिन करा"
    },
    "dont_have_account": {
        "en": "New farmer? Click 'Farmer Registration' to create a free account.",
        "mr": "नवीन शेतकरी आहात का? मोफत खात्यासाठी 'नवीन शेतकरी नोंदणी' वर क्लिक करा."
    },

    # Dashboard
    "welcome_farmer": {
        "en": "Welcome, Farmer",
        "mr": "स्वागत आहे, शेतकरी बंधू"
    },
    "farmer_id_badge": {
        "en": "Farmer ID",
        "mr": "शेतकरी आयडी"
    },
    "total_personal_diagnoses": {
        "en": "My Total Diagnoses",
        "mr": "माझ्या एकूण तपासण्या"
    },
    "healthy_samples": {
        "en": "Healthy Samples",
        "mr": "निरोगी नमुने"
    },
    "disease_cases": {
        "en": "Diseases Detected",
        "mr": "रोग आढळलेले नमुने"
    },
    "last_diagnosis_date": {
        "en": "Last Diagnosis",
        "mr": "शेवटची तपासणी"
    },
    "no_diagnoses_yet": {
        "en": "No diagnoses recorded yet",
        "mr": "अद्याप कोणतीही तपासणी झालेली नाही"
    },

    # Profile & Password Update
    "profile_header": {
        "en": "Farmer Profile Information",
        "mr": "शेतकरी प्रोफाइल माहिती"
    },
    "update_profile_btn": {
        "en": "💾 Save Profile Changes",
        "mr": "💾 प्रोफाइल बदल जतन करा"
    },
    "change_password_header": {
        "en": "Change Account Password",
        "mr": "पासवर्ड बदला"
    },
    "current_password": {
        "en": "Current Password",
        "mr": "सध्याचा पासवर्ड"
    },
    "new_password": {
        "en": "New Password (min 6 characters)",
        "mr": "नवीन पासवर्ड (किमान ६ अक्षरे)"
    },
    "confirm_new_password": {
        "en": "Confirm New Password",
        "mr": "नवीन पासवर्डची पुष्टी करा"
    },
    "update_password_btn": {
        "en": "🔒 Update Password",
        "mr": "🔒 नवीन पासवर्ड लागू करा"
    },

    # History Page
    "history_title": {
        "en": "📜 My Diagnosis History",
        "mr": "📜 माझा तपासणी इतिहास"
    },
    "history_subtitle": {
        "en": "Private records of your past guava foliage and fruit disease scans.",
        "mr": "तुमच्या पेरूच्या झाडांच्या तपासण्यांचा वैयक्तिक इतिहास व उपाययोजना."
    },
    "filter_target": {
        "en": "Filter by Target",
        "mr": "तपासणी प्रकारानुसार निवडा"
    },
    "filter_disease": {
        "en": "Filter by Disease",
        "mr": "रोग प्रकारानुसार निवडा"
    },
    "delete_record_btn": {
        "en": "🗑️ Delete Record",
        "mr": "🗑️ नोंद हटवा"
    },
    "record_deleted": {
        "en": "Diagnosis record deleted successfully.",
        "mr": "तपासणी नोंद यशस्वीरित्या हटवली."
    },

    # AI Detection
    "analyze_btn": {
        "en": "🔍 Analyze Foliage Now",
        "mr": "🔍 पानाचे विश्लेषण करा"
    },
    "camera_option": {
        "en": "📸 Use Device Camera",
        "mr": "📸 थेट कॅमेरा वापरा"
    },
    "upload_option": {
        "en": "📁 Upload Image File",
        "mr": "📁 फोटो फाईल निवडा"
    },
    "saved_to_history": {
        "en": "✅ Analysis successfully recorded to your personal history!",
        "mr": "✅ हे निदान तुमच्या वैयक्तिक शेतकरी इतिहासामध्ये जतन करण्यात आले आहे!"
    }
}

def t(key: str, is_mr: bool = False) -> str:
    """Helper function to fetch translated text."""
    lang = "mr" if is_mr else "en"
    if key in TRANSLATIONS and lang in TRANSLATIONS[key]:
        return TRANSLATIONS[key][lang]
    return key
