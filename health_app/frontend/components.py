import streamlit as st
from datetime import date

def custom_date_input(label, key, help):
    selected_date = st.date_input(
        label=label,
        key=key,
        help=help,
    )
    return selected_date.strftime("%Y-%m-%d")  # フォーマット済み文字列を返す

# [cm]を[m]に変換する関
def cm_to_m(cm:float):
    return cm / 100

# 身長・体重から標準体重を計算する関数
def standard_weight(height: float):
    standard_weight = 22*(cm_to_m(height)**2)
    return standard_weight

# 身長・体重から美容体重を計算する関数
def beauty_weight(height: float):
    beauty_weight = 20*(cm_to_m(height)**2)
    return beauty_weight

# 身長・体重からシンデレラ体重を計算する関数
def cinderella_weight(height: float):
    cinderella_weight = 18*(cm_to_m(height)**2)
    return cinderella_weight

# 身長・体重からBMIを計算する関数
def bmi(height: float, weight: float):
    bmi = weight / (cm_to_m(height)**2)
    return bmi

# 身長・体重から肥満度を計算する関数
def obesity_degree(height: float, weight: float):
    bmi_value = bmi(height, weight)
    if bmi_value < 18.5:
        return "痩せ型"
    elif 18.5 <= bmi_value < 25:
        return "普通"
    elif 25 <= bmi_value < 30:
        return "肥満（1度）"
    elif 30 <= bmi_value < 35:
        return "肥満（2度）"
    elif 35 <= bmi_value < 40:
        return "肥満（3度）"
    else:
        return "肥満（4度）"
