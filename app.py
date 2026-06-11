import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# 🎨 تصميم التنسيقات النظيفة وتطهير الهوامش والمربعات الزائدة نهائياً
css_style = """
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

/* 🔴 زر حفظ العقار باللون الأحمر الأصلي */
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

/* ⚪ أزرار التحميل والتعديل باللون الأبيض الأصلي والحواف الخفيفة */
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

/* 🔵 تصميم الصناديق الزرقاء الموحدة للعدادات الكلاسيكية */
.metric-box-twin { 
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
    color: white !important; 
    padding: 12px 15px; 
    border-radius: 10px; 
    text-align: center; 
    box-shadow: 0 4px 8px rgba(3
