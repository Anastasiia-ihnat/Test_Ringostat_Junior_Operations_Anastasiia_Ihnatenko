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
    
    # 2. Шукаємо, в якому рядку знаходиться слово 'ZohoCRM'
    # Це допоможе нам точно знайти початок таблиці, незалежно від кількості рядків зверху
    start_row = full_df[full_df.astype(str).apply(lambda x: x.str.contains('ZohoCRM')).any(axis=1)].index[0]
    
    # 3. Перечитуємо файл вже з правильного місця
    df = pd.read_csv('test_analitika.csv', skiprows=start_row)
    
    # 4. Чистимо дані
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[:, [0, 1, 2, 3]] 
    df.columns = ['CRM', 'Lost', 'Won', 'Win_Rate']
    
    # Видаляємо порожні рядки або рядки, де замість CRM якийсь інший текст
    df = df[df['CRM'].str.contains('CRM', na=False)]
    
    # 5. Конвертуємо Win Rate у числа (обробляємо і коми, і крапки)
    df['Win_Rate_Num'] = df['Win_Rate'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
    
    # Метрики
    best_crm = df.sort_values(by='Win_Rate_Num', ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Найефективніша CRM", best_crm['CRM'])
    col2.metric("Найвищий Win Rate", f"{best_crm['Win_Rate_Num']}%")
    col3.metric("Успішних угод (всього)", int(pd.to_numeric(df['Won']).sum()))

    st.markdown("---")
    st.write("### Аналіз ефективності CRM систем")
    
    fig = px.bar(df, x='Win_Rate_Num', y='CRM', 
                 orientation='h', color='Win_Rate_Num', 
                 color_continuous_scale='Portland',
                 labels={'Win_Rate_Num': 'Win Rate (%)'})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Показати повну таблицю даних"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Помилка в обробці даних: {e}")
    st.info("Спробуйте ще раз оновити файл на GitHub.")
