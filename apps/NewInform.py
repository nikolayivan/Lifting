import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os

from openpyxl import workbook
from openpyxl import load_workbook

from data.create_data import create_table

if 'Count' not in st.session_state:
    st.session_state['Count'] = 0

def app():
    st.title('Показатели')
