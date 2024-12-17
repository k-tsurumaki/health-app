import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Health Tracker",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def set_custom_css():
    st.markdown("""
        <style>
        /* カスタムフォントとページ全体の設定 */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f7f9;
        }
        /* タイトルスタイル */
        .main-title {
            color: #2c3e50;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        /* ボタンカスタマイズ */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        </style>
    """, unsafe_allow_html=True)
