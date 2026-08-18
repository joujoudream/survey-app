import streamlit as st
import pandas as pd
import requests
import base64
import os
import glob
import io

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
        if dataframe.empty:
            df_secure = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
        else:
            df_secure = dataframe.copy()
            
        csv_content = df_secure.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True).to_csv(index=False).encode('utf-8-sig')
        encoded_content = base64.b64encode(csv_content).decode('utf-8')
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{OUTPUT_FILENAME}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        data = {"message": "تحديث تلقائي فوري لسجل العقارات الميداني - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except:
        return False

# دالة قراءة الملف عند بدء التشغيل
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
                df_git = pd.read_csv(io.BytesIO(csv_bytes), encoding='utf-8-sig', dtype={"المنطقة": str, "رقم العقار": str})
                if "المنطقة" in df_git.columns and "رقم العقار" in df_git.columns:
                    return df_git[["المنطقة", "رقم العقار"]]
        except: pass
    return pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🎨 التنسيقات والواجهات الرسومية
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
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04) !important; margin: 10px auto 15px auto !important; border: 1px solid #e2e8f0 !important; max-width: 550px !important; 
}
.sig-title { color: #4A5568 !important; font-size: 13px; font-weight: bold; }
.sig-name { color: #E53E3E !important; font-size: 18px; font-weight: 700; margin-top: 2px; }

div[data-testid="stTextInput"] input {
    font-size: 20px !important;
    font-weight: bold !important;
    color: #1E3A8A !important;
    height: 48px !important;
}
div[data-testid="stTextInput"] label p {
    font-size: 16px !important;
    font-weight: bold !important;
    color: #2D3748 !important;
}

div.stButton > button, div.stDownloadButton > button {
    background-color: #EF4444 !important; color: white !important; border: 1px solid #DC2626 !important;
    font-weight: 700 !important; font-size: 16px !important; height: 50px !important; border-radius: 10px !important; width: 100% !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover { background-color: #DC2626 !important; }

.print-section-box {
    background-color: #ffffff !important; padding: 15px !important; border-radius: 10px !important;
    border: 1px solid #cbd5e0 !important; margin-top: 20px !important;
}
div.print-zone-btn > div.stDownloadButton > button {
    background-color: #2563EB !important; border: 1px solid #1D4ED8 !important;
}
div.print-zone-btn > div.stDownloadButton > button:hover { background-color: #1D4ED8 !important; }

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
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# 🛡️ إدارة حالة الجلسة
if "local_db" not in st.session_state or st.session_state.local_db is None: 
    st.session_state.local_db = load_any_local_file()

if not isinstance(st.session_state.local_db, pd.DataFrame) or "المنطقة" not in st.session_state.local_db.columns or "رقم العقار" not in st.session_state.local_db.columns:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False

# متغيّرات إدارة التعديل والحذف
if 'selected_property' not in st.session_state: st.session_state.selected_property = None
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'selected_index' not in st.session_state: st.session_state.selected_index = None

if st.session_state.local_db.empty:
    st.session_state.show_uploader = True
else:
    st.session_state.show_uploader = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)
    
    if st.session_state.show_uploader:
        uploaded_file = st.file_uploader("📂 رفع واستيراد ملف بيانات قائم (Excel / CSV) لتحديث السجل فوراُ", type=["xlsx", "xls", "csv"], key="excel_uploader_widget")
        if uploaded_file is not None:
            df_uploaded = None
            try:
                if uploaded_file.name.lower().endswith('.csv'):
                    for encoding_type in ['utf-8-sig', 'utf-8', 'cp1256', 'latin-1']:
                        try:
                            df_uploaded = pd.read_csv(uploaded_file, encoding=encoding_type, dtype={"المنطقة": str, "رقم العقار": str})
                            if "المنطقة" in df_uploaded.columns and "رقم العقار" in df_uploaded.columns:
                                break
                        except: continue
                else:
                    df_uploaded = pd.read_excel(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                
                if df_uploaded is not None and "المنطقة" in df_uploaded.columns and "رقم العقار" in df_uploaded.columns:
                    cleaned_uploaded = df_uploaded[["المنطقة", "رقم العقار"]].dropna().copy()
                    cleaned_uploaded["المنطقة"] = cleaned_uploaded["المنطقة"].astype(str).str.strip()
                    cleaned_uploaded["رقم العقار"] = cleaned_uploaded["رقم العقار"].astype(str).str.strip()
                    
                    st.session_state.local_db = cleaned_uploaded
                    st.session_state.local_db = st.session_state.local_db.drop_duplicates(subset=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    st.session_state.show_uploader = False
                    st.session_state.focus_on_region = True
                    st.rerun()
            except:
                st.error("❌ فشل قراءة الملف.")

    df = st.session_state.local_db
    
    # 📋 إدخال العقارات الجديدة
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="النبطية، صور، صيدا...", key="region_field_unique").strip()
    with input_col2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field_unique").strip()
    
    st.session_state.clear_trigger = False

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", key="save_btn_main_unique", use_container_width=True)
    with action_col2:
        if not df.empty:
            sorted_df = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
            csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تنزيل سجل البيانات يدوياً (مباشر)",
                data=csv_data,
                file_name="KhatibAlami_Midan_Data.csv",
                mime="text/csv",
                key="download_btn_csv_direct_unique",
                use_container_width=True
            )
        else:
            st.button("📥 تنزيل سجل البيانات (السجل فارغ)", disabled=True, use_container_width=True, key="download_disabled_btn")

    if btn_save:
        if region_input and property_number:
            is_duplicate = False
            if not df.empty:
                is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            
            if is_duplicate: 
                st.error("❌ إلغاء: هذا العقار مسجل سابقاً في هذه المنطقة!")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                upload_to_github(st.session_state.local_db)
                st.rerun()
        else: 
            st.warning("⚠️ فضلاً، يرجى ملء حقول المنطقة ورقم العقار أولاً.")

    # الإحصائيات
    total_count = len(st.session_state.local_db)
    region_count = 0
    if region_input and not st.session_state.local_db.empty:
        region_count = len(st.session_state.local_db[st.session_state.local_db["المنطقة"].str.strip().str.lower() == region_input.lower()])

    st.markdown("<br>", unsafe_allow_html=True)

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='blue-total-metric'><div class='blue-total-title'>🗄️ TOTAL PROPERTY COUNT IN FILE</div><div class='blue-total-value'>{total_count}</div></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown("<div class='midan-interactive-box'>", unsafe_allow_html=True)
        display_label = f"🔸 عدد عقارات منطقة ({region_input if region_input else '...'})"
        if st.button(label=f"{display_label}\n{region_count}", key="go_to_region_btn_unique", use_container_width=True):
            st.session_state.focus_on_region = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض جدول المنطقة
    if region_input and not st.session_state.local_db.empty:
        filtered_df = st.session_state.local_db[st.session_state.local_db["المنطقة"].str.strip().str.lower() == region_input.lower()]
        if not filtered_df.empty:
            display_sheet = pd.DataFrame(filtered_df["رقم العقار"].values, columns=["رقم العقار"]).sort_values(by="رقم العقار").reset_index(drop=True)
            display_sheet.index += 1
            st.dataframe(display_sheet, use_container_width=True, height=200)

    # 🖨️ مركز الطباعة
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='print-section-box'>", unsafe_allow_html=True)
        st.subheader("🖨️ مركز فرز وطباعة تقارير المناطق")
        
        if not df.empty:
            available_regions = sorted(df["المنطقة"].unique())
            selected_print_region = st.selectbox("اختر المنطقة المراد طباعة كشف عقاراتها الاستقصائي:", available_regions, key="print_region_select_unique")
            
            if selected_print_region:
                print_filtered_df = df[df["المنطقة"] == selected_print_region].sort_values(by="رقم العقار").reset_index(drop=True)
                csv_print_bytes = print_filtered_df.to_csv(index=False).encode('utf-8-sig')
                
                st.write(f"📊 يحتوي الكشف الحالي لـ **{selected_print_region}** على **{len(print_filtered_df)}** عقار مسجل.")
                st.markdown("<div class='print-zone-btn'>", unsafe_allow_html=True)
                st.download_button(
                    label=f"🖨️ تصدير وتحميل كشف ({selected_print_region}) للطباعة الفورية",
                    data=csv_print_bytes,
                    file_name=f"كشف_عقارات_{selected_print_region}.csv",
                    mime="text/csv",
                    key="final_print_trigger_btn_unique",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ لا توجد مناطق مسجلة بعد في السجل لتصدير تقاريرها.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 🔍 البحث والتعديل والحذف المنفصل
    search_query = st.text_input(
        label="🔍 اكتب اسم المنطقة أو رقم العقار للبحث السريع والتعديل أو الحذف...",
        value=st.session_state.search_val,
        key="search_input_field_unique"
    ).strip()
    st.session_state.search_val = search_query

    if search_query and not st.session_state.local_db.empty:
        matched_records = st.session_state.local_db[
            st.session_state.local_db["المنطقة"].astype(str).str.contains(search_query, case=False, na=False) | 
            st.session_state.local_db["رقم العقار"].astype(str).str.contains(search_query, case=False, na=False)
        ]
        
        if not matched_records.empty:
            st.write(f"📋 تم العثور على {len(matched_records)} نتيجة:")
            for idx, row in matched_records.iterrows():
                col_info, col_edit, col_del = st.columns([3, 1, 1])
                with col_info:
                    st.info(f"📍 المنطقة: {row['المنطقة']} | 🔢 العقار: {row['رقم العقار']}")
                with col_edit:
                    if st.button("✏️ تعديل", key=f"edit_btn_{idx}"):
                        st.session_state.selected_property = row.to_dict()
                        st.session_state.selected_index = idx
                        st.session_state.edit_mode = True
                        st.rerun()
                with col_del:
                    if st.button("🗑️ حذف", key=f"del_btn_{idx}"):
                        st.session_state.selected_property = row.to_dict()
                        st.session_state.selected_index = idx
                        st.session_state.edit_mode = False
                        st.rerun()
        else:
            st.warning("⚠️ لم يتم العثور على نتائج تطابق البحث.")

    # ⚙️ لوحة تنفيذ التعديل أو الحذف
    if st.session_state.selected_property is not None:
        st.markdown("---")
        prop = st.session_state.selected_property
        idx = st.session_state.selected_index
        
        if st.session_state.edit_mode:
            st.subheader("✏️ تعديل بيانات العقار المحدد")
            new_region = st.text_input("اسم المنطقة الجغرافية", value=prop.get('المنطقة', ''), key="mod_region_inp")
            new_number = st.text_input("رقم العقار الجديد", value=prop.get('رقم العقار', ''), key="mod_prop_inp")
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 حفظ التعديلات", use_container_width=True, key="save_mod_btn"):
                    st.session_state.local_db.at[idx, 'المنطقة'] = new_region
                    st.session_state.local_db.at[idx, 'رقم العقار'] = new_number
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.success("✅ تم تعديل بيانات العقار بنجاح!")
                    st.session_state.selected_property = None
                    st.session_state.edit_mode = False
                    st.rerun()
                    
            with col_cancel:
                if st.button("❌ إلغاء", use_container_width=True, key="cancel_mod_btn"):
                    st.session_state.selected_property = None
                    st.session_state.edit_mode = False
                    st.rerun()

        else:
            st.subheader("🗑️ تأكيد حذف العقار")
            st.error(f"هل أنت تأكد من حذف العقار رقم [{prop.get('رقم العقار')}] في منطقة [{prop.get('المنطقة')}]؟")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("🔥 نعم، قم بالحذف", use_container_width=True, key="confirm_del_btn"):
                    st.session_state.local_db.drop(index=idx, inplace=True)
                    st.session_state.local_db.reset_index(drop=True, inplace=True)
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.success("🗑️ تم حذف العقار بنجاح!")
                    st.session_state.selected_property = None
                    st.rerun()
                    
            with col_cancel:
                if st.button("❌ إلغاء", use_container_width=True, key="cancel_del_btn"):
                    st.session_state.selected_property = None
                    st.rerun()

    # JavaScript للتركيز والتنقل السريع
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
        "window.propMidanHandler = function(e) { if (e.key === 'Enter') { if (propInput.value.trim() !== '') { e.preventDefault(); saveBtn.click(); setTimeout(function() { regInput.focus(); regInput.select(); }, 50); } } };",
        "propInput.addEventListener('keydown', window.propMidanHandler);",
        "}",
        "}; setTimeout(attachMidanEvents, 50); setInterval(attachMidanEvents, 200);",
        "</script>"
    ]
    st.components.v1.html("".join(js_code), height=0)
