import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Ringostat Test", layout="wide")

st.title("Аналітичний дашборд Ringostat")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # Завантажуємо файл
    df = pd.read_csv('test_analitika.csv', skiprows=11)
    
    # Вибираємо потрібні колонки
    df = df.iloc[:, [0, 1, 2, 3]]
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Очищення даних
    df = df.dropna(subset=['CRM'])
    df['Win_Rate'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.')
    df['Win_Rate'] = pd.to_numeric(df['Win_Rate'], errors='coerce')
    df = df.dropna(subset=['Win_Rate'])

    # Відображення метрик
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Загальна кількість успішних угод", int(pd.to_numeric(df['Won'], errors='coerce').sum()))
    with c2:
        top = df.sort_values(by='Win_Rate', ascending=False).iloc[0]
        st.metric("Найкраща конверсія", f"{top['CRM']} ({top['Win_Rate']}%)")

    # Графік
    st.subheader("Ефективність CRM за Win Rate (%)")
    fig = px.bar(df, x='Win_Rate', y='CRM', orientation='h', 
                 color='Win_Rate', color_continuous_scale='Portland')
    st.plotly_chart(fig, use_container_width=True)

    # Таблиця
    st.write("### Вихідні дані")
    st.dataframe(df)

except Exception as e:
    st.error(f"Виникла помилка: {e}")
