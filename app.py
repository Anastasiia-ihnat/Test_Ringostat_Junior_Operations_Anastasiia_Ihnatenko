import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Ringostat Test - Anastasiia Ihnatenko", layout="wide")

st.header("Тестове завдання для Ringostat")
st.subheader("Посада: Junior Operations Specialist")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # Завантаження даних
    df = pd.read_csv('test_analitika.csv', skiprows=11)
    
    # Очищення даних
    df = df.dropna(subset=[df.columns[0]])
    df.columns = [c.strip() for c in df.columns]
    
    # Вибір колонок
    df = df.iloc[:, [0, 1, 2, 3]]
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Перетворення відсотків у числа
    df['Win_Rate_Num'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
    
    # Розрахунок метрик
    best_crm = df[df['Win_Rate_Num'] < 100].sort_values(by='Win_Rate_Num', ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Найефективніша CRM", best_crm['CRM'])
    col2.metric("Найвищий Win Rate", f"{best_crm['Win_Rate_Num']}%")
    col3.metric("Успішних угод (всього)", int(df['Won'].sum()))

    # Графік
    st.markdown("---")
    st.write("### Аналіз конверсії за типами CRM")
    
    fig = px.bar(df, x='Win_Rate_Num', y='CRM', 
                 orientation='h', 
                 title="Конверсія у виграш за типами CRM",
                 color='Win_Rate_Num', 
                 color_continuous_scale='Portland',
                 labels={'Win_Rate_Num': 'Win Rate (%)'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Таблиця
    with st.expander("Показати повну таблицю даних"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Помилка в обробці даних: {e}")
