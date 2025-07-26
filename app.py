import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------
# 1. إخفاء شعار ستريملت والقوائم
# ---------------------------
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 2rem;}

        .logo-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: -10px;
        }

        .logo-text {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .title-line {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .logo-img {
            height: 120px;
        }

        .kfupm {
            font-size: 46px;
            font-weight: bold;
            color: white;
        }

        .cyclists {
            font-size: 46px;
            font-weight: bold;
            color: orange;
        }

        .desc {
            color: gray;
            font-size: 17px;
            margin-top: -10px;
        }

        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-align: right;
            margin-top: 40px;
            margin-bottom: 10px;
        }

        .update-note {
            text-align: right;
            font-size: 16px;
            color: #ccc;
        }
    </style>

    <div class='logo-bar'>
        <div class='logo-text'>
            <div class='title-line'>
                <span class='kfupm'>KFUPM</span>
                <span class='cyclists'>CYCLISTS</span>
            </div>
            <div class='desc'>🚴‍♂️ نادي دراجي جامعة الملك فهد للبترول و المعادن</div>
        </div>
        <img class='logo-img' src='https://i.imgur.com/bND8Lte.png' />
    </div>

    <div class='main-title'>🚴‍♂️ نتائج دوري الدراجين 251</div>
    <div class='update-note'>📊 تحديث تلقائي كامل من Google Sheets</div>
""", unsafe_allow_html=True)

# ---------------------------
# 2. تحميل الإعدادات من Google Sheets
# ---------------------------
config_sheet_id = "1Z7uxg5oIMOwKW1dANOwoxgqv7ewjnpu5euNfALb2VRs"
config_url = f"https://docs.google.com/spreadsheets/d/{config_sheet_id}/gviz/tq?tqx=out:csv"
config_df = pd.read_csv(config_url)

sheet_id = config_df.loc[config_df['المفتاح'] == 'sheet_id', 'القيمة'].values[0]
sheet_name = config_df.loc[config_df['المفتاح'] == 'sheet_name', 'القيمة'].values[0]

# ---------------------------
# 3. قراءة وتجهيز البيانات
# ---------------------------
data_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(data_url).dropna()
df.columns = df.columns.str.strip()
name_col = df.columns[0]
points_col = df.columns[1]
df[points_col] = pd.to_numeric(df[points_col], errors='coerce')
df_grouped = df.groupby(name_col, as_index=False)[points_col].sum()
df_grouped = df_grouped.sort_values(points_col, ascending=False)

# ---------------------------
# 4. عرض الرسم البياني
# ---------------------------
chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X(f'{name_col}:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y(f'{points_col}:Q', title='النقاط'),
    color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[name_col, points_col]
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
