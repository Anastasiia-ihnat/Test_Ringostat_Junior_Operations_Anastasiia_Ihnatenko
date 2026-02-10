import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Налаштування сторінки
st.set_page_config(page_title="Ringostat Test - Anastasiia Ihnatenko", layout="wide")

st.header("Тестове завдання для Ringostat")
st.subheader("Посада: Junior Operations Specialist")
st.write("Виконавець: Анастасія Ігнатенко")

# 2. Функція завантаження та обробки
try:
    # Читаємо файл, пропускаючи перші 11 рядків
    df = pd.read_csv('test_analitika.csv', skiprows=11)
    
    # Прибираємо порожні рядки та чистимо назви колонок
    df = df.dropna(subset=[df.columns[0]])
    df.columns = [c.strip() for c in df.columns]
    
    # Вибираємо тільки потрібні 4 колонки (CRM, Lost, Won, Win Rate)
    df = df.iloc[:, [0, 1, 2, 3]]
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Перетворюємо Win_Rate у число (прибираємо % та міняємо коми на крапки)
    df['Win_Rate_Num'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
    
    # 3. Метрики
    best_crm = df[df['Win_Rate_Num'] < 100].sort_values(by='Win_Rate_Num', ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Найефективніша CRM", best_crm['CRM'])
    col2.metric("Найвищий Win Rate", f"{best_crm['Win_Rate_Num']}%")
    col3.metric("Успішних угод (всього)", int(df['Won'].sum()))

    # 4. Графік
    st.markdown("---")
    st.write("### Аналіз конверсії за типами CRM")
    
    fig = px.bar(df, x='Win_Rate_Num', y='CRM', 
                 orientation='h', 
                 color='Win_Rate_Num', 
                 color_continuous_scale='Portland',
                 labels={'Win_Rate_Num': 'Win Rate (%)'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. Таблиця для перевірки
    with st.expander("Показати повну таблицю даних"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Помилка в обробці даних: {e}")
