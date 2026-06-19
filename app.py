import streamlit as st
import pandas as pd
import requests
import base64
import os
from PIL import Image

# 🌐 1. إعدادات الصفحة الرسمية للشركة
st.set_page_config(
    page_title="Khatib & Alami Company", 
    page_icon="K_and_A_icon.ico" if os.path.exists("K_and_A_icon.ico") else "🏢", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔑 إعدادات الربط التلقائي بمنصة GitHub
GITHUB_TOKEN = "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع_YOUR_USERNAME/YOUR_REPO"
GITHUB_FILENAME = "KhatibAlami_Midan_Data.csv"

def upload_to_github(dataframe):
    try:
        csv_content = dataframe.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True).to_csv(index=False).encode('utf-8-sig')
        encoded_content = base64.b64encode(csv_content).decode('utf-8')
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILENAME}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        data = {"message": "تحديث تلقائي لسجل العقارات الميداني - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except Exception as e:
        return False

# 🎨 الستايل الجديد القوي والمباشر لاستهداف التحديث الأخير لـ Streamlit مجدداً وضمان التغيير
ultimate_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');

/* توحيد الخط والاتجاه */
html, body, [class*='css'], [data-testid="stAppViewContainer"] { 
    font-family: 'Tajawal', sans-serif !important; 
    direction: rtl !important; 
    text-align: right !important; 
}
.stApp { 
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; 
}
header[data-testid='stHeader'] { 
    background: transparent !important; 
    display: none !important; 
}

/* هيدر الشركة والموقع */
.header-card { 
    background-color: #EBF8FF !important; 
    padding: 20px 12px !important; 
    border-radius: 12px !important; 
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08) !important; 
    margin-bottom: 2px !important; 
    text-align: center !important; 
    border: 1px solid #BEE3F8 !important; 
}
.company-header { 
    color: #1E3A8A !important; 
    font-family: 'Arial', sans-serif !important; 
    font-size: 28px !important; 
    font-weight: bold !important; 
}
.company-subtitle { 
    color: #2D3748 !important; 
    font-size: 15px !important; 
    font-weight: 500 !important; 
    margin-top: 4px !important; 
}
.main-signature-card { 
    background-color: #ffffff !important; 
    padding: 14px 16px !important; 
    border-radius: 10px !important; 
    text-align: center !important; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04) !important; 
    margin: 10px auto 20px auto !important; 
    border: 1px solid #e2e8f0 !important; 
    max-width: 550px !important; 
}

/* 🚨 1. إصلاح وتوسيع الأزرار التشغيلية الحمراء (توسيع العرض لملء الحاوية بالكامل) */
div[data-testid="stColumn"] button, 
div[data-testid="element-container"] button,
button[data-testid*="baseButton"] {
    background-color: #EF4444 !important;
    color: white !important;
    border: 1px solid #DC2626 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    height: 54px !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 6px rgba(239, 68, 68, 0.25) !important;
    width: 100% !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}
div[data-testid="stColumn"] button:hover,
button[data-testid*="baseButton"]:hover {
    background-color: #DC2626 !important;
    box-shadow: 0 6px 12px rgba(220, 38, 38, 0.4) !important;
}

/* 🔵 2. تعديل وتثبيت خلفية المربع الإحصائي الأزرق الكبير (مجموع العقارات) */
div[data-testid="stMetric"], 
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    text-align: center !important;
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.2) !important;
    border: none !important;
    height: 110px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}
div[data-testid="stMetric"] *, 
[data-testid="metric-container"] * {
    color: white !important;
}

/* 🔵 3. استهداف زر إحصاء المنطقة التفاعلي وجعله متطابقاً تماماً في الحجم والخلفية الزرقاء مع المربع الكبير */
div.midan-container button {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    height: 110px !important; /* تطابق تام في الارتفاع */
    width: 100% !important;
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.2) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: pre-line !important;
}
div.midan-container button:hover {
    background: linear-gradient(135deg, #172554 0%, #1D4ED8 100%) !important;
    box-shadow: 0 8px 16px rgba(29, 78, 216, 0.35) !important;
}

div[data-testid='stHorizontalBlock'] { gap: 16px !important; }
[data-testid='stInputInstructions'] { display: none !important; visibility: hidden !important; }
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# إدارة الذاكرة المحلية للجلسة
if "local_db" not in st.session_state: st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
if "file_uploaded" not in st.session_state: st.session_state.file_uploaded = False
if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False

col1, col2, col3 = st.columns(
