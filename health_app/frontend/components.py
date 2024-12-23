import streamlit as st
from datetime import date
from health_app.backend.schemas.user import GenderType


def custom_date_input(label, key, help):
    selected_date = st.date_input(
        label=label,
        key=key,
        help=help,
    )
    return selected_date.strftime("%Y-%m-%d")  # フォーマット済み文字列を返す


# [cm]を[m]に変換する関
def cm_to_m(cm: float):
    return cm / 100


# 身長・体重から標準体重を計算する関数
def standard_weight(height: float):
    standard_weight = 22 * (cm_to_m(height) ** 2)
    return standard_weight


# 身長・体重から美容体重を計算する関数
def beauty_weight(height: float):
    beauty_weight = 20 * (cm_to_m(height) ** 2)
    return beauty_weight


# 身長・体重からシンデレラ体重を計算する関数
def cinderella_weight(height: float):
    cinderella_weight = 18 * (cm_to_m(height) ** 2)
    return cinderella_weight


# 身長・体重からBMIを計算する関数
def bmi(height: float, weight: float):
    bmi = weight / (cm_to_m(height) ** 2)
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


# 年齢・身長・体重・性別から基礎代謝量を計算する関数
def bmr(age: int, height: float, weight: float, gender: GenderType):
    if gender == "man":
        bmr = 66 + 13.7 * weight + 5.0 * height - 6.8 * age
    else:
        bmr = 665 + 9.6 * weight + 1.7 * height - 7.0 * age
    return bmr

# 年齢・性別から1日の推定摂取カロリーを計算する関数
def daily_caloric_needs(age: int, gender: str) -> int:
    if gender == "man":
        if 12 <= age <= 14:
            return 2600
        elif 15 <= age <= 17:
            return 2800
        elif 18 <= age <= 29:
            return 2650
        elif 30 <= age <= 49:
            return 2700
        elif 50 <= age <= 64:
            return 2600
        elif 65 <= age <= 74:
            return 2400
    elif gender == "woman":
        if 12 <= age <= 14:
            return 2400
        elif 15 <= age <= 17:
            return 2300
        elif 18 <= age <= 29:
            return 2000
        elif 30 <= age <= 49:
            return 2050
        elif 50 <= age <= 64:
            return 1950
        elif 65 <= age <= 74:
            return 1850
    return 0  # 年齢が範囲外の場合や性別が不明な場合は0を返す