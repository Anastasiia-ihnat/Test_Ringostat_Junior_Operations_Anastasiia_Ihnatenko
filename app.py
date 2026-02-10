import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ringostat Test", layout="wide")
st.title("Аналітичний дашборд Ringostat")
st.write("Виконавець: Анастасія Ігнатенко")

try:
    # 1. Читаємо файл БЕЗ заголовків, щоб самі їх призначити
    # Пропускаємо перші 11 рядків мета-даних
    df = pd.read_csv('test_analitika.csv', skiprows=11, header=None)
    
    # 2. Призначаємо імена за номерами колонок, які ми побачили в логах
    # 2 - CRM (AmoCRM), 7 - Stage (Negotiations)
    df = df.iloc[:, [2, 7]]
    df.columns = ['CRM', 'Stage']
    
    # 3. Рахуємо кількість Won та Lost для кожної CRM
    # Припускаємо, що успішна угода містить "Won" або "Success" у назві стадії
    analysis = df.groupby(['CRM', 'Stage']).size().unstack(fill_value=0)
    
    # Створюємо колонки Won/Lost, якщо їх немає в початкових даних
    if 'Won' not in analysis.columns:
        # Шукаємо колонку, яка схожа на успіх (наприклад, 'Closed won' або 'Перемога')
        won_cols = [c for c in analysis.columns if 'won' in str(c).lower() or 'success' in str(c).lower()]
        analysis['Won'] = analysis[won_cols].sum(axis=1) if won_cols else 0
        
    if 'Lost' not in analysis.columns:
        lost_cols = [c for c in analysis.columns if 'lost' in str(c).lower() or 'fail' in str(c).lower()]
        analysis['Lost'] = analysis[lost_cols].sum(axis=1) if lost_cols else 0

    # 4. Розрахунок Win Rate
    analysis['Total'] = analysis['Won'] + analysis['Lost']
    analysis['Win_Rate'] = (analysis['Won'] / analysis['Total'] * 100).round(2).fillna(0)
    analysis = analysis.reset_index()

    # Видаляємо рядки, де немає даних про угоди
    analysis = analysis[analysis['Total'] > 0]

    # Відображення
    st.divider()
    if not analysis.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Загальна кількість успішних угод", int(analysis['Won'].sum()))
        with c2:
            top = analysis.sort_values(by='Win_Rate', ascending=False).iloc[0]
            st.metric("Найкраща конверсія", f"{top['CRM']} ({top['Win_Rate']}%)")

        # Графік
        st.subheader("Ефективність CRM за Win Rate (%)")
        fig = px.bar(analysis, x='Win_Rate', y='CRM', orientation='h',
                     color='Win_Rate', color_continuous_scale='Portland',
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Детальний розрахунок")
        st.dataframe(analysis[['CRM', 'Lost', 'Won', 'Win_Rate']])
    else:
        st.warning("Дані знайдено, але статусів 'Won' або 'Lost' у колонці Stage немає.")
        st.write("Ось які статуси є у вашому файлі:", df['Stage'].unique())

except Exception as e:
    st.error(f"Помилка: {e}")
