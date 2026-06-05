import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة والخطوط لتناسب اللغة العربية
st.set_page_config(page_title="برنامج مسح الأضرار الذكي", layout="centered")
st.markdown("""
    <style>
    body { background-color: #f8f9fa; }
    h1, h2, h3, p, label, .stMarkdown { text-align: right; direction: rtl; font-family: 'Arial', sans-serif; }
    .stTextInput input, .stSelectbox div { text-align: right; direction: rtl; }
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; width: 100%; font-size: 18px; }
    .stAlert p { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# اسم ملف البيانات السحابي
DATA_FILE = "survey_data.csv"

# تحميل البيانات السابقة أو إنشاء جدول جديد
if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE)
    except:
        df = pd.DataFrame(columns=["اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])
else:
    df = pd.DataFrame(columns=["اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])

# الواجهة الرئيسية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ منظومة إدخال بيانات مسح الأضرار</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# القسم الأول: معلومات العمل
st.markdown("### 🏢 معلومات العمل الأساسية")
company_name = st.text_input("اسم الشركة", value="Khatib & Alami")
project_name = st.text_input("اسم المشروع")

# القسم الثاني: المنطقة والعقار والبحث الذكي
st.markdown("### 📍 تفاصيل الموقع والبحث التلقائي")
region_input = st.text_input("أدخل اسم المنطقة:")

# منطق البحث التلقائي بمجرد الكتابة
if region_input.strip() != "":
    # تصفية الجدول بناءً على المنطقة
    filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.strip().lower()]
    total_properties = len(filtered_df)
    
    if total_properties > 0:
        st.info(f"📊 **معلومات سابقة للمنطقة ({region_input}):**")
        st.write(f"🔢 **عدد العقارات المسجلة سابقاً هنا:** {total_properties} عقار")
        
        # عرض أرقام العقارات السابقة
        previous_numbers = filtered_df["رقم العقار"].unique()
        st.write("📋 **أرقام العقارات المسجلة سابقاً في هذه المنطقة:**")
        st.code(", ".join(map(str, previous_numbers)))
    else:
        st.success(f"✨ هذه المنطقة ({region_input}) جديدة تماماً، لا توجد عقارات مسجلة لها مسبقاً.")

property_number = st.text_input("أدخل رقم العقار الجديد المراد تسجيله:")

# زر الحفظ
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 حفظ البيانات وإضافتها للجدول السحابي"):
    if company_name and project_name and region_input and property_number:
        new_row = {
            "اسم الشركة": company_name,
            "اسم المشروع": project_name,
            "المنطقة": region_input.strip(),
            "رقم العقار": property_number.strip()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ تم حفظ البيانات بنجاح في السحابة!")
        st.rerun()
    else:
        st.error("⚠️ يرجى ملء جميع الحقول أولاً قبل الحفظ.")

# عرض الجدول الإجمالي في الأسفل مع إمكانية تحميله كملف Excel/CSV
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 🗂️ قاعدة البيانات الإجمالية المحدثة")
st.dataframe(df, use_container_width=True)

# زر لتحميل البيانات مباشرة للحاسوب في أي وقت
csv_buffer = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 تحميل الجدول الإجمالي كـ ملف CSV للعمل",
    data=csv_buffer,
    file_name="damage_survey_report.csv",
    mime="text/csv"
)
