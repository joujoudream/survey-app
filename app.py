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

# حفظ اسم المنطقة لتسهيل الإدخال المتتابع للميدان
if "last_region" not in st.session_state:
    st.session_state.last_region = ""

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
    
    # [1] خانات إدخال البيانات الرئيسية في الواجهة المفتوحة
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="اكتب اسم المنطقة ثم اضغط Enter...").strip()
    with c2:
        property_number = st.text_input("🔢 رقم العقار الجديد", placeholder="أدخل رقم العقار ثم اضغط Enter للحفظ...").strip()

    # [2] لوحة أزرار التحكم والعمليات مباشرة تحت الخانات
    b1, b2 = st.columns(2)
    
    with b1:
        # 🔍 زر فحص وجود العقار مسبقاً
        btn_check = st.button("🔍 زر فحص وجود العقار مسبقاً", type="secondary")
    with b2:
        # 🚀 زر حفظ العقار والتحقق من التكرار (أضفنا له لافتة نصية ليتعرف عليه الجافا سكريبت ويضغط عليه تلقائياً)
        btn_save = st.button("🚀 زر حفظ العقار والتحقق من التكرار", type="primary", help="save_trigger_btn")

    # 🔑 سحر الجافا سكريبت المزدوج: قفز من الأولى للثانية + حفظ تلقائي عند ضغط ENTER في الثانية
    st.components.v1.html(
        """
        <script>
        var setupEnterLogic = function() {
            var mainDoc = window.parent.document;
            var inputs = mainDoc.getElementsByTagName('input');
            var buttons = mainDoc.getElementsByTagName('button');
            
            var firstInput = null;
            var secondInput = null;
            var saveButton = null;
            
            // تحديد الحقول بناءً على الـ placeholder
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].getAttribute('placeholder') === 'اكتب اسم المنطقة ثم اضغط Enter...') {
                    firstInput = inputs[i];
                }
                if (inputs[i].getAttribute('placeholder') === 'أدخل رقم العقار ثم اضغط Enter للحفظ...') {
                    secondInput = inputs[i];
                }
            }
            
            // تحديد زر الحفظ
            for (var j = 0; j < buttons.length; j++) {
                if (buttons[j].textContent.includes('🚀 زر حفظ العقار والتحقق من التكرار')) {
                    saveButton = buttons[j];
                }
            }
            
            // 1. منطق الخانة الأولى: الانتقال للخانة الثانية
            if (firstInput && secondInput) {
                firstInput.removeEventListener('keydown', window.firstHandler);
                window.firstHandler = function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        e.stopPropagation();
                        secondInput.focus();
                    }
                };
                firstInput.addEventListener('keydown', window.firstHandler);
            }
            
            // 2. منطق الخانة الثانية: تفعيل زر الحفظ تلقائياً عند ضغط Enter
            if (secondInput && saveButton) {
                secondInput.removeEventListener('keydown', window.secondHandler);
                window.secondHandler = function(e) {
                    if (e.key === 'Enter') {
                        if (secondInput.value.trim() !== "") {
                            e.preventDefault();
                            e.stopPropagation();
                            saveButton.click(); // ضغط زر الحفظ تلقائياً!
                        }
                    }
                };
                secondInput.addEventListener('keydown', window.secondHandler);
            }
        };
        
        // تشغيل الفحص والتأكد من ربط العناصر بشكل دوري ومستقر
        setTimeout(setupEnterLogic, 500);
        setInterval(setupEnterLogic, 1500);
        </script>
        """,
        height=0,
    )

    # معالجة منطق الحفظ عند الضغط (أو عند إطلاق الحفظ التلقائي)
    if btn_save:
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                              (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            if is_duplicate:
                st.error(f"❌ إلغاء: هذا العقار مسجل سابقاً في هذه المنطقة!")
            else:
                new_row = {"المنطقة": region_input, "رقم QR / العقار": property_number} # توافقاً مع الهيكلية الحالية للملف
                # تعديل طفيف ليتطابق مع مسميات الأعمدة الأصلية
                new_row = {"المنطقة": region_input, "رقم العقار": property_number}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df = df.sort_values(by="المنطقة").reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ تم حفظ العقار بنجاح وتحديث السحابة!")
                st.session_state.last_region = region_input
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ.")

    # [3] العدادات الإحصائية الفورية تحت الأزرار
    st.markdown("<br>", unsafe_allow_html=True)
    
    region_properties_count = 0
    if region_input:
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        region_properties_count = len(filtered_df)
        
        # عرض رسالة الفحص المباشر فقط في حال ضغط زر الفحص 🔍
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
    
    # محرّر الجدول التفاعلي الكلي
    edited_df = st.data_editor(
        display_df, 
        use_container_width=True, 
        num_rows="dynamic",
        key="data_editor_key"
    )
    
    # زر حفظ التعديلات المباشرة في الجدول
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
