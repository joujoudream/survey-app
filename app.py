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

# 🎨 التنسيقات المطابقة للتصميم الأصلي
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

/* كروت الترويسة */
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

/* صندوق رفع الملفات */
.upload-box-style {
    background-color: #ffffff !important;
    padding: 15px !important;
    border-radius: 10px !important;
    border: 2px dashed #3182ce !important;
    margin-bottom: 15px !important;
}

/* تنسيق مربعات النصوص */
div[data-testid="stTextInput"] input {
    font-size: 18px !important;
    font-weight: bold !important;
    color: #1E3A8A !important;
    height: 48px !important;
}

/* الأزرار */
div.stButton > button, div.stDownloadButton > button {
    background-color: #EF4444 !important;
    color: #FFFFFF !important;
    border: 1px solid #DC2626 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-radius: 8px !important;
    height: 48px !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover { background-color: #DC2626 !important; }

/* العداد الأزرق الكبيرة (على اليسار) */
.blue-total-metric {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    padding: 15px !important;
    border-radius: 12px !important;
    text-align: center !important;
    height: 110px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25) !important;
}
.blue-total-title { font-size: 13px !important; font-weight: bold !important; color: #ffffff !important; letter-spacing: 1px; }
.blue-total-value { font-size: 34px !important; font-weight: 900 !important; color: #ffffff !important; }

/* العداد الأحمر الخاص بالمنطقة الحالية (على اليمين) */
.red-region-metric {
    background-color: #EF4444 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    height: 110px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 16px !important;
    font-weight: bold !important;
    text-align: center !important;
    box-shadow: 0 4px 10px rgba(239, 68, 68, 0.2) !important;
}

/* صندوق طباعة تقارير المناطق */
.print-section-box {
    background-color: #ffffff !important;
    padding: 18px !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e0 !important;
    margin-top: 15px !important;
}

/* بطاقات البحث */
.result-card {
    background-color: #DCE7F6 !important;
    padding: 10px 15px !important;
    border-radius: 8px !important;
    color: #1E3A8A !important;
    font-weight: bold !important;
    font-size: 16px !important;
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

if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""

if 'selected_property' not in st.session_state: st.session_state.selected_property = None
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'selected_index' not in st.session_state: st.session_state.selected_index = None
if 'should_scroll' not in st.session_state: st.session_state.should_scroll = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)

    # 📂 1. قسم تحميل ملف إكسل / CSV لأول مرة عند فتح التطبيق
    with st.expander("📁 رفع ملف Excel أو CSV قديم للبدء منه (اختياري)", expanded=False):
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

    df = st.session_state.local_db
    
    # 📋 حقول الإدخال الأساسية
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="النبطية، صور، صيدا...", key="region_field_main").strip()
    with input_col2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field_main").strip()
    
    st.session_state.clear_trigger = False

    # 🚀 أزرار الحفظ والتنزيل اليدوي تحت الحقول مباشرة
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", key="save_btn_main", use_container_width=True)
    with action_col2:
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

    # 📊 العدادات الهامة (العداد الأحمر على اليمين والعداد الأزرق على اليسار)
    st.markdown("<br>", unsafe_allow_html=True)
    stat_col1, stat_col2 = st.columns(2)
    
    region_count = 0
    if region_input and not df.empty:
        region_count = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()].shape[0]

    # 🔴 العداد الأحمر على اليمين
    with stat_col1:
        st.markdown(
            f"<div class='red-region-metric'>🔸 عدد عقارات منطقة ({region_input if region_input else '...'}) <br> [{region_count}]</div>", 
            unsafe_allow_html=True
        )

    # 🔵 العداد الأزرق الإجمالي على اليسار
    with stat_col2:
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

    # تنفيذ عملية الحفظ
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
                c_info, c_edit, c_del = st.columns([3.5, 1, 1])
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
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 حفظ التعديلات الآن", use_container_width=True, key="save_edit_now"):
                    st.session_state.local_db.at[idx, 'المنطقة'] = mod_region
                    st.session_state.local_db.at[idx, 'رقم العقار'] = mod_number
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.success("✅ تم تعديل البيانات بنجاح!")
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
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("🔥 نعم، قم بالحذف النهائي", use_container_width=True, key="confirm_del_now"):
                    st.session_state.local_db.drop(index=idx, inplace=True)
                    st.session_state.local_db.reset_index(drop=True, inplace=True)
                    
                    sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                    sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                    upload_to_github(st.session_state.local_db)
                    
                    st.success("🗑️ تم حذف العقار بنجاح!")
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
