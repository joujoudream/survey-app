import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# 🎨 ستايل CSS حديث ومحصن تماماً يضمن ظهور الألوان وتناسق الحقول على أي سيرفر
clean_css = "<style>@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap'); html, body, [class*='css'] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; } .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); } header[data-testid='stHeader'] { background: transparent !important; height: 0px !important; display: none !important; } .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; } .header-card { background-color: #EBF8FF; padding: 20px 12px; border-radius: 12px; box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08); margin-bottom: 2px; text-align: center; border: 1px solid #BEE3F8; } .company-header { color: #1E3A8A; font-family: 'Arial', sans-serif; font-size: 28px; font-weight: bold; margin: 0; line-height: 1.2; } .company-subtitle { color: #2D3748; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: 500; margin-top: 4px; } .main-signature-card { background-color: #ffffff; padding: 8px 16px; border-radius: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04); margin-top: 4px; margin-bottom: 15px; border: 1px solid #e2e8f0; width: 100%; max-width: 550px; margin-left: auto; margin-right: auto; } .sig-title { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; color: #1E3A8A; margin: 0; } .sig-name { font-family: 'Arial', sans-serif; font-size: 14px; font-weight: bold; color: #475569; margin: 2px 0; } .sig-note { font-size: 11px; color: #3b82f6; font-weight: 500; margin: 0; } div[data-testid='stBlock'] button[type='button']:contains('🚀') { background-color: #EF4444 !important; color: white !important; border: none !important; font-weight: 700 !important; height: 45px !important; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2) !important; } div[data-testid='stBlock'] button[type='button']:contains('🚀'):hover { background-color: #DC2626 !important; } div[data-testid='stMetric'] { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important; color: white !important; padding: 12px !important; border-radius: 10px !important; text-align: center !important; box-shadow: 0 4px 8px rgba(30, 58, 138, 0.15) !important; } div[data-testid='stMetric'] * { color: white !important; } div[data-testid='stHorizontalBlock'] { gap: 10px !important; } [data-testid='stInputInstructions'] { display: none !important; visibility: hidden !important; }</style>"
st.markdown(clean_css, unsafe_allow_html=True)

