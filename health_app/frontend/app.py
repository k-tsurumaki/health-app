import streamlit as st
import requests

BASE_URL = "http://localhost:8000/api/v1"

def post_data(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, json=data)
        if 200 <= response.status_code < 300:
            st.success("データが正常に送信されました。")
        else:
            st.error(f"エラーが発生しました: {response.text}")
    except Exception as e:
        st.error(f"リクエストに失敗しました: {str(e)}")
        
def get_weight_records(endpoint, user_id:int):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, params={"user_id": user_id})
    if 200 <= response.status_code < 300:
        data = response.json()
        return data
    return []
