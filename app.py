import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والجماليات العصرية (CSS الاحترافي المخصص)
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

    /* 1️⃣ المربع النافر الملون بالأزرق الفاتح الهادئ للعناوين فقط */
    .header-card {
        background-color: #EBF8FF; /* تلوين المساحة بالأزرق الفاتح المريح */
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.1);
        margin-top: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #BEE3F8; /* إطار أزرق متناسق لإبراز النفور */
    }

    /* تنسيق كلمة الشركة بداخل المربع الأزرق الفاتح */
    .company-header {
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin: 0;
    }

    /* تنسيق العبارة الثانية تحتها مباشرة */
    .company-subtitle {
        color: #2D3748;
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 8px;
        margin-bottom: 0;
    }

    /* 2️⃣ المربع الأبيض الثاني المنفصل الخاص ببيانات الإدخال */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border: 1px solid #e2e8f0;
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

    h3 { color: #334155; font-size: 20px; margin-top: 0px; margin-bottom: 20px; }

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
    .footer-sub {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة قاعدة البيانات والترتيب التلقائي للمناطق (بدون عمود الوقت)
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

# 3. تنظيم مساحة العمل وسط الصفحة
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # 🟦 المربع الأول: مربع العنوان النافر المستقل والمعدل بالأزرق الفاتح
    st.markdown("""
        <div class='header-card'>
            <div class='company-header'>KhatibAlami Company</div>
            <div class='company-subtitle'>War Damage Assessment 2006</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ⬜ المربع الثاني: مربع إدخال البيانات المنفصل تماماً
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    st.markdown("### 📋 تفاصيل الموقع والتحقق الذكي")
    
    total_properties_count = len(df)
    
    if "region_val" not in st.session_state:
        st.session_state.region_val = ""

    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة", value=st.session_state.region_val, placeholder="مثال: الضاحية الجنوبية، صور، بعلبك...", key="region_field").strip()
    
    is_existing_region = False
    region_properties_count = 0
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        region_properties_count = len(filtered_df)
        if region_properties_count > 0:
            is_existing_region = True
            st.info(f"💡 المنطقة مسجلة مسبقاً وتحتوي على **{region_properties_count}** عقارات مسجلة.")
            with st.expander("👁️ مراجعة أرقام العقارات السابقة في هذه المنطقة"):
                st.write(", ".join(filtered_df["رقم العقار"].unique()))
        else:
            st.success("✨ هذه المنطقة جديدة تماماً ولم تُمسح من قبل.")

    with c2:
        if is_existing_region:
            property_number = st.text_input("🔢 رقم العقار الجديد", placeholder="أدخل رقم العقار الحالي للمسح...", key="prop_field", autocomplete="on").strip()
            st.components.v1.html(
                """
                <script>
                    var inputs = window.parent.document.getElementsByTagName('input');
                    for (var i = 0; i < inputs.length; i++) {
                        if (inputs[i].getAttribute('aria-label') == '🔢 رقم العقار الجديد') {
                            inputs[i].focus();
                            break;
                        }
                    }
                </script>
                """,
                height=0,
            )
        else:
            property_number = st.text_input("🔢 رقم العقار الجديد", placeholder="أدخل رقم العقار الحالي للمسح...", key="prop_field").strip()

    # عرض لوحة الإحصائيات بداخل مربع البيانات
    st.markdown("<br>", unsafe_allow_html=True)
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_properties_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

    # زر الحفظ والتحقق من التكرار
    if st.button("🚀 حفظ العقار والتحقق من التكرار"):
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                              (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            
            if is_duplicate:
                st.error(f"❌ تنبيه: العقار رقم ({property_number}) مسجل مسبقاً بالفعل في منطقة ({region_input})!")
            else:
                new_row = {
                    "المنطقة": region_input,
                    "رقم العقار": property_number
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df = df.sort_values(by="المنطقة").reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ تم حفظ البيانات بنجاح وتحديث السحابة!")
                st.session_state.region_val = region_input
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى إدخال المنطقة ورقم العقار أولاً.")
            
    st.markdown("<p style='font-size:13px; color:#64748b; margin-top: 15px;'>بمجرد كتابة اسم المنطقة، سيقوم النظام تلقائياً بفحص العقارات المسجلة مسبقاً لحمايتها من التكرار وعرض إحصاء دقيق لها.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 4. محرك البحث وقاعدة البيانات المرتبة
st.markdown("---")
st.markdown("### 📊 قاعدة البيانات المسجلة والتقارير")

if not df.empty:
    search_query = st.text_input("🔍 محرك البحث السريع (ابحث باسم المنطقة أو رقم العقار):", placeholder="اكتب اسم المنطقة أو رقم العقار المُراد العثور عليه...").strip()
    
    if search_query:
        display_df = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | 
                        df["رقم العقار"].str.contains(search_query, case=False, na=False)]
        st.caption(f"🔎 تم العثور على {len(display_df)} سجل يطابق بحثك.")
    else:
        display_df = df

    st.dataframe(display_df, use_container_width=True)
    
    m1, m2 = st.columns([2, 1])
    
    with m1:
        st.markdown("#### 🗑️ إجراءات إدارة السجلات")
        delete_options = [f"{i} | {row['المنطقة']} - عقار رقم ({row['رقم العقار']})" for i, row in df.iterrows()]
        to_delete = st.selectbox("اختر السجل المراد حذفه نهائياً:", options=delete_options)
        if st.button("🗑️ حذف السجل المختار"):
            idx = int(to_delete.split(" | ")[0])
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("🗑️ تم حذف السجل بنجاح وتحديث قاعدة البيانات.")
            st.rerun()
            
    with m2:
        st.markdown("#### 📥 التصدير")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 تحميل التقرير الشامل (CSV / Excel)",
            data=csv,
            file_name="War_Damage_Report.csv",
            mime="text/csv"
        )
else:
    st.info("لا توجد سجلات مسجلة حالياً في النظام.")

# 5. التوقيع والتوثيق الثابت في آخر الواجهة كما في الـ PDF
st.markdown("""
    <div class='footer-section'>
        <div>PArchiving</div>
        <div>S,Walid Mrad</div>
        <div class='footer-sub'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v3.0</div>
    </div>
""", unsafe_allow_html=True)
