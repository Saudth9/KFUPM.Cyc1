import streamlit as st
import pandas as pd
import altair as alt

# ID الجدول من Google Sheets
sheet_id = "اكتب_الـ_ID_هنا"
sheet_name = "Sheet1"
csv_url = f"sheet_id = "1FZxOqW9vS5xPQdN4Ib2o3G9Xb7mG3y8eKlHZLZ0RjU4"

# تحميل البيانات
df = pd.read_csv(csv_url).dropna()

# الحصول على أسماء الأعمدة تلقائيًا
name_col = df.columns[0]  # اسم العمود الأول (المشارك)
points_col = df.columns[1]  # اسم العمود الثاني (مجموع النقاط)

# تحويل النقاط إلى رقمية
df[points_col] = pd.to_numeric(df[points_col], errors='coerce')

# تجميع النقاط حسب الاسم
df_grouped = df.groupby(name_col, as_index=False)[points_col].sum()
df_grouped = df_grouped.sort_values(points_col, ascending=False)

# العنوان
st.title("🚴‍♂️ نتائج دوري الدراجين ٢٥١")
st.markdown("📊 تحديث تلقائي من Google Sheets")

# رسم الرسم البياني
chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X(f'{name_col}:N', sort='-y', title='المشارك', axis=alt.Axis(labelFontSize=16)),
    y=alt.Y(f'{points_col}:Q', title='النقاط'),
    color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[name_col, points_col]
).properties(width=1000, height=500)

st.altair_chart(chart, use_container_width=True)
