import streamlit as st
import pandas as pd
import requests
import base64
import glob
import io

# 🌐 1. إعدادات الصفحة
st.set_page_config(
    page_title="Khatib & Alami Company", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔑 إعدادات GitHub
GITHUB_TOKEN = "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع_YOUR_USERNAME/YOUR_REPO"
OUTPUT_FILENAME = "KhatibAlami_Midan_Data.csv"

# دالة الرفع على GitHub
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
        data = {"message": "تحديث تلقائي - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except:
        return False

# دالة تحميل البيانات تلقائياً
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

# 🎨 التنسيقات
ultimate_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=400;700;900&display=swap');
html, body, [class*='css'], [data-testid='stAppViewContainer'] { 
    font-family: 'Tajawal', sans-serif !important; 
    direction: rtl !important; 
    text-align: right !important; 
}
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; }
header[data-testid='stHeader'] { background: transparent !important; display: none !important; }
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

/* كروت الترويسة الرئيسية */
.header-card { 
    background-color: #EBF8FF !important; padding: 22px 15px !important; border-radius: 14px !important; 
    box-shadow: 0 6px 14px rgba(30, 58, 138, 0.1) !important; margin-bottom: 4px !important; text-align: center !important; border: 2px solid #BEE3F8 !important; 
}
.company-header { color: #1E3A8A !important; font-family: 'Arial', sans-serif !important; font-size: 34px !important; font-weight: 900 !important; letter-spacing: 0.5px; }
.company-subtitle { color: #2D3748 !important; font-size: 18px !important; font-weight: 700 !important; margin-top: 4px !important; }

/* بطاقة التوقيع */
.main-signature-card { 
    background-color: #ffffff !important; padding: 12px 18px !important; border-radius: 12px !important; text-align: center !important; 
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important; margin: 8px auto 12px auto !important; border: 1.5px solid #cbd5e0 !important; max-width: 600px !important; 
}
.sig-title { color: #4A5568 !important; font-size: 16px !important; font-weight: 700 !important; }
.sig-name { color: #E53E3E !important; font-size: 22px !important; font-weight: 900 !important; margin-top: 2px; }

/* عناوين الحقول والمدخلات */
label[data-testid="stWidgetLabel"] p {
    font-size: 19px !important;
    font-weight: 900 !important;
    color: #1E3A8A !important;
}

div[data-testid="column"] {
    padding-left: 3px !important;
    padding-right: 3px !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.2rem !important;
}

/* إخفاء زر Submit */
div[data-testid="stFormSubmitButton"] button {
    opacity: 0 !important;
    height: 1px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}

div[data-testid="stForm"] {
    border: none !important;
    padding: 0px !important;
    background: transparent !important;
}

/* مربعات النصوص */
div[data-testid="stTextInput"] input {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #1E3A8A !important;
    height: 50px !important;
}

/* الأزرار */
div.stButton > button, div.stDownloadButton > button {
    background-color: #EF4444 !important;
    color: #FFFFFF !important;
    border: 1px solid #DC2626 !important;
    font-weight: 900 !important;
    font-size: 17px !important;
    border-radius: 8px !important;
    height: 50px !important;
    width: 100% !important;
    margin-bottom: 2px !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover { 
    background-color: #DC2626 !important; 
}

/* العداد الأزرق الكبير */
.blue-total-metric {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    padding: 10px !important;
    border-radius: 12px !important;
    text-align: center !important;
    height: 110px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25) !important;
}
.blue-total-title { font-size: 15px !important; font-weight: 900 !important; color: #ffffff !important; letter-spacing: 0.5px; }
.blue-total-value { font-size: 38px !important; font-weight: 900 !important; color: #ffffff !important; }

/* العداد الأحمر للمنطقة */
.red-region-metric {
    background-color: #EF4444 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    height: 110px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 18px !important;
    font-weight: 900 !important;
    text-align: center !important;
    box-shadow: 0 4px 10px rgba(239, 68, 68, 0.2) !important;
}

/* صندوق الطباعة */
.print-section-box {
    background-color: #ffffff !important;
    padding: 18px !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e0 !important;
    margin-top: 12px !important;
}
.print-section-box h3 {
    font-size: 24px !important;
    font-weight: 900 !important;
    color: #1E3A8A !important;
}

/* بطاقات البحث */
.result-card {
    background-color: #DCE7F6 !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    color: #1E3A8A !important;
    font-weight: 900 !important;
    font-size: 17px !important;
    text-align: right !important;
    border: 1px solid #BEE3F8 !important;
    height: 48px !important;
    display: flex !important;
    align-items: center !important;
}

iframe[title="st.iframe"] { display: none !important; }
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# 🛡️ إدارة حالة الجلسة
if "local_db" not in st.session_state or st.session_state.local_db is None: 
    st.session_state.local_db = load_any_local_file()

if not isinstance(st.session_state.local_db, pd.DataFrame) or "المنطقة" not in st.session_state.local_db.columns or "رقم العقار" not in st.session_state.local_db.columns:
    st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

if "region_input_val" not in st.session_state: st.session_state.region_input_val = ""
if "prop_input_val" not in st.session_state: st.session_state.prop_input_val = ""
if "focus_field" not in st.session_state: st.session_state.focus_field = "region"
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "notification_msg" not in st.session_state: st.session_state.notification_msg = None
if "notification_type" not in st.session_state: st.session_state.notification_type = None

if 'selected_property' not in st.session_state: st.session_state.selected_property = None
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'selected_index' not in st.session_state: st.session_state.selected_index = None
if 'should_scroll' not in st.session_state: st.session_state.should_scroll = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)

    df = st.session_state.local_db

    # 📂 رفع ملف قديم
    if df.empty:
        with st.expander("📁 رفع ملف Excel أو CSV قديم للبدء منه (يظهر لأول مرة فقط)", expanded=True):
            uploaded_file = st.file_uploader("قم بسحب وإفلات ملف البيانات هنا أو اختر الملف من جهازك:", type=["csv", "xlsx", "xls"])
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_up = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                    else:
                        df_up = pd.read_excel(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                    
                    if "المنطقة" in df_up.columns and "رقم العقار" in df_up.columns:
                        st.session_state.local_db = df_up[["المنطقة", "رقم العقار"]].dropna()
                        st.session_state.local_db.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                        upload_to_github(st.session_state.local_db)
                        st.success("✅ تم تحميل الملف بنجاح ودمجه في النظام!")
                        st.rerun()
                    else:
                        st.error("❌ الملف لا يحتوي على الأعمدة المطلوبة: ('المنطقة' و 'رقم العقار')")
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء قراءة الملف: {e}")

    # 📝 نموذج الإدخال
    with st.form("entry_form"):
        input_col1, input_col2 = st.columns([1, 1], gap="small")
        with input_col1:
            region_val = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.region_input_val, placeholder="النبطية، صور، صيدا...", key="form_region").strip()
        with input_col2:
            prop_val = st.text_input("🔢 رقم العقار الجديد", value=st.session_state.prop_input_val, placeholder="ادخل رقم العقار الحالي....", key="form_prop").strip()

        submitted = st.form_submit_button("Submit")

    # 📥 الأزرار متجاورة
    btn_row_col1, btn_row_col2 = st.columns([1, 1], gap="small")
    with btn_row_col1:
        btn_save_manual = st.button("🚀 حفظ العقار والتحقق من التكرار", key="manual_save_btn", use_container_width=True)

    with btn_row_col2:
        if not df.empty:
            sorted_df = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
            csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تنزيل شيت البيانات الحالي (Excel/CSV)",
                data=csv_data,
                file_name="KhatibAlami_Midan_Data.csv",
                mime="text/csv",
                key="download_btn_csv_direct",
                use_container_width=True
            )
        else:
            st.button("📥 تنزيل شيت البيانات الحالي (فارغ)", disabled=True, use_container_width=True)

    # معالجة الضغط على Enter أو زر الحفظ
    if submitted or btn_save_manual:
        st.session_state.notification_msg = None
        st.session_state.notification_type = None

        # 🔹 الحالة 1: الضغط على Enter بعد إدخال اسم المنطقة فقط
        if region_val and not prop_val:
            st.session_state.region_input_val = region_val
            st.session_state.prop_input_val = ""
            st.session_state.focus_field = "property"
            st.rerun()

        # 🔹 الحالة 2: الضغط على Enter بعد إدخال رقم العقار
        elif region_val and prop_val:
            is_duplicate = False
            if not df.empty:
                is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_val.lower()) & (df["رقم العقار"].str.strip() == prop_val)].shape[0] > 0
            
            if is_duplicate:
                st.session_state.notification_msg = f"⚠️ العقار رقم [{prop_val}] مكرر ومسجل سابقاً في منطقة [{region_val}]!"
                st.session_state.notification_type = "error"
                # 🎯 عند التكرار: تفريغ رقم العقار والتوجه فوراً لخانة العقار لإعادة الكتابة
                st.session_state.region_input_val = region_val
                st.session_state.prop_input_val = ""
                st.session_state.focus_field = "property"
            else:
                new_row = pd.DataFrame([{"المنطقة": region_val, "رقم العقار": prop_val}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                upload_to_github(st.session_state.local_db)
                
                st.session_state.notification_msg = f"✅ تم حفظ العقار [{prop_val}] بنجاح في منطقة [{region_val}]!"
                st.session_state.notification_type = "success"
                # 🎯 عند النجاح: الاحتفاظ باسم المنطقة وتفريغ العقار والتوجه لاسم المنطقة
                st.session_state.region_input_val = region_val
                st.session_state.prop_input_val = ""
                st.session_state.focus_field = "region"

            st.rerun()

    # عرض الرسالة عند التكرار أو الحفظ
    if st.session_state.notification_msg:
        if st.session_state.notification_type == "error":
            st.error(st.session_state.notification_msg)
        elif st.session_state.notification_type == "success":
            st.success(st.session_state.notification_msg)

    # 🎯 سكربت التوجيه والتركيز (JavaScript)
    if st.session_state.focus_field == "property":
        js_focus = """
        <script>
            setTimeout(function() {
                var inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 2) {
                    inputs[1].focus();
                    inputs[1].select();
                }
            }, 50);
        </script>
        """
        st.components.v1.html(js_focus, height=0)
    elif st.session_state.focus_field == "region":
        js_focus = """
        <script>
            setTimeout(function() {
                var inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 1) {
                    inputs[0].focus();
                    inputs[0].select();
                }
            }, 50);
        </script>
        """
        st.components.v1.html(js_focus, height=0)

    # 📊 العدادات المباشرة
    stat_col1, stat_col2 = st.columns([1, 1], gap="small")
    
    current_reg = st.session_state.region_input_val
    region_count = 0
    if current_reg and not df.empty:
        region_count = df[df["المنطقة"].str.strip().str.lower() == current_reg.lower()].shape[0]

    # 🔵 العداد الأزرق الإجمالي
    with stat_col1:
        total_count = len(df) if not df.empty else 0
        st.markdown(
            f"""
            <div class='blue-total-metric'>
                <div class='blue-total-title'>TOTAL PROPERTY COUNT IN FILE 📱</div>
                <div class='blue-total-value'>{total_count}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # 🔴 العداد الأحمر للمنطقة
    with stat_col2:
        st.markdown(
            f"<div class='red-region-metric'>🔸 عدد عقارات منطقة ({current_reg if current_reg else '...'}) <br> [{region_count}]</div>", 
            unsafe_allow_html=True
        )

    # 🖨️ مركز فرز وطباعة تقارير المناطق
    st.markdown("<div class='print-section-box'>", unsafe_allow_html=True)
    st.subheader("🖨️ مركز فرز وطباعة تقارير المناطق")
    
    if not df.empty:
        available_regions = sorted(df["المنطقة"].unique())
        selected_print_region = st.selectbox("اختر المنطقة المراد طباعة كشف عقاراتها الاستقصائي:", available_regions, key="print_region_select")
        
        if selected_print_region:
            print_filtered_df = df[df["المنطقة"] == selected_print_region].sort_values(by="رقم العقار").reset_index(drop=True)
            csv_print_bytes = print_filtered_df.to_csv(index=False).encode('utf-8-sig')
            
            st.write(f"📊 يحتوي الكشف الحالي لـ **{selected_print_region}** على **{len(print_filtered_df)}** عقار مسجل.")
            st.download_button(
                label=f"🖨️ تصدير وتحميل كشف ({selected_print_region}) للطباعة الفورية",
                data=csv_print_bytes,
                file_name=f"كشف_عقارات_{selected_print_region}.csv",
                mime="text/csv",
                key="final_print_trigger_btn",
                use_container_width=True
            )
    else:
        st.info("ℹ️ لا توجد مناطق مسجلة بعد في السجل لتصدير تقاريرها.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 🔍 محرك البحث السريع والتعديل والحذف
    search_query = st.text_input(
        label="🔍 اكتب اسم المنطقة أو رقم العقار للبحث السريع والتعديل أو الحذف...",
        value=st.session_state.search_val,
        key="search_input_field"
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
                c_info, c_edit, c_del = st.columns([3.5, 1, 1], gap="small")
                with c_info:
                    st.markdown(f"<div class='result-card'>📍 المنطقة: {row['المنطقة']} | 🔢 العقار: {row['رقم العقار']}</div>", unsafe_allow_html=True)
                with c_edit:
                    if st.button("✏️ تعديل", key=f"edit_btn_{idx}", use_container_width=True):
                        st.session_state.selected_property = row.to_dict()
                        st.session_state.selected_index = idx
                        st.session_state.edit_mode = True
                        st.session_state.should_scroll = True
                        st.rerun()
                with c_del:
                    if st.button("🗑️ حذف", key=f"del_btn_{idx}", use_container_width=True):
                        st.session_state.selected_property = row.to_dict()
                        st.session_state.selected_index = idx
                        st.session_state.edit_mode = False
                        st.session_state.should_scroll = True
                        st.rerun()

    # ⚙️ لوحة التعديل أو الحذف المباشرة
    if st.session_state.selected_property is not None:
        st.markdown("<div id='scroll_target'></div>", unsafe_allow_html=True)
        prop = st.session_state.selected_property
        idx = st.session_state.selected_index
        
        st.markdown("---")
        if st.session_state.edit_mode:
            st.subheader("✏️ تعديل بيانات العقار")
            mod_region = st.text_input("اسم المنطقة الجغرافية", value=prop.get('المنطقة', ''), key="mod_reg_val")
            mod_number = st.text_input("رقم العقار الجديد", value=prop.get('رقم العقار', ''), key="mod_num_val")
            
            col_save, col_cancel = st.columns([1, 1], gap="small")
            with col_save:
                if st.button("💾 حفظ التعديلات الآن", use_container_width=True, key="save_edit_now"):
                    st.session_state.local_db.at[idx, 'المنطقة'] = mod_region
                    st.session_state.local_db.at[idx, 'رقم العقار'] = mod_number
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.session_state.selected_property = None
                    st.session_state.edit_mode = False
                    st.rerun()
                    
            with col_cancel:
                if st.button("❌ إلغاء", use_container_width=True, key="cancel_edit_now"):
                    st.session_state.selected_property = None
                    st.session_state.edit_mode = False
                    st.rerun()

        else:
            st.subheader("🗑️ تأكيد الحذف")
            st.error(f"هل أنت تأكد من حذف العقار رقم [{prop.get('رقم العقار')}] من منطقة [{prop.get('المنطقة')}]؟")
            
            col_confirm, col_cancel = st.columns([1, 1], gap="small")
            with col_confirm:
                if st.button("🔥 نعم، قم بالحذف النهائي", use_container_width=True, key="confirm_del_now"):
                    st.session_state.local_db.drop(index=idx, inplace=True)
                    st.session_state.local_db.reset_index(drop=True, inplace=True)
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.session_state.selected_property = None
                    st.rerun()
                    
            with col_cancel:
                if st.button("❌ إلغاء", use_container_width=True, key="cancel_del_now"):
                    st.session_state.selected_property = None
                    st.rerun()

    # 📜 التمرير السلس
    if st.session_state.should_scroll:
        st.session_state.should_scroll = False
        js_code = """
        <script>
            setTimeout(function() {
                var element = window.parent.document.getElementById('scroll_target');
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 200);
        </script>
        """
        st.components.v1.html(js_code, height=0)
