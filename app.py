import streamlit as st

# كود CSS لضبط محاذاة الأعمدة وجعل العناصر متناسقة على نفس الخط
st.markdown("""
    <style>
    /* جعل محتوى الأعمدة يترتب عمودياً من الأسفل ليصبحوا على نفس الخط */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)
