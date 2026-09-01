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

# دالة تحميل البيانات
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
                csv_bytes = base64.b64encode(file_data["content"])
                df_git = pd.read_csv(io.BytesIO(csv_bytes), encoding='utf-8-sig', dtype={"المنطقة": str, "رقم العقار": str})
                if "المنطقة" in df_git.columns and "رقم العقار" in df_git.columns:
                    return df_git[["المنطقة", "رقم العقار"]]
        except: pass
    return pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🎨 CSS المحسّن لعزل الأزرار وتصليح الألوان والأنماط
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

/* الترويسة */
.header-card { 
    background-color: #EBF8FF !important; padding: 22px 15px !important; border-radius: 14px !important; 
    box-shadow: 0 6px 14px rgba(30, 58, 138, 0.1) !important; margin-bottom: 4px !important; text-align: center !important; border: 2px solid #BEE3F8 !important; 
}
.company-header { color: #1E3A8A !important; font-family: 'Arial', sans-serif !important; font-size: 34px !important; font-weight: 900 !important; }
.company-subtitle { color: #2D3748 !important; font-size: 18px !important; font-weight: 700 !important; margin-top: 4px !important; }

.main-signature-card { 
    background-color: #ffffff !important; padding: 12px 18px !important; border-radius: 12px !important; text-align: center !important; 
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important; margin: 8px auto 12px auto !important; border: 1.5px solid #cbd5e0 !important; max-width: 600px !important; 
}
.sig-title { color: #4A5568 !important; font-size: 16px !important; font-weight: 700 !important; }
.sig-name { color: #E53E3E !important; font-size: 22px !important; font-weight: 900 !important; margin-top: 2px; }

/* مدخلات النصوص */
label[data-testid="stWidgetLabel"] p { font-size: 19px !important; font-weight: 900 !important; color: #1E3A8A !important; }
div[data-testid="column"] { padding-left: 3px !important; padding-right: 3px !important; }
div[data-testid="stVerticalBlock"] { gap: 0.2rem !important; }

div[data-testid="stFormSubmitButton"] button { opacity: 0 !important; height: 1px !important; padding: 0 !important; margin: 0 !important; border: none !important; }
div[data-testid="stForm"] { border: none !important; padding: 0px !important; background: transparent !important; }
div[data-testid="stTextInput"] input { font-size: 20px !important; font-weight: 700 !important; color: #1E3A8A !important; height: 50px !important; }

/* 🟥 زر حفظ العقار الرئيسي (أحمر) */
div[data-testid="stButton"] > button:has(p:contains("حفظ العقار والتحقق من التكرار")),
div[data-testid="stButton"] > button:has(div:contains("حفظ العقار والتحقق من التكرار")) {
    background-color: #EF4444 !important;
    color: #FFFFFF !important;
    border: 1px solid #DC2626 !important;
    font-weight: 900 !important;
    font-size: 17px !important;
    border-radius: 8px !important;
    height: 50px !important;
}

/* 📥 زر تنزيل شيت البيانات (رمادي موحد أو أحمر خفيف) */
div[data-testid="stDownloadButton"] > button {
    background-color: #E2E8F0 !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    border-radius: 8px !important;
    height: 50px !important;
}

/* 🔵 الزر الأزرق الكبير لإجمالي العقارات */
div[data-testid="stButton"] > button:has(p:contains("TOTAL PROPERTY COUNT")),
div[data-testid="stButton"] > button:has(div:contains("TOTAL PROPERTY COUNT")) {
    background: #2563EB !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    height: 110px !important;
    border: 1px solid #1D4ED8 !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
    font-size: 20px !important;
    font-weight: 900 !important;
}

/* 🔴 العداد الأحمر الخاص بالمنطقة */
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

/* 🖨️ زر تصدير التقرير للطباعة */
div[data-testid="stDownloadButton"] > button:has(p:contains("تصدير وتحميل كشف")),
div[data-testid="stDownloadButton"] > button:has(div:contains("تصدير وتحميل كشف")) {
    background-color: #059669 !important;
    color: #ffffff !important;
    border: 1px solid #047857 !important;
    font-weight: 900 !important;
    font-size: 17px !important;
    height: 50px !important;
}

/* صندوق الطباعة */
.print-section-box {
    background-color: #ffffff !important;
    padding: 18px !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e0 !important;
    margin-top: 12px !important;
}

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
if "prop_key_counter" not in st.session_state: st.session_state.prop_key_counter = 0
if "focus_field" not in st.session_state: st.session_state.focus_field = "region"
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "notification_msg" not in st.session_state: st.session_state.notification_msg = None
if "notification_type" not in st.session_state: st.session_state.notification_type = None

if 'selected_property' not in st.session_state: st.session_state.selected_property = None
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'selected_index' not in st.session_state: st.session_state.selected_index = None
if 'should_scroll' not in st.session_state: st.session_state.should_scroll = False
if "show_full_table" not in st.session_state: st.session_state.show_full_table = False

# 🏛️ الترويسة
col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)

    df = st.session_state.local_db

    # 📝 نموذج الإدخال
    with st.form("entry_form"):
        input_col1, input_col2 = st.columns([1, 1], gap="small")
        with input_col1:
            region_val = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.region_input_val, placeholder="النبطية، صور، صيدا...", key="form_region").strip()
        with input_col2:
            prop_val = st.text_input("🔢 رقم العقار الجديد", value="", placeholder="ادخل رقم العقار الحالي....", key=f"form_prop_{st.session_state.prop_key_counter}").strip()

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

        if region_val and not prop_val:
            st.session_state.region_input_val = region_val
            st.session_state.focus_field = "property"
            st.rerun()

        elif region_val and prop_val:
            is_duplicate = False
            if not df.empty:
                is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_val.lower()) & (df["رقم العقار"].str.strip() == prop_val)].shape[0] > 0
            
            if is_duplicate:
                st.session_state.notification_msg = f"⚠️ العقار رقم [{prop_val}] مكرر ومسجل سابقاً في منطقة [{region_val}]!"
                st.session_state.notification_type = "error"
                st.session_state.prop_key_counter += 1
                st.session_state.region_input_val = region_val
                st.session_state.focus_field = "region"
            else:
                new_row = pd.DataFrame([{"المنطقة": region_val, "رقم العقار": prop_val}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                upload_to_github(st.session_state.local_db)
                
                st.session_state.notification_msg = None
                st.session_state.notification_type = None
                st.session_state.prop_key_counter += 1
                st.session_state.region_input_val = region_val
                st.session_state.focus_field = "region"

            st.rerun()

    if st.session_state.notification_msg and st.session_state.notification_type == "error":
        st.error(st.session_state.notification_msg)

    # 🎯 التركيز التلقائي
    if st.session_state.focus_field == "property":
        js_focus = """
        <script>
            setTimeout(function() {
                var inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 2) { inputs[1].focus(); }
            }, 50);
        </script>
        """
        st.components.v1.html(js_focus, height=0)
    elif st.session_state.focus_field == "region":
        js_focus = """
        <script>
            setTimeout(function() {
                var inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 1) { inputs[0].focus(); inputs[0].select(); }
            }, 50);
        </script>
        """
        st.components.v1.html(js_focus, height=0)

    # 📊 العدادات
    stat_col1, stat_col2 = st.columns([1, 1], gap="small")
    
    current_reg = st.session_state.region_input_val
    region_count = 0
    if current_reg and not df.empty:
        region_count = df[df["المنطقة"].str.strip().str.lower() == current_reg.lower()].shape[0]

    with stat_col1:
        total_count = len(df) if not df.empty else 0
        if st.button(f"📱 TOTAL PROPERTY COUNT IN FILE\n{total_count}", key="blue_total_btn", use_container_width=True):
            st.session_state.show_full_table = not st.session_state.show_full_table
            st.rerun()

    with stat_col2:
        st.markdown(
            f"<div class='red-region-metric'>🔸 عدد عقارات منطقة ({current_reg if current_reg else '...'}) <br> [{region_count}]</div>", 
            unsafe_allow_html=True
        )

    if st.session_state.show_full_table:
        st.markdown("---")
        st.subheader("📋 كشف البيانات الكاملة المسجلة بالنظام")
        if not df.empty:
            sorted_table = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
            st.dataframe(sorted_table, use_container_width=True, height=350)

    # 🖨️ مركز الطباعة
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
    st.markdown("</div>", unsafe_allow_html=True)
