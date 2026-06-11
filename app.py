import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# 🎨 التنسيقات الذهبية النقية - الصناديق أصبحت توأماً حقيقياً 100% بدون أي أزرار ميكانيكية زائدة
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
    
    /* 🔵 صندوق العدادات الموحد تماماً - حجم، زوايا، وخلفية زرقاء متطابقة */
    .metric-box-twin-final { 
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
    .metric-val-twin-final { font-size: 26px; font-weight: bold; line-height: 1.1; color: white !important; }
    .metric-lbl-twin-final { font-size: 13px; opacity: 0.95; margin-top: 5px; color: white !important; }
    
    /* جعل الحاوية اليمنى تفاعلية بالكامل مع الماوس */
    .clickable-card-container {
        display: block;
        text-decoration: none !important;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        width: 100%;
        height: 85px;
    }
    .clickable-card-container:hover {
        transform: translateY(-3px);
        filter: brightness(1.15);
    }
    
    div.stButton > button, div.stDownloadButton > button { border: none; padding: 8px 12px; border-radius: 8px; font-weight: 700; transition: all 0.3s ease; width: 100%; height: 40px; margin-top: 2px; margin-bottom: 2px; }
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

# التقاط حدث الضغط المباشر على بطاقة المنطقة جغرافيا لتجنب أزرار Streamlit
query_params = st.query_params
if "action" in query_params and query_params["action"] == "open_sheet":
    st.session_state.show_excel_sheet = True
    # تنظيف الرابط فوراً لمنع التكرار اللانهائي
    st.query_params.clear()

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v7.0</div></div>""", unsafe_allow_html=True)
    
    if not st.session_state.file_uploaded:
        st.markdown("### 📥 خطوة 1: رفع ملف البيانات الاحتياطي")
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) الذي قمت بتنزيله سابقاً لاستعادة الأعداد والمتابعة:", type=["csv"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                st.session_state.local_db = uploaded_df[["المنطقة", "رقم العقار"]]
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل الملف بنجاح واستعادة كافة البيانات!")
                st.rerun()  
            except Exception as e:
                st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db
    st.markdown("---")
    
    # حقول الإدخال الأساسية الثنائية (المنطقة والعقار)
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="ادخل اسم المنطقة الحالية ....", key="region_field").strip()
    with c2:
        prop_val = "" if st.session_state.clear_trigger else ""
