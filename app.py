import streamlit as st

# إخفاء شعار Streamlit و"Fork" والـ hamburger menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

import streamlit as st
# تعديل شكل Streamlit وإضافة الشعار
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
        body {
            background-color: #111;
            color: white;
        }
    </style>
    <div style='text-align: center; margin-bottom: 20px;'>
        <img src='https://i.imgur.com/jtBDxJV.png' style='max-width: 300px;'>
    </div>
""", unsafe_allow_html=True)

import pandas as pd
import altair as alt

# ID ملف الإعدادات (config)
config_sheet_id = "1Z7uxg5oIMOwKW1dANOwoxgqv7ewjnpu5euNfALb2VRs"
config_url = f"https://docs.google.com/spreadsheets/d/{config_sheet_id}/gviz/tq?tqx=out:csv"

# قراءة الإعدادات
config_df = pd.read_csv(config_url)
sheet_id = config_df.loc[config_df['المفتاح'] == 'sheet_id', 'القيمة'].values[0]
sheet_name = config_df.loc[config_df['المفتاح'] == 'sheet_name', 'القيمة'].values[0]

# رابط البيانات
data_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# قراءة وتجهيز البيانات
df = pd.read_csv(data_url).dropna()
df.columns = df.columns.str.strip()
name_col = df.columns[0]
points_col = df.columns[1]
df[points_col] = pd.to_numeric(df[points_col], errors='coerce')
df_grouped = df.groupby(name_col, as_index=False)[points_col].sum()
df_grouped = df_grouped.sort_values(points_col, ascending=False)

# عرض البيانات
st.title("🚴‍♂️ نتائج دوري الدراجين 251")
st.markdown("📊 تحديث تلقائي كامل من Google Sheets")

chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X(f'{name_col}:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y(f'{points_col}:Q', title='النقاط'),
    color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[name_col, points_col]
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
