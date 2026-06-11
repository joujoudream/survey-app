import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# 🎨 التنسيقات الذهبية الصارمة - إبقاء الأزرار الأصلية وتطهير المربع الأبيض نهائياً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    header[data-testid="stHeader"] { background: transparent !important; height: 0px !important; display: none !important; }
    
    .block-container { 
        padding-top: 2.5rem !important; 
        padding-bottom: 1rem !important; 
    }
    
    .header-card { 
        background-color: #EBF8FF; 
        padding: 24px 12px 20px 12px; 
        border-radius: 12px; 
        box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08); 
        margin-top: 10px; 
        margin-bottom: 2px; 
        text-align: center; 
        border: 1px solid #BEE3F8; 
    }
    .company-header { color: #1E3A8A; font-family: 'Arial', sans-serif; font-size: 30px; font-weight: bold; margin: 0; line-height: 1.2; }
    .company-subtitle { color: #2D3748; font-family: 'Arial', sans-serif; font-size: 16px; font-weight: 500; margin-top: 6px; }
    
    .main-signature-card { 
        background-color: #ffffff; 
        padding: 8px 16px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04); 
        margin-top: 4px; 
        margin-bottom: 12px; 
        border: 1px solid #e2e8f0; 
        width: 100%; 
        max-width: 550px; 
        margin-left: auto; 
        margin-right: auto; 
    }
    .sig-title { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; color: #1E3A8A; margin: 0; }
    .sig-name { font-family: 'Arial', sans-serif; font-size: 14px; font-weight: bold; color: #475569; margin: 2px 0; }
    .sig-note { font-size: 11px; color: #3b82f6; font-weight: 500; margin: 0; }
    
    /* 🔴 زر حفظ العقار باللون الأحمر الناري الأصلي */
    div.red-save-btn div.stButton > button {
        background-color: #EF4444 !important;
        color: white !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100% !important;
        height: 44px !important;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2) !important;
        transition: all 0.2s ease;
    }
    div.red-save-btn div.stButton > button:hover { background-color: #DC2626 !important; }
    
    /* ⚪ زر تحميل ملف الإكسيل باللون الأبيض الأصلي */
    div.white-download-btn div.stDownloadButton > button, div.white-download-btn div.stButton > button {
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        border: 1px solid #CBD5E1 !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100% !important;
        height: 44px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease;
    }
    div.white-download-btn div.stDownloadButton > button:hover { background-color: #F8FAFC !important; border-color: #94A3B8 !important; }
    
    /* 🔵 تصميم الصناديق الزرقاء الموحدة الملكية */
    .metric-box-twin { 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
        color: white !important; 
        padding: 12px 15px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.15); 
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
        text-decoration: none !important;
    }
    .metric-val-twin { font-size: 26px; font-weight: bold; line-height: 1.1; color: white !important; }
    .metric-lbl-twin { font-size: 13px; opacity: 0.95; margin-top: 5px; color: white !important; }
    
    /* جعل الحاوية اليسرى رابطاً تفاعلياً نظيفاً 100% مستحيل ينتج مربع أبيض */
    .clickable-card-link {
        display: block;
        text-decoration: none !important;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        width: 100%;
        height: 85px;
    }
    .clickable-card-link:hover {
        transform: translateY(-3px);
        filter: brightness(1.15);
    }
    
    div[data-testid="stVerticalBlock"] > div { depth: 0 !important; margin-bottom: -0.3rem !important; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    [data-testid="stInputInstructions"] { display: none !important; visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة الـ Session State
if "local_db" not in st.session_state:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False
if "show_excel_sheet" not in st.session_state: st.session_state.show_excel_sheet = False

# التقاط حدث الضغط المباشر على بطاقة المنطقة جغرافياً بدون عناصر أزرار Streamlit
current_params = st.query_params
if "view" in current_params and current_params["view"] == "excel_sheet":
    st.session_state.show_excel_sheet = True
    st.query_params.clear() # تنظيف الرابط فوراً لحفظ السلاسة

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>صمم بعناية لأجل دقة
