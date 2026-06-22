import streamlit as st
import pandas as pd
import requests
import base64
import os
import glob

# 🌐 1. إعدادات الصفحة الرسمية للشركة
st.set_page_config(
    page_title="Khatib & Alami Company", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔑 إعدادات الحساب والمستودع الخاص بك على GitHub
GITHUB_TOKEN = "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع_YOUR_USERNAME/YOUR_REPO"
OUTPUT_FILENAME = "KhatibAlami_Midan_Data.csv"

# دالة الرفع والمزامنة التلقائية على GitHub
def upload_to_github(dataframe):
    if GITHUB_TOKEN == "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN":
        return False
    try:
        csv_content = dataframe.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True).to_csv(index=False).encode('utf-8-sig')
        encoded_content = base64.b64encode(csv_content).decode('utf-8')
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{OUTPUT_FILENAME}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        data = {"message": "تحديث تلقائي فوري لسجل العقارات الميداني - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except Exception as e:
        return False

# دالة قراءة الملف بجانب الكود بأي صيغة وترميز عربي عند بدء التشغيل
def load_any_local_file():
    local_files = glob.glob("*.csv") + glob.glob("*.xlsx") + glob.glob("*.xls") + glob.glob("*.CSV") + glob.glob("*.XLSX")
    for f_path in local_files:
        if "~$" in f_path: continue
        try:
            if f_path.lower().endswith('.csv'):
                for encoding_type in ['utf-8-sig', 'utf-8', 'cp1256', 'latin-1']:
                    try:
                        df_loaded = pd.read_csv(f_path, encoding=encoding_type, dtype={"المنطقة": str, "رقم العقار": str})
                        if "المنطقة" in df_loaded.columns and "رقم العقار" in df_loaded.columns:
                            return df_loaded[["المنطقة", "رقم العقار"]]
                    except: continue
            elif f_path.lower().endswith(('.xlsx', '.xls')):
                df_loaded = pd.read_excel(f_path, dtype={"المنطقة": str, "رقم العقار": str})
                if "المنطقة" in df_loaded.columns and "رقم العقار" in df_loaded.columns:
                    return df_loaded[["المنطقة", "رقم العقار"]]
        except: pass

    if GITHUB_TOKEN != "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN":
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{OUTPUT_FILENAME}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                file_data = res.json()
                csv_bytes = base64.b64decode(file_data["content"])
                import io
                return pd.read_csv(io.BytesIO(csv_bytes), encoding='utf-8-sig', dtype={"المنطقة": str, "رقم العقار": str})
        except: pass
    return pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🎨 التنسيقات والواجهات الرسومية المعتمدة للشركة
ultimate_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');
html, body, [class*='css'], [data-testid='stAppViewContainer'] { 
    font-family: 'Tajawal', sans-serif !important; 
    direction: rtl !important; 
    text-align: right !important; 
}
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; }
header[data-testid='stHeader'] { background: transparent !important; display: none !important; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
.header-card { 
    background-color: #EBF8FF !important; padding: 20px 12px !important; border-radius: 12px !important; 
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08) !important; margin-bottom: 2px !important; text-align: center !important; border: 1px solid #BEE3F8 !important; 
}
.company-header { color: #1E3A8A !important; font-family: 'Arial', sans-serif !important; font-size: 28px !important; font-weight: bold !important; }
.company-subtitle { color: #2D3748 !important; font-size: 15px !important; font-weight: 500 !important; margin-top: 4px !important; }
.main-signature-card { 
    background-color: #ffffff !important; padding: 14px 16px !important; border-radius: 10px !important; text-align: center !important; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04) !important; margin: 10px auto 20px auto !important; border: 1px solid #e2e8f0 !important; max-width: 550px !important; 
}
.sig-title { color: #4A5568 !important; font-size: 13px; font-weight: bold; }
.sig-name { color: #E53E3E !important; font-size: 18px; font-weight: 700; margin-top: 2px; }

/* تنسيق أزرار الحفظ والتنزيل */
div.stButton > button {
    background-color: #EF4444 !important; color: white !important; border: 1px solid #DC2626 !important;
    font-weight: 700 !important; font-size: 16px !important; height: 50px !important; border-radius: 10px !important; width: 100% !important;
}
div.stButton > button:hover { background-color: #DC2626 !important; }

.blue-total-metric {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important; padding: 20px !important; border-radius: 12px !important;
    text-align: center !important; height: 125px !important; display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: center !important;
}
.blue-total-title { font-size: 15px !important; font-weight: bold !important; color: #ffffff !important; margin-bottom: 6px !important; }
.blue-total-value { font-size: 36px !important; font-weight: 700 !important; color: #ffffff !important; }
div.midan-interactive-box button {
    background: #ffffff !important; color: #2d3748 !important; border: 1px solid #cbd5e0 !important; border-radius: 12px !important;
    height: 125px !important; width: 100% !important; font-size: 16px !important; font-weight: bold; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; white-space: pre-line !important;
}
.info-file-card {
    background-color: #FFFAF0 !important; border: 1px solid #FEEBC8 !important; border-radius: 12px !important;
    padding: 20px !important; margin-top: 25px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
}
.info-file-title { color: #DD6B20 !important; font-size: 18px !important; font-weight: bold !important; margin-bottom: 10px !important; border-bottom: 2px solid #FEEBC8; padding-bottom: 5px; }
.info-file-text { color: #4A5568 !important; font-size: 14.5px !important; line-height: 1.7 !important; }
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# إدارة الذاكرة وحفظ الجلسة
if "local_db" not in st.session_state: st.session_state.local_db = load_any_local_file()
if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 📂 [جديد] صندوق رفع وتحديث ملف المعلومات والعقارات الفوري
    st.markdown("### 📥 رفع وتحديث ملف البيانات مباشرة للبرنامج")
    uploaded_file = st.file_uploader("اسحب ملف الـ CSV أو الإكسيل المعدل وضعه هنا لتحديث السجل فوراً وللقراءة المباشرة:", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # قراءة الملف المرفوع حسب نوعه وبأكثر من ترميز للأحرف العربية
            if uploaded_file.name.lower().endswith('.csv'):
                uploaded_df = None
                for encoding_type in ['utf-8-sig', 'utf-8', 'cp1256', 'latin-1']:
                    try:
                        uploaded_df = pd.read_csv(uploaded_file, encoding=encoding_type, dtype={"المنطقة": str, "رقم العقار": str})
                        if "المنطقة" in uploaded_df.columns and "رقم العقار" in uploaded_df.columns:
                            break
                    except: continue
            else:
                uploaded_df = pd.read_excel(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
            
            if uploaded_df is not None and "المنطقة" in uploaded_df.columns and "رقم العقار" in uploaded_df.columns:
                # تصفية الأعمدة وتخزينها في الجلسة
                st.session_state.local_db = uploaded_df[["المنطقة", "رقم العقار"]].dropna(subset=["المنطقة", "رقم العقار"])
                
                # حفظ الملف محلياً بجانب السكريبت ليثبت عند إعادة التشغيل
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                
                # رفع الملف فوراً ومزامنته على مستودع GitHub الخاص بك
                upload_to_github(st.session_state.local_db)
                st.success(f"✅ تم رفع وقراءة ملف '{uploaded_file.name}' بنجاح وحفظه وتأمين مزامنته سحابياً!")
            else:
                st.error("❌ خطأ: تأكد من أن الملف يحتوي على أعمدة باسم 'المنطقة' و 'رقم العقار' بشكل صحيح.")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء معالجة الملف: {str(e)}")

    df = st.session_state.local_db
    st.markdown("---")
    
    # 📋 حقول المدخلات الميدانية السريعة
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="النبطية، صور، صيدا...", key="region_field").strip()
    with input_col2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field").strip()
    
    st.session_state.clear_trigger = False

    # 🟥 أزرار الحفظ والتنزيل اليدوي
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", key="save_btn_main", use_container_width=True)
    with action_col2:
        btn_download = st.button("📥 تنزيل يدوي إضافي للسجل (نسخة مؤكدة)", key="download_btn_main", use_container_width=True)
        if btn_download:
            if not df.empty:
                sorted_df = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="💾 اضغط هنا لتأكيد التنزيل", data=csv_data, file_name=OUTPUT_FILENAME, mime="text/csv", key="confirm_dl_btn", use_container_width=True)
            else: st.warning("⚠️ السجل فارغ حالياً!")

    if btn_save:
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            if is_duplicate: st.error("❌ إلغاء: هذا العقار مسجل سابقاً في هذه المنطقة!")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                upload_to_github(st.session_state.local_db)
                st.success(f"✅ تم حفظ وتأمين العقار رقم ({property_number}) بنجاح!")
                st.rerun()
        else: st.warning("⚠️ فضلاً، يرجى ملء حقول المنطقة ورقم العقار أولاً.")

    # الإحصائيات الفورية
    total_count = len(st.session_state.local_db)
    region_count = 0
    if region_input:
        region_count = len(st.session_state.local_db[st.session_state.local_db["المنطقة"].str.strip().str.lower() == region_input.lower()])

    st.markdown("<br>", unsafe_allow_html=True)

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='blue-total-metric'><div class='blue-total-title'>🗄️ TOTAL PROPERTY COUNT IN FILE</div><div class='blue-total-value'>{total_count}</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown("<div class='midan-interactive-box'>", unsafe_allow_html=True)
        display_label = f"🔸 عدد عقارات منطقة ({region_input if region_input else '...'})"
        if st.button(label=f"{display_label}\n{region_count}", key="go_to_region_btn", use_container_width=True):
            st.session_state.focus_on_region = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if region_input:
        st.markdown(f"### 📊 ملف العقارات الجاري العمل عليها في منطقة: ({region_input})")
        filtered_df = st.session_state.local_db[st.session_state.local_db["المنطقة"].str.strip().str.lower() == region_input.lower()]
        if not filtered_df.empty:
            display_sheet = pd.DataFrame(filtered_df["رقم العقار"].values, columns=["رقم العقار"]).sort_values(by="رقم العقار").reset_index(drop=True)
            display_sheet.index += 1
            st.dataframe(display_sheet, use_container_width=True, height=200)
        else: st.info("ℹ️ لا توجد عقارات مسجلة لهذه المنطقة حالياً.")

    st.markdown("---")

    # محرك البحث والتصحيح والتعديل الفوري
    search_query = st.text_input("🔍 البحث الفوري عن عقار وتعديله:", value=st.session_state.search_val, placeholder="اكتب اسم المنطقة أو رقم العقار للبحث السريع والتعديل...", key="search_modify_field").strip()
    st.session_state.search_val = search_query

    if search_query:
        matched_records = st.session_state.local_db[st.session_state.local_db["المنطقة"].str.contains(search_query, case=False, na=False) | st.session_state.local_db["رقم العقار"].astype(str).str.contains(search_query, case=False, na=False)]
        if not matched_records.empty:
            st.info(f"📋 تم العثور على ({len(matched_records)}) سجل متطابق:")
            for idx, row in matched_records.iterrows():
                with st.expander(f"⚙️ تعديل العقار رقم {row['رقم العقار']} في {row['المنطقة']}", expanded=True):
                    edit_c1, edit_c2 = st.columns(2)
                    with edit_c1: new_edit_region = st.text_input("تعديل اسم المنطقة", value=row['المنطقة'], key=f"edit_reg_{idx}").strip()
                    with edit_c2: new_edit_prop = st.text_input("تعديل رقم العقار", value=row['رقم العقار'], key=f"edit_prop_{idx}").strip()
                    if st.button("💾 حفظ تعديلات السجل", key=f"save_edit_{idx}", use_container_width=True):
                        if new_edit_region and new_edit_prop:
                            st.session_state.local_db.at[idx, "المنطقة"] = new_edit_region
                            st.session_state.local_db.at[idx, "رقم العقار"] = new_edit_prop
                            sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                            sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                            upload_to_github(st.session_state.local_db)
                            st.session_state.search_val = ""         
                            st.success("✅ تم تحديث وتصحيح السجل ومزامنته بنجاح!")
                            st.rerun()

    # 📖 ملف معلومات وإرشادات البرنامج الثابتة
    st.markdown("""
    <div class='info-file-card'>
        <div class='info-file-title'>📖 ملف معلومات البرنامج وإرشادات الميدان</div>
        <div class='info-file-text'>
            مرحباً بك في نظام حصر الأضرار والطباعة الميداني لشركة <b>Khatib & Alami</b>.<br>
            • <b>ميزة الرفع الجديدة:</b> يمكنك الآن استخدام الصندوق العلوي لرفع ملف عقارات كامل ومعدل من جهازك مباشرة.<br>
            • <b>إدخال البيانات الحرة:</b> اكتب اسم المنطقة، واضغط <b>Enter</b> لينتقل المؤشر تلقائياً لحقل رقم العقار لبدء العمل المباشر.<br>
            • <b>منع التكرار:</b> يفحص البرنامج التكرار آلياً ويمنع إدخال نفس العقار مرتين بالخطأ في نفس المنطقة الجغرافية.<br>
            • <b>المزامنة السحابية الفورية:</b> كل عقار جديد تحفظه أو ملف ترفعه، يتم بث نسخه منه مباشرة لمستودع <b>GitHub</b> لضمان عدم ضياع أي بيانات.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # أتمتة جافا سكربت للتنقل السريع
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
