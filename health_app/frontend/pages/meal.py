import streamlit as st
from PIL import Image
from health_app.frontend.app import post_data
from health_app.frontend.style import set_page_config, set_custom_css
from health_app.frontend.components import custom_date_input


def record_meal_page():
    set_page_config()
    set_custom_css()
    
    st.title("食事記録ページ🍴")
    st.write("日付と食事を記録しよう！")
    
    date = custom_date_input()
    uploaded_image = st.file_uploader("食事の画像をアップロード", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた食事の画像")
        
    else:
        st.warning("画像をアップロードしてください")

if __name__ == "__main__":
    record_meal_page()