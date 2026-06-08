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

    /* 1️⃣ المربع النافر الملون بالأزرق الفاتح للعناوين فقط في الأعلى */
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

    /* تنسيق الأزرار الاحترافي */
    div.stButton > button {
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    /* أزرار الحفظ والبحث (أزرق) */
    .st-emotion-cache-18ni7ap, div.stButton > button:first-child {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
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

# 2. إدارة قاعدة البيانات والترتيب التلقائي (بدون عمود الوقت)
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

# إدارة الذاكرة المؤقتة للتعديل والمسح الجغرافي
if "region_val" not in st.session_state: st.session_state.region_val = ""
if "edit_index" not in st.session_state: st.session_state.edit_index = None
if "edit_region" not in st.session_state: st.session_state.edit_region = ""
if "edit_prop" not in st.session_state: st.session_state.edit_prop = ""

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
    
    # العدادات الإحصائية الإجمالية
    total_properties_count = len(df)
    
    # حقول الإدخال الأساسية للعقار الجديد أو الفحص
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.region_val, placeholder="مثال: حارة حريك، بنت جبيل، صور...").strip()
    with c2:
        property_number = st.text_input("🔢 رقم العقار المُراد التعامل معه", placeholder="أدخل رقم العقار...").strip()

    # لوحة أزرار التحكم والعمليات (فحص / حفظ) تحت الحقول مباشرة
    b1, b2 = st.columns(2)
    
    with b1:
        # زر فحص وجود العقار (البحث المباشر)
        if st.button("🔍 زر فحص وجود العقار مسبقاً"):
            if region_input and property_number:
                check_exist = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                                 (df["رقم العقار"].str.strip() == property_number)]
                if not check_exist.empty:
                    st.warning(f"⚠️ تنبيه: العقار رقم ({property_number}) موجود ومسجل مسبقاً بالفعل في ({region_input})!")
                else:
                    st.success(f"✨ ممتاز: العقار رقم ({property_number}) غير مسجل في ({region_input})، يمكنك حفظه الآن كعقار جديد.")
            else:
                st.info("💡 يرجى إدخال اسم المنطقة ورقم العقار معاً لتتمكن من فحص السجل بنجاح.")

    with b2:
        # زر حفظ العقار الجديد
        if st.button("🚀 زر حفظ العقار والتحقق من التكرار"):
            if region_input and property_number:
                is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                                  (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
                
                if is_duplicate:
                    st.error(f"❌ إلغاء: هذا العقار مسجل سابقاً! يرجى التحقق من الرقم أو تعديله.")
                else:
                    new_row = {"المنطقة": region_input, "رقم العقار": property_number}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df = df.sort_values(by="المنطقة").reset_index(drop=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("✅ تم حفظ العقار بنجاح وتحديث قاعدة البيانات!")
                    st.session_state.region_val = region_input
                    st.rerun()
            else:
                st.warning("⚠️ يرجى ملء الخانات أولاً قبل الضغط على زر الحفظ.")

    # عرض لوحة العدادات الإحصائية الفورية
    st.markdown("<br>", unsafe_allow_html=True)
    region_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]) if region_input else 0
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

# 4. قسم محرك البحث الشامل، التعديل، والحذف
st.markdown("---")

if not df.empty:
    # خانة البحث السريع المفتوحة للجدول
    search_query = st.text_input("🔍 محرك البحث السريع بالجدول (ابحث باسم المنطقة أو رقم العقار):", placeholder="اكتب للبحث الفوري...").strip()
    
    if search_query:
        display_df = df
