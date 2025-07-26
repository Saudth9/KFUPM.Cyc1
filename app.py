import streamlit as st
import pandas as pd
import altair as alt

# رابط Google Sheet
sheet_id = "1hzxrBWgNpeSN-aEB9oV8O4awj6JBpvw7TJ4aJy7uLEE"
sheet_name = "Sheet1"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    # قراءة البيانات
    df = pd.read_csv(csv_url).dropna()

    # استخراج أسماء الأعمدة تلقائياً
    name_col = df.columns[0]  # مثلاً: "اللاعب"
    points_col = df.columns[1]  # مثلاً: "مجموع النقاط"

    # تنظيف وتحويل البيانات
    df[points_col] = pd.to_numeric(df[points_col], errors='coerce')
    df = df.sort_values(points_col)

    # واجهة ستريملت
    st.set_page_config(page_title="دوري الدراجين ٢٤٢", layout="wide")
    st.title("🚴‍♂️ نتائج دوري الدراجين ٢٤٢")
    st.markdown("📊 تحديث تلقائي من Google Sheets")

    # رسم بياني أفقي (قلب الجدول)
    chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(f'{points_col}:Q', title='النقاط'),
        x=alt.X(f'{name_col}:N', sort='-y', title=name_col),
        color=alt.Color(f'{points_col}:Q', scale=alt.Scale(scheme='blues')),
        tooltip=[name_col, points_col]
    ).properties(width=800, height=500)

    st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error("⚠️ حدث خطأ أثناء تحميل البيانات من Google Sheet.")
    st.exception(e)
