import streamlit as st
import pandas as pd
import requests
import base64
import os
from PIL import Image

# 🌐 1. إعدادات الصفحة الرسمية للشركة
st.set_page_config(
    page_title="Khatib & Alami Company", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔑 إعدادات الحساب والمستودع الخاص بك على GitHub (يرجى ملء البيانات هنا لتفعيل الربط التلقائي)
GITHUB_TOKEN = "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع_YOUR_USERNAME/YOUR_REPO"
GITHUB_FILENAME = "KhatibAlami_Midan_Data.csv"

# دالة الرفع والمزامنة التلقائية على GitHub
def upload_to_github(dataframe):
    if GITHUB_TOKEN == "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN":
        return False
    try:
        csv_content = dataframe.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True).to_csv(index=False).encode('utf-8-sig')
        encoded_content = base64.b64encode(csv_content).decode('utf-8')
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILENAME}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        data = {"message": "تحديث تلقائي فوري لسجل العقارات الميداني - الريس وليد", "content": encoded_content}
        if sha: data["sha"] = sha
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code in [200, 201]
    except Exception as e:
        return False

# دالة التحميل التلقائي للملف عند بدء تشغيل البرنامج
def load_initial_data():
    # 1. محاولة تحميل الملف محلياً من الجهاز أولاً
    if os.path.exists(GITHUB_FILENAME):
        try:
            return pd.read_csv(GITHUB_FILENAME, dtype={"المنطقة": str, "رقم العقار": str})
        except:
            pass
            
    # 2. إذا لم يوجد محلياً، محاولة سحبه تلقائياً من GitHub
    if GITHUB_TOKEN != "ضع_هنا_رمز_الوصول_الخاص_بك_YOUR_GITHUB_TOKEN":
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILENAME}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                file_data = res.json()
                csv_bytes = base64.b64decode(file_data["content"])
                import io
                return pd.read_csv(io.BytesIO(csv_bytes), dtype={"المنطقة": str, "رقم العقار": str})
        except:
            pass
            
    # 3. إذا فشل كل شيء، يتم إنشاء جدول فارغ جديد
    return pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🎨 الـ CSS الهندسي المستقر لحماية الألوان والتناسق الأفقي تماماً كما طلبت
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
