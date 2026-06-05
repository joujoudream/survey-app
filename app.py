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
        df = pd.read_csv(DATA_FILE, dtype={"رقم العقار": str})
    except:
        df = pd.DataFrame(columns=["اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])
else:
    df = pd.DataFrame(columns=["اسم الشركة", "اسم المشروع", "المنطقة", "رقم العقار"])

# الواجهة الرئيسية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ منظومة إدخال بيانات مسح الأضرار المحدثة</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# القسم الأول: معلومات العمل
st.markdown("### 🏢 معلومات العمل الأساسية")
company_name = st.text_input("اسم الشركة", value="Khatib & Alami")
project_name = st.text_input("اسم المشروع")

# القسم الثاني: المنطقة والعقار والبحث الذكي
st.markdown("### 📍 تفاصيل الموقع والتحقق من التكرار")
region_input = st.text_input("أدخل اسم المنطقة:").strip()

# منطق البحث التلقائي بمجرد الكتابة
if region_input != "":
    filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
    total_properties = len(filtered_df)
    
    if total_properties > 0:
        st.info(f"📊 **معلومات سابقة للمنطقة ({region_input}):**")
        st.write(f"🔢 **عدد العقارات المسجلة سابقاً هنا:** {total_properties} عقار")
        previous_numbers = filtered_df["رقم العقار"].unique()
        st.write("📋 **أرقام العقارات المسجلة سابقاً في هذه المنطقة:**")
        st.code(", ".join(map(str, previous_numbers)))
    else:
        st.success(f"✨ هذه المنطقة ({region_input}) جديدة تماماً، لا توجد عقارات مسجلة لها مسبقاً.")

property_number = st.text_input("أدخل رقم العقار الجديد المراد تسجيله:").strip()

# زر الحفظ مع ميزة منع التكرار
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 حفظ البيانات وإضافتها للجدول السحابي"):
    if company_name and project_name and region_input and property_number:
        # التحقق إذا كان رقم العقار موجوداً مسبقاً في نفس المنطقة
        is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                          (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
        
        if is_duplicate:
            st.error(f"⚠️ **تنبيه:** رقم العقار ({property_number}) موجود بالفعل في منطقة ({region_input})! تم إلغاء الزيادة لمنع التكرار.")
        else:
            new_row = {
                "اسم الشركة": company_name,
                "اسم المشروع": project_name,
                "المنطقة": region_input,
                "رقم العقار": property_number
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ تم حفظ البيانات بنجاح في السحابة!")
            st.rerun()
    else:
        st.error("⚠️ يرجى ملء جميع الحقول أولاً قبل الحفظ.")

# عرض الجدول الإجمالي مع خاصية الحذف
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 🗂️ قاعدة البيانات الإجمالية وإدارة المدخلات")

if not df.empty:
    # عرض الجدول للمراجعة
    st.dataframe(df, use_container_width=True)
    
    # قسم الحذف المخصص
    st.markdown("### 🗑️ حذف سطر أو عقار خاطئ")
    # إنشاء قائمة بالأسطر المتاحة للحذف لسهولة الاختيار
    delete_options = [f"سطر {i}: {row['المنطقة']} - عقار رقم ({row['رقم العقار']})" for i, row in df.iterrows()]
    selected_to_delete = st.selectbox("اختر العقار الذي تريد حذفه نهائياً:", options=delete_options)
    
    if st.button("❌ تأكيد حذف العقار المحدد"):
        # الحصول على رقم السطر (Index) من النص المحدد
        index_to_delete = int(selected_to_delete.split(":")[0].replace("سطر ", ""))
        # حذف السطر وإعادة ترتيب الجدول
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("🗑️ تم حذف العقار بنجاح وتحديث قاعدة البيانات!")
        st.rerun()
else:
    st.info("📂 قاعدة البيانات فارغة حالياً.")

# زر لتحميل البيانات مباشرة للحاسوب
csv_buffer = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 تحميل الجدول الإجمالي كـ ملف CSV للعمل",
    data=csv_buffer,
    file_name="damage_survey_report.csv",
    mime="text/csv"
)
