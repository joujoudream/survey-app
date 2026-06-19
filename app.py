import streamlit as st
import pandas as pd
import requests
import base64
import os
from PIL import Image

# 🌐 1. إعدادات الصفحة الرسمية للشركة
st.set_page_config(
    page_title="Khatib & Alami Company", 
    page_icon="K_and_A_icon.ico" if os.path.exists("K_and_A_icon.ico") else "🏢", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔑 إعدادات الربط التلقائي بمنصة GitHub
GITHUB_TOKEN = "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع_YOUR_USERNAME/YOUR_REPO"
GITHUB_FILENAME = "KhatibAlami_Midan_Data.csv"

def upload_to_github(dataframe):
    try:
        csv_content = dataframe.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True).to_csv(index=False).encode('utf-8-sig')
        encoded_content = base64.b64encode(csv_content).decode('utf-8')
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILENAME}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        data = {"message": "تحديث تلقائي لسجل العقارات الميداني - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except Exception as e:
        return False

# 🎨 الستايل الهندسي الصارم لحل أخطاء الحجم والتناظر البصري للأزرار والمربعات الإحصائية
ultimate_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=300;500;700&display=swap');
html, body, [class*='css'], [data-testid="stAppViewContainer"] { 
    font-family: 'Tajawal', sans-serif !important; 
    direction: rtl !important; 
    text-align: right !important; 
}
.stApp { 
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; 
}
header[data-testid='stHeader'] { 
    background: transparent !important; 
    display: none !important; 
}
.block-container { 
    padding-top: 1.5rem !important; 
    padding-bottom: 1rem !important; 
}

/* هيدر وبطاقة تعريف الشركة */
.header-card { 
    background-color: #EBF8FF !important; 
    padding: 20px 12px !important; 
    border-radius: 12px !important; 
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.08) !important; 
    margin-bottom: 2px !important; 
    text-align: center !important; 
    border: 1px solid #BEE3F8 !important; 
}
.company-header { 
    color: #1E3A8A !important; 
    font-family: 'Arial', sans-serif !important; 
    font-size: 28px !important; 
    font-weight: bold !important; 
}
.company-subtitle { 
    color: #2D3748 !important; 
    font-size: 15px !important; 
    font-weight: 500 !important; 
    margin-top: 4px !important; 
}
.main-signature-card { 
    background-color: #ffffff !important; 
    padding: 14px 16px !important; 
    border-radius: 10px !important; 
    text-align: center !important; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04) !important; 
    margin: 10px auto 20px auto !important; 
    border: 1px solid #e2e8f0 !important; 
    max-width: 550px !important; 
}

/* 🛑 حل الخطأ الأول: إجبار الأزرار الحمراء التشغيلية على أخذ كامل العرض وبحجم كبير ومتناسق تماماً */
div[data-testid="stColumn"] button[data-testid="baseButton-secondary"],
div[data-testid="stColumn"] button[data-testid="baseButton-primary"],
div[data-testid="stColumn"] button {
    background: #EF4444 !important;
    color: white !important;
    border: 1px solid #DC2626 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    height: 52px !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 6px rgba(239, 68, 68, 0.25) !important;
    width: 100% !important;
    display: block !important;
}
div[data-testid="stColumn"] button:hover {
    background: #DC2626 !important;
    box-shadow: 0 6px 12px rgba(220, 38, 38, 0.4) !important;
}

/* 🔵 حل الخطأ الثاني: تثبيت وتوحيد حجم المربع الإحصائي الأزرق الكبير بالكامل */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    text-align: center !important;
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.2) !important;
    border: none !important;
    height: 105px !important; /* توحيد الارتفاع البرمجي صراحة */
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: white !important;
}

