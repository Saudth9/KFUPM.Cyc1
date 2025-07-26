import streamlit as st
import pandas as pd
import altair as alt

# إعداد الرابط الصحيح للـ Google Sheet
sheet_id = "YOUR_SHEET_ID_HERE"  # 👈 استبدل هذا بالـ ID حقك
sheet_name = "Sheet1"  # تأكد من الاسم بالضبط
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# تحميل البيانات من Google Sheets
df = pd.read_csv(csv_url)
df = df.dropna()
df['مجموع النقاط'] = pd.to_numeric(df['مجموع النقاط'], errors='coerce')
df = df.sort_values('مجموع النقاط', ascending=False)

# إعداد الواجهة
st.title("🚴‍♂️ نتائج دوري الدراجين ٢٥١")
st.markdown("📊 تحديث تلقائي من Google Sheets")

# رسم الرسم البياني باستخدام Altair
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('اللاعب:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y('مجموع النقاط:Q', title='النقاط'),
    color=alt.Color('مجموع النقاط:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['اللاعب', 'مجموع النقاط']
).properties(
    width=1000,
    height=500
)

st.altair_chart(chart, use_container_width=True)
