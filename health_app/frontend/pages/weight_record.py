import streamlit as st
from health_app.frontend.app import post_data
from health_app.frontend.style import set_page_config, set_custom_css

def record_weight_page():
    set_page_config()
    set_custom_css()

    # タイトル部分
    st.markdown("<h1 class='main-title'>体重記録ページ 📝</h1>", unsafe_allow_html=True)

    # 2列のレイアウト
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://via.placeholder.com/400x300?text=体重管理", use_column_width=True)

    with col2:
        st.subheader("体重を入力してください")
        date = st.date_input("日付を選択")
        weight = st.number_input("体重 (kg)", min_value=0.0, step=0.1, format="%.1f")

        if st.button("記録を保存"):
            if date and weight > 0:
                data = {"date": str(date), "weight": weight}
                post_data("/record_weight", data)
            else:
                st.warning("正しいデータを入力してください。")

if __name__ == "__main__":
    record_weight_page()
