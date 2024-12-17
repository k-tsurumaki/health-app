import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

def post_data(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success("データが正常に送信されました。")
        else:
            st.error(f"エラーが発生しました: {response.text}")
    except Exception as e:
        st.error(f"リクエストに失敗しました: {str(e)}")
