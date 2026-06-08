import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والجماليات (CSS المخصص والمفتوح)
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

    /* 1️⃣ المربع النافر الملون بالأزرق الفاتح للعناوين في الأعلى */
    .header-card {
        background-color: #EBF8FF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.1);
        margin-top: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #BEE3F8;
    }

    .company-header {
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin: 0;
    }

    .company-subtitle {
        color: #2D3748;
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 8px;
        margin-bottom: 0;
    }

    /* كروت الإحصائيات الزرقاء */
    .metric-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
        margin-bottom: 20px;
    }
    .metric-val { font-size: 28px; font-weight: bold; }
    .metric-lbl { font-size: 14px; opacity: 0.9; }

    /* تنسيق الأزرار */
    div.stButton > button {
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
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
    .footer-sub {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة قاعدة البيانات والترتيب التلقائي
DATA_FILE = "survey_data.csv"

if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE, dtype={"رقم العقار": str})
    except:
        df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
else:
    df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if not df.empty:
    df = df.sort_values(by="المنطقة").reset_index(drop=True)

# إدارة الذاكرة للحقول والتعديل
if "input_region" not in st.session_state: st.session_state.input_region = ""
if "input_prop" not in st.session_state: st.session_state.input_prop = ""
if "edit_mode_index" not in st.session_state: st.session_state.edit_mode_index = None

# 3. تنظيم مساحة العمل وسط الصفحة
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # 🟦 المربع الأول: مربع العنوان النافر المستقل بالأزرق الفاتح
    st.markdown("""
        <div class='header-card'>
            <div class='company-header'>KhatibAlami Company</div>
            <div class='company-subtitle'>War Damage Assessment 2006</div>
        </div>
    """, unsafe_allow_html=True)
    
    total_properties_count = len(df)
    
    # حقول الإدخال المرتبطة بالذاكرة (لتتغير تلقائياً عند الضغط على تعديل)
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.input_region, placeholder="مثال: حارة حريك، بنت جبيل، صور...", key="reg_input_key").strip()
    with c2:
        property_number = st.text_input("🔢 رقم العقار", value=st.session_state.input_prop, placeholder="أدخل رقم العقار...", key="prop_input_key").strip()

    # لوحة أزرار التحكم الفورية (فحص / حفظ أو تحديث)
    b1, b2 = st.columns(2)
    
    with b1:
        # 🔍 زر فحص الوجود
        if st.button("🔍 زر فحص وجود العقار مسبقاً", type="secondary"):
            if region_input and property_number:
                check_exist = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                                 (df["رقم العقار"].str.strip() == property_number)]
                if not check_exist.empty:
                    st.warning(f"⚠️ تنبيه: العقار رقم ({property_number}) مسجل مسبقاً في ({region_input})!")
                else:
                    st.success(f"✨ ممتاز: العقار رقم ({property_number}) جديد وغير مسجل في ({region_input}).")
            else:
                st.info("💡 يرجى كتابة اسم المنطقة ورقم العقار أولاً لعمل الفحص.")

    with b2:
        # زر الحفظ الديناميكي (يتغير حسب وضع التعديل)
        if st.session_state.edit_mode_index is not None:
            # وضع التعديل
            if st.button("💾 حفظ التعديلات الحالية العقار", type="primary"):
                if region_input and property_number:
                    idx = st.session_state.edit_mode_index
                    df.loc[idx, "المنطقة"] = region_input
                    df.loc[idx, "رقم العقار"] = property_number
                    df = df.sort_values(by="المنطقة").reset_index(drop=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("✅ تم تعديل وحفظ السجل بنجاح!")
                    # تصفير الذاكرة بعد التعديل
                    st.session_state.edit_mode_index = None
                    st.session_state.input_region = ""
                    st.session_state.input_prop = ""
                    st.rerun()
                else:
                    st.error("❌ الحقول فارغة!")
        else:
            # وضع الإدخال العادي
            if st.button("🚀 زر حفظ العقار والتحقق من التكرار", type="primary"):
                if region_input and property_number:
                    is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                                      (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
                    if is_duplicate:
                        st.error(f"❌ إلغاء: هذا العقار مسجل سابقاً!")
                    else:
                        new_row = {"المنطقة": region_input, "رقم العقار": property_number}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        df = df.sort_values(by="المنطقة").reset_index(drop=True)
                        df.to_csv(DATA_FILE, index=False)
                        st.success("✅ تم حفظ العقار بنجاح!")
                        st.session_state.input_region = region_input
                        st.session_state.input_prop = ""
                        st.rerun()
                else:
                    st.warning("⚠️ يرجى ملء الخانات أولاً.")

    # عرض لوحة العدادات الإحصائية
    st.markdown("<br>", unsafe_allow_html=True)
    region_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]) if region_input else 0
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

# 4. محرك البحث والجدول وإدارة السجلات
st.markdown("---")

if not df.empty:
    search_query = st.text_input("🔍 محرك البحث السريع بالجدول (ابحث باسم المنطقة أو رقم العقار):", placeholder="اكتب للبحث الفوري...").strip()
    
    if search_query:
        display_df = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | 
                        df["رقم العقار"].str.contains(search_query, case=False, na=False)]
    else:
        display_df = df

    st.dataframe(display_df, use_container_width=True)
    
    # ⚙️ لوحة الإدارة السفلية للحذف والتعديل
    st.markdown("### ⚙️ لوحة إدارة السجلات (تعديل / حذف)")
    management_options = [f"{i} | {row['المنطقة']} - عقار رقم ({row['رقم العقار']})" for i, row in df.iterrows()]
    selected_record = st.selectbox("اختر السجل المراد التعامل معه:", options=management_options)
    
    idx_selected = int(selected_record.split(" | ")[0])
    
    m_btn1, m_btn2 = st.columns(2)
    with m_btn1:
        # 🗑️ زر الحذف
        if st.button("🗑️ زر حذف السجل المختار نهائياً"):
            df = df.drop(idx_selected).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("🗑️ تم حذف السجل بنجاح.")
            st.rerun()
            
    with m_btn2:
        # ✏️ زر التعديل (يرفع البيانات للحقول في الأعلى فوراً)
        if st.button("✏️ زر تعديل السجل المختار (رفع إلى الحقول الأعلى)"):
            st.session_state.edit_mode_index = idx_selected
            st.session_state.input_region = df.loc[idx_selected, "المنطقة"]
            st.session_state.input_prop = df.loc[idx_selected, "رقم العقار"]
            st.success("✏️ تم رفع البيانات إلى الحقول في الأعلى! يمكنك تعديلها الآن ثم الضغط على حفظ التعديلات.")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="💾 تحميل التقرير الشامل المحدث (CSV / Excel)",
        data=csv,
        file_name="War_Damage_Report.csv",
        mime="text/csv"
    )
else:
    st.info("لا توجد سجلات مسجلة حالياً.")

# 5. التوقيع والتوثيق الثابت والمحسّن
st.markdown("""
    <div class='footer-section'>
        <div>Printing & Archiving</div>
        <div>S.Walid Murad</div>
        <div class='footer-sub'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v3.0</div>
    </div>
""", unsafe_allow_html=True)
