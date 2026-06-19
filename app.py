import streamlit as st
import pandas as pd
import requests
import base64
import os

# 🌐 إعدادات الصفحة
st.set_page_config(page_title="Khatib & Alami", page_icon="🏢", layout="centered")

# 🎨 تنسيق CSS لضمان الشكل الجمالي (كما في image_3be47b.jpg)
st.markdown("""
<style>
    .header-card { background-color: #EBF8FF; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #BEE3F8; }
    .company-header { color: #1E3A8A; font-size: 28px; font-weight: bold; }
    .company-subtitle { color: #2D3748; font-size: 15px; margin-top: 5px; }
    .sig-name { color: #E53E3E; font-size: 18px; font-weight: bold; margin-top: 10px; }
    div.stButton > button { background-color: #EF4444; color: white; font-weight: bold; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# 🛠️ دالة حفظ البيانات
def save_data(df):
    df.to_csv("KhatibAlami_Data.csv", index=False, encoding='utf-8-sig')

# 📋 تحميل البيانات
if "df" not in st.session_state:
    if os.path.exists("KhatibAlami_Data.csv"):
        st.session_state.df = pd.read_csv("KhatibAlami_Data.csv", dtype=str)
    else:
        st.session_state.df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🏗️ بناء الواجهة (مطابق للتصميم المطلوب)
st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div><div class='sig-name'>Printing & Archiving - S,Walid Mrad</div></div>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    region = st.text_input("📍 اسم المنطقة الجغرافية")
with col2:
    prop = st.text_input("🔢 رقم العقار الجديد")

if st.button("🚀 حفظ العقار والتحقق من التكرار"):
    if region and prop:
        # فحص التكرار
        if not ((st.session_state.df['المنطقة'] == region) & (st.session_state.df['رقم العقار'] == prop)).any():
            new_row = pd.DataFrame({"المنطقة": [region], "رقم العقار": [prop]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            save_data(st.session_state.df)
            st.success("✅ تم حفظ العقار بنجاح!")
        else:
            st.warning("⚠️ هذا العقار مسجل مسبقاً في هذه المنطقة.")
    else:
        st.error("❌ يرجى ملء كافة الحقول.")

# عرض سريع لآخر المدخلات
st.write("### 📊 السجل الأخير")
st.dataframe(st.session_state.df.tail(5), use_container_width=True)
