import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# التنسيقات وحماية الواجهة وضبط الأحجام
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
        overflow: visible !important; 
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
    
    .metric-box { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; padding: 8px 15px; border-radius: 10px; text-align: center; box-shadow: 0 3px 6px rgba(59, 130, 246, 0.15); margin-top: 2px; margin-bottom: 2px; }
    .metric-val { font-size: 22px; font-weight: bold; }
    .metric-lbl { font-size: 12px; opacity: 0.9; }
    
    div.stButton > button, div.stDownloadButton > button { border: none; padding: 8px 12px; border-radius: 8px; font-weight: 700; transition: all 0.3s ease; width: 100%; height: 40px; margin-top: 2px; margin-bottom: 2px; }
    
    div[data-testid="stVerticalBlock"] > div { depth: 0 !important; margin-bottom: -0.3rem !important; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    
    [data-testid="stInputInstructions"] { display: none !important; visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة الـ Session State لحفظ واستعادة البيانات
if "local_db" not in st.session_state:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار", "رقم المشروع"])

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "last_project" not in st.session_state: st.session_state.last_project = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False

# متغير للتحكم بقيمة حقل البحث عند إنهاء التعديل
if "search_val" not in st.session_state:
    st.session_state.search_val = ""

# متغير توجيه الفوكس لحقل المنطقة بعد التعديل
if "focus_on_region" not in st.session_state:
    st.session_state.focus_on_region = False

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v6.1</div></div>""", unsafe_allow_html=True)
    
    if not st.session_state.file_uploaded:
        st.markdown("### 📥 خطوة 1: رفع ملف البيانات الاحتياطي")
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) الذي قمت بتنزيله سابقاً لاستعادة الأعداد والمتابعة:", type=["csv"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str, "رقم المشروع": str})
                if "رقم المشروع" not in uploaded_df.columns:
                    uploaded_df["رقم المشروع"] = ""
                st.session_state.local_db = uploaded_df
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل الملف بنجاح واستعادة كافة البيانات!")
                st.rerun()  
            except Exception as e:
                st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db

    st.markdown("---")
    
    # حقول الإدخال الأساسية
    c1, c2, c3 = st.columns(3)
    with c1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="ادخل اسم المنطقة....", key="region_field").strip()
    with c2:
        project_input = st.text_input("📁 رقم المشروع الحالي", value=st.session_state.last_project, placeholder="ادخل رقم المشروع....", key="project_field").strip()
    with c3:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار....", key="property_field").strip()
    
    st.session_state.clear_trigger = False

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", type="primary", use_container_width=True)
        
    with action_col2:
        if not df.empty:
            sorted_df = df.sort_values(by=["المنطقة", "رقم المشروع", "رقم العقار"]).reset_index(drop=True)
            csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="🟢 تحميل وتنزيل سجل CSV النهائي", data=csv_data, file_name="KhatibAlami_Midan_Data.csv", mime="text/csv", use_container_width=True)
        else:
            st.button("🟢 سجل CSV فارغ حالياً", disabled=True, use_container_width=True)

    total_properties_count = len(df)
    region_properties_count = 0
    if region_input:
        region_properties_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()])

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1: st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2: st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_properties_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ربط حقل البحث بالـ Session State للتحكم بمسحه لاحقاً فور الحفظ
    search_query = st.text_input("🔍 البحث الفوري عن عقار، منطقة أو مشروع وتعديله:", value=st.session_state.search_val, placeholder="البحث الفوري...", key="search_modify_field").strip()
    st.session_state.search_val = search_query

    # جافا سكريبت الذكي للتنقل الفوري والتركيز التلقائي على الحقول
    focus_script = "false"
    if st.session_state.focus_on_region:
        focus_script = "true"
        st.session_state.focus_on_region = False

    st.components.v1.html(f"""<script>
        var attachMidanEvents = function() {{(
            var mainDoc = window.parent.document; var inputs = mainDoc.getElementsByTagName('input'); var buttons = mainDoc.getElementsByTagName('button');
            var regInput = null; var projInput = null; var propInput = null; var saveBtn = null; var searchInput = null;
            
            for (var i = 0; i < inputs.length; i++) {{
                if (inputs[i].getAttribute('placeholder') === 'ادخل اسم المنطقة....') regInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'ادخل رقم المشروع....') projInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'ادخل رقم العقار....') propInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'البحث الفوري...') searchInput = inputs[i];
            }}
            for (var j = 0; j < buttons.length; j++) {{ if (buttons[j].textContent.includes('🚀 حفظ العقار والتحقق من التكرار')) saveBtn = buttons[j]; }}
            
            var activeInput = mainDoc.activeElement;
            var isUserInSearchOrEdit = false;
            if (searchInput && (searchInput.value.trim() !== "" || activeInput === searchInput)) {{ isUserInSearchOrEdit = true; }}
            if (activeInput && (activeInput.id.includes('edit_reg_') || activeInput.id.includes('edit_proj_') || activeInput.id.includes('edit_prop_'))) {{ isUserInSearchOrEdit = true; }}
            
            // إذا انتهى التعديل، نجبر الماوس على الذهاب مباشرة للمنطقة
            if ({focus_script} && regInput) {{
                regInput.focus();
                regInput.select();
            }} else if (regInput && !isUserInSearchOrEdit && activeInput !== regInput && activeInput !== projInput && activeInput !== propInput) {{
                regInput.focus();
            }}
            
            if (regInput && projInput) {{
                regInput.removeEventListener('keydown', window.regMidanHandler);
                window.regMidanHandler = function(e) {{ if (e.key === 'Enter') {{ e.preventDefault(); e.stopPropagation(); projInput.focus(); projInput.select(); }} }};
                regInput.addEventListener('keydown', window.regMidanHandler);
            }}
            if (projInput && propInput) {{
                projInput.removeEventListener('keydown', window.projMidanHandler);
                window.projMidanHandler = function(e) {{ if (e.key === 'Enter') {{ e.preventDefault(); e.stopPropagation(); propInput.focus(); propInput.select(); }} }};
                projInput.addEventListener('keydown', window.projMidanHandler);
            }}
            if (propInput && saveBtn && regInput) {{
                propInput.removeEventListener('keydown', window.propMidanHandler);
                window.propMidanHandler = function(e) {{ 
                    if (e.key === 'Enter') {{ 
                        if (propInput.value.trim() !== "") {{ 
                            e.preventDefault(); e.stopPropagation();
                            saveBtn.click(); 
                            setTimeout(function() {{ projInput.focus(); projInput.select(); }}, 80); 
                        }} 
                    }} 
                }};
                propInput.addEventListener('keydown', window.propMidanHandler);
            }}
        )}}; setTimeout(attachMidanEvents, 200); setInterval(attachMidanEvents, 1000);
    </script>""", height=0)

    # معالجة وحفظ البيانات وتطبيق التحقق الثلاثي من التكرار
    if btn_save:
        if region_input and project_input and property_number:
            is_duplicate = df[
                (df["المنطقة"].str.strip().str.lower() == region_input.lower()) & 
                (df["رقم المشروع"].str.strip().str.lower() == project_input.lower()) & 
                (df["رقم العقار"].str.strip() == property_number)
            ].shape[0] > 0
            
            if is_duplicate:
                st.error(f"❌ إلغاء: هذا العقار رقم ({property_number}) مسجل مسبقاً في نفس المشروع [{project_input}] بمنطقة [{region_input}]!")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم المشروع": project_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.last_project = project_input
                st.session_state.clear_trigger = True
                st.success(f"✅ تم حفظ العقار رقم ({property_number}) للمشروع ({project_input}) بنجاح!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء كافة الخانات الثلاثة قبل الحفظ.")

    # تشغيل منطق التعديل والبحث المباشر
    if search_query:
        matched_records = df[
            df["المنطقة"].str.contains(search_query, case=False, na=False) | 
            df["رقم المشروع"].astype(str).str.contains(search_query, case=False, na=False) | 
            df["رقم العقار"].astype(str).str.contains(search_query, case=False, na=False)
        ]
        
        if not matched_records.empty:
            st.info(f"📋 تم العثور على ({len(matched_records)}) سجل متطابق:")
            for idx, row in matched_records.iterrows():
                with st.expander(f"⚙️ تعديل عقار {row['رقم العقار']} - مشروع {row['رقم المشروع']} - منطقة {row['المنطقة']}", expanded=True):
                    edit_c1, edit_c2, edit_c3 = st.columns(3)
                    with edit_c1:
                        new_edit_region = st.text_input("تعديل اسم المنطقة", value=row['المنطقة'], key=f"edit_reg_{idx}").strip()
                    with edit_c2:
                        new_edit_project = st.text_input("تعديل رقم المشروع", value=row['رقم المشروع'], key=f"edit_proj_{idx}").strip()
                    with edit_c3:
                        new_edit_prop = st.text_input("تعديل رقم العقار", value=row['رقم العقار'], key=f"edit_prop_{idx}").strip()
                    
                    save_edit_btn = st.button("💾 حفظ التعديلات", key=f"save_edit_{idx}")
                    if save_edit_btn:
                        if new_edit_region and new_edit_project and new_edit_prop:
                            check_dup = df[
                                (df["المنطقة"].str.strip().str.lower() == new_edit_region.lower()) & 
                                (df["رقم المشروع"].str.strip().str.lower() == new_edit_project.lower()) & 
                                (df["رقم العقار"].str.strip() == new_edit_prop) & 
                                (df.index != idx)
                            ]
                            if not check_dup.empty:
                                st.error("❌ خطأ: التعديل المختار يطابق تماماً سجلاً آخر موجود بالفعل!")
                            else:
                                st.session_state.local_db.at[idx, "المنطقة"] = new_edit_region
                                st.session_state.local_db.at[idx, "رقم المشروع"] = new_edit_project
                                st.session_state.local_db.at[idx, "رقم العقار"] = new_edit_prop
                                
                                # التعديل الحاسم: مسح نص البحث فوراً لإخفاء صناديق التعديل وتوجيه الماوس للمنطقة
                                st.session_state.search_val = ""
                                st.session_state.focus_on_region = True
                                
                                st.success("✅ تم التحديث بنجاح وتم مسح شاشة البحث!")
                                st.rerun()
                        else:
                            st.error("⚠️ لا يمكن ترك الحقول فارغة.")
        else:
            st.warning("ℹ️ لم يتم العثور على أي بيانات مطابقة للبحث.")
