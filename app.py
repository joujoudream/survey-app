import streamlit as st
import pandas as pd
import os

# إعدادات بسيطة
st.set_page_config(page_title="Khatib & Alami", layout="centered")

# تنسيق الواجهة (شكل ثابت ومريح للعين)
st.markdown("""
    <style>
    .main-title { text-align: center; color: #1E3A8A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏢 Khatib & Alami Company</h1>", unsafe_allow_html=True)
st.subheader("نظام الإدخال الميداني")

# تحميل البيانات
if not os.path.exists("KhatibAlami_Midan_Data.csv"):
    df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
    df.to_csv("KhatibAlami_Midan_Data.csv", index=False, encoding='utf-8-sig')
else:
    df = pd.read_csv("KhatibAlami_Midan_Data.csv", dtype=str)

# حقول الإدخال
region = st.text_input("📍 المنطقة")
prop = st.text_input("🔢 رقم العقار")

# زر الحفظ المباشر
if st.button("💾 حفظ"):
    if region and prop:
        new_entry = pd.DataFrame({"المنطقة": [region], "رقم العقار": [prop]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv("KhatibAlami_Midan_Data.csv", index=False, encoding='utf-8-sig')
        st.success("تم الحفظ!")
        st.rerun() # تحديث الصفحة لرؤية الإضافة فوراً
    else:
        st.error("يرجى تعبئة الحقول المطلوبة")

# عرض البيانات
st.write("---")
st.table(df.tail(10)) # عرض آخر 10 عقارات دخلت
