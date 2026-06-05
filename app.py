import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والجماليات العصرية (CSS الاحترافي)
st.set_page_config(page_title="KhatibAlami Company", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }

    .company-header {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .company-subtitle {
        text-align: center;
        color: #475569;
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-bottom: 30px;
    }

    h3 { color: #334155; font-size: 20px; margin-top: 20px; }

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

    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .stAlert { border-radius: 12px; }

    .footer-section {
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        color: #475569;
        line-height: 1.6;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة البيانات (تم حذف عمود التاريخ والوقت تماماً)
DATA_FILE = "survey_data.csv"

if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE, dtype={"رقم العقار": str})
    except:
        df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
else:
    df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# ترتيب الجدول تلقائياً بحسب اسم المنطقة (أبجدياً) إذا لم يكن فارغاً
if not df.empty:
    df = df.sort_values(by="المنطقة").reset_index(drop=True)

# 3. الهوية الرسمية في أعلى الواجهة
st.markdown("<div class='company-header'>KhatibAlami Company</div>", unsafe_allow_html=True)
st.markdown("<div class='company-subtitle'>War Damage Assessment 2006</div>", unsafe_allow_html=True)

# تنظيم مساحة العمل
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    st.markdown("### 📋 إدخال بيانات عقار جديد")
    
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة").strip()
    with c2:
        property_number = st.text_input("🔢 رقم العقار").strip()

    # فحص المنطقة فوراً أثناء الكتابة لمنع التكرار
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        if not filtered_df.empty:
            st.info(f"💡 المنطقة مسجلة مسبقاً وتحتوي على **{len(filtered_df)}** عقارات مسجلة.")
            with st.expander("👁️ مراجعة أرقام العقارات السابقة في هذه المنطقة"):
                st.write(", ".join(filtered_df["رقم العقار"].unique()))
        else:
            st.success("✨ هذه المنطقة جديدة تماماً ولم تُمسح من قبل.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر الحفظ والتحقق الذكي
    if st.button("🚀 حفظ العقار في قاعدة البيانات السحابية"):
        if region_input and property_number:
            # التحقق التام من التكرار
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                              (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            
            if is_duplicate:
                st.error(f"❌ تنبيه: العقار رقم ({property_number}) مسجل مسبقاً بالفعل في منطقة ({region_input})! تم إلغاء الإضافة لمنع التكرار.")
            else:
                new_row = {
                    "المنطقة": region_input,
                    "رقم العقار": property_number
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                # إعادة الترتيب الأبجدي قبل الحفظ النهائي في الملف
                df = df.sort_values(by="المنطقة").reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ تم حفظ البيانات بنجاح وتحديث السحابة!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى إدخال المنطقة ورقم العقار أولاً.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 4. عرض قاعدة البيانات المرتبة وإدارة السجلات
st.markdown("---")
st.markdown("### 📊 السجلات والتقارير الميدانية (مرتبة أبجدياً حسب المنطقة)")

if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    m1, m2 = st.columns([2, 1])
    
    with m1:
        st.markdown("#### 🗑️ لوحة حذف وإدارة البيانات")
        delete_options = [f"{i} | {row['المنطقة']} - عقار رقم Packs ({row['رقم العقار']})" for i, row in df.iterrows()]
        to_delete = st.selectbox("اختر السجل الخاطئ لحذفه نهائياً:", options=delete_options)
        if st.button("🗑️ تأكيد الحذف النهائي للسجل المختار"):
            idx = int(to_delete.split(" | ")[0])
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("🗑️ تم حذف السجل بنجاح وتحديث قاعدة البيانات.")
            st.rerun()
            
    with m2:
        st.markdown("#### 📥 التصدير والتقارير")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 تحميل التقرير الشامل (CSV / Excel)",
            data=csv,
            file_name="War_Damage_Report.csv",
            mime="text/csv"
        )
else:
    st.info("لا توجد سجلات مسجلة حالياً في النظام.")

# 5. التوقيع والتوثيق الثابت في آخر الواجهة
st.markdown("""
    <div class='footer-section'>
        <div>PArchiving</div>
        <div>S,Walid Mrad</div>
    </div>
""", unsafe_allow_html=True)
