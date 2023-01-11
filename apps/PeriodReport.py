import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os

import plotly.express as px
import plotly.graph_objects as go

from openpyxl import workbook
from openpyxl import load_workbook

from googleapiclient.discovery import build
from google.oauth2 import service_account

from func.SaveToSheet import ConnectToSheet, ReadSheet

import datetime
import time
import pytz

if 'Count' not in st.session_state:
    st.session_state['Count'] = 0

def app():
    st.title('Отчет за выбранный период')
    df1 = pd.DataFrame(columns = ['Объект','Дата формирования', 'Спуски', 'Подъемы', 'Итого по прибыли', 'ЗП', 'Хоз.нужды', 'Утилизация', 'Итого по расходам', 'Доход'])
    tz = pytz.timezone('Europe/Moscow')

    col1, col2 = st.columns(2)
    with col1:
        StartDate = st.date_input("Выбирете начальную дату:", value=datetime.datetime.now(tz))
    with col2:
        EndDate = st.date_input("Выбирете конечную дату:", value=datetime.datetime.now(tz))

    Object = st.multiselect("Выбирете один или несколько ЖК:",["ЖК «120 Квартал»","ЖК «Центральный»"])

    if not Object:
        st.stop()

    df2 = ReadSheet(Object, df1, StartDate, EndDate)

    TotalDowns = df2['Спуски'].sum()
    TotalUps = df2['Подъемы'].sum()
    TotaIncome = df2['Итого по прибыли'].sum()
    TotalWage = df2['ЗП'].sum()
    TotalHozNeeds = df2['Хоз.нужды'].sum()
    TotalUtilization = df2['Утилизация'].sum()
    TotalExpenditure = df2['Итого по расходам'].sum()
    TotalProfit = df2['Доход'].sum()

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        st.metric(label="Спуски:", value=f"{TotalDowns} ₽", delta="0 ₽")
    with col2:
        st.metric(label="Подъемы:", value=f"{TotalUps} ₽", delta="0 ₽")
    with col3:
        st.metric(label="Прибыль:", value=f"{TotaIncome} ₽", delta="0 ₽")
    with col5:
        st.metric(label="ЗП:", value=f"{TotalWage} ₽", delta="0 ₽")
    with col6:
        st.metric(label="Хоз.нужды:", value=f"{TotalHozNeeds} ₽", delta="0 ₽")
    with col7:
        st.metric(label="Утилизация:", value=f"{TotalUtilization} ₽", delta="0 ₽")
    with col8:
        st.metric(label="Расход:", value=f"{TotalExpenditure} ₽", delta="0 ₽")
    with col10:
        st.metric(label="Доход:", value=f"{TotalProfit} ₽", delta="0 ₽")

    st.write("##")

    with st.expander("Посмотреть результаты"):

        col1, col2 = st.columns(2)
        with col1:
            #fig = px.bar(df2, x=df2.index.get_level_values(0), y=['Спуски','Подъемы'], title="Спуски и Подъемы по дням")
            #st.plotly_chart(fig, use_container_width=True)
            st.bar_chart(df2, x=df2.index.get_level_values(0), y=['Спуски','Подъемы'])
        with col2:
            fig = px.bar(df2, x=df2.index.get_level_values(0), y=['ЗП', 'Хоз.нужды', 'Утилизация'], title="Расходы по дням")
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            fig = go.Figure(data=[go.Pie(labels=['Спуски','Подъемы'], values=[TotalDowns,TotalUps], hole=.3, textinfo='value + percent', textfont_size=15)])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure(data=[go.Pie(labels=['ЗП','Хоз.нужды','Утилизация'], values=[TotalWage,TotalHozNeeds,TotalUtilization], hole=.3, textinfo='value + percent', textfont_size=15)])
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            fig = go.Figure(data=[go.Pie(labels=['Прибыль','Расход'], values=[TotaIncome,TotalExpenditure], hole=.3, textinfo='value + percent', textfont_size=15)])
            st.plotly_chart(fig, use_container_width=True)


        # df3 = df2.groupby(level=0).sum()
        #
        # col1, col2 = st.columns(2)
        # with col1:
        #     fig = px.line(df3, x=df3.index.get_level_values(0), y='Итого по прибыли', title="Сумманые Доходы по дням")
        #     fig.update_layout(yaxis_range=[0,100000])
        #     st.plotly_chart(fig, use_container_width=True)
        #
        # with col2:
        #     fig = px.line(df3, x=df3.index.get_level_values(0), y='Итого по расходам', title="Сумманые Расходы по дням")
        #     fig.update_layout(yaxis_range=[0,100000])
        #     st.plotly_chart(fig, use_container_width=True)
