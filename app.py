import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ringostat Test", layout="wide")

st.title("Аналітичний дашборд Ringostat")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # Завантажуємо файл, пропускаючи мета-дані (11 рядків)
    df = pd.read_csv('test_analitika.csv', skiprows=11)
    
    # Залишаємо лише перші 4 колонки
    df = df.iloc[:, [0, 1, 2, 3]]
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Видаляємо порожні рядки
    df = df.dropna(subset=['CRM'])
    
    # Чистимо відсотки (замінюємо кому на крапку, якщо вона є)
    df['Win_Rate'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.')
    df['Win_Rate'] = pd.to_numeric(df['Win_Rate'], errors='coerce')
    
    # Видаляємо рядки, де не вдалося отримати число
    df = df.dropna(subset=['Win_Rate'])

    # Метрики
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Загальна кількість успішних угод", int(pd.to_numeric(df['Won'], errors='coerce').sum()))
    with col2:
        top_crm = df.sort_values(by='Win_Rate', ascending=False).iloc[0]
        st.metric("Найкраща конверсія", f"{top_crm['CRM']} ({top_crm['Win_Rate']}%)")

    # Графік
    st.subheader("Ефективність CRM за Win Rate (%)")
    fig = px.bar(df, x='Win_Rate', y='CRM', orientation='h', 
                 color='Win_Rate', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # Таблиця
    st.write("### Вихідні дані")
    st.dataframe(df)

except Exception as e:
    st.error(f"Виникла помилка: {e}")
    st.write("Спробуйте перевірити файл 'test_analitika.csv' на GitHub.")
