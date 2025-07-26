import streamlit as st
import pandas as pd
import altair as alt

# بيانات الرابط
sheet_id = "اكتب_الـ_ID_الجديد_هنا"
sheet_name = "Sheet1"  # تأكد من الاسم بالضبط
csv_url = f"1ABcD12345EfGHIJKLmNOPQRstUVwxYZ"

# تحميل البيانات
df = pd.read_csv(csv_url)
df = df.dropna()
df['مجموع النقاط'] = pd.to_numeric(df['مجموع النقاط'], errors='coerce')
df = df.sort_values('مجموع النقاط', ascending=False)

# رسم بياني
st.title("🚴‍♂️ نتائج دوري الدراجين ٢٥١")
st.markdown("📊 تحديث تلقائي من Google Sheets")

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('اللاعب:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=14)),
    y=alt.Y('مجموع النقاط:Q', title='النقاط'),
    color=alt.Color('مجموع النقاط:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['اللاعب', 'مجموع النقاط']
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
