import streamlit as st
import pandas as pd
import altair as alt

# رابط Google Sheet
sheet_id = "https://docs.google.com/spreadsheets/d/1hzxrBWgNpeSN-aEB9oV8O4awj6JBpvw7TJ4aJy7uLEE/edit?gid=0#gid=0"
sheet_name = "Sheet1"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(csv_url)
    df = df.dropna()
    df['مجموع النقاط'] = pd.to_numeric(df['مجموع النقاط'], errors='coerce')
    df = df.sort_values('مجموع النقاط', ascending=False)  # ترتيب تنازلي

    # واجهة Streamlit
    st.set_page_config(page_title="دوري الدراجين ٢٥١", layout="wide")
    st.title("🚴‍♂️ نتائج دوري الدراجين ٢٥١")
    st.markdown("📊 تحديث تلقائي من Google Sheets")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('اللاعب:N', sort='-y', title='اللاعب'),
        y=alt.Y('مجموع النقاط:Q', title='النقاط'),
        color=alt.Color('مجموع النقاط:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['اللاعب', 'مجموع النقاط']
    ).configure_axisX(labelFontSize=14).configure_axisY(labelFontSize=14).properties(width=1000, height=500)

    st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error("تأكد من أن رابط Google Sheet صحيح، حدث خطأ أثناء جلب البيانات.")
    st.exception(e)
