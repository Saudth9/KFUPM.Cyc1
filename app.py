import streamlit as st
import pandas as pd
import altair as alt

# رابط Google Sheet
sheet_id = "1hzxrBWgNpeSN-aEB9oV8O4awj6JBpvw7TJ4aJy7uLEE"
sheet_name = "Sheet1"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# قراءة البيانات
df = pd.read_csv(csv_url)
df = df.dropna()
df['مجموع النقاط'] = pd.to_numeric(df['مجموع النقاط'], errors='coerce')
df = df.sort_values('مجموع النقاط')

# واجهة Streamlit
st.title("🚴‍♂️ نتائج دوري الدراجين ٢٤٢")
st.markdown("📊 تحديث تلقائي من Google Sheets")

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('مجموع النقاط:Q', title='النقاط'),
    y=alt.Y('اللاعب:N', sort='-x', title='اللاعب'),
    color=alt.Color('مجموع النقاط:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['اللاعب', 'مجموع النقاط']
).properties(width=700, height=500)

st.altair_chart(chart, use_container_width=True)