# إدارة وحفظ حالات السجل والتحكم بالمؤشر الذكي
if "local_db" not in st.session_state:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    # الهيدر الأساسي وبطاقة التوقيع الخاصة بك
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>تم التحديث للأداء الأقصى والتنسيق الكامل | KhatibAlami System v8.0</div></div>", unsafe_allow_html=True)
    
    # نافذة رفع الملف الاحتياطي المدمجة
    with st.expander("📥 خطوة 1: رفع ملف البيانات الاحتياطي (إذا وجد)", expanded=not st.session_state.file_uploaded):
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) المستخرج سابقاً لمتابعة العمل على البيانات:", type=["csv"])
        if uploaded_file is not None and not st.session_state.file_uploaded:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                st.session_state.local_db = uploaded_df[["المنطقة", "رقم العقار"]]
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل السجل بنجاح!")
                st.rerun()  
            except Exception as e:
                st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db
    st.markdown("---")
    
    # حقول الإدخال مصفوفة أفقياً بشكل متقارب جداً وسلس
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="النبطية، صور، صيدا...", key="region_field").strip()
    with input_col2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field").strip()
    
    st.session_state.clear_trigger = False

    # صف أزرار التفاعل والإجراءات الرئيسية
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", type="primary", use_container_width=True)
        
    with action_col2:
        if not df.empty:
            sorted_df = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
            csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="🟢 تحميل وتنزيل سجل CSV النهائي", data=csv_data, file_name="KhatibAlami_Midan_Data.csv", mime="text/csv", use_container_width=True)
        else:
            st.button("🟢 سجل CSV فارغ حالياً", disabled=True, use_container_width=True)

    # احتساب الإحصائيات الفورية للعقارات الميدانية
    total_count = len(df)
    region_count = 0
    if region_input:
        region_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()])

    st.markdown("<br>", unsafe_allow_html=True)

    # العدادات والبطاقات الإحصائية الذكية
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric(label="🗄️ مجموع عدد العقارات الكلي", value=total_count)
    with stat_col2:
        st.button(f"📍 {region_count} | اضغط لعرض عقارات هذه المنطقة", use_container_width=True)

    # جدول استعراض عقارات المنطقة الحالية
    if region_input:
        st.markdown(f"### 📊 ملف العقارات الجاري العمل عليها في منطقة: ({region_input})")
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        
        if not filtered_df.empty:
            display_sheet = pd.DataFrame(filtered_df["رقم العقار"].values, columns=["رقم العقار"])
            display_sheet = display_sheet.sort_values(by="رقم العقار").reset_index(drop=True)
            display_sheet.index += 1
            st.dataframe(display_sheet, use_container_width=True, height=200)
        else:
            st.info("ℹ️ لا توجد عقارات مسجلة لهذه المنطقة حالياً في السجل الحالي.")

    st.markdown("---")

    # محرك البحث الفوري لغايات المراجعة والتعديل السريع
    search_query = st.text_input("🔍 البحث الفوري عن عقار وتعديله:", value=st.session_state.search_val, placeholder="اكتب اسم المنطقة أو رقم العقار للبحث السريع والتعديل...", key="search_modify_field").strip()
    st.session_state.search_val = search_query

    # منطق معالجة زر الحفظ ومنع التكرار الصارم
    if btn_save:
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            if is_duplicate:
                st.error("❌ إلغاء: هذا العقار مسجل سابقاً في هذه المنطقة!")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                st.success(f"✅ تم حفظ العقار رقم ({property_number}) بنجاح!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء حقول المنطقة ورقم العقار أولاً.")

    # عرض نتائج لوحة التعديل الفوري
    if search_query:
        matched_records = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | df["رقم العقار"].astype(str).str.contains(search_query, case=False, na=False)]
        if not matched_records.empty:
            st.info(f"📋 تم العثور على ({len(matched_records)}) سجل متطابق:")
            for idx, row in matched_records.iterrows():
                with st.expander(f"⚙️ تعديل العقار رقم {row['رقم العقار']} في {row['المنطقة']}", expanded=True):
                    edit_c1, edit_c2 = st.columns(2)
                    with edit_c1:
                        new_edit_region = st.text_input("تعديل اسم المنطقة", value=row['المنطقة'], key=f"edit_reg_{idx}").strip()
                    with edit_c2:
                        new_edit_prop = st.text_input("تعديل رقم العقار", value=row['رقم العقار'], key=f"edit_prop_{idx}").strip()
                    
                    save_edit_btn = st.button("💾 حفظ التعديلات", key=f"save_edit_{idx}")
                    if save_edit_btn:
                        if new_edit_region and new_edit_prop:
                            st.session_state.local_db.at[idx, "المنطقة"] = new_edit_region
                            st.session_state.local_db.at[idx, "رقم العقار"] = new_edit_prop
                            st.session_state.search_val = ""         
                            st.success("✅ تم تحديث وتصحيح السجل بنجاح!")
                            st.rerun()

    # جافا سكريبت إدارة مؤشر الكتابة التلقائي لزر الـ Enter
    focus_script = "true" if st.session_state.focus_on_region else "false"
    st.session_state.focus_on_region = False

    js_code = [
        "<script>",
        "var attachMidanEvents = function() {",
        "var mainDoc = window.parent.document; var inputs = mainDoc.getElementsByTagName('input'); var buttons = mainDoc.getElementsByTagName('button');",
        "var regInput = null; var propInput = null; var saveBtn = null;",
        "for (var i = 0; i < inputs.length; i++) {",
        "if (inputs[i].getAttribute('placeholder') === 'النبطية، صور، صيدا...') regInput = inputs[i];",
        "if (inputs[i].getAttribute('placeholder') === 'ادخل رقم العقار الحالي....') propInput = inputs[i];",
        "}",
        "for (var j = 0; j < buttons.length; j++) { if (buttons[j].textContent.includes('🚀')) saveBtn = buttons[j]; }",
        "var activeInput = mainDoc.activeElement;",
        "if (" + focus_script + " && regInput) { regInput.focus(); regInput.select(); }",
        "else if (regInput && activeInput !== regInput && activeInput !== propInput && (!activeInput || activeInput.tagName !== 'INPUT')) { regInput.focus(); }",
        "if (regInput && propInput) {",
        "regInput.removeEventListener('keydown', window.regMidanHandler);",
        "window.regMidanHandler = function(e) { if (e.key === 'Enter') { e.preventDefault(); propInput.focus(); propInput.select(); } };",
        "regInput.addEventListener('keydown', window.regMidanHandler);",
        "}",
        "if (propInput && saveBtn && regInput) {",
        "propInput.removeEventListener('keydown', window.propMidanHandler);",
        "window.propMidanHandler = function(e) { if (e.key === 'Enter') { if (propInput.value.trim() !== '') { e.preventDefault(); saveBtn.click(); setTimeout(function() { regInput.focus(); regInput.select(); }, 100); } } };",
        "propInput.addEventListener('keydown', window.propMidanHandler);",
        "}",
        "}; setTimeout(attachMidanEvents, 200); setInterval(attachMidanEvents, 1000);",
        "</script>"
    ]
    st.components.v1.html("".join(js_code), height=0)
