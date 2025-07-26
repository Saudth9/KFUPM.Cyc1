import streamlit as st
import pandas as pd
import altair as alt

# 1. ثابت: ID للملف اللي فيه config
config_sheet_id = "1zA5rXXXXXX_ID_الثابت_اللي_فيه_الاعدادات"
config_sheet_id = "1AbCDefGhIJklMNOPQRstuVWXYZ1234567"
config_url = f"https://docs.google.com/spreadsheets/d

# 2. نقرأ ملف الإعدادات
config_df = pd.read_csv(config_url)
sheet_id = config_df.loc[config_df['المفتاح'] == 'sheet_id', 'القيمة'].values[0]
sheet_name = config_df.loc[config_df['المفتاح'] == 'sheet_name', 'القيمة'].values[0]

# 3. نستخدمهم لرابط البيانات الحقيقي
data_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# 4. تحميل وتجهيز البيانات
df = pd.read_csv(data_url).dropna()
name_col = df.columns[0]
points_col = df.columns[1]
df[points_col] = pd.to_numeric(df[points_col], errors='coerce')
df_grouped = df.groupby(name_col, as_index=False)[points_col].sum()
df_grouped = df_grouped.sort_values(points_col, ascending=False)

# 5. عرض النتائج
st.title("🚴‍♂️ نتائج دوري الدراجين ٢٥١")
st.markdown("📊 تحديث تلقائي كامل من Google Sheets")

chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X(f'{name_col}:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y(f'{points_col}:Q', title='النقاط'),
    color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[name_col, points_col]
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
