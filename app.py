import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والجماليات العصرية (CSS الاحترافي المخصص)
st.set_page_config(page_title="KhatibAlami Company", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* المربع النافر للعناوين */
    .header-card {
        background-color: #EBF8FF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.1);
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
        border: 1px solid #BEE3F8;
    }

    .company-header {
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        font-weight: bold;
        margin: 0;
    }

    .company-subtitle {
        color: #2D3748;
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        font-weight: 500;
        margin-top: 8px;
    }

    /* قسم التوقيع والتوثيق في الواجهة الأساسية بالأعلى */
    .main-signature-card {
        background-color: #ffffff;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border: 1px solid #e2e8f0;
    }
    .sig-title {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #1E3A8A;
        margin: 0;
    }
    .sig-name {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        font-weight: bold;
        color: #475569;
        margin: 2px 0;
    }
    .sig-note {
        font-size: 13px;
        color: #3b82f6;
        font-weight: 500;
        margin: 0;
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

    /* تنسيق أزرار الواجهة */
    div.stButton > button {
        border: none;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة قاعدة البيانات والترتيب التلقائي للمناطق
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

# الذاكرة الداخلية للحفاظ على المنطقة وتصفير حقل الرقم بأمان
if "last_region" not in st.session_state:
    st.session_state.last_region = ""
if "clear_trigger" not in st.session_state:
    st.session_state.clear_trigger = False

# 3. تنظيم مساحة العمل وسط الصفحة
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # 🟦 [أولاً] مربع العنوان النافر المستقل بالأزرق الفاتح
    st.markdown("""
        <div class='header-card'>
            <div class='company-header'>KhatibAlami Company</div>
            <div class='company-subtitle'>War Damage Assessment 2006</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ✍️ [ثانياً] التوقيع والتوثيق الثابت في قمة الصفحة
    st.markdown("""
        <div class='main-signature-card'>
            <div class='sig-title'>Printing & Archiving</div>
            <div class='sig-name'>S,Walid Mrad</div>
            <div class='sig-note'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v3.0</div>
        </div>
    """, unsafe_allow_html=True)
    
    total_properties_count = len(df)
    
    # [ثالثاً] خانات إدخال البيانات الرئيسية في الواجهة المفتوحة
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input(
            "📍 اسم المنطقة الجغرافية", 
            value=st.session_state.last_region, 
            placeholder="ادخل اسم المنطقة الحالية...",
            key="region_field"
        ).strip()
    with c2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input(
            "🔢 رقم العقار الجديد", 
            value=prop_val,
            placeholder="ادخل رقم العقار الحالي...",
            key="property_field"
        ).strip()

    # إعادة تعيين مفتاح التصفير للاستخدام القادم
    st.session_state.clear_trigger = False

    # زر حفظ العقار الفعلي بالخلفية عند ضغط Enter
    btn_save = st.button("🚀 زر حفظ العقار والتحقق من التكرار", type="primary")

    # 🔑 كود التظليل الكلي والتوجيه التلقائي للمؤشر عند ضغط ENTER
    st.components.v1.html(
        """
        <script>
        var attachMidanEvents = function() {
            var mainDoc = window.parent.document;
            var inputs = mainDoc.getElementsByTagName('input');
            var buttons = mainDoc.getElementsByTagName('button');
            
            var regInput = null;
            var propInput = null;
            var saveBtn = null;
            
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].getAttribute('placeholder') === 'ادخل اسم المنطقة الحالية...') {
                    regInput = inputs[i];
                }
                if (inputs[i].getAttribute('placeholder') === 'ادخل رقم العقار الحالي...') {
                    propInput = inputs[i];
                }
            }
            
            for (var j = 0; j < buttons.length; j++) {
                if (buttons[j].textContent.includes('🚀 زر حفظ العقار والتحقق من التكرار')) {
                    saveBtn = buttons[j];
                }
            }
            
            // 1. عند ضغط Enter في خانة المنطقة -> اقفز فوراً لخانة الرقم وتحديد محتواها
            if (regInput && propInput) {
                regInput.removeEventListener('keydown', window.regMidanHandler);
                window.regMidanHandler = function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        propInput.focus();
                        propInput.select();
                    }
                };
                regInput.addEventListener('keydown', window.regMidanHandler);
            }
            
            // 2. عند ضغط Enter في خانة الرقم -> احفظ واجعل مؤشر الماوس يعود للمنطقة ويظلل النص القديم بالكامل تلقائياً
            if (propInput && saveBtn && regInput) {
                propInput.removeEventListener('keydown', window.propMidanHandler);
                window.propMidanHandler = function(e) {
                    if (e.key === 'Enter') {
                        if (propInput.value.trim() !== "") {
                            e.preventDefault();
                            saveBtn.click(); // تفعيل الحفظ الفوري لبايثون
                            
                            // إرجاع المؤشر وتظليل النص القديم بالكامل فوراً للسرعة القصوى
                            setTimeout(function() {
                                regInput.focus();
                                regInput.select(); // تظليل النص القديم لتكتب فوقه مباشرة دون مسح بالماوس
                            }, 80);
                        }
                    }
                };
                propInput.addEventListener('keydown', window.propMidanHandler);
            }
        };
        
        setTimeout(attachMidanEvents, 200);
        setInterval(attachMidanEvents, 1000);
        </script>
        """,
        height=0,
    )

    # معالجة منطق الحفظ عند التفعيل (من خلال الضغط بالـ Enter أو النقر اليدوي)
    if btn_save:
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                              (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            if is_duplicate:
                st.error(f"❌ إلغاء: هذا العقار مسجل سابقاً في هذه المنطقة!")
            else:
                new_row = {"المنطقة": region_input, "رقم العقار": property_number}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df = df.sort_values(by="المنطقة").reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                
                # تثبيت المنطقة القديمة وتجهيز حقل الرقم للتفريغ
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                st.success(f"✅ تم حفظ العقار رقم ({property_number}) بنجاح!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ.")

    # [رابعاً] العدادات الإحصائية الفورية تحت الأزرار مباشرة
    st.markdown("<br>", unsafe_allow_html=True)
    
    region_properties_count = 0
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        region_properties_count = len(filtered_df)

    # عرض كروت العدادات الزرقاء
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_properties_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

    # 🛑 [خامساً وأخيراً] نقل جدول البيانات التفاعلي الذكي إلى آخر الصفحة تماماً مع إخفاء أزرار التحميل
    st.markdown("---")
    
    if not df.empty:
        search_query = st.text_input("🔍 محرك البحث السريع بالجدول (اكتب المنطقة أو رقم العقار للتصفية الفورية):", placeholder="اكتب للبحث الفوري بداخل السجلات...").strip()
        
        if search_query:
            display_df = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | 
                            df["رقم العقار"].str.contains(search_query, case=False, na=False)]
        else:
            display_df = df

        st.markdown("### ✏️ جدول البيانات التفاعلي الذكي (تعديل مباشر بنقرتين / حذف)")
        
        # تم وضع الجدول هنا، مع تصفية وعرض نظيف بدون خيار تحميل
        edited_df = st.data_editor(
            display_df, 
            use_container_width=True, 
            num_rows="dynamic",
            key="data_editor_key"
        )
        
        if st.button("💾 حفظ التعديلات الميدانية على السحابة", type="primary"):
            if search_query:
                df.update(edited_df)
            else:
                df = edited_df
                
            df = df.sort_values(by="المنطقة").reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("💾 تم حفظ كافة التعديلات وعمليات الحذف بنجاح!")
            st.rerun()
    else:
        st.info("لا توجد سجلات مسجلة حالياً.")
