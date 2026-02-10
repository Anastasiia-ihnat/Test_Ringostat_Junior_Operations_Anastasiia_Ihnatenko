import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ringostat Test - Anastasiia Ihnatenko", layout="wide")

st.header("Тестове завдання для Ringostat")
st.subheader("Посада: Junior Operations Specialist")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # 1. Читаємо файл повністю
    full_df = pd.read_csv('test_analitika.csv', header=None)
    
    # 2. Знаходимо рядок, де починаються дані (шукаємо "ZohoCRM")
    start_row = 0
    for i, row in full_df.iterrows():
        if 'ZohoCRM' in str(row.values):
            start_row = i
            break
    
    # 3. Перечитуємо з правильного рядка
    df = pd.read_csv('test_analitika.csv', skiprows=start_row)
    
    # 4. Чистимо колонки
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[:, [0, 1, 2, 3]] 
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Прибираємо сміття (рядки, де CRM - це NaN або не містить назву системи)
    df = df.dropna(subset=['CRM'])
    df = df[df['CRM'].str.contains('CRM|Pipedrive|Bitrix|amoCRM|Salesforce', case=False, na=False)]
    
    # 5. Конвертуємо Win Rate у числа
    df['Win_Rate_Num'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
    
    # 6. Метрики
    best_crm = df.sort_values(by='Win_Rate_Num', ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Найефективніша CRM", best_crm['CRM'])
    col2.metric("Найвищий Win Rate", f"{best_crm['Win_Rate_Num']}%")
    col3.metric("Успішних угод (всього)", int(pd.to_numeric(df['Won']).sum()))

    st.markdown("---")
    st.write("### Аналіз ефективності CRM систем")
    
    # 7. Графік
    fig = px.bar(df, x='Win_Rate_Num', y='CRM', 
                 orientation='h', color='Win_Rate_Num', 
                 color_continuous_scale='Portland',
                 labels={'Win_Rate_Num': 'Win Rate (%)'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Переглянути вихідні дані"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Помилка: {e}")
