import streamlit as st
import pandas as pd
import numpy as np
import os
# import gspread
import datetime
import time
import pytz

from datetime import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account


def ConnectToSheet():
    SCOPES = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    SERVICE_ACCOUNT_FILE = 'keys.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    SPREADSHEET_ID = '1fppbnkXV77_Y0FhU1v_h-4aGzKz9I2d41FBKLteDvrM'
    return sheet, SPREADSHEET_ID

def SaveToSheet(sheet, SPREADSHEET_ID, Object, df):
    data = [df.iloc[0].to_list()]
    request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=Object+'!A1:DJ', valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body={'values':data})
    response = request.execute()

def ReadSheet(Object, df1, StartDate, EndDate):
    sheet, SPREADSHEET_ID = ConnectToSheet()

    for i in Object:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=i+'!A1:DJ').execute()
        values = result.get('values', [])

        if not values:
            st.error('No data found.')
        else:
            for count, row in enumerate(values):
                if count > 0:
                    df1.loc[len(df1)] = row

    df1['Дата формирования'] = pd.to_datetime(df1['Дата формирования'], format='%Y%m%d', errors='ignore')
    df1[['Спуски', 'Подъемы', 'Итого по прибыли', 'ЗП', 'Хоз.нужды', 'Утилизация', 'Итого по расходам', 'Доход']] = df1[['Спуски', 'Подъемы', 'Итого по прибыли', 'ЗП', 'Хоз.нужды', 'Утилизация', 'Итого по расходам', 'Доход']].apply(pd.to_numeric)
    df1 = df1.set_index('Дата формирования')
    df1 = df1.groupby([df1.index, 'Объект']).sum()
    df2 = df1.loc[str(StartDate) : str(EndDate)]
    st.dataframe(df2)
    return df2

def CheckDate(Object, df1, Date):
    sheet, SPREADSHEET_ID = ConnectToSheet()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=Object+'!A1:DJ').execute()
    values = result.get('values', [])

    if not values:
        st.error('No data found.')
    else:
        for count, row in enumerate(values):
            if count > 0:
                if row[1] == str(Date):
                    st.error(f"Отчет за {str(row[1])} число для {Object} уже добавлен! Выбирете другую дату...")
                    st.stop()
