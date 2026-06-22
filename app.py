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
                return pd.read_csv(io.BytesIO(csv_bytes), encoding='utf-8-sig', dtype={"المنطقة": str, "رقم العقار
