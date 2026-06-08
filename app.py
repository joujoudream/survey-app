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

    /* المربع النافر الملون بالأزرق الفاتح للعناوين في الأعلى */
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

    /* كروت الإحصائيات الزرقاء العصرية */
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
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
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

# تهيئة متغيرات الحفظ والتحكم بالتركيز بداخل السيرفر ومخزن الصفحة
if "last_region" not in st.session_state:
    st.session_state.last_region = ""
if "focus_target" not in st.session_state:
    st.session_state.focus_target = "region"  # البدء بتركيز المنطقة
if "prop_value" not in st.session_state:
    st.session_state.prop_value = ""

# --- الدوال البرمجية المسؤولة عن معالجة ضغط زر ENTER بنقاء بايثون كامل ---

def on_region_enter():
    """عند ضغط Enter في خانة المنطقة، نقوم بتجهيز النظام لنقل التركيز لخانة الرقم"""
    if st.session_state.region_key.strip():
        st.session_state.last_region = st.session_state.region_key.strip()
        st.session_state.focus_target = "property"

def on_property_enter():
    """عند ضغط Enter في خانة الرقم، يتم الحفظ التلقائي فوراً وإعادة المؤشر للمنطقة"""
    global df
    reg = st.session_state.get("region_key", "").strip()
    prop = st.session_state.get("property_key", "").strip()
    
    if reg and prop:
        # فحص التكرار
        is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == reg.lower()) & 
                          (df["رقم العقار"].str.strip() == prop)].shape[0] > 0
        if is_duplicate:
            st.session_state["error_msg"] = f"❌ إلغاء: هذا العقار ({prop}) مسجل سابقاً في منطقة ({reg})!"
        else:
            # إضافة السجل الجديد وحفظه
            new_row = {"المنطقة": reg, "رقم العقار": prop}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df = df.sort_values(by="المنطقة").reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.session_state["success_msg"] = f"✅ تم حفظ العقار رقم ({prop}) بنجاح!"
            # تصفير حقل الرقم والعودة بالتركيز للمنطقة
            st.session_state.prop_value = ""
            st.session_state.focus_target = "region"
    else:
        st.session_state["warning_msg"] = "⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ."

