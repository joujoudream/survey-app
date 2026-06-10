import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khatib & Alami Company", layout="wide", initial_sidebar_state="collapsed")

# التنسيقات وحماية الواجهة وإلغاء التنبيهات الافتراضية تماماً
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

if "local_db" not in st.session_state:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div><div class='sig-note'>صمم بعناية لأجل دقة التوثيق والراحة | KhatibAlami System v5.6</div></div>""", unsafe_allow_html=True)
    
    if not st.session_state.file_uploaded:
        st.markdown("### 📥 خطوة 1: رفع ملف البيانات الاحتياطي")
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) الذي قمت بتنزيله سابقاً لاستعادة الأعداد والمتابعة:", type=["csv"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                st.session_state.local_db = uploaded_df
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل الملف بنجاح واستعادة كافة البيانات!")
                st.rerun()  
            except Exception as e:
                st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db

    st.markdown("---")
    
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

    total_properties_count = len(df)
    region_properties_count = 0
    if region_input:
        region_properties_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()])

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1: st.markdown(f"<div class='metric-box'><div class='metric-val'>{total_properties_count}</div><div class='metric-lbl'>📊 مجموع عدد العقارات الكلي</div></div>", unsafe_allow_html=True)
    with stat_col2: st.markdown(f"<div class='metric-box'><div class='metric-val'>{region_properties_count}</div><div class='metric-lbl'>📍 عدد العقارات في نفس المنطقة الحالية</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    search_query = st.text_input("🔍 البحث الفوري عن عقار وتعديله:", placeholder="البحث الفوري عن عقار وتعديله...", key="search_modify_field").strip()

    # جافا سكريبت لمنع طلب Enter مرتين وللإدخال الفوري بنقرة واحدة
    st.components.v1.html("""<script>
        var attachMidanEvents = function() {
            var mainDoc = window.parent.document; var inputs = mainDoc.getElementsByTagName('input'); var buttons = mainDoc.getElementsByTagName('button');
            var regInput = null; var propInput = null; var saveBtn = null; var searchInput = null;
            
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].getAttribute('placeholder') === 'ادخل اسم المنطقة الحالية ....') regInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'ادخل رقم العقار الحالي....') propInput = inputs[i];
                if (inputs[i].getAttribute('placeholder') === 'البحث الفوري عن عقار وتعديله...') searchInput = inputs[i];
            }
            for (var j = 0; j < buttons.length; j++) { if (buttons[j].textContent.includes('🚀 حفظ العقار والتحقق من التكرار')) saveBtn = buttons[j]; }
            
            var activeInput = mainDoc.activeElement;
            var isUserInSearchOrEdit = false;
            if (searchInput && (searchInput.value.trim() !== "" || activeInput === searchInput)) { isUserInSearchOrEdit = true; }
            if (activeInput && (activeInput.id.includes('edit_reg_') || activeInput.id.includes('edit_prop_'))) { isUserInSearchOrEdit = true; }
            
            if (regInput && !isUserInSearchOrEdit && activeInput !== regInput && activeInput !== propInput) { regInput.focus(); }
            
            if (regInput && propInput) {
                regInput.removeEventListener('keydown', window.regMidanHandler);
                window.regMidanHandler = function(e) { 
                    if (e.key === 'Enter') { 
                        e.preventDefault(); e.stopPropagation();
                        propInput.focus(); propInput.select(); 
                    } 
                };
                regInput.addEventListener('keydown', window.regMidanHandler);
            }
            if (propInput && saveBtn && regInput) {
                propInput.removeEventListener('keydown', window.propMidanHandler);
                window.propMidanHandler = function(e) { 
                    if (e.key === 'Enter') { 
                        if (propInput.value.trim() !== "") { 
                            e.preventDefault(); e.stopPropagation();
                            saveBtn.click(); 
                            setTimeout(function() { regInput.focus(); regInput.select(); }, 80); 
                        } 
                    } 
                };
                propInput.addEventListener('keydown', window.propMidanHandler);
            }
        }; setTimeout(attachMidanEvents, 200); setInterval(attachMidanEvents, 1000);
    </script>""", height=0)

    # معالجة وحفظ البيانات وتطبيق شروط منع التكرار الشاملة
    if btn_save:
        if region_input and property_number:
            # التحقق من وجود رقم العقار في أي منطقة على إمتداد قاعدة البيانات بالكامل
            duplicate_record = df[df["رقم العقار"].str.strip() == property_number]
            
            if not duplicate_record.empty:
                # العثور على اسم المنطقة الأولى التي تحتوي على هذا العقار لعرضها في التنبيه
                existing_region = duplicate_record.iloc[0]["المنطقة"]
                st.error(f"❌ إلغاء: رقم العقار ({property_number}) مسجل مسبقاً في منطقة [{existing_region}]! ممنوع التكرار في جميع المناطق.")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                st.success(f"✅ تم حفظ العقار رقم ({property_number}) بنجاح!")
                st.rerun()
        else:
            st.warning("⚠️ فضلاً، يرجى ملء الخانات أولاً قبل الحفظ.")

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
                            # عند التعد