/* 🔵 حل الخطأ الثاني: جعل زر إحصاء المنطقة التفاعلي متطابق تماماً في الحجم واللون التدرجي مع المربع الأزرق الكلي */
div.midan-metric-btn button {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    height: 105px !important; /* تطابق تام في الارتفاع بالبكسل */
    width: 100% !important;
    box-shadow: 0 6px 12px rgba(30, 58, 138, 0.2) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: pre-line !important;
}
div.midan-metric-btn button:hover {
    background: linear-gradient(135deg, #172554 0%, #1D4ED8 100%) !important;
    box-shadow: 0 8px 16px rgba(29, 78, 216, 0.35) !important;
}

div[data-testid='stHorizontalBlock'] { gap: 16px !important; }
[data-testid='stInputInstructions'] { display: none !important; visibility: hidden !important; }
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# إدارة الذاكرة المحلية للجلسة
if "local_db" not in st.session_state: st.session_state.local_db = pd.DataFrame(columns=["المنطقة", "رقم العقار"])
if "file_uploaded" not in st.session_state: st.session_state.file_uploaded = False
if "last_region" not in st.session_state: st.session_state.last_region = ""
if "clear_trigger" not in st.session_state: st.session_state.clear_trigger = False
if "search_val" not in st.session_state: st.session_state.search_val = ""
if "focus_on_region" not in st.session_state: st.session_state.focus_on_region = False

col1, col2, col3 = st.columns([0.5, 11, 0.5])
with col2:
    # هيدر الشركة الرئيسي
    st.markdown("<div class='header-card'><div class='company-header'>Khatib & Alami Company</div><div class='company-subtitle'>War Damage Assessment 2006</div></div>", unsafe_allow_html=True)
    
    # بطاقة التوقيع
    st.markdown("<div class='main-signature-card'><div class='sig-title'>Printing & Archiving</div><div class='sig-name'>S,Walid Mrad</div></div>", unsafe_allow_html=True)

    # نافذة الرفع الاحتياطي للملف القديم
    with st.expander("📥 خطوة 1: رفع ملف البيانات الاحتياطي (إذا وجد)", expanded=not st.session_state.file_uploaded):
        uploaded_file = st.file_uploader("اختر ملف الإكسيل (CSV) المستخرج سابقاً لمتابعة العمل على البيانات:", type=["csv"])
        if uploaded_file is not None and not st.session_state.file_uploaded:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype={"المنطقة": str, "رقم العقار": str})
                st.session_state.local_db = uploaded_df[["المنطقة", "رقم العقار"]]
                st.session_state.file_uploaded = True  
                st.success("✅ تم تحميل السجل بنجاح!")
                st.rerun()  
            except Exception as e: st.error("❌ حدث خطأ أثناء قراءة الملف.")
    
    df = st.session_state.local_db
    st.markdown("---")
    
    # حقول إدخال البيانات الميدانية
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        region_input = st.text_input("📍 اسم المنطقة الجغرافية", value=st.session_state.last_region, placeholder="النبطية، صور، صيدا...", key="region_field").strip()
    with input_col2:
        prop_val = "" if st.session_state.clear_trigger else ""
        property_number = st.text_input("🔢 رقم العقار الجديد", value=prop_val, placeholder="ادخل رقم العقار الحالي....", key="property_field").strip()
    
    st.session_state.clear_trigger = False

    # الأزرار الحمراء الكبيرة المتناسقة أفقياً تماماً 100%
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        btn_save = st.button("🚀 حفظ العقار والتحقق من التكرار", key="save_btn_main")
    with action_col2:
        btn_download = st.button("📥 تحميل وتنزيل سجل CSV ومزامنته", key="download_btn_main")
        if btn_download:
            if not df.empty:
                if GITHUB_TOKEN != "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN":
                    with st.spinner("🔄 جاري المزامنة..."):
                        success = upload_to_github(df)
                        if success: st.success("☁️ تم تأمين النسخة على GitHub!")
                sorted_df = df.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                csv_data = sorted_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="💾 اضغط هنا لتأكيد التنزيل لجهازك", data=csv_data, file_name=GITHUB_FILENAME, mime="text/csv", key="confirm_dl_btn")
            else: st.warning("⚠️ السجل فارغ حالياً!")

    # حساب الإحصائيات الفورية لعرضها داخل المربعات المتطابقة
    total_count = len(df)
    region_count = 0
    if region_input:
        region_count = len(df[df["المنطقة"].str.strip().str.lower() == region_input.lower()])

    st.markdown("<br>", unsafe_allow_html=True)

    # 📊 قسم المربعات الإحصائية الزرقاء (متطابقة ومتناظرة في الارتفاع والألوان 100%)
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1: 
        st.metric(label="🗄️ مجموع عدد العقارات الكلي في الملف", value=total_count)
    with stat_col2: 
        # الحاوية المخصصة لإجبار كبسة المنطقة على التطابق اللوني والهندسي التام مع المربع الكلي
        st.markdown("<div class='midan-metric-btn'>", unsafe_allow_html=True)
        display_label = f"📍 عدد عقارات منطقة ({region_input if region_input else '...'})"
        
        if st.button(label=f"{display_label}\n{region_count}", key="go_to_region_btn"):
            st.session_state.focus_on_region = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # جدول مراجعة السجلات الحالية للمنطقة
    if region_input:
        st.markdown(f"### 📊 ملف العقارات الجاري العمل عليها في منطقة: ({region_input})")
        filtered_df = df[df["المنطقة"].str.strip().str.lower() == region_input.lower()]
        if not filtered_df.empty:
            display_sheet = pd.DataFrame(filtered_df["رقم العقار"].values, columns=["رقم العقار"]).sort_values(by="رقم العقار").reset_index(drop=True)
            display_sheet.index += 1
            st.dataframe(display_sheet, use_container_width=True, height=200)
        else: st.info("ℹ️ لا توجد عقارات مسجلة لهذه المنطقة حالياً.")

    st.markdown("---")

    # محرك البحث الفوري والتصحيح
    search_query = st.text_input("🔍 البحث الفوري عن عقار وتعديله:", value=st.session_state.search_val, placeholder="اكتب اسم المنطقة أو رقم العقار للبحث السريع والتعديل...", key="search_modify_field").strip()
    st.session_state.search_val = search_query

    if btn_save:
        if region_input and property_number:
            is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_input.lower()) & (df["رقم العقار"].str.strip() == property_number)].shape[0] > 0
            if is_duplicate: st.error("❌ إلغاء: هذا العقار مسجل سابقاً in هذه المنطقة!")
            else:
                new_row = pd.DataFrame([{"المنطقة": region_input, "رقم العقار": property_number}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                st.session_state.last_region = region_input
                st.session_state.clear_trigger = True
                st.success(f"✅ تم حفظ العقار رقم ({property_number}) بنجاح!")
                st.rerun()
        else: st.warning("⚠️ فضلاً، يرجى ملء حقول المنطقة ورقم العقار أولاً.")

    if search_query:
        matched_records = df[df["المنطقة"].str.contains(search_query, case=False, na=False) | df["رقم العقار"].astype(str).str.contains(search_query, case=False, na=False)]
        if not matched_records.empty:
            st.info(f"📋 تم العثور على ({len(matched_records)}) سجل متطابق:")
            for idx, row in matched_records.iterrows():
                with st.expander(f"⚙️ تعديل العقار رقم {row['رقم العقار']} في {row['المنطقة']}", expanded=True):
                    edit_c1, edit_c2 = st.columns(2)
                    with edit_c1: new_edit_region = st.text_input("تعديل اسم المنطقة", value=row['المنطقة'], key=f"edit_reg_{idx}").strip()
                    with edit_c2: new_edit_prop = st.text_input("تعديل رقم العقار", value=row['رقم العقار'], key=f"edit_prop_{idx}").strip()
                    if st.button("💾 حفظ تعديلات السجل", key=f"save_edit_{idx}"):
                        if new_edit_region and new_edit_prop:
                            st.session_state.local_db.at[idx, "المنطقة"] = new_edit_region
                            st.session_state.local_db.at[idx, "رقم العقار"] = new_edit_prop
                            st.session_state.search_val = ""         
                            st.success("✅ تم تحديث وتصحيح السجل بنجاح!")
                            st.rerun()

    # نص أتمتة جافا سكربت للقفز الفوري وتحديد حقل المنطقة دغري عند كبس الزر التفاعلي
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
