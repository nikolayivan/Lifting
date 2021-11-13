import streamlit as st
from multiapp import MultiApp
from apps import DailyReport, PeriodReport

from PIL import Image

app = MultiApp()
st.set_page_config(page_title = 'Лебёдки', layout = 'wide', page_icon='🏢')
image = Image.open("img\ВЦСПС.png")
st.sidebar.image(image)

# Add all your application here
app.add_app("Ежедневный отчет", DailyReport.app)
app.add_app("Отчет за период", PeriodReport.app)

# The main app
app.run()