# 3. تنظيم مساحة العمل وسط الصفحة
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # 🟦 مربع العنوان النافر المستقل بالأزرق الفاتح
    st.markdown("""
        <div class='header-card'>
            <div class='company-header'>KhatibAlami Company</div>
            <div class='company-subtitle'>War Damage Assessment 2006</div>
        </div>
    """, unsafe_allow_html=True)
    
    total_properties_count = len(df)
    
    # [1] خانات إدخال البيانات الرئيسية باستخدام المحرك المستقر الذكي
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input(
            "📍 اسم المنطقة الجغرافية", 
            value=st.session_state.last_region, 
            placeholder="اكتب اسم المنطقة ثم اضغط Enter...",
            key="region_key",
            on_change=on_region_enter
        ).strip()
    with c2:
        property_number = st.text_input(
            "🔢 رقم العقار الجديد", 
            value=st.session_state.prop_value,
            placeholder="أدخل رقم العقار ثم اضغط Enter للحفظ التلقائي...",
            key="property_key",
            on_change=on_property_enter
        ).strip()

    # 🔑 كود حقن صغير جداً ومضمون يقرأ حالة البايثون ويجبر المتصفح على نقل المؤشر (Focus) الفعلي فوراً دون اعتراض الـ Rerun
    js_focus_code = ""
    if st.session_state.focus_target == "property":
        js_focus_code = """
            <script>
            var mainDoc = window.parent.document;
            var inputs = mainDoc.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].getAttribute('placeholder') === 'أدخل رقم العقار ثم اضغط Enter للحفظ التلقائي...') {
                    inputs[i].focus();
                    break;
                }
            }
            </script>
        """
    elif st.session_state.focus_target == "region":
        js_focus_code = """
            <script>
            var mainDoc = window.parent.document;
            var inputs = mainDoc.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].getAttribute('placeholder') === 'اكتب اسم المنطقة ثم اضغط Enter...') {
                    inputs[i].focus();
                    inputs[i].select();
                    break;
                }
            }
            </script>
        """
    st.components.v1.html(js_focus_code, height=0)

    # عرض رسائل النجاح أو الأخطاء الناتجة عن ضغط الـ ENTER
    if "error_msg" in st.session_state:
        st.error(st.session_state.pop("error_msg"))
    if "success_msg" in st.session_state:
        st.success(st.session_state.pop("success_msg"))
    if "warning_msg" in st.session_state:
        st.warning(st.session_state.pop("warning_msg"))

    # [2] لوحة أزرار التحكم التقليدية للمراجعة اليدوية
    b1, b2 = st.columns(2)
    with b1:
        btn_check = st.button("🔍 زر فحص وجود العقار مسبقاً", type="secondary")
    with b2:
        btn_save = st.button("🚀 زر حفظ العقار والتحقق من التكرار", type="primary")

    # معالجة ضغط الأزرار اليدوية بالماوس (اختياري)
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
                st.success("✅ تم حفظ العقار بنجاح وتحديث السحابة!")
                st.session_state.last_region = region_input
                st.session_state.prop_value = ""
                st.session_state.focus_target = "region"
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ.")

    # [3] العدادات الإحصائية الفورية تحت الأزرار مباشرة
    st.markdown("<br>", unsafe_allow_html=True)
    
    region_properties_count = 0
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        region_properties_count = len(filtered_df)
        
        if btn_check and property_number:
            match = filtered_df[filtered_df["رقم العقار"].str.strip() == property_number]
            if not match.empty:
                st.warning(f"⚠️ تنبيه: العقار رقم ({property_number}) موجود ومسجل مسبقاً بالفعل في منطقة ({region_input})!")
            else:
                st.success(f"✨ ممتاز: العقار رقم ({property_number}) جديد كلياً وغير مسجل في منطقة ({region_input}). يمكنك حفظه الآن.")

    # عرض كروت العدادات الزرقاء تحت الأزرار مباشرة ودون أي زحام
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_properties_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:13px; color:#64748b;'>بمجرد كتابة اسم المنطقة، سيقوم النظام تلقائياً بتحديث إحصاء العقارات المسجلة لحمايتها من التكرار.</p>", unsafe_allow_html=True)

# 4. محرك البحث والجدول التفاعلي للتعديل والحذف السريع
st.markdown("---")

if not df.empty:
    search_query = st.text_input("🔍 محرك البحث السريع بالجدول (اكتب المنطقة أو رقم العقار للتصفية الفورية):", placeholder="اكتب للبحث الفوري بداخل السجلات...").strip()
    
    if search_query:
        display_df = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | 
                        df["رقم العقار"].str.contains(search_query, case=False, na=False)]
    else:
        display_df = df

    st.markdown("### ✏️ جدول البيانات التفاعلي الذكي (تعديل مباشر بنقرتين / حذف)")
    st.caption("💡 للتعديل: انقر مرتين داخل أي خانة في الجدول وعدّلها بيدك فوراً! للحذف: استخدم سلة المهملات بجانب السطر أو حدد السطر واضغط Delete.")
    
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

    # زر تحميل التقارير للمكتب
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل التقرير الشامل بصيغة (Excel / CSV)",
        data=csv,
        file_name="War_Damage_Report.csv",
        mime="text/csv"
    )
else:
    st.info("لا توجد سجلات مسجلة حالياً.")

# 5. التوقيع والتوثيق الثابت المحسن في أسفل الصفحة
st.markdown("""
    <div class='footer-section'>
        <div>Printing & Archiving</div>
        <div>S.Walid Murad</div>
        <div class='footer-sub'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v3.0</div>
    </div>
""", unsafe_allow_html=True)
