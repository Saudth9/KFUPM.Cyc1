import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------
# 1. إعداد CSS مخصص
# ---------------------------
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
        body {
            background-color: #111;
            color: white;
        }

        @keyframes pop-in {
            0%   { transform: scale(0.5); opacity: 0; }
            80%  { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }

        .logo-container {
            text-align: center;
            animation: pop-in 1s ease-out;
            margin-bottom: 20px;
        }

        .logo-title {
            font-size: 48px;
            font-weight: bold;
            color: white;
        }

        .logo-subtitle {
            font-size: 48px;
            font-weight: bold;
            color: orange;
        }

        .logo-desc {
            font-size: 20px;
            color: gray;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 2. عرض الشعار
# ---------------------------
st.image("a0f80259-2ff4-42d5-89cb-c6d55716b9b5.png", width=100)

# ---------------------------
# 3. عرض العنوان النصي
# ---------------------------
st.markdown("""
    <div class='logo-container'>
        <span class='logo-title'>KFUPM</span>
        <span class='logo-subtitle'>CYCLISTS</span><br>
        <span class='logo-desc'>🚴‍♂️ نادي دراجي جامعة الملك فهد للبترول والمعادن</span>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# 4. تحميل إعدادات Google Sheets
# ---------------------------
config_sheet_id = "1Z7uxg5oIMOwKW1dANOwoxgqv7ewjnpu5euNfALb2VRs"
config_url = f"https://docs.google.com/spreadsheets/d/{config_sheet_id}/gviz/tq?tqx=out:csv"
config_df = pd.read_csv(config_url)

sheet_id = config_df.loc[config_df['المفتاح'] == 'sheet_id', 'القيمة'].values[0]
sheet_name = config_df.loc[config_df['المفتاح'] == 'sheet_name', 'القيمة'].values[0]

# ---------------------------
# 5. قراءة وتجهيز البيانات
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
# 6. عرض الرسم البياني
# ---------------------------
st.title("🚴‍♂️ نتائج دوري الدراجين 251")
st.markdown("📊 تحديث تلقائي كامل من Google Sheets")

chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X(f'{name_col}:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y(f'{points_col}:Q', title='النقاط'),
    color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[name_col, points_col]
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
