import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# 🎨 التنسيقات الذهبية الموحدة مع الإخفاء الكامل للمربع الأبيض والزر الشفاف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    header[data-testid="stHeader"] { background: transparent !important; height: 0px !important; display: none !important; }
    
    .block-container { 
        padding-top: 2.5rem !important; 
        padding-bottom: 1rem !important; 
    }
    
    .header-card { 
        background-color: #EBF8FF; 
        padding: 24px 12px 20px 12px; 
        border-radius: 12px; 
        box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08); 
        margin-top: 10px; 
        margin-bottom: 2px; 
        text-align: center; 
        border: 1px solid #BEE3F8; 
    }
    .company-header { color: #1E3A8A; font-family: 'Arial', sans-serif; font-size: 30px; font-weight: bold; margin: 0; line-height: 1.2; }
    .company-subtitle { color: #2D3748; font-family: 'Arial', sans-serif; font-size: 16px; font-weight: 500; margin-top: 6px; }
    
    .main-signature-card { 
        background-color: #ffffff; 
        padding: 8px 16px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04); 
        margin-top: 4px; 
        margin-bottom: 12px; 
        border: 1px solid #e2e8f0; 
        width: 100%; 
        max-width: 550px; 
        margin-left: auto; 
        margin-right: auto; 
    }
    .sig-title { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; color: #1E3A8A; margin: 0; }
    .sig-name { font-family: 'Arial', sans-serif; font-size: 14px; font-weight: bold; color: #475569; margin: 2px 0; }
    .sig-note { font-size: 11px; color: #3b82f6; font-weight: 500; margin: 0; }
    
    /* 🔵 تصميم العدادات المتطابقة تماماً كتوأم أزرق ملكي */
    .metric-box-twin { 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
        color: white !important; 
        padding: 12px 15px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.15); 
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
    }
    .metric-val-twin { font-size: 26px; font-weight: bold; line-height: 1.1; color: white !important; }
    .metric-lbl-twin { font-size: 13px; opacity: 0.95; margin-top: 5px; color: white !important; }
    
    /* 🔴 تفجير وإلغاء المربع الأبيض الافتراضي من الحاوية نهائياً */
    div[data-testid="stBlock"] div.stButton {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* جعل الزر الميكانيكي الشفاف ممتداً فوق كامل مساحة الصندوق الأزرق للضغط المباشر */
    div.stButton > button.hidden-clickable-btn {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 85px !important;
        background: transparent !important;
        background-color: transparent !important;
        color: transparent !important;
        color: rgba(0,0,0,0) !important;
        border: none !important;
        box-shadow: none !important;
        cursor: pointer !important;
        z-index: 10;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* الحاوية التفاعلية مع تأثير التمرير الصاعد */
    .interactive-container {
        position: relative;
        width: 100%;
        height: 85px;
        transition: all 0.2s ease-in-out;
    }
    .interactive-container:hover {
        transform: translateY(-3px);
        filter: brightness(1.15);
    }
    
    div.stButton > button, div.stDownloadButton > button { border: none; padding: 8px 12px; border-radius: 8px; font-weight: 700; transition: all 0.3s ease; width: 100%; height: 40px; margin-top: 2px; margin-bottom: 2px; }
    div[data-testid="stVerticalBlock"] > div { depth: 0 !important; margin-bottom: -0.3rem !important; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    [data-testid="stInputInstructions"] { display: none !important; visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة الـ Session State
if "local_db" not in st.session_state:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False
if "show_excel_sheet" not in st.session_state: st.session_state.show_excel_sheet = False

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v6.9</div></div>""", unsafe_allow_html=True)
    
    if not st.session_state.file_uploaded:
        st.markdown("### 📥 خطوة 1: رفع ملف البيانات الاحتياطي")
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) الذي قمت بتنزيله سابقاً لاستعادة الأعداد والمتابعة:", type=["csv"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                st.session_state.local_db = uploaded_df[["المنطقة", "رقم العقار"]]
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل الملف بنجاح واستعادة كافة البيانات!")
                st.rerun()  
            except Exception as e:
                st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db
    st.markdown("---")
    
    # حقول الإدخال الأساسية الثنائية (المنطقة والعقار)
    c1, c2 = st.columns(2)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="ادخل اسم المنطقة الحالية ....", key="region_field").strip()
    with c2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field").strip()
    
    st.session_state.clear_trigger = False

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

    # احتساب الأعداد بدقة للحقول
    total_properties_count = len(df)
    region_properties_count = 0
    if region_input:
        region_properties_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()])

    # 📊 عرض التوأم المتطابق بالكامل باللون الأزرق الملكي والحجم الموحد 100% النظيف تماماً
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1: 
        # العداد الكلي الثابت
        st.markdown(f"""
            <div class='metric-box-twin'>
                <div class='metric-val-twin'>{total_properties_count}</div>
                <div class='metric-lbl-twin'>📊 مجموع عدد العقارات الكلي</div>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col2: 
        # العداد المحلي التفاعلي المتطابق بالكامل
        st.markdown(f"""
            <div class='interactive-container'>
                <div class='metric-box-twin'>
                    <div class='metric-val-twin'>{region_properties_count}</div>
                    <div class='metric-lbl-twin'>📍 عدد العقارات في نفس المنطقة (اضغط للعرض)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # زر شفاف صامت بالكامل وبدون إظهار أي مربعات بيضاء في الخلفية
        btn_show_sheet = st.button("", key="regional_action_trigger_secret_key")
        
        # كود التثبيت الفوري لإخفاء بقايا أزرار الـ Streamlit البيضاء وجعلها غير مرئية
        st.markdown("""
            <script>
            var allButtons = window.parent.document.querySelectorAll('div.stButton > button');
            allButtons.forEach(function(b) {
                if(b.innerHTML === "" || b.innerText === "" || b.textContent === "") {
                    b.classList.add('hidden-clickable-btn');
                    // إخفاء حاوية الإطار الخارجي لمنع ظهور أي بقايا بيضاء
                    if(b.parentElement) {
                        b.parentElement.style.background = 'transparent';
                        b.parentElement.style.backgroundColor = 'transparent';
                    }
                }
            });
            </script>
        """, unsafe_allow_html=True)
        
        if btn_show_sheet:
            st.session_state.show_excel_sheet = True

    # 📊 عرض الجدول المخصص والمصفى بدقة لأرقام العقارات الحقيقية
    if st.session_state.show_excel_sheet and region_input:
        st.markdown("<div id='excel_section'></div>", unsafe_allow_html=True) 
        st.markdown(f"### 📊 أرقام العقارات الجاري العمل عليها في منطقة: ({region_input})")
        
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        
        if not filtered_df.empty:
            excel_sheet_df = pd.DataFrame(filtered_df["رقم العقار"].values, columns=["رقم العقار"])
            excel_sheet_df = excel_sheet_df.sort_values(by="رقم العقار").reset_index(drop=True)
            excel_sheet_df.index += 1
            
            st.dataframe(excel_sheet_df, use_container_width=True, height=220)
            
            if st.button("❌ إغلاق وعودة لسطر الإدخال", key="close_excel_btn"):
                st.session_state.show_excel_sheet = False
                st.rerun()
        else:
            st.warning("ℹ️ هذه المنطقة لا تحتوي على أي عقارات مسجلة حالياً.")

    st.markdown("---")

    # حقل البحث الفوري والتعديل
    search_query = st.text_input("🔍 البحث الفوري عن عقار وتعديله:", value=st.session_state.search_val, placeholder="البحث الفوري عن عقار وتعديله...", key="search_modify_field").strip()
    st.session_state.search_val = search_query

    focus_script = "false"
    if st.session_state.focus_on_region:
        focus_script = "true"
        st.session_state.focus_on_region = False

    scroll_script = "false"
    if st.session_state.show_excel_sheet:
        scroll_script = "true"

    st.components.v1.html(f"""<script>
        var attachMidanEvents = function() {{
            var mainDoc = window.parent.document; var inputs = mainDoc.getElementsByTagName('input'); var buttons = mainDoc.getElementsByTagName('button');
            var regInput = null; var propInput = null; var saveBtn = null; var searchInput = null;
            
            for (var i = 0; i < inputs.length; i++) {{
                if (inputs[i].getAttribute('placeholder') === 'ادخل اسم المنطقة الحالية ....') regInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'ادخل رقم العقار الحالي....') propInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'البحث الفوري عن عقار وتعديله...') searchInput = inputs[i];
            }}
            for (var j = 0; j < buttons.length; j++) {{ if (buttons[j].textContent.includes('🚀 حفظ العقار والتحقق من التكرار')) saveBtn = buttons[j]; }}
            
            var activeInput = mainDoc.activeElement;
            var isUserInSearchOrEdit = false;
            if (searchInput && (searchInput.value.trim() !== "" || activeInput === searchInput)) {{ isUserInSearchOrEdit = true; }}
            if (activeInput && (activeInput.id.includes('edit_reg_') || activeInput.id.includes('edit_prop_'))) {{ isUserInSearchOrEdit = true; }}
            
            if ({focus_script} && regInput) {{
                regInput.focus();
                regInput.select();
            }} else if (regInput && !isUserInSearchOrEdit && activeInput !== regInput && activeInput !== propInput) {{
                regInput.focus();
            }}
            
            if ({scroll_script}) {{
                var target = mainDoc.getElementById('excel_section');
                if(target) {{ target.scrollIntoView({{ behavior: 'smooth', block: 'center' }}); }}
            }}
            
            if (regInput && propInput) {{
                regInput.removeEventListener('keydown', window.regMidanHandler);
                window.regMidanHandler = function(e) {{ if (e.key === 'Enter') {{ e.preventDefault(); e.stopPropagation(); propInput.focus(); propInput.select(); }} }};
                regInput.addEventListener('keydown', window.regMidanHandler);
            }}
            if (propInput && saveBtn && regInput) {{
                propInput.removeEventListener('keydown', window.propMidanHandler);
                window.propMidanHandler = function(e) {{ 
                    if (e.key === 'Enter') {{ 
                        if (propInput.value.trim() !== "") {{ 
                            e.preventDefault(); e.stopPropagation();
                            saveBtn.click(); 
                            setTimeout(function() {{ regInput.focus(); regInput.select(); }}, 80); 
                        }} 
                    }} 
                }};
                propInput.addEventListener('keydown', window.propMidanHandler);
            }}
        }}; setTimeout(attachMidanEvents, 200); setInterval(attachMidanEvents, 1000);
    </script>""", height=0)

    # حفظ البيانات والتحقق من التكرار
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
            st.warning("⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ.")

    # التعديل والبحث
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
                            check_dup = df[(df["المنطقة"].str.strip().str.lower() == new_edit_region.lower()) & (df["رقم العقار"].str.strip() == new_edit_prop) & (df.index != idx)]
                            if not check_dup.empty:
                                st.error("❌ خطأ: هذا العقار مسجل مسبقاً في هذه المنطقة المحددة!")
                            else:
                                st.session_state.local_db.at[idx, "المنطقة"] = new_edit_region
                                st.session_state.local_db.at[idx, "رقم العقار"] = new_edit_prop
                                st.session_state.search_val = ""         
                                st.session_state.last_region = ""        
                                st.session_state.focus_on_region = True  
                                st.success("✅ تم التحديث، ومسح الحقول للبدء بمنطقة جديدة!")
                                st.rerun()
                        else:
                            st.error("⚠️ لا يمكن ترك الحقول فارغة.")
