import streamlit as st
import pandas as pd
import numpy as np
from func.SaveToSheet import ConnectToSheet, SaveToSheet, CheckDate
import os

import datetime
import time
import pytz

from PIL import Image

def app():
    st.title('Ежедневный отчет')
    df1 = pd.DataFrame(columns = ['Объект','Дата формирования', 'Спуски', 'Подъемы', 'Итого по прибыли', 'ЗП', 'Хоз.нужды', 'Утилизация', 'Итого по расходам', 'Доход'])

    Object = st.selectbox("Выбирете ЖК", ["ЖК «120 Квартал»","ЖК «Центральный»"])

    image_1 = Image.open(r'\img\ЖК 120 квартал.jpg')
    image_2 = Image.open(r'\img\ЖК Центральный.jpg')

    if Object == "ЖК «120 Квартал»":
        st.image(image_1, width=400)
    elif Object == "ЖК «Центральный»":
        st.image(image_2, width=400)

    tz = pytz.timezone('Europe/Moscow')
    Date = st.date_input("Выбирете дату отчета", value=datetime.datetime.now(tz))

    if Date:
        CheckDate(Object, df1, Date)

    st.subheader('Доход:')
    Up = st.number_input('Укажите прибыль по подъемам, руб', min_value=0)
    Down = st.number_input('Укажите прибыль по спускам, руб', min_value=0)

    Income = Up + Down
    st.write("Итого по доходу:", Income, 'руб.')

    st.subheader('Расходы:')
    Wage = st.number_input('Укажите расход по З/П, руб', min_value=0)
    HozNeeds = st.number_input('Укажите расход по Хоз.нуждам, руб', min_value=0)
    Utilization = st.number_input('Укажите расход за утилизацию мусора, руб', min_value=0)

    Expenditure = Wage + HozNeeds + Utilization
    st.write("Итого по расходу:", Expenditure, 'руб.')

    st.subheader('Отчет:')
    Profit =  Income - Expenditure
    st.write("Итого по прибыли:", Profit, 'руб.')

    df = pd.DataFrame({'Объект': [Object],
                        'Дата формирования': [Date.strftime("%d-%b-%Y")],
                        'Спуски': [str(Up)],
                        'Подъемы': [str(Down)],
                        'Итого по прибыли': [str(Income)],
                        'ЗП': [str(Wage)],
                        'Хоз.нужды': [str(HozNeeds)],
                        'Утилизация': [str(Utilization)],
                        'Итого по расходам': [str(Expenditure)],
                        'ДОХОД': [str(Profit)] })

    st.dataframe(df.iloc[0])
    st.write('Если данные введены коректно, то нажмите кнопку отправить.')

    if st.button('Отправить'):
        try:
            sheet, SPREADSHEET_ID = ConnectToSheet()
            SaveToSheet(sheet, SPREADSHEET_ID, Object, df)
            st.success("Отчет успешно отправлен!")
        except:
            st.error("Отчет не отправлен!")
