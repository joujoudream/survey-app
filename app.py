import streamlit as st
import pandas as pd
import requests
import base64
import glob

# 🌐 إعدادات أساسية
st.set_page_config(page_title="Khatib & Alami", page_icon="🏢", layout="centered")

GITHUB_TOKEN = "ضع_هنا_TOKEN_الخاص_بك"
GITHUB_REPO = "اسم_حسابك/اسم_المستودع"
OUTPUT_FILENAME = "KhatibAlami_Midan_Data.csv"

# دالة المزامنة السريعة
def sync_data(df):
    try:
        csv_content = df.to_csv(index=False).encode('utf-8-sig')
        # الحفظ المحلي
        df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
        # المزامنة مع GitHub (إذا تم وضع الـ Token)
        if GITHUB_TOKEN != "ضع_هنا_TOKEN_الخاص_بك":
            encoded = base64.b64encode(csv_content).decode('utf-8')
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{OUTPUT_FILENAME}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            res = requests.get(url, headers=headers)
            sha = res.json().get("sha") if res.status_code == 200 else None
            data = {"message": "تحديث سريع", "content": encoded}
            if sha: data["sha"] = sha
            requests.put(url, headers=headers, json=data)
    except: pass

# تحميل البيانات
if "df" not in st.session_state:
    files = glob.glob("*.csv")
    if files: st.session_state.df = pd.read_csv(files[0], dtype=str)
    else: st.session_state.df = pd.DataFrame(columns=["المنطقة", "رقم العقار"])

# 🎨 واجهة مباشرة
st.title("🏢 Khatib & Alami - إدخال سريع")
region = st.text_input("📍 المنطقة")
prop = st.text_input("🔢 رقم العقار")

if st.button("🚀 حفظ العقار"):
    if region and prop:
        new_row = pd.DataFrame({"المنطقة": [region], "رقم العقار": [prop]})
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        sync_data(st.session_state.df)
        st.success("تم الحفظ!")
    else:
        st.error("يرجى ملء الحقول")

st.write("---")
st.dataframe(st.session_state.df.tail(10)) # عرض آخر 10 عقارات فقط
