import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Ringostat Test - Anastasiia Ihnatenko", layout="wide")

# Заголовок на сторінці
st.header("Тестове завдання для Ringostat")
st.subheader("Посада: Junior Operations Specialist")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # Зчитуємо дані без пропуску рядків спочатку, а потім знайдемо потрібний заголовок
    raw_df = pd.read_csv('test_analitika.csv')
    # Шукаємо рядок, де починаються дані (де в першій колонці є слово 'ZohoCRM' або 'CRM')
    df = pd.read_csv('test_analitika.csv', skiprows=11)
    
    # Очищення назв стовпців
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[:, [0, 1, 2, 3]] 
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Конвертація Win Rate у числа
    df['Win_Rate_Num'] = df['Win_Rate'].str.replace('%', '').astype(float)
    
    # Розрахунок показників
    best_crm = df[df['Win_Rate_Num'] < 100].sort_values(by='Win_Rate_Num', ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Найефективніша CRM", best_crm['CRM'])
    col2.metric("Найвищий Win Rate", f"{best_crm['Win_Rate_Num']}%")
    col3.metric("Успішних угод (всього)", int(df['Won'].sum()))

    st.markdown("---")
    st.write("### Аналіз ефективності CRM систем")
    
    # Графік
    fig = px.bar(df[df['Won']+df['Lost'] > 0], x='Win_Rate_Num', y='CRM', 
                 orientation='h', color='Win_Rate_Num', 
                 color_continuous_scale='Portland',
                 labels={'Win_Rate_Num': 'Win Rate (%)'})
    st.plotly_chart(fig, use_container_width=True)

    # Таблиця
    with st.expander("Переглянути таблицю даних"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Помилка: Переконайтеся, що файл 'test_analitika.csv' завантажений коректно.")
