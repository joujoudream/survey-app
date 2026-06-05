import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. إعدادات الصفحة والجماليات (CSS الاحترافي)
st.set_page_config(page_title="نظام مسح الأضرار | الاحترافي", layout="wide", initial_sidebar_state="collapsed")

# حقن CSS مخصص لتحسين الواجهة بشكل جذري
st.markdown("""
    <style>
    /* استيراد خطوط عربية جميلة */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* خلفية الصفحة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* تصميم البطاقة الرئيسية للمدخلات */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }

    /* تحسين العناوين */
    h1 { color: #1E3A8A; font-weight: 700; font-size: 32px; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }
    h3 { color: #334155; font-size: 20px; margin-top: 20px; }

    /* تحسين الأزرار */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }

    /* تحسين جداول البيانات */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .stAlert { border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة البيانات
DATA_FILE = "survey_data.csv"

if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE, dtype={"رقم العقار": str})
    except:
        df = pd.DataFrame(columns=["تاريخ الإدخال", "اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])
else:
    df = pd.DataFrame(columns=["تاريخ الإدخال", "اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])

# 3. محتوى الصفحة
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='border:none;'>🏢 نظام مسح الأضرار والمتابعة الميدانية</h1>
        <p style='color: #64748b; font-size: 18px;'>أداة مهنية متطورة لإدارة البيانات بدقة وسرعة</p>
    </div>
""", unsafe_allow_html=True)

# استخدام الأعمدة لتنظيم المساحة
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    st.markdown("### 📋 إدخال بيانات عقار جديد")
    
    # توزيع المدخلات في أعمدة داخل البطاقة
    c1, c2 = st.columns(2)
    with c1:
        company_name = st.text_input("🏢 اسم الشركة", value="Khatib & Alami")
        region_input = st.text_input("📍 اسم المنطقة").strip()
    with c2:
        project_name = st.text_input("🏗️ اسم المشروع")
        property_number = st.text_input("🔢 رقم العقار").strip()

    # فحص المنطقة فور الكتابة
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        if not filtered_df.empty:
            st.info(f"💡 المنطقة مسجلة مسبقاً وبها **{len(filtered_df)}** عقارات.")
            with st.expander("👁️ عرض أرقام العقارات الحالية"):
                st.write(", ".join(filtered_df["رقم العقار"].unique()))
        else:
            st.success("✨ منطقة جديدة")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر الحفظ
    if st.button("🚀 حفظ العقار في قاعدة البيانات"):
        if company_name and project_name and region_input and property_number:
            # التحقق من التكرار
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                              (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            
            if is_duplicate:
                st.error(f"❌ خطأ: العقار رقم ({property_number}) مسجل مسبقاً في منطقة ({region_input})!")
            else:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_row = {
                    "تاريخ الإدخال": now,
                    "اسم الشركة": company_name,
                    "اسم المشروع": project_name,
                    "المنطقة": region_input,
                    "رقم العقار": property_number
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ تم الحفظ بنجاح!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، أكمل جميع البيانات")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 4. عرض البيانات وإدارة الحذف
st.markdown("---")
st.markdown("### 📊 قاعدة البيانات المسجلة")

if not df.empty:
    # عرض الجدول بتنسيق أنيق
    st.dataframe(df, use_container_width=True)
    
    # لوحة إدارة متطورة في الأسفل
    m1, m2 = st.columns([2, 1])
    
    with m1:
        st.markdown("#### 🗑️ إدارة السجلات")
        delete_options = [f"{i} | {row['المنطقة']} - عقار {row['رقم العقار']}" for i, row in df.iterrows()]
        to_delete = st.selectbox("اختر السطر المراد حذفه:", options=delete_options)
        if st.button("🗑️ حذف السجل المختار نهائياً"):
            idx = int(to_delete.split(" | ")[0])
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("تم الحذف بنجاح")
            st.rerun()
            
    with m2:
        st.markdown("#### 📥 التقارير")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 تحميل التقرير (Excel/CSV)",
            data=csv,
            file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
else:
    st.info("لا توجد بيانات مسجلة حالياً.")

st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #94a3b8; font-size: 14px;'>
        نظام مسح الأضرار الذكي v2.0 | تم التصميم لأجل التميز والراحة
    </div>
""", unsafe_allow_html=True)
